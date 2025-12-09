#!/usr/bin/env python3
"""
Adversarial Specification Verification Tool

This tool verifies that a specification document properly addresses all inputs:
- Human input documents
- Reverse-engineered requirements documents  
- Constitution of guiding principles

It performs adversarial analysis to find gaps, contradictions, violations, and weaknesses.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
import hashlib


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class Violation:
    """Represents a verification violation"""
    severity: Severity
    category: str
    title: str
    description: str
    evidence: List[str] = field(default_factory=list)
    line_numbers: List[int] = field(default_factory=list)
    
    def __str__(self):
        result = f"\n[{self.severity.value}] {self.category}: {self.title}\n"
        result += f"  {self.description}\n"
        if self.evidence:
            result += f"  Evidence:\n"
            for e in self.evidence[:3]:  # Limit to first 3 pieces of evidence
                result += f"    - {e}\n"
        if self.line_numbers:
            result += f"  Lines: {', '.join(map(str, sorted(self.line_numbers)[:5]))}\n"
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


class DocumentParser:
    """Parses various document formats"""
    
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
    def extract_requirements(lines: List[str], source: str) -> List[Requirement]:
        """Extract requirements from document lines"""
        requirements = []
        
        # Patterns that indicate requirements
        req_patterns = [
            r'(?:REQ|REQUIREMENT|SHALL|MUST|SHOULD|NEEDS?)\s*[-:]?\s*(.+)',
            r'(?:The system|The application|It)\s+(?:shall|must|should|needs? to)\s+(.+)',
            r'^\s*[-*]\s+(.+(?:shall|must|should|required|necessary).+)',
            r'^\s*\d+\.\s+(.+)',  # Numbered items
        ]
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or len(line) < 10:
                continue
                
            for pattern in req_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    text = match.group(1) if match.lastindex else line
                    text = text.strip().rstrip('.;,')
                    
                    # Generate ID from content hash
                    req_id = f"REQ_{hashlib.md5(text.encode()).hexdigest()[:8]}"
                    
                    # Determine priority
                    priority = "HIGH" if any(word in line.lower() for word in ['must', 'shall', 'critical']) else "NORMAL"
                    
                    # Extract tags
                    tags = DocumentParser._extract_tags(line)
                    
                    req = Requirement(
                        id=req_id,
                        text=text,
                        source=source,
                        line_number=line_num,
                        priority=priority,
                        tags=tags
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
            
            # Check for category headers
            if line.isupper() and len(line.split()) <= 5:
                current_category = line
                continue
            
            for pattern in principle_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    text = match.group(1) if match.lastindex else line
                    text = text.strip().rstrip('.;,')
                    
                    if len(text) < 10:  # Skip very short lines
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
            r'^#{1,6}\s+(.+)',  # Markdown headers
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
                    
                    # Try to extract referenced requirement IDs
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


class SpecificationVerifier:
    """Performs adversarial verification of specifications"""
    
    def __init__(self):
        self.violations: List[Violation] = []
        self.requirements: List[Requirement] = []
        self.principles: List[Principle] = []
        self.specifications: List[SpecificationItem] = []
    
    def load_documents(self, human_inputs: List[Path], requirements_docs: List[Path], 
                      constitution: Path, specification: Path):
        """Load all input documents"""
        parser = DocumentParser()
        
        # Load human input requirements
        for doc in human_inputs:
            lines = parser.parse_file(doc)
            reqs = parser.extract_requirements(lines, f"HUMAN_INPUT:{doc.name}")
            self.requirements.extend(reqs)
        
        # Load reverse-engineered requirements
        for doc in requirements_docs:
            lines = parser.parse_file(doc)
            reqs = parser.extract_requirements(lines, f"REV_ENG:{doc.name}")
            self.requirements.extend(reqs)
        
        # Load constitution/principles
        lines = parser.parse_file(constitution)
        self.principles = parser.extract_principles(lines)
        
        # Load specification
        lines = parser.parse_file(specification)
        self.specifications = parser.extract_specifications(lines)
        
        print(f"Loaded: {len(self.requirements)} requirements, {len(self.principles)} principles, "
              f"{len(self.specifications)} specification items")
    
    def verify(self):
        """Run all verification checks"""
        print("\n" + "="*80)
        print("RUNNING ADVERSARIAL VERIFICATION")
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
        
        # Build a semantic map of specification content
        spec_text = " ".join([s.text.lower() for s in self.specifications])
        
        uncovered = []
        partially_covered = []
        
        for req in self.requirements:
            # Check for direct coverage
            req_keywords = set(re.findall(r'\w+', req.text.lower()))
            req_keywords = {w for w in req_keywords if len(w) > 3}  # Filter short words
            
            if not req_keywords:
                continue
            
            # Count how many requirement keywords appear in spec
            matches = sum(1 for keyword in req_keywords if keyword in spec_text)
            coverage = matches / len(req_keywords) if req_keywords else 0
            
            if coverage == 0:
                uncovered.append(req)
            elif coverage < 0.5:
                partially_covered.append(req)
        
        # Report uncovered requirements
        if uncovered:
            self.violations.append(Violation(
                severity=Severity.CRITICAL,
                category="COVERAGE",
                title=f"{len(uncovered)} requirements have NO coverage in specification",
                description=f"The following requirements are completely missing from the specification:",
                evidence=[f"{r.id} [{r.source}]: {r.text[:100]}..." for r in uncovered[:5]]
            ))
        
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
            
            if coverage < 0.3:  # Very low match to requirements
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
            
            # Extract prohibitions and requirements from principle
            principle_lower = principle.text.lower()
            
            # Check for negative constraints (must not, shall not, etc.)
            if any(phrase in principle_lower for phrase in ['must not', 'shall not', 'cannot', 'prohibited']):
                # Extract what is prohibited
                prohibited_terms = self._extract_key_terms(principle.text)
                
                # Check if specification violates this
                for spec in self.specifications:
                    spec_lower = spec.text.lower()
                    for term in prohibited_terms:
                        if term.lower() in spec_lower:
                            violations_found.append((principle, spec, term))
            
            # Check for positive constraints (must, shall, required to)
            elif any(phrase in principle_lower for phrase in ['must', 'shall', 'required']):
                required_terms = self._extract_key_terms(principle.text)
                
                # Check if any specification addresses this principle
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
            
            self.violations.append(Violation(
                severity=Severity.CRITICAL,
                category="PRINCIPLE_VIOLATION",
                title=f"{len(violations_found)} principle violations detected",
                description="Mandatory principles have been violated or ignored:",
                evidence=evidence
            ))
        
        print(f"  ✓ Principle violations: {len(violations_found)}")
    
    def check_ambiguity(self):
        """Check for ambiguous or unclear specifications"""
        print("\n[CHECK] Ambiguity Detection...")
        
        ambiguous_specs = []
        
        # Words/phrases that indicate ambiguity
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
            self.violations.append(Violation(
                severity=Severity.MEDIUM,
                category="AMBIGUITY",
                title=f"{len(ambiguous_specs)} ambiguous specifications detected",
                description="These specifications contain vague or ambiguous language:",
                evidence=[f"Line {s.line_number}: '{s.text[:80]}...' (contains: {', '.join(ind)})" 
                         for s, ind in ambiguous_specs[:5]],
                line_numbers=[s.line_number for s, _ in ambiguous_specs]
            ))
        
        print(f"  ✓ Ambiguous specifications: {len(ambiguous_specs)}")
    
    def check_contradictions(self):
        """Look for contradictory specifications"""
        print("\n[CHECK] Contradiction Detection...")
        
        contradictions = []
        
        # Look for opposing statements
        for i, spec1 in enumerate(self.specifications):
            for spec2 in self.specifications[i+1:]:
                # Check for negation patterns
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
        
        # Check coverage of important aspects
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
                # Check if requirements mention this aspect
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
        
        # Already handled in check_orphaned_specifications
        # This is a placeholder for additional scope creep checks
        pass
    
    def check_vagueness(self):
        """Check for vague or non-specific specifications"""
        print("\n[CHECK] Vagueness Detection...")
        
        vague_specs = []
        
        # Look for specifications without concrete details
        for spec in self.specifications:
            # Check for lack of numbers, specific terms, etc.
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
        
        # Testable specs usually have concrete criteria
        testable_indicators = [
            r'\d+',  # Numbers
            r'(?:shall|must|will)\s+(?:be|have|support|provide)',  # Concrete requirements
            r'(?:return|output|display|store|send)',  # Observable actions
        ]
        
        for spec in self.specifications:
            is_testable = any(re.search(pattern, spec.text, re.IGNORECASE) 
                            for pattern in testable_indicators)
            
            # Check for untestable language
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
        
        # Check for inconsistent terminology (e.g., "user" vs "customer" vs "client")
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
        # Remove common words and extract meaningful terms
        words = re.findall(r'\w+', text.lower())
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'shall', 'should', 'must', 'may', 'can', 'could', 'not'}
        return [w for w in words if len(w) > 3 and w not in stop_words]
    
    def _are_contradictory(self, text1: str, text2: str) -> bool:
        """Check if two texts are contradictory"""
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        # Extract key terms
        terms1 = set(self._extract_key_terms(text1))
        terms2 = set(self._extract_key_terms(text2))
        
        # Check for significant overlap in terms
        overlap = terms1 & terms2
        if len(overlap) < 2:
            return False
        
        # Check for negation patterns
        negations = ['not', 'no', 'never', 'without', 'cannot', 'must not', 'shall not']
        has_negation1 = any(neg in text1_lower for neg in negations)
        has_negation2 = any(neg in text2_lower for neg in negations)
        
        # If one has negation and the other doesn't, with similar terms, likely contradictory
        if has_negation1 != has_negation2 and len(overlap) >= 3:
            return True
        
        return False
    
    def generate_report(self) -> str:
        """Generate a comprehensive verification report"""
        report = []
        report.append("\n" + "="*80)
        report.append("ADVERSARIAL SPECIFICATION VERIFICATION REPORT")
        report.append("="*80)
        
        # Summary statistics
        report.append(f"\n📊 SUMMARY STATISTICS")
        report.append(f"  Requirements analyzed: {len(self.requirements)}")
        report.append(f"  Principles checked: {len(self.principles)}")
        report.append(f"  Specification items: {len(self.specifications)}")
        report.append(f"  Total violations found: {len(self.violations)}")
        
        # Violations by severity
        severity_counts = defaultdict(int)
        for v in self.violations:
            severity_counts[v.severity] += 1
        
        report.append(f"\n🚨 VIOLATIONS BY SEVERITY")
        for severity in Severity:
            count = severity_counts[severity]
            if count > 0:
                report.append(f"  {severity.value}: {count}")
        
        # Detailed violations
        report.append(f"\n📋 DETAILED VIOLATIONS")
        
        # Sort by severity
        severity_order = {Severity.CRITICAL: 0, Severity.HIGH: 1, 
                         Severity.MEDIUM: 2, Severity.LOW: 3, Severity.INFO: 4}
        sorted_violations = sorted(self.violations, key=lambda v: severity_order[v.severity])
        
        for violation in sorted_violations:
            report.append(str(violation))
        
        # Overall verdict
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
        description='Adversarial Specification Verification Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --human-input input1.txt input2.txt \\
           --requirements reqs.txt \\
           --constitution principles.txt \\
           --specification spec.txt

  %(prog)s -i inputs/ -r reqs/ -c constitution.txt -s spec.md --output report.txt
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
    
    # Run verification
    verifier = SpecificationVerifier()
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
                'line_numbers': v.line_numbers
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


