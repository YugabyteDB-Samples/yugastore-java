#!/bin/bash
# Demo script for the Specification Verifier

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "================================"
echo "Specification Verifier Demo"
echo "================================"
echo ""
echo "This demo will run the adversarial specification verifier"
echo "on example documents that contain deliberate issues."
echo ""
echo "Expected findings:"
echo "  - Missing requirements (password reset, accessibility, etc.)"
echo "  - Principle violations (logging passwords)"
echo "  - Ambiguous specifications (vague language)"
echo "  - Scope creep (features not in requirements)"
echo "  - Testability issues"
echo ""
read -p "Press Enter to continue..."

echo ""
echo "Running verification..."
echo ""

python3 "$ROOT_DIR/spec_verifier.py" \
  --human-input "$SCRIPT_DIR/human_input.txt" \
  --requirements "$SCRIPT_DIR/reverse_eng_requirements.txt" \
  --constitution "$SCRIPT_DIR/constitution.txt" \
  --specification "$SCRIPT_DIR/specification_with_issues.md"

EXIT_CODE=$?

echo ""
echo "================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Verification PASSED"
else
    echo "❌ Verification FAILED (exit code: $EXIT_CODE)"
fi
echo "================================"

exit $EXIT_CODE


