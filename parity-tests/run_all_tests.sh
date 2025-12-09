#!/bin/bash
#
# Run all parity tests for Yugastore microservices
#
# This script discovers and runs all Python unit tests in the parity-tests subdirectories.
# It creates a virtual environment if needed, installs dependencies, and runs pytest.
#
# Usage:
#   ./run_all_tests.sh              # Run all tests
#   ./run_all_tests.sh --verbose    # Run with verbose output
#   ./run_all_tests.sh --coverage   # Run with coverage report
#   ./run_all_tests.sh --service <name>  # Run tests for specific service only
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
VERBOSE=""
COVERAGE=""
SERVICE_FILTER=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --verbose, -v       Run tests with verbose output"
    echo "  --coverage, -c      Generate coverage report"
    echo "  --service, -s NAME  Run tests for specific service only"
    echo "  --help, -h          Show this help message"
    echo ""
    echo "Available services:"
    for dir in "${SCRIPT_DIR}"/*-tests; do
        if [[ -d "$dir" ]]; then
            echo "  - $(basename "$dir" | sed 's/-tests$//')"
        fi
    done
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE="-v"
            shift
            ;;
        --coverage|-c)
            COVERAGE="--cov=. --cov-report=term-missing --cov-report=html:coverage_report"
            shift
            ;;
        --service|-s)
            SERVICE_FILTER="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Check for Python 3
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    log_error "Python 3 is required but not found"
    exit 1
fi

log_info "Using Python: $($PYTHON_CMD --version)"

# Create virtual environment if it doesn't exist
if [[ ! -d "$VENV_DIR" ]]; then
    log_info "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
fi

# Activate virtual environment
log_info "Activating virtual environment..."
source "${VENV_DIR}/bin/activate"

# Upgrade pip
pip install --quiet --upgrade pip

# Collect all requirements and install
log_info "Installing dependencies..."
TEMP_REQUIREMENTS=$(mktemp)
cat "${SCRIPT_DIR}"/*/requirements.txt 2>/dev/null | sort -u > "$TEMP_REQUIREMENTS"
pip install --quiet -r "$TEMP_REQUIREMENTS"
rm "$TEMP_REQUIREMENTS"

# Find test directories
TEST_DIRS=()
for dir in "${SCRIPT_DIR}"/*-tests; do
    if [[ -d "$dir" ]]; then
        if [[ -n "$SERVICE_FILTER" ]]; then
            if [[ "$(basename "$dir")" == *"${SERVICE_FILTER}"* ]]; then
                TEST_DIRS+=("$dir")
            fi
        else
            TEST_DIRS+=("$dir")
        fi
    fi
done

if [[ ${#TEST_DIRS[@]} -eq 0 ]]; then
    log_error "No test directories found"
    if [[ -n "$SERVICE_FILTER" ]]; then
        log_error "No tests matching service filter: $SERVICE_FILTER"
    fi
    exit 1
fi

# Print test summary
echo ""
echo "========================================"
echo "       Parity Tests Runner"
echo "========================================"
echo ""
log_info "Found ${#TEST_DIRS[@]} test suite(s):"
for dir in "${TEST_DIRS[@]}"; do
    echo "  - $(basename "$dir")"
done
echo ""

# Run tests
FAILED_SUITES=()
PASSED_SUITES=()
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0

for test_dir in "${TEST_DIRS[@]}"; do
    suite_name=$(basename "$test_dir")
    echo ""
    echo "----------------------------------------"
    log_info "Running: ${suite_name}"
    echo "----------------------------------------"

    cd "$test_dir"

    # Run pytest and capture result
    set +e
    if [[ -n "$COVERAGE" ]]; then
        pytest $VERBOSE $COVERAGE . 2>&1
    else
        pytest $VERBOSE . 2>&1
    fi
    result=$?
    set -e

    if [[ $result -eq 0 ]]; then
        log_success "${suite_name} passed"
        PASSED_SUITES+=("$suite_name")
    else
        log_error "${suite_name} failed"
        FAILED_SUITES+=("$suite_name")
    fi

    cd "$SCRIPT_DIR"
done

# Print summary
echo ""
echo "========================================"
echo "           Test Summary"
echo "========================================"
echo ""

if [[ ${#PASSED_SUITES[@]} -gt 0 ]]; then
    log_success "Passed suites (${#PASSED_SUITES[@]}):"
    for suite in "${PASSED_SUITES[@]}"; do
        echo "  ✓ $suite"
    done
fi

if [[ ${#FAILED_SUITES[@]} -gt 0 ]]; then
    echo ""
    log_error "Failed suites (${#FAILED_SUITES[@]}):"
    for suite in "${FAILED_SUITES[@]}"; do
        echo "  ✗ $suite"
    done
fi

echo ""
echo "----------------------------------------"
echo "Total: ${#TEST_DIRS[@]} suite(s), ${#PASSED_SUITES[@]} passed, ${#FAILED_SUITES[@]} failed"
echo "----------------------------------------"

# Deactivate virtual environment
deactivate

# Exit with appropriate code
if [[ ${#FAILED_SUITES[@]} -gt 0 ]]; then
    exit 1
fi

exit 0
