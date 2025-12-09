# Adversarial Specification Verification Tool

## Overview

This tool performs rigorous, adversarial verification of specification documents against their input sources. It's designed to catch:

- **Missing requirements** - Requirements that aren't addressed in the specification
- **Principle violations** - Violations of guiding principles from the constitution
- **Contradictions** - Conflicting specifications
- **Scope creep** - Specifications that don't trace back to requirements
- **Ambiguity** - Vague or unclear language
- **Untestable specs** - Specifications without measurable criteria
- **Incomplete coverage** - Missing important aspects (security, error handling, etc.)
- **Inconsistencies** - Inconsistent terminology or formatting

## Installation

The tool is a standalone Python 3 script with no external dependencies:

```bash
chmod +x spec_verifier.py
```

## Usage

### Basic Usage

```bash
./spec_verifier.py \
  --human-input input1.txt input2.txt \
  --requirements requirements.txt \
  --constitution principles.txt \
  --specification spec.txt
```

### Parameters

- `-i, --human-input`: One or more human input documents (required)
- `-r, --requirements`: One or more reverse-engineered requirements documents (required)
- `-c, --constitution`: Constitution/guiding principles document (required)
- `-s, --specification`: Specification document to verify (required)
- `-o, --output`: Output file for report (optional, defaults to stdout)
- `--json`: Output violations in JSON format (optional)

### Examples

**Example 1: Basic verification**
```bash
./spec_verifier.py \
  -i docs/user_story.txt docs/stakeholder_input.txt \
  -r docs/reverse_eng_requirements.txt \
  -c docs/architecture_principles.txt \
  -s docs/technical_specification.txt
```

**Example 2: Save report to file**
```bash
./spec_verifier.py \
  -i inputs/*.txt \
  -r requirements/*.md \
  -c constitution.txt \
  -s specification.md \
  -o verification_report.txt
```

**Example 3: JSON output for CI/CD integration**
```bash
./spec_verifier.py \
  -i input.txt \
  -r reqs.txt \
  -c principles.txt \
  -s spec.txt \
  --json > violations.json
```

## Document Format Requirements

### Input Documents (Human Input & Requirements)

The tool automatically extracts requirements from various formats:

**Supported patterns:**
- `REQ-001: The system must...`
- `REQUIREMENT: Users shall be able to...`
- `The system must provide...`
- `- The application should support...`
- Numbered lists: `1. System needs to...`

**Example:**
```
User Story: Authentication

REQ-001: The system must support user login with email and password
REQ-002: Users shall be able to reset their password via email
- The system should lock accounts after 5 failed login attempts
- Session timeout must be configurable
```

### Constitution (Guiding Principles)

Principles that the specification must adhere to:

**Supported patterns:**
- `PRINCIPLE: Never store passwords in plaintext`
- `RULE: All API responses must include error codes`
- `- Security must be prioritized over convenience`
- Mandatory indicators: `must`, `shall`, `required`, `mandatory`

**Example:**
```
SECURITY PRINCIPLES

PRINCIPLE: All user data must be encrypted at rest and in transit
PRINCIPLE: Authentication must not use weak passwords (min 8 chars)
RULE: The system shall never log sensitive information

PERFORMANCE PRINCIPLES

- Response times must be under 200ms for 95th percentile
- The system must handle at least 1000 concurrent users
```

### Specification Document

The document being verified:

**Supported patterns:**
- `SPEC-001: Implementation of...`
- `### Authentication System`
- `- The login endpoint accepts...`
- Markdown headers and lists

**Example:**
```
# Technical Specification

## Authentication

SPEC-001: User authentication endpoint at /api/auth/login
- Accepts email and password in request body
- Returns JWT token valid for 24 hours
- Implements rate limiting: 5 attempts per 15 minutes

SPEC-002: Password storage using bcrypt with cost factor 12
REQ-001, REQ-002 (references which requirements this addresses)
```

## Verification Checks

