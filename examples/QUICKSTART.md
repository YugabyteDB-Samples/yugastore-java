# Quick Start Guide

## Run the Demo

The easiest way to see the tool in action is to run the demo:

```bash
cd examples/
./run_demo.sh
```

This will run the verifier against example documents that contain deliberate issues to demonstrate the tool's capabilities.

## Expected Output

The demo will find multiple violations including:

### Critical Issues
- **Missing Requirements**: Password reset functionality (REQ-012) not covered
- **Principle Violations**: Specification logs passwords in violation of security principles
- **Missing Coverage**: Several requirements completely unaddressed

### High Severity Issues
- **Scope Creep**: Cryptocurrency payment support not in original requirements
- **Scope Creep**: Social media integration not requested
- **Incomplete Coverage**: Accessibility requirements ignored

### Medium Severity Issues
- **Ambiguity**: Vague terms like "reasonable", "as needed", "nice, modern look"
- **Testability**: Specifications without measurable criteria
- **Vagueness**: Terms like "various techniques", "optimized"

## Use With Your Own Documents

### Step 1: Prepare Your Documents

Create four types of documents:

1. **Human Input** (`my_input.txt`):
```
REQ-001: Users must be able to login
REQ-002: The system shall send email notifications
...
```

2. **Requirements** (`my_requirements.txt`):
```
REQ-100: The API must use REST
REQ-101: Data must be encrypted
...
```

3. **Constitution** (`my_principles.txt`):
```
PRINCIPLE: Passwords must never be stored in plaintext
RULE: All APIs must have authentication
...
```

4. **Specification** (`my_spec.md`):
```
# Technical Specification

SPEC-001: Login endpoint at /api/auth/login
- Accepts username and password
- Returns JWT token
...
```

### Step 2: Run Verification

```bash
../spec_verifier.py \
  --human-input my_input.txt \
  --requirements my_requirements.txt \
  --constitution my_principles.txt \
  --specification my_spec.md
```

### Step 3: Review Report

The tool will output a detailed report showing:
- Summary statistics
- Violations by severity
- Detailed findings with evidence
- Overall verdict

### Step 4: Fix Issues and Re-run

Address the violations and run again until satisfied.

## JSON Output

For programmatic processing:

```bash
../spec_verifier.py \
  --human-input my_input.txt \
  --requirements my_requirements.txt \
  --constitution my_principles.txt \
  --specification my_spec.md \
  --json > violations.json
```

Process with jq:
```bash
# Count critical violations
cat violations.json | jq '[.[] | select(.severity=="CRITICAL")] | length'

# List all missing requirements
cat violations.json | jq -r '.[] | select(.category=="COVERAGE") | .evidence[]'
```

## Tips for Best Results

1. **Use Clear Markers**: Start requirements with REQ-001, MUST, SHALL
2. **Be Explicit**: Use specific, measurable language
3. **Reference Requirements**: Link specs to requirements (e.g., "Addresses: REQ-001")
4. **Use Consistent Terms**: Don't mix "user" and "customer"
5. **Make Principles Clear**: Use "must" and "must not" language

## Common Issues

**No requirements found?**
- Ensure documents use patterns like "REQ-001:", "must", "shall", "- item"

**Too many false positives?**
- Focus on CRITICAL and HIGH severity first
- Tool is intentionally strict
- Some warnings are subjective

**Orphaned specifications?**
- Add explicit requirement references
- Use similar terminology between requirements and specs
- May indicate missing requirements

## Next Steps

- Read the full [README](../SPEC_VERIFIER_README.md)
- Integrate into your CI/CD pipeline
- Customize for your project's needs
- Run iteratively during specification development


