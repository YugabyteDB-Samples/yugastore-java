#!/bin/bash
# Demo script for the Enhanced Specification Verifier with Deep Analysis

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "================================================================"
echo "Enhanced Specification Verifier Demo"
echo "with Deep Source Document Analysis"
echo "================================================================"
echo ""
echo "This demo shows the enhanced verifier that can fetch and analyze"
echo "original source documents (transcripts, emails, design docs) when"
echo "it finds violations."
echo ""
echo "Setup required:"
echo "  1. Start the mock API server (in another terminal):"
echo "     cd examples && python3 mock_source_api.py"
echo ""
echo "  2. Run this demo"
echo ""

# Check if API server is running
if ! curl -s http://localhost:8888/documents/transcript-stakeholder-meeting-2024-01-15 \
     -H "Authorization: Bearer test-token" > /dev/null 2>&1; then
    echo "❌ ERROR: Mock API server not running on localhost:8888"
    echo ""
    echo "Please start it in another terminal:"
    echo "  cd $SCRIPT_DIR"
    echo "  python3 mock_source_api.py"
    echo ""
    exit 1
fi

echo "✓ API server is running"
echo ""
read -p "Press Enter to run verification with deep analysis..."

echo ""
echo "Running enhanced verification..."
echo ""

python3 "$ROOT_DIR/spec_verifier_enhanced.py" \
  --human-input "$SCRIPT_DIR/human_input_with_sources.txt" \
  --requirements "$SCRIPT_DIR/reverse_eng_requirements.txt" \
  --constitution "$SCRIPT_DIR/constitution.txt" \
  --specification "$SCRIPT_DIR/specification_with_issues.md" \
  --deep-analysis \
  --api-config "$SCRIPT_DIR/api_config.json"

EXIT_CODE=$?

echo ""
echo "================================================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Verification PASSED"
else
    echo "❌ Verification FAILED (exit code: $EXIT_CODE)"
fi
echo "================================================================"
echo ""
echo "Notice the '🔍 Deep Analysis' sections in the report above."
echo "These show insights from the original source documents!"
echo ""

exit $EXIT_CODE


