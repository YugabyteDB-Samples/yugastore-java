# Specification Verifier - Overview

## What Is This?

An **adversarial verification tool** that validates specification documents against their input sources (requirements, principles, and stakeholder input). It's designed to catch problems early through rigorous, skeptical analysis.

## The Problem It Solves

Bad specifications lead to:
- ❌ Missing features
- ❌ Security vulnerabilities  
- ❌ Wasted development time
- ❌ Scope creep
- ❌ Untestable requirements
- ❌ Customer dissatisfaction

This tool catches these issues **before** they become code.

## Quick Demo

```bash
# Run the demo to see it in action
cd examples/
./run_demo.sh
```

Expected output: The tool will find ~8 violation categories including:
- Missing requirements (password reset, accessibility)
- Security violations (logging passwords)
- Scope creep (features not in requirements)
- Ambiguous language
- Untestable specifications

## Basic Usage

```bash
./spec_verifier.py \
  --human-input user_stories.txt \
  --requirements technical_reqs.txt \
  --constitution principles.txt \
  --specification spec_to_verify.md
```

**Exit codes:**
- `0` = Passed (no critical issues)
- `1` = Failed (critical violations found)

## What It Checks

| Check | Severity | Finds |
|-------|----------|-------|
| Missing Requirements | CRITICAL | Requirements not in spec |
| Principle Violations | CRITICAL | Violations of mandatory rules |
| Contradictions | CRITICAL | Conflicting specs |
| Scope Creep | HIGH | Untraced specifications |
| Completeness | HIGH | Missing aspects (security, etc.) |
| Ambiguity | MEDIUM | Vague language ("reasonable", "TBD") |
| Testability | MEDIUM | No measurable criteria |
| Vagueness | MEDIUM | Lacks concrete details |
| Consistency | LOW | Inconsistent terminology |

## Key Features

✅ **Zero Dependencies** - Pure Python 3, no pip install needed  
✅ **Format Agnostic** - Works with text, markdown, any plain text  
✅ **Adversarial** - Skeptical and thorough by design  
✅ **CI/CD Ready** - Exit codes, JSON output, fast execution  
✅ **Detailed Reports** - Line numbers, evidence, categorized violations  
✅ **Extensible** - Easy to add custom verification rules  

## Documentation

- **Start Here**: [`examples/QUICKSTART.md`](examples/QUICKSTART.md)
- **Full Docs**: [`SPEC_VERIFIER_README.md`](SPEC_VERIFIER_README.md)
- **Summary**: [`SPEC_VERIFIER_SUMMARY.md`](SPEC_VERIFIER_SUMMARY.md)
- **Examples**: [`examples/README.md`](examples/README.md)

## File Structure

```
/spec_verifier.py                         # Main tool (executable)
/test_verifier.sh                         # Test script
/SPEC_VERIFIER_README.md                  # Full documentation
/SPEC_VERIFIER_SUMMARY.md                 # Detailed summary
/VERIFIER_OVERVIEW.md                     # This file
/examples/
  ├── run_demo.sh                         # Demo script
  ├── QUICKSTART.md                       # Quick start guide  
  ├── README.md                           # Examples documentation
  ├── human_input.txt                     # Example: user stories
  ├── reverse_eng_requirements.txt        # Example: technical reqs
  ├── constitution.txt                    # Example: principles
  ├── specification_with_issues.md        # Example: bad spec
  └── specification_fixed.md              # Example: good spec
```

## Testing

Run the test suite:

```bash
./test_verifier.sh
```

This verifies:
1. Python 3 is available
2. Main script is executable
3. Example files exist
4. Help flag works
5. Verification runs correctly

## Real-World Example

### Input: User Story
```
REQ-001: Users must be able to reset their password via email
```

### Input: Security Principle
```
PRINCIPLE: The system must never log passwords in plaintext
```

### Bad Specification
```
SPEC-020: Login attempts are logged including the password for debugging
```

### What the Tool Finds
```
[CRITICAL] COVERAGE: REQ-001 has NO coverage in specification
  Password reset functionality is completely missing

[CRITICAL] PRINCIPLE_VIOLATION: Logging passwords violates security principle
  Line 20: Specification logs passwords in violation of mandatory principle
```

### Fixed Specification
```
SPEC-020: Login attempts are logged with: timestamp, email (not password), 
          IP address, user-agent
Addresses: Security logging requirement

SPEC-021: Password reset functionality
- POST /api/auth/password-reset/request - Send reset email
- Token valid for 1 hour, single-use
- POST /api/auth/password-reset/confirm - Complete reset
Addresses: REQ-001
```

## Use Cases

### 1. Pre-Implementation Review
Run before starting development to catch spec issues early.

### 2. Stakeholder Approval
Verify spec completeness before stakeholder sign-off.

### 3. Requirements Changes
Re-verify when requirements change to ensure spec stays aligned.

### 4. CI/CD Pipeline
Automatically verify specs on every commit/PR.

### 5. Quality Gate
Make passing verification a requirement for spec approval.

## Integration Examples

### Git Pre-commit Hook
```bash
#!/bin/bash
./spec_verifier.py [...] || exit 1
```

### GitHub Actions
```yaml
- name: Verify Specification
  run: ./spec_verifier.py [...] --json > violations.json
```

### Makefile
```makefile
verify-spec:
	./spec_verifier.py [...] || (echo "Spec verification failed" && exit 1)
```

## Philosophy

The tool embodies **"Trust, but verify"**

It applies adversarial thinking:
- "Did you REALLY address all requirements?"
- "Are you violating your own principles?"
- "Can this actually be tested?"
- "Is this specific enough to implement?"
- "Are you adding unrequested features?"

Better to catch issues in specs (cheap to fix) than in code (expensive to fix) or production (very expensive to fix).

## Limitations

**False Positives**: The tool is intentionally strict and may flag valid specifications. This is by design - better to be too careful than miss real issues.

**Keyword-Based**: Uses pattern matching, not true semantic understanding. May miss context-specific issues.

**Format Dependent**: Works best with well-structured documents using clear requirement markers.

These limitations are acceptable trade-offs for:
- Zero dependencies
- Fast execution
- Easy deployment
- Predictable behavior

## Getting Started (5 Minutes)

```bash
# 1. Test that everything works
./test_verifier.sh

# 2. Run the demo
cd examples/
./run_demo.sh

# 3. Review the example specifications
less specification_with_issues.md
less specification_fixed.md

# 4. Read the quick start
less QUICKSTART.md

# 5. Try with your own documents
cd ..
./spec_verifier.py \
  --human-input your_input.txt \
  --requirements your_reqs.txt \
  --constitution your_principles.txt \
  --specification your_spec.md
```

## Success Metrics

The tool is successful when it:
1. ✅ Finds missing requirements before coding starts
2. ✅ Catches principle violations in specifications  
3. ✅ Identifies ambiguous language
4. ✅ Prevents scope creep
5. ✅ Improves spec quality over time

## Support & Help

- Run `./spec_verifier.py --help` for command-line options
- See `SPEC_VERIFIER_README.md` for full documentation
- Check `examples/QUICKSTART.md` for getting started
- Review example documents in `examples/` directory

## Version

- **Built**: December 2025
- **Language**: Python 3 (3.7+)
- **Dependencies**: None (standard library only)
- **License**: Same as parent project

---

**Remember**: This tool is adversarial by design. It's meant to find problems. Don't take violations personally - they're opportunities to improve your specifications before they become expensive bugs.

**Start with**: `cd examples && ./run_demo.sh`


