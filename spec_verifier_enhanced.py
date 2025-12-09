#!/usr/bin/env python3
"""
Adversarial Specification Verification Tool - Enhanced with Source Document Analysis

This tool verifies that a specification document properly addresses all inputs:
- Human input documents (which may be summaries of original sources)
- Reverse-engineered requirements documents  
- Constitution of guiding principles

When violations are detected, it can fetch and analyze original source documents via API
for deeper investigation (transcripts, emails, design documents, etc.)
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional, Any
import hashlib
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class SourceDocument:
    """Represents an original source document"""
    doc_id: str
    doc_type: str  # 'transcript', 'email', 'design_doc', 'meeting_notes', etc.
    url: str
    title: str
    date: Optional[str] = None
    participants: List[str] = field(default_factory=list)
    content: Optional[str] = None
    fetched: bool = False


@dataclass
class Violation:
    """Represents a verification violation"""
    severity: Severity
    category: str
    title: str
    description: str
    evidence: List[str] = field(default_factory=list)
    line_numbers: List[int] = field(default_factory=list)
    related_requirements: List[str] = field(default_factory=list)
    source_documents: List[SourceDocument] = field(default_factory=list)
    deep_analysis: Optional[str] = None
    
    def __str__(self):
        result = f"\n[{self.severity.value}] {self.category}: {self.title}\n"
        result += f"  {self.description}\n"
        if self.evidence:
            result += f"  Evidence:\n"
            for e in self.evidence[:3]:
                result += f"    - {e}\n"
        if self.line_numbers:
            result += f"  Lines: {', '.join(map(str, sorted(self.line_numbers)[:5]))}\n"
        if self.source_documents:
            result += f"  📄 Source Documents Analyzed: {len(self.source_documents)}\n"
            for doc in self.source_documents[:3]:
                result += f"    - {doc.doc_type}: {doc.title}\n"
        if self.deep_analysis:
            result += f"  🔍 Deep Analysis:\n"
            for line in self.deep_analysis.split('\n')[:5]:
                if line.strip():
                    result += f"    {line}\n"
        return result


@dataclass
class Requirement:
    """Represents a requirement extracted from documents"""
    id: str
    text: str
    source: str
    line_number: int
    priority: str = "NORMAL"
    tags: Set[str] = field(default_factory=set)
    source_doc_refs: List[str] = field(default_factory=list)  # IDs of original source documents
    
    def __hash__(self):
        return hash(self.id)


@dataclass 
class Principle:
    """Represents a guiding principle"""
    id: str
    text: str
    category: str
    mandatory: bool = True
    line_number: int = 0


@dataclass
class SpecificationItem:
    """Represents an item in the specification"""
    id: str
    text: str
    line_number: int
    addresses_requirements: Set[str] = field(default_factory=set)
    tags: Set[str] = field(default_factory=set)


class SourceDocumentAPI:
    """Handles API calls to fetch original source documents"""
    
    def __init__(self, api_config: Optional[Dict[str, Any]] = None):
        self.api_config = api_config or {}
        self.cache: Dict[str, SourceDocument] = {}
        self.base_url = self.api_config.get('base_url', '')
        self.api_key = self.api_config.get('api_key', '')
        self.timeout = self.api_config.get('timeout', 30)
        self.max_retries = self.api_config.get('max_retries', 3)
        self.enabled = self.api_config.get('enabled', False)
        
    def fetch_document(self, doc_id: str, doc_type: str = 'unknown') -> Optional[SourceDocument]:
        """Fetch a source document by ID"""
        if not self.enabled:
            return None
            
        # Check cache first
        if doc_id in self.cache:
            return self.cache[doc_id]
        
        try:
            # Construct API URL
            url = f"{self.base_url}/documents/{doc_id}"
            
            # Prepare request
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'SpecVerifier/2.0'
            }
            
            request = urllib.request.Request(url, headers=headers)
            
            # Make request with timeout
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                doc = SourceDocument(
                    doc_id=doc_id,
                    doc_type=data.get('type', doc_type),
                    url=url,
                    title=data.get('title', f'Document {doc_id}'),
                    date=data.get('date'),
                    participants=data.get('participants', []),
                    content=data.get('content', ''),
                    fetched=True
                )
                
                # Cache the document
                self.cache[doc_id] = doc
                return doc
                
        except urllib.error.HTTPError as e:
            print(f"  ⚠️  API Error: HTTP {e.code} fetching {doc_id}", file=sys.stderr)
            return None
        except urllib.error.URLError as e:
            print(f"  ⚠️  Network Error: {e.reason} fetching {doc_id}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"  ⚠️  Error fetching {doc_id}: {e}", file=sys.stderr)
            return None
    
    def fetch_multiple(self, doc_ids: List[str]) -> List[SourceDocument]:
        """Fetch multiple documents"""
        documents = []
        for doc_id in doc_ids:
            doc = self.fetch_document(doc_id)
            if doc:
                documents.append(doc)
        return documents


class DocumentParser:
    """Parses various document formats and extracts source document references"""
    
    @staticmethod
    def parse_file(filepath: Path) -> List[str]:
        """Parse a file and return lines"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.readlines()
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            return []
    
    @staticmethod
    def extract_source_refs(text: str) -> List[str]:
        """Extract source document references from text"""
        # Look for patterns like:
        # [SRC:transcript-2024-01-15]
        # [SOURCE:email-stakeholder-001]
        # [DOC:design-doc-v2]
        refs = re.findall(r'\[(?:SRC|SOURCE|DOC):([^\]]+)\]', text, re.IGNORECASE)
        return refs
    
    @staticmethod
    def extract_requirements(lines: List[str], source: str) -> List[Requirement]:
        """Extract requirements from document lines"""
        requirements = []
        
        req_patterns = [
            r'(?:REQ|REQUIREMENT|SHALL|MUST|SHOULD|NEEDS?)\s*[-:]?\s*(.+)',
            r'(?:The system|The application|It)\s+(?:shall|must|should|needs? to)\s+(.+)',
            r'^\s*[-*]\s+(.+(?:shall|must|should|required|necessary).+)',
            r'^\s*\d+\.\s+(.+)',
        ]
        
        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            if not line_stripped or len(line_stripped) < 10:
                continue
            
            # Extract source document references
            source_refs = DocumentParser.extract_source_refs(line_stripped)
            
            for pattern in req_patterns:
                match = re.search(pattern, line_stripped, re.IGNORECASE)
                if match:
                    text = match.group(1) if match.lastindex else line_stripped
                    text = text.strip().rstrip('.;,')
                    
                    # Remove source refs from text
                    clean_text = re.sub(r'\[(?:SRC|SOURCE|DOC):[^\]]+\]', '', text).strip()
                    
                    req_id = f"REQ_{hashlib.md5(clean_text.encode()).hexdigest()[:8]}"
                    priority = "HIGH" if any(word in line.lower() for word in ['must', 'shall', 'critical']) else "NORMAL"
                    tags = DocumentParser._extract_tags(line_stripped)
                    
                    req = Requirement(
                        id=req_id,
                        text=clean_text,
                        source=source,
                        line_number=line_num,
                        priority=priority,
                        tags=tags,
                        source_doc_refs=source_refs
                    )
                    requirements.append(req)
                    break
        
        return requirements
    
    @staticmethod
    def extract_principles(lines: List[str]) -> List[Principle]:
        """Extract guiding principles from constitution document"""
        principles = []
        
        principle_patterns = [
            r'(?:PRINCIPLE|RULE|GUIDELINE|CONSTRAINT)\s*[-:]?\s*(.+)',
            r'^\s*[-*]\s+(.+)',
            r'^\s*\d+\.\s+(.+)',
        ]
        
        current_category = "GENERAL"
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            if line.isupper() and len(line.split()) <= 5:
                current_category = line
                continue
            
            for pattern in principle_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    text = match.group(1) if match.lastindex else line
                    text = text.strip().rstrip('.;,')
                    
                    if len(text) < 10:
                        continue
                    
                    principle_id = f"PRIN_{hashlib.md5(text.encode()).hexdigest()[:8]}"
                    mandatory = any(word in line.lower() for word in ['must', 'shall', 'required', 'mandatory'])
                    
                    principle = Principle(
                        id=principle_id,
                        text=text,
                        category=current_category,
                        mandatory=mandatory,
                        line_number=line_num
                    )
                    principles.append(principle)
                    break
        
        return principles
    
    @staticmethod
    def extract_specifications(lines: List[str]) -> List[SpecificationItem]:
        """Extract specification items from specification document"""
        specs = []
        
        spec_patterns = [
            r'(?:SPEC|SPECIFICATION)\s*[-:]?\s*(.+)',
            r'^\s*[-*]\s+(.+)',
            r'^\s*\d+\.\s+(.+)',
            r'^#{1,6}\s+(.+)',
        ]
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or len(line) < 10:
                continue
            
            for pattern in spec_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    text = match.group(1) if match.lastindex else line
                    text = text.strip().rstrip('.;,')
                    
                    spec_id = f"SPEC_{hashlib.md5(text.encode()).hexdigest()[:8]}"
                    ref_reqs = set(re.findall(r'REQ[_-]?\w+', line, re.IGNORECASE))
                    tags = DocumentParser._extract_tags(line)
                    
                    spec = SpecificationItem(
                        id=spec_id,
                        text=text,
                        line_number=line_num,
                        addresses_requirements=ref_reqs,
                        tags=tags
                    )
                    specs.append(spec)
                    break
        
        return specs
    
    @staticmethod
    def _extract_tags(text: str) -> Set[str]:
        """Extract semantic tags from text"""
        tags = set()
        
        tag_keywords = {
            'security': ['security', 'authentication', 'authorization', 'encrypt', 'secure'],
            'performance': ['performance', 'speed', 'latency', 'throughput', 'optimize'],
            'ui': ['ui', 'user interface', 'display', 'screen', 'view'],
            'api': ['api', 'endpoint', 'rest', 'service'],
            'database': ['database', 'data', 'storage', 'persist', 'store'],
            'validation': ['validate', 'validation', 'verify', 'check'],
            'error_handling': ['error', 'exception', 'failure', 'handle'],
            'logging': ['log', 'logging', 'audit', 'track'],
        }
        
        text_lower = text.lower()
        for tag, keywords in tag_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.add(tag)
        
        return tags


