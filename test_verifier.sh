#!/bin/bash
# Test script to verify the spec verifier is working correctly

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Testing Specification Verifier..."
echo ""

# Test 1: Check if Python 3 is available
echo "[1/5] Checking Python 3..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "  ✓ Found: $PYTHON_VERSION"
else
    echo "  ✗ Python 3 not found. Please install Python 3."
    exit 1
fi

# Test 2: Check if spec_verifier.py exists and is executable
echo "[2/5] Checking spec_verifier.py..."
if [ -x "$SCRIPT_DIR/spec_verifier.py" ]; then
    echo "  ✓ spec_verifier.py exists and is executable"
else
    echo "  ✗ spec_verifier.py not found or not executable"
    exit 1
fi

# Test 3: Check if example files exist
echo "[3/5] Checking example files..."
REQUIRED_FILES=(
    "examples/human_input.txt"
    "examples/reverse_eng_requirements.txt"
    "examples/constitution.txt"
    "examples/specification_with_issues.md"
)

ALL_EXIST=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file not found"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = false ]; then
    exit 1
fi

# Test 4: Test --help flag
echo "[4/5] Testing --help flag..."
if python3 "$SCRIPT_DIR/spec_verifier.py" --help &> /dev/null; then
    echo "  ✓ Help flag works"
else
    echo "  ✗ Help flag failed"
    exit 1
fi

# Test 5: Run actual verification (expect it to fail with violations)
echo "[5/5] Running verification test..."
if python3 "$SCRIPT_DIR/spec_verifier.py" \
    --human-input "$SCRIPT_DIR/examples/human_input.txt" \
    --requirements "$SCRIPT_DIR/examples/reverse_eng_requirements.txt" \
    --constitution "$SCRIPT_DIR/examples/constitution.txt" \
    --specification "$SCRIPT_DIR/examples/specification_with_issues.md" \
    > /dev/null 2>&1; then
    echo "  ✗ Expected verification to fail (find violations), but it passed"
    exit 1
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 1 ]; then
        echo "  ✓ Verification correctly found violations (exit code 1)"
    else
        echo "  ✗ Unexpected exit code: $EXIT_CODE"
        exit 1
    fi
fi

echo ""
echo "============================================"
echo "✅ All tests passed!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Run the demo: cd examples && ./run_demo.sh"
echo "  2. Read the docs: less SPEC_VERIFIER_README.md"
echo "  3. Try with your own documents"
echo ""