### 1. Requirement Coverage
**Severity: CRITICAL**
- Checks if all requirements are addressed in the specification
- Identifies completely missing requirements
- Flags partially covered requirements

### 2. Principle Violations
**Severity: CRITICAL**
- Verifies specification adheres to mandatory principles
- Detects violations of "must not" constraints
- Ensures "must have" principles are addressed

### 3. Contradictions
**Severity: CRITICAL**
- Finds specifications that contradict each other
- Uses semantic analysis to detect conflicts

### 4. Scope Creep / Orphaned Specifications
**Severity: HIGH**
- Identifies specifications that don't trace to any requirement
- Flags potential gold-plating or scope creep

### 5. Completeness
**Severity: HIGH**
- Checks if important aspects are covered:
  - Security
  - Error handling
  - Performance
  - Validation
  - Logging/auditing

### 6. Ambiguity
**Severity: MEDIUM**
- Detects vague language:
  - "appropriate", "reasonable", "adequate"
  - "as needed", "if possible"
  - "TBD", "TODO"
  - "fast", "slow", "good"

### 7. Testability
**Severity: MEDIUM**
- Identifies specifications without measurable criteria
- Flags subjective terms ("user-friendly", "intuitive")
- Ensures specifications are verifiable

### 8. Vagueness
**Severity: MEDIUM**
- Finds specifications lacking concrete details
- Checks for absence of numbers/specific terms

### 9. Consistency
**Severity: LOW**
- Checks for inconsistent terminology
- Examples: "user" vs "customer", "login" vs "sign in"

## Understanding the Report

### Report Structure

```
================================================================================
ADVERSARIAL SPECIFICATION VERIFICATION REPORT
================================================================================

📊 SUMMARY STATISTICS
  Requirements analyzed: 45
  Principles checked: 12
  Specification items: 38
  Total violations found: 7

🚨 VIOLATIONS BY SEVERITY
  CRITICAL: 2
  HIGH: 3
  MEDIUM: 2

📋 DETAILED VIOLATIONS

[CRITICAL] COVERAGE: 3 requirements have NO coverage in specification
  The following requirements are completely missing from the specification:
  Evidence:
    - REQ_a3b4c5d6 [HUMAN_INPUT:story.txt]: Users must be able to export data...
    - REQ_f7e8d9c0 [REV_ENG:reqs.txt]: System shall provide audit logging...

[HIGH] SCOPE_CREEP: 2 specification items appear to be out of scope
  These specifications don't clearly relate to any input requirements:
  Evidence:
    - SPEC_1a2b3c4d (line 45): Implement blockchain-based ledger for...

================================================================================
VERDICT
================================================================================
❌ FAILED - 2 CRITICAL issues must be resolved
================================================================================
```

### Exit Codes

- **0**: Passed (no critical violations)
- **1**: Failed (critical violations found)

Use in CI/CD pipelines:
```bash
./spec_verifier.py -i input.txt -r req.txt -c prin.txt -s spec.txt || exit 1
```

## Integration Examples

### Git Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

