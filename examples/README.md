# Specification Verifier Examples

This directory contains example documents that demonstrate the Specification Verifier tool.

## Quick Start

### Basic Verifier
```bash
./run_demo.sh
```

### Enhanced Verifier (with Deep Analysis)
```bash
# Terminal 1: Start mock API server
python3 mock_source_api.py

# Terminal 2: Run demo
./run_demo_enhanced.sh
```

The enhanced version fetches original source documents (transcripts, emails, design docs) when it finds violations!

## Example Documents

### Input Documents (Basic)

1. **`human_input.txt`** - User stories and stakeholder requirements
   - Search and discovery requirements
   - Shopping cart functionality
   - User authentication
   - Checkout and payment
   - Performance and security requirements

2. **`reverse_eng_requirements.txt`** - Technical requirements from legacy system analysis
   - System architecture
   - API requirements
   - Error handling
   - Monitoring and logging
   - Integration requirements

3. **`constitution.txt`** - Guiding principles and architectural constraints
   - Security principles
   - Performance principles
   - Data integrity principles
   - Code quality principles
   - User experience principles
   - Compliance requirements

### Specification Documents

4. **`specification_with_issues.md`** - Specification with deliberate problems
   - **Use this to see the tool in action**
   - Contains missing requirements
   - Has principle violations (logs passwords!)
   - Includes scope creep
   - Uses ambiguous language
   - Demonstrates what NOT to do

5. **`specification_fixed.md`** - Improved specification
   - Shows how to address violations
   - More concrete and specific
   - Better requirement coverage
   - Demonstrates best practices

## What You'll See

When you run the demo against `specification_with_issues.md`:

### Critical Issues Found
- ❌ Password reset functionality missing
- ❌ Accessibility requirements not addressed
- ❌ Passwords being logged (security violation!)

### High Severity Issues
- ⚠️ Admin dashboard not in requirements (scope creep)
- ⚠️ Social media features not requested
- ⚠️ Cryptocurrency support not in requirements

### Medium Severity Issues
- ⚠️ Ambiguous terms like "fast", "efficient", "nice"
- ⚠️ Missing measurable criteria
- ⚠️ Vague specifications

## Example Output

```
================================================================================
ADVERSARIAL SPECIFICATION VERIFICATION REPORT
================================================================================

📊 SUMMARY STATISTICS
  Requirements analyzed: 61
  Principles checked: 44
  Specification items: 91
  Total violations found: 8

🚨 VIOLATIONS BY SEVERITY
  CRITICAL: 2
  HIGH: 2
  MEDIUM: 3
  LOW: 1

📋 DETAILED VIOLATIONS

[CRITICAL] COVERAGE: 4 requirements have NO coverage in specification
  The following requirements are completely missing from the specification:
  Evidence:
    - REQ_0499f2c1: Session tokens need to be cryptographically secure...
    - REQ_e2f8333d: Sensitive data must never appear in logs...
    - REQ_e93b9d65: Color contrast needs to meet WCAG 2.1 AA standards...

[CRITICAL] PRINCIPLE_VIOLATION: 26 principle violations detected
  Mandatory principles have been violated or ignored:
  Evidence:
    - Principle 'The system shall not log credit card numbers...' violated
    - Specification logs passwords in plain text for debugging

...

================================================================================
VERDICT
================================================================================
❌ FAILED - 2 CRITICAL issues must be resolved
================================================================================
```

## Try It Yourself

### Run against the problematic spec:
```bash
../spec_verifier.py \
  --human-input human_input.txt \
  --requirements reverse_eng_requirements.txt \
  --constitution constitution.txt \
  --specification specification_with_issues.md
```

### Run against the fixed spec:
```bash
../spec_verifier.py \
  --human-input human_input.txt \
  --requirements reverse_eng_requirements.txt \
  --constitution constitution.txt \
  --specification specification_fixed.md
```

### Save report to file:
```bash
../spec_verifier.py \
  -i human_input.txt \
  -r reverse_eng_requirements.txt \
  -c constitution.txt \
  -s specification_with_issues.md \
  -o report.txt
```

### Get JSON output:
```bash
../spec_verifier.py \
  -i human_input.txt \
  -r reverse_eng_requirements.txt \
  -c constitution.txt \
  -s specification_with_issues.md \
  --json
```

## Learning Points

By comparing the two specifications, you'll learn:

1. **How to write concrete requirements**
   - Bad: "The system should be fast"
   - Good: "95th percentile response time < 200ms"

2. **How to avoid security violations**
   - Bad: "Log password attempts for debugging"
   - Good: "Log timestamp, email (not password), IP address"

3. **How to prevent scope creep**
   - Don't add features not in requirements
   - Trace every specification to a requirement

4. **How to make specs testable**
   - Bad: "User-friendly interface"
   - Good: "WCAG 2.1 AA compliance with 4.5:1 contrast ratio"

5. **How to address all requirements**
   - Check every requirement is covered
   - Don't leave requirements unaddressed

## Next Steps

1. ✅ Run the demo
2. ✅ Review the violations found
3. ✅ Compare the two specification documents
4. ✅ Try with your own documents
5. ✅ Integrate into your workflow

## Documentation

- **Quick Start**: `QUICKSTART.md`
- **Full Documentation**: `../SPEC_VERIFIER_README.md`
- **Summary**: `../SPEC_VERIFIER_SUMMARY.md`

## Questions?

Run `../spec_verifier.py --help` for command-line options.