class DeepAnalyzer:
    """Performs deep analysis on source documents when violations are found"""
    
    def __init__(self, api_client: SourceDocumentAPI):
        self.api_client = api_client
    
    def analyze_missing_requirement(self, requirement: Requirement) -> Tuple[List[SourceDocument], str]:
        """Analyze source documents to understand why requirement is missing"""
        if not requirement.source_doc_refs:
            return [], "No source documents referenced for deeper analysis"
        
        # Fetch source documents
        source_docs = self.api_client.fetch_multiple(requirement.source_doc_refs)
        
        if not source_docs:
            return [], "Could not fetch source documents"
        
        analysis = []
        analysis.append(f"Analyzed {len(source_docs)} source document(s):")
        
        for doc in source_docs:
            if not doc.content:
                continue
            
            # Search for requirement keywords in source
            req_keywords = set(re.findall(r'\w+', requirement.text.lower()))
            req_keywords = {w for w in req_keywords if len(w) > 3}
            
            # Find relevant sections
            doc_lower = doc.content.lower()
            matches = []
            for keyword in list(req_keywords)[:5]:  # Top 5 keywords
                if keyword in doc_lower:
                    # Find context around keyword
                    idx = doc_lower.find(keyword)
                    start = max(0, idx - 50)
                    end = min(len(doc.content), idx + 100)
                    context = doc.content[start:end].replace('\n', ' ')
                    matches.append(f"'{keyword}': ...{context}...")
            
            if matches:
                analysis.append(f"  In {doc.title} ({doc.doc_type}):")
                analysis.extend([f"    - {m}" for m in matches[:2]])
            else:
                analysis.append(f"  In {doc.title}: No direct mentions found")
        
        return source_docs, '\n'.join(analysis)
    
    def analyze_principle_violation(self, principle: Principle, spec_item: SpecificationItem,
                                   related_reqs: List[Requirement]) -> Tuple[List[SourceDocument], str]:
        """Analyze why a principle was violated"""
        source_doc_ids = []
        for req in related_reqs:
            source_doc_ids.extend(req.source_doc_refs)
        
        if not source_doc_ids:
            return [], "No source documents available for analysis"
        
        source_docs = self.api_client.fetch_multiple(list(set(source_doc_ids)))
        
        if not source_docs:
            return [], "Could not fetch source documents"
        
        analysis = []
        analysis.append(f"Checking if source documents justify this violation:")
        
        # Look for explicit mentions or contradictions
        principle_keywords = set(re.findall(r'\w+', principle.text.lower()))
        principle_keywords = {w for w in principle_keywords if len(w) > 4}
        
        for doc in source_docs:
            if not doc.content:
                continue
            
            doc_lower = doc.content.lower()
            relevant_found = False
            
            for keyword in list(principle_keywords)[:3]:
                if keyword in doc_lower:
                    relevant_found = True
                    break
            
            if relevant_found:
                analysis.append(f"  {doc.title} mentions related concepts")
            else:
                analysis.append(f"  {doc.title} does not discuss this principle")
        
        return source_docs, '\n'.join(analysis)
    
    def analyze_ambiguity(self, spec_item: SpecificationItem, requirements: List[Requirement]) -> Tuple[List[SourceDocument], str]:
        """Analyze source documents to clarify ambiguous specifications"""
        # Find requirements that might relate to this spec
        spec_keywords = set(re.findall(r'\w+', spec_item.text.lower()))
        spec_keywords = {w for w in spec_keywords if len(w) > 3}
        
        related_reqs = []
        for req in requirements:
            req_keywords = set(re.findall(r'\w+', req.text.lower()))
            overlap = spec_keywords & req_keywords
            if len(overlap) >= 2:
                related_reqs.append(req)
        
        source_doc_ids = []
        for req in related_reqs:
            source_doc_ids.extend(req.source_doc_refs)
        
        if not source_doc_ids:
            return [], "No source documents to clarify this ambiguity"
        
        source_docs = self.api_client.fetch_multiple(list(set(source_doc_ids)))
        
        analysis = []
        analysis.append(f"Searched source documents for clarification:")
        
        for doc in source_docs:
            if doc.content:
                analysis.append(f"  {doc.title} ({doc.doc_type}) - {len(doc.content)} chars analyzed")
        
        return source_docs, '\n'.join(analysis)