if git diff --cached --name-only | grep -q "specification.md"; then
    echo "Verifying specification..."
    ./spec_verifier.py \
        -i docs/inputs/*.txt \
        -r docs/requirements/*.md \
        -c docs/principles.txt \
        -s docs/specification.md
    
    if [ $? -ne 0 ]; then
        echo "❌ Specification verification failed!"
        echo "Fix violations before committing."
        exit 1
    fi
fi
```

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Verify Specification

on:
  pull_request:
    paths:
      - 'docs/specification.md'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Specification Verification
        run: |
          python3 spec_verifier.py \
            -i docs/inputs/*.txt \
            -r docs/requirements/*.md \
            -c docs/principles.txt \
            -s docs/specification.md \
            --json > violations.json
      
      - name: Upload Report
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: verification-report
          path: violations.json
```

### Makefile Integration

```makefile
.PHONY: verify-spec
verify-spec:
	@echo "Running adversarial specification verification..."
	@./spec_verifier.py \
		-i docs/user_stories.txt docs/stakeholder_input.txt \
		-r docs/requirements.md \
		-c docs/architecture_principles.txt \
		-s docs/technical_spec.md \
		-o reports/verification_$(shell date +%Y%m%d_%H%M%S).txt
```

## Advanced Features

### JSON Output for Programmatic Access

```bash
./spec_verifier.py [...] --json > violations.json
```

JSON structure:
```json
[
  {
    "severity": "CRITICAL",
    "category": "COVERAGE",
    "title": "3 requirements have NO coverage",
    "description": "The following requirements are completely missing...",
    "evidence": ["REQ_123: User must be able to...", "..."],
    "line_numbers": [45, 67, 89]
  }
]
```

Process with `jq`:
```bash
# Count critical violations
cat violations.json | jq '[.[] | select(.severity=="CRITICAL")] | length'

# Extract all missing requirements
cat violations.json | jq -r '.[] | select(.category=="COVERAGE") | .evidence[]'
```

## Best Practices

### 1. Run Early and Often
Run verification during the specification drafting process, not just at the end.

### 2. Use Consistent Formatting
- Start requirements with clear markers (REQ-001, MUST, SHALL)
- Use structured formats (markdown, numbered lists)
- Be explicit about requirement IDs

### 3. Make Principles Machine-Readable
- Use clear "must/must not" language
- Keep principles atomic (one principle per line)
- Use consistent terminology

### 4. Reference Requirements in Specs
Include requirement IDs in specification items:
```
SPEC-005: Implements user authentication (addresses REQ-001, REQ-002)
```

### 5. Address All Violation Severities
- **CRITICAL**: Must fix before proceeding
- **HIGH**: Should fix, represents significant gaps
- **MEDIUM**: Address to improve quality
- **LOW**: Nice to have, improves consistency

### 6. Iterate
The tool is adversarial by design - it's meant to find problems. Use it iteratively:
1. Run verification
2. Fix violations
3. Re-run
4. Repeat until satisfied

## Limitations

### Current Limitations

1. **Semantic Understanding**: Uses keyword matching and heuristics, not true natural language understanding
2. **False Positives**: May flag valid specifications as violations
3. **Context Sensitivity**: Cannot understand domain-specific terminology without configuration
4. **Format Dependency**: Works best with structured documents

### Known Issues

- May miss requirements written in very unconventional formats
- Cannot detect logical inconsistencies that require deep domain knowledge
- Terminology checks use hardcoded word lists

### Future Enhancements

- [ ] Integration with LLMs for semantic understanding
- [ ] Custom rule definitions
- [ ] Configurable severity levels
- [ ] Multi-language support
- [ ] Traceability matrix generation
- [ ] HTML report generation
- [ ] Interactive mode with fix suggestions

## Troubleshooting

### "No requirements found"
- Check that input documents use recognizable patterns (REQ, MUST, SHALL, numbered lists)
- Try making requirements more explicit

### "Too many false positives"
- Review ambiguity and vagueness checks
- Consider that the tool is intentionally strict
- Focus on CRITICAL and HIGH severity issues first

### "Specifications marked as orphaned but they're valid"
- Ensure specification text uses similar terminology to requirements
- Add explicit requirement references in specifications
- May indicate requirements document is incomplete

## Contributing

To extend the verification checks:

1. Add a new method to the `SpecificationVerifier` class:
```python
def check_my_custom_rule(self):
    print("\n[CHECK] My Custom Rule...")
    violations = []
    
    # Your verification logic here
    
    if violations:
        self.violations.append(Violation(...))
```

2. Call it from the `verify()` method:
```python
def verify(self):
    # ... existing checks ...
    self.check_my_custom_rule()
```

## License

Same as parent project (see LICENSE file)

## Support

For issues, questions, or contributions, please file an issue in the project repository.


