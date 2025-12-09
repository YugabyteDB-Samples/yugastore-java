# 🛡️ Adversarial Specification Verifier

> **Verify your specifications before they become bugs**

## 🚀 Quick Start (30 seconds)

```bash
# Test the tool
./test_verifier.sh

# See it in action
cd examples && ./run_demo.sh
```

## 📖 What Does It Do?

Takes your specification document and **adversarially** verifies it against:
- ✅ Human input documents (user stories, stakeholder needs)
- ✅ Requirements documents (technical requirements)
- ✅ Constitution (guiding principles, constraints)

**Finds:**
- ❌ Missing requirements
- ❌ Principle violations
- ❌ Contradictions
- ❌ Scope creep
- ❌ Ambiguous language
- ❌ Untestable specs

## 💡 Why?

Bad specs → Wasted time + Missing features + Security issues + Unhappy customers

This tool catches problems **early** when they're cheap to fix.

## 🎯 Basic Usage

```bash
./spec_verifier.py \
  --human-input user_stories.txt \
  --requirements technical_reqs.txt \
  --constitution principles.txt \
  --specification your_spec.md
```

**Returns:**
- Exit code `0` = ✅ Passed
- Exit code `1` = ❌ Failed (with detailed report)

## 📚 Documentation

Pick your path:

1. **Just want to try it?** → Run `cd examples && ./run_demo.sh`
2. **Want to use it now?** → Read [`examples/QUICKSTART.md`](examples/QUICKSTART.md)
3. **Want all the details?** → Read [`SPEC_VERIFIER_README.md`](SPEC_VERIFIER_README.md)
4. **Want the overview?** → Read [`VERIFIER_OVERVIEW.md`](VERIFIER_OVERVIEW.md)
5. **Want the deep dive?** → Read [`SPEC_VERIFIER_SUMMARY.md`](SPEC_VERIFIER_SUMMARY.md)

## ⚡ Features

- **Zero dependencies** - Pure Python 3
- **Format agnostic** - Text, markdown, anything
- **Adversarial** - Skeptical by design
- **Fast** - Runs in seconds
- **CI/CD ready** - Exit codes, JSON output
- **Extensible** - Easy to add rules

## 🎬 Demo Output Preview

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

[CRITICAL] COVERAGE: 4 requirements have NO coverage
  - Password reset functionality (REQ-012) not addressed
  - Accessibility requirements missing

[CRITICAL] PRINCIPLE_VIOLATION: Logging passwords violates security principle
  Line 61: "Failed attempts logged including password for debugging"

[HIGH] SCOPE_CREEP: 22 specifications appear out of scope
  - Admin dashboard (not in requirements)
  - Social media integration (not requested)
  - Cryptocurrency support (not requested)

================================================================================
VERDICT: ❌ FAILED - 2 CRITICAL issues must be resolved
================================================================================
```

## 🏃 Next Steps

```bash
# 1. Verify installation
./test_verifier.sh

# 2. Run demo
cd examples && ./run_demo.sh

# 3. Review examples
cd examples
cat specification_with_issues.md    # Bad spec (has issues)
cat specification_fixed.md          # Good spec (issues fixed)

# 4. Try with your docs
cd ..
./spec_verifier.py -i your_input.txt -r your_reqs.txt -c your_principles.txt -s your_spec.md

# 5. Get help
./spec_verifier.py --help
```

## 🤔 FAQ

**Q: Do I need to install anything?**  
A: No. Just Python 3 (which you probably already have).

**Q: What formats does it support?**  
A: Any plain text format - .txt, .md, etc.

**Q: Will it work with my documents?**  
A: Yes, if they use common requirement patterns like "REQ-001:", "MUST", "SHALL", or numbered/bulleted lists.

**Q: Won't it have false positives?**  
A: Yes, intentionally. Better to catch too much than miss real issues.

**Q: How long does it take to run?**  
A: Seconds, even for large documents.

**Q: Can I use it in CI/CD?**  
A: Yes! Exit codes, JSON output, fast execution.

## 🎓 Learning Resources

The `examples/` directory contains:
- Example input documents
- Example specifications (good and bad)
- Demo script
- Quick start guide

Compare `specification_with_issues.md` (bad) vs `specification_fixed.md` (good) to learn best practices.

## 🔧 Integration

**Git hook:**
```bash
./spec_verifier.py [...] || exit 1
```

**GitHub Actions:**
```yaml
- run: ./spec_verifier.py [...] --json > violations.json
```

**Makefile:**
```makefile
verify: spec_verifier.py -i input.txt -r reqs.txt -c const.txt -s spec.md
```

## 📝 License

Same as parent project (bookstore-r-us)

---

**Start here:** `./test_verifier.sh` → `cd examples && ./run_demo.sh` → Try with your docs!

**Need help?** Read [`VERIFIER_OVERVIEW.md`](VERIFIER_OVERVIEW.md) or [`SPEC_VERIFIER_README.md`](SPEC_VERIFIER_README.md)