class SpecificationVerifier:
    """Performs adversarial verification of specifications with deep source analysis"""
    
    def __init__(self, api_config: Optional[Dict[str, Any]] = None, enable_deep_analysis: bool = False):
        self.violations: List[Violation] = []
        self.requirements: List[Requirement] = []
        self.principles: List[Principle] = []
        self.specifications: List[SpecificationItem] = []
        self.api_client = SourceDocumentAPI(api_config)
        self.deep_analyzer = DeepAnalyzer(self.api_client)
        self.enable_deep_analysis = enable_deep_analysis and self.api_client.enabled
    
    def load_documents(self, human_inputs: List[Path], requirements_docs: List[Path], 
                      constitution: Path, specification: Path):
        """Load all input documents"""
        parser = DocumentParser()
        
        for doc in human_inputs:
            lines = parser.parse_file(doc)
            reqs = parser.extract_requirements(lines, f"HUMAN_INPUT:{doc.name}")
            self.requirements.extend(reqs)
        
        for doc in requirements_docs:
            lines = parser.parse_file(doc)
            reqs = parser.extract_requirements(lines, f"REV_ENG:{doc.name}")
            self.requirements.extend(reqs)
        
        lines = parser.parse_file(constitution)
        self.principles = parser.extract_principles(lines)
        
        lines = parser.parse_file(specification)
        self.specifications = parser.extract_specifications(lines)
        
        print(f"Loaded: {len(self.requirements)} requirements, {len(self.principles)} principles, "
              f"{len(self.specifications)} specification items")
        
        # Count requirements with source references
        reqs_with_sources = sum(1 for r in self.requirements if r.source_doc_refs)
        if reqs_with_sources > 0:
            print(f"Found {reqs_with_sources} requirements with source document references")
            if self.enable_deep_analysis:
                print(f"✓ Deep analysis enabled - will fetch source documents for violations")
    
    def verify(self):
        """Run all verification checks"""
        print("\n" + "="*80)
        print("RUNNING ADVERSARIAL VERIFICATION")
        if self.enable_deep_analysis:
            print("(with deep source document analysis)")
        print("="*80)
        
        self.check_requirement_coverage()
        self.check_orphaned_specifications()
        self.check_principle_violations()
        self.check_ambiguity()
        self.check_contradictions()
        self.check_completeness()
        self.check_scope_creep()
        self.check_vagueness()
        self.check_testability()
        self.check_consistency()
    
    def check_requirement_coverage(self):
        """Verify all requirements are addressed in specification"""
        print("\n[CHECK] Requirement Coverage Analysis...")
        
        spec_text = " ".join([s.text.lower() for s in self.specifications])
        
        uncovered = []
        partially_covered = []
        
        for req in self.requirements:
            req_keywords = set(re.findall(r'\w+', req.text.lower()))
            req_keywords = {w for w in req_keywords if len(w) > 3}
            
            if not req_keywords:
                continue
            
            matches = sum(1 for keyword in req_keywords if keyword in spec_text)
            coverage = matches / len(req_keywords) if req_keywords else 0
            
            if coverage == 0:
                uncovered.append(req)
            elif coverage < 0.5:
                partially_covered.append(req)
        
        if uncovered:
            evidence = [f"{r.id} [{r.source}]: {r.text[:100]}..." for r in uncovered[:5]]
            
            violation = Violation(
                severity=Severity.CRITICAL,
                category="COVERAGE",
                title=f"{len(uncovered)} requirements have NO coverage in specification",
                description=f"The following requirements are completely missing from the specification:",
                evidence=evidence,
                related_requirements=[r.id for r in uncovered]
            )
            
            # Deep analysis for critical missing requirements
            if self.enable_deep_analysis and uncovered:
                print("  🔍 Performing deep analysis on uncovered requirements...")
                for req in uncovered[:3]:  # Analyze top 3
                    if req.source_doc_refs:
                        docs, analysis = self.deep_analyzer.analyze_missing_requirement(req)
                        violation.source_documents.extend(docs)
                        if analysis and not violation.deep_analysis:
                            violation.deep_analysis = analysis
                        elif analysis:
                            violation.deep_analysis += "\n" + analysis
            
            self.violations.append(violation)
        
        if partially_covered:
            self.violations.append(Violation(
                severity=Severity.HIGH,
                category="COVERAGE",
                title=f"{len(partially_covered)} requirements have PARTIAL coverage",
                description="These requirements are only partially addressed:",
                evidence=[f"{r.id} [{r.source}]: {r.text[:100]}..." for r in partially_covered[:5]]
            ))
        
        print(f"  ✓ Uncovered requirements: {len(uncovered)}")
        print(f"  ✓ Partially covered requirements: {len(partially_covered)}")
    
    def check_orphaned_specifications(self):
        """Find specification items that don't map to any requirement"""
        print("\n[CHECK] Orphaned Specifications (Scope Creep)...")
        
        req_text = " ".join([r.text.lower() for r in self.requirements])
        
        orphaned = []
        for spec in self.specifications:
            spec_keywords = set(re.findall(r'\w+', spec.text.lower()))
            spec_keywords = {w for w in spec_keywords if len(w) > 3}
            
            if not spec_keywords:
                continue
            
            matches = sum(1 for keyword in spec_keywords if keyword in req_text)
            coverage = matches / len(spec_keywords) if spec_keywords else 0
            
            if coverage < 0.3:
                orphaned.append(spec)
        
        if orphaned:
            self.violations.append(Violation(
                severity=Severity.HIGH,
                category="SCOPE_CREEP",
                title=f"{len(orphaned)} specification items appear to be out of scope",
                description="These specifications don't clearly relate to any input requirements:",
                evidence=[f"{s.id} (line {s.line_number}): {s.text[:100]}..." for s in orphaned[:5]],
                line_numbers=[s.line_number for s in orphaned]
            ))
        
        print(f"  ✓ Orphaned specifications: {len(orphaned)}")
    
    def check_principle_violations(self):
        """Check for violations of guiding principles"""
        print("\n[CHECK] Principle Violations...")
        
        violations_found = []
        
        for principle in self.principles:
            if not principle.mandatory:
                continue
            
            principle_lower = principle.text.lower()
            
            if any(phrase in principle_lower for phrase in ['must not', 'shall not', 'cannot', 'prohibited']):
                prohibited_terms = self._extract_key_terms(principle.text)
                
                for spec in self.specifications:
                    spec_lower = spec.text.lower()
                    for term in prohibited_terms:
                        if term.lower() in spec_lower:
                            violations_found.append((principle, spec, term))
            
            elif any(phrase in principle_lower for phrase in ['must', 'shall', 'required']):
                required_terms = self._extract_key_terms(principle.text)
                
                spec_text = " ".join([s.text.lower() for s in self.specifications])
                found = any(term.lower() in spec_text for term in required_terms)
                
                if not found:
                    violations_found.append((principle, None, "Not addressed"))
        
        if violations_found:
            evidence = []
            for principle, spec, issue in violations_found[:5]:
                if spec:
                    evidence.append(f"Principle '{principle.text[:60]}...' violated by spec at line {spec.line_number}")
                else:
                    evidence.append(f"Principle '{principle.text[:60]}...' not addressed in specification")
            
            violation = Violation(
                severity=Severity.CRITICAL,
                category="PRINCIPLE_VIOLATION",
                title=f"{len(violations_found)} principle violations detected",
                description="Mandatory principles have been violated or ignored:",
                evidence=evidence
            )
            
            # Deep analysis for principle violations
            if self.enable_deep_analysis and violations_found:
                print("  🔍 Performing deep analysis on principle violations...")
                principle, spec, _ = violations_found[0]
                if spec:
                    # Find related requirements
                    related_reqs = [r for r in self.requirements if any(
                        tag in spec.tags for tag in r.tags
                    )][:3]
                    
                    if any(r.source_doc_refs for r in related_reqs):
                        docs, analysis = self.deep_analyzer.analyze_principle_violation(
                            principle, spec, related_reqs
                        )
                        violation.source_documents = docs
                        violation.deep_analysis = analysis
            
            self.violations.append(violation)
        
        print(f"  ✓ Principle violations: {len(violations_found)}")
    
    def check_ambiguity(self):
        """Check for ambiguous or unclear specifications"""
        print("\n[CHECK] Ambiguity Detection...")
        
        ambiguous_specs = []
        
        ambiguous_indicators = [
            'appropriate', 'reasonable', 'adequate', 'sufficient',
            'as needed', 'if possible', 'etc', 'and so on',
            'various', 'several', 'some', 'many', 'few',
            'fast', 'slow', 'good', 'bad', 'efficient',
            'might', 'may', 'could', 'possibly', 'probably',
            'tbd', 'todo', 'to be determined', 'to be decided'
        ]
        
        for spec in self.specifications:
            spec_lower = spec.text.lower()
            found_indicators = [ind for ind in ambiguous_indicators if ind in spec_lower]
            
            if found_indicators:
                ambiguous_specs.append((spec, found_indicators))
        
        if ambiguous_specs:
            violation = Violation(
                severity=Severity.MEDIUM,
                category="AMBIGUITY",
                title=f"{len(ambiguous_specs)} ambiguous specifications detected",
                description="These specifications contain vague or ambiguous language:",
                evidence=[f"Line {s.line_number}: '{s.text[:80]}...' (contains: {', '.join(ind)})" 
                         for s, ind in ambiguous_specs[:5]],
                line_numbers=[s.line_number for s, _ in ambiguous_specs]
            )
            
            # Deep analysis for ambiguous specs
            if self.enable_deep_analysis and ambiguous_specs:
                print("  🔍 Analyzing source documents to clarify ambiguity...")
                spec, _ = ambiguous_specs[0]
                docs, analysis = self.deep_analyzer.analyze_ambiguity(spec, self.requirements)
                if docs:
                    violation.source_documents = docs
                    violation.deep_analysis = analysis
            
            self.violations.append(violation)
        
        print(f"  ✓ Ambiguous specifications: {len(ambiguous_specs)}")
    
    def check_contradictions(self):
        """Look for contradictory specifications"""
        print("\n[CHECK] Contradiction Detection...")
        
        contradictions = []
        
        for i, spec1 in enumerate(self.specifications):
            for spec2 in self.specifications[i+1:]:
                if self._are_contradictory(spec1.text, spec2.text):
                    contradictions.append((spec1, spec2))
        
        if contradictions:
            self.violations.append(Violation(
                severity=Severity.CRITICAL,
                category="CONTRADICTION",
                title=f"{len(contradictions)} potential contradictions found",
                description="These specification pairs may contradict each other:",
                evidence=[f"Line {s1.line_number} vs Line {s2.line_number}: '{s1.text[:60]}...' contradicts '{s2.text[:60]}...'" 
                         for s1, s2 in contradictions[:3]],
                line_numbers=[s.line_number for pair in contradictions for s in pair]
            ))
        
        print(f"  ✓ Contradictions: {len(contradictions)}")
    
    def check_completeness(self):
        """Check for completeness across different aspects"""
        print("\n[CHECK] Completeness Analysis...")
        
        aspects = {
            'security': ['security', 'authentication', 'authorization', 'encrypt'],
            'error_handling': ['error', 'exception', 'failure', 'handle'],
            'performance': ['performance', 'speed', 'latency', 'scale'],
            'validation': ['validate', 'validation', 'verify', 'check'],
            'logging': ['log', 'audit', 'track', 'monitor'],
        }
        
        spec_text = " ".join([s.text.lower() for s in self.specifications])
        missing_aspects = []
        
        for aspect, keywords in aspects.items():
            if not any(keyword in spec_text for keyword in keywords):
                req_text = " ".join([r.text.lower() for r in self.requirements])
                if any(keyword in req_text for keyword in keywords):
                    missing_aspects.append(aspect)
        
        if missing_aspects:
            self.violations.append(Violation(
                severity=Severity.HIGH,
                category="COMPLETENESS",
                title=f"Missing {len(missing_aspects)} important aspects",
                description=f"Requirements mention these aspects, but specification doesn't address them:",
                evidence=missing_aspects
            ))
        
        print(f"  ✓ Missing aspects: {len(missing_aspects)}")
    
    def check_scope_creep(self):
        """Detect potential scope creep"""
        print("\n[CHECK] Scope Creep Detection...")
        pass
    
    def check_vagueness(self):
        """Check for vague or non-specific specifications"""
        print("\n[CHECK] Vagueness Detection...")
        
        vague_specs = []
        
        for spec in self.specifications:
            has_numbers = bool(re.search(r'\d+', spec.text))
            has_specifics = any(word in spec.text.lower() for word in 
                              ['exactly', 'specifically', 'must', 'shall', 'will'])
            
            word_count = len(spec.text.split())
            
            if not has_numbers and not has_specifics and word_count > 10:
                vague_specs.append(spec)
        
        if vague_specs:
            self.violations.append(Violation(
                severity=Severity.MEDIUM,
                category="VAGUENESS",
                title=f"{len(vague_specs)} vague specifications",
                description="These specifications lack concrete details or measurable criteria:",
                evidence=[f"Line {s.line_number}: {s.text[:100]}..." for s in vague_specs[:5]],
                line_numbers=[s.line_number for s in vague_specs]
            ))
        
        print(f"  ✓ Vague specifications: {len(vague_specs)}")
    
    def check_testability(self):
        """Check if specifications are testable"""
        print("\n[CHECK] Testability Analysis...")
        
        untestable = []
        
        testable_indicators = [
            r'\d+',
            r'(?:shall|must|will)\s+(?:be|have|support|provide)',
            r'(?:return|output|display|store|send)',
        ]
        
        for spec in self.specifications:
            is_testable = any(re.search(pattern, spec.text, re.IGNORECASE) 
                            for pattern in testable_indicators)
            
            untestable_words = ['appropriate', 'adequate', 'reasonable', 'user-friendly', 
                              'intuitive', 'easy', 'simple', 'good', 'nice']
            has_untestable = any(word in spec.text.lower() for word in untestable_words)
            
            if not is_testable or has_untestable:
                untestable.append(spec)
        
        if untestable:
            self.violations.append(Violation(
                severity=Severity.MEDIUM,
                category="TESTABILITY",
                title=f"{len(untestable)} specifications may not be testable",
                description="These specifications lack concrete, measurable acceptance criteria:",
                evidence=[f"Line {s.line_number}: {s.text[:100]}..." for s in untestable[:5]],
                line_numbers=[s.line_number for s in untestable]
            ))
        
        print(f"  ✓ Untestable specifications: {len(untestable)}")
    
    def check_consistency(self):
        """Check for consistency in terminology and formatting"""
        print("\n[CHECK] Consistency Analysis...")
        
        inconsistencies = []
        
        terms_to_check = [
            ['user', 'customer', 'client'],
            ['login', 'sign in', 'authenticate'],
            ['database', 'data store', 'repository'],
            ['api', 'service', 'endpoint'],
        ]
        
        spec_text_lower = " ".join([s.text.lower() for s in self.specifications])
        
        for term_group in terms_to_check:
            found_terms = [term for term in term_group if term in spec_text_lower]
            if len(found_terms) > 1:
                inconsistencies.append(f"Inconsistent terminology: {' vs '.join(found_terms)}")
        
        if inconsistencies:
            self.violations.append(Violation(
                severity=Severity.LOW,
                category="CONSISTENCY",
                title=f"{len(inconsistencies)} consistency issues",
                description="Found inconsistent terminology or formatting:",
                evidence=inconsistencies
            ))
        
        print(f"  ✓ Consistency issues: {len(inconsistencies)}")
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text"""
        words = re.findall(r'\w+', text.lower())
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'shall', 'should', 'must', 'may', 'can', 'could', 'not'}
        return [w for w in words if len(w) > 3 and w not in stop_words]
    
    def _are_contradictory(self, text1: str, text2: str) -> bool:
        """Check if two texts are contradictory"""
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        terms1 = set(self._extract_key_terms(text1))
        terms2 = set(self._extract_key_terms(text2))
        
        overlap = terms1 & terms2
        if len(overlap) < 2:
            return False
        
        negations = ['not', 'no', 'never', 'without', 'cannot', 'must not', 'shall not']
        has_negation1 = any(neg in text1_lower for neg in negations)
        has_negation2 = any(neg in text2_lower for neg in negations)
        
        if has_negation1 != has_negation2 and len(overlap) >= 3:
            return True
        
        return False
    
    def generate_report(self) -> str:
        """Generate a comprehensive verification report"""
        report = []
        report.append("\n" + "="*80)
        report.append("ADVERSARIAL SPECIFICATION VERIFICATION REPORT")
        if self.enable_deep_analysis:
            report.append("(Enhanced with Source Document Analysis)")
        report.append("="*80)
        
        report.append(f"\n📊 SUMMARY STATISTICS")
        report.append(f"  Requirements analyzed: {len(self.requirements)}")
        report.append(f"  Principles checked: {len(self.principles)}")
        report.append(f"  Specification items: {len(self.specifications)}")
        report.append(f"  Total violations found: {len(self.violations)}")
        
        if self.enable_deep_analysis:
            total_docs = sum(len(v.source_documents) for v in self.violations)
            if total_docs > 0:
                report.append(f"  Source documents analyzed: {total_docs}")
        
        severity_counts = defaultdict(int)
        for v in self.violations:
            severity_counts[v.severity] += 1
        
        report.append(f"\n🚨 VIOLATIONS BY SEVERITY")
        for severity in Severity:
            count = severity_counts[severity]
            if count > 0:
                report.append(f"  {severity.value}: {count}")
        
        report.append(f"\n📋 DETAILED VIOLATIONS")
        
        severity_order = {Severity.CRITICAL: 0, Severity.HIGH: 1, 
                         Severity.MEDIUM: 2, Severity.LOW: 3, Severity.INFO: 4}
        sorted_violations = sorted(self.violations, key=lambda v: severity_order[v.severity])
        
        for violation in sorted_violations:
            report.append(str(violation))
        
        report.append("\n" + "="*80)
        report.append("VERDICT")
        report.append("="*80)
        
        critical_count = severity_counts[Severity.CRITICAL]
        high_count = severity_counts[Severity.HIGH]
        
        if critical_count > 0:
            verdict = f"❌ FAILED - {critical_count} CRITICAL issues must be resolved"
        elif high_count > 5:
            verdict = f"⚠️  CONDITIONAL FAIL - {high_count} HIGH severity issues need attention"
        elif high_count > 0:
            verdict = f"⚠️  PASS WITH CONCERNS - {high_count} HIGH severity issues present"
        else:
            verdict = "✅ PASSED - Minor issues only"
        
        report.append(verdict)
        report.append("="*80)
        
        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description='Adversarial Specification Verification Tool with Source Document Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic verification
  %(prog)s --human-input input1.txt input2.txt \\
           --requirements reqs.txt \\
           --constitution principles.txt \\
           --specification spec.txt

  # With deep analysis (requires API config)
  %(prog)s -i inputs/ -r reqs/ -c constitution.txt -s spec.md \\
           --deep-analysis \\
           --api-config api_config.json

  # Custom API configuration
  %(prog)s [...] --deep-analysis \\
           --api-url https://api.example.com \\
           --api-key YOUR_API_KEY
        """
    )
    
    parser.add_argument('-i', '--human-input', nargs='+', required=True,
                       help='Human input documents (one or more files)')
    parser.add_argument('-r', '--requirements', nargs='+', required=True,
                       help='Reverse-engineered requirements documents')
    parser.add_argument('-c', '--constitution', required=True,
                       help='Constitution/guiding principles document')
    parser.add_argument('-s', '--specification', required=True,
                       help='Specification document to verify')
    parser.add_argument('-o', '--output', help='Output report file (default: stdout)')
    parser.add_argument('--json', action='store_true',
                       help='Output violations in JSON format')
    
    # Deep analysis options
    parser.add_argument('--deep-analysis', action='store_true',
                       help='Enable deep analysis of source documents when violations found')
    parser.add_argument('--api-config', type=str,
                       help='Path to API configuration JSON file')
    parser.add_argument('--api-url', type=str,
                       help='Base URL for source document API')
    parser.add_argument('--api-key', type=str,
                       help='API key for authentication')
    parser.add_argument('--api-timeout', type=int, default=30,
                       help='API request timeout in seconds (default: 30)')
    
    args = parser.parse_args()
    
    # Convert paths
    human_inputs = [Path(p) for p in args.human_input]
    requirements = [Path(p) for p in args.requirements]
    constitution = Path(args.constitution)
    specification = Path(args.specification)
    
    # Verify files exist
    for filepath in human_inputs + requirements + [constitution, specification]:
        if not filepath.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
    
    # Configure API
    api_config = {}
    if args.api_config:
        with open(args.api_config, 'r') as f:
            api_config = json.load(f)
    else:
        if args.api_url:
            api_config['base_url'] = args.api_url
        if args.api_key:
            api_config['api_key'] = args.api_key
        api_config['timeout'] = args.api_timeout
    
    # Enable API if deep analysis requested and config provided
    if args.deep_analysis:
        if not api_config.get('base_url'):
            print("Warning: Deep analysis requested but no API URL provided. Running without deep analysis.", 
                  file=sys.stderr)
            api_config['enabled'] = False
        else:
            api_config['enabled'] = True
    else:
        api_config['enabled'] = False
    
    # Run verification
    verifier = SpecificationVerifier(
        api_config=api_config,
        enable_deep_analysis=args.deep_analysis
    )
    verifier.load_documents(human_inputs, requirements, constitution, specification)
    verifier.verify()
    
    # Generate report
    if args.json:
        output = json.dumps([
            {
                'severity': v.severity.value,
                'category': v.category,
                'title': v.title,
                'description': v.description,
                'evidence': v.evidence,
                'line_numbers': v.line_numbers,
                'source_documents': [
                    {
                        'id': d.doc_id,
                        'type': d.doc_type,
                        'title': d.title,
                        'url': d.url
                    } for d in v.source_documents
                ] if v.source_documents else [],
                'deep_analysis': v.deep_analysis
            }
            for v in verifier.violations
        ], indent=2)
    else:
        output = verifier.generate_report()
    
    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"\nReport written to: {args.output}")
    else:
        print(output)
    
    # Exit with error code if critical violations found
    critical_count = sum(1 for v in verifier.violations if v.severity == Severity.CRITICAL)
    sys.exit(1 if critical_count > 0 else 0)


if __name__ == '__main__':
    main()


