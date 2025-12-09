# Verification Agent

Perform quality checks on GitHub issues labeled `ingested` by running functional tests and identifying defects.

## Instructions

### 1. Enumerate Issues

List all open issues with the `ingested` label:
```bash
gh issue list --label "ingested" --state open --json number,title,body,url,labels
```

### 2. For Each Issue

#### Step 1: Checkout the Implementation Branch
```bash
git fetch origin
git checkout issue-<number>
```

If no branch exists, skip this issue and report it.

#### Step 2: Start Required Services

**Python Backend Services (`python_services/`):**
```bash
cd python_services
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
```

**Next.js Frontend (`nextjs-frontend/`):**
```bash
cd nextjs-frontend
npm install
npm run dev &
```

**Wait for services to be ready:**
```bash
# Health check endpoints
curl --retry 10 --retry-delay 2 http://localhost:8000/health
curl --retry 10 --retry-delay 2 http://localhost:3000
```

#### Step 3: Identify Test Scope

Based on the issue's technical specifications and acceptance criteria:
- Identify which services/components were modified
- Determine relevant API endpoints to test
- Identify UI flows to validate
- Review acceptance criteria for testable assertions

#### Step 4: Create/Update Test Assets

**Create functional tests in `parity-tests/verification/`:**

```python
# parity-tests/verification/test_issue_<number>.py
import pytest
import requests

class TestIssue<Number>:
    """
    Verification tests for Issue #<number>: <title>

    Acceptance Criteria:
    - [ ] Criterion 1
    - [ ] Criterion 2
    """

    BASE_URL = "http://localhost:8000"
    FRONTEND_URL = "http://localhost:3000"

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data and preconditions"""
        pass

    def test_acceptance_criterion_1(self):
        """Verify: <criterion 1>"""
        # Arrange
        # Act
        # Assert
        pass

    def test_acceptance_criterion_2(self):
        """Verify: <criterion 2>"""
        pass

    def test_edge_case_1(self):
        """Edge case: <description>"""
        pass

    def test_error_handling(self):
        """Verify proper error handling"""
        pass
```

**For UI tests, use Playwright or Selenium:**
```python
# parity-tests/verification/test_issue_<number>_ui.py
from playwright.sync_api import sync_playwright
import pytest

class TestIssue<Number>UI:
    def test_ui_flow(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://localhost:3000")
            # UI assertions
            browser.close()
```

#### Step 5: Execute Tests

```bash
cd parity-tests/verification
pytest test_issue_<number>.py -v --tb=long 2>&1 | tee test_output_<number>.log
```

#### Step 6: Debug Loop

```
while tests_failing:
    analyze_failure(test_output)

    if is_test_issue:
        fix_test()
    elif is_code_bug:
        document_bug()
        break  # Exit loop to create bug issue

    run_tests_again()
```

### 3. Handle Test Results

#### Path A: All Tests Pass
- Mark verification as complete
- Add comment to original issue with test results
- Update issue label from `ingested` to `verified`

```bash
gh issue comment <number> --body "## ✅ Verification Complete

All functional tests passed.

**Test Results:**
- Tests run: X
- Passed: X
- Failed: 0

**Services Tested:**
- Backend API: ✅
- Frontend UI: ✅

**Coverage:**
- Acceptance criteria verified: X/X
"

gh issue edit <number> --remove-label "ingested" --add-label "verified"
```

#### Path B: Bugs Found

For each bug discovered:

##### Step 1: Root Cause Analysis
- Identify the failing test and error message
- Trace through code to find the root cause
- Determine if it's a regression, new bug, or edge case
- Document the code path that leads to the failure

##### Step 2: Create Reproduction Steps
```markdown
## Steps to Reproduce
1. Start the application with `<command>`
2. Navigate to <location> or call <endpoint>
3. Perform <action>
4. Observe <unexpected behavior>

## Expected Behavior
<what should happen>

## Actual Behavior
<what actually happens>

## Error Output
```
<stack trace or error message>
```
```

##### Step 3: Create Bug Issue

```bash
gh issue create \
  --title "Bug: <concise description>" \
  --label "ingested" \
  --label "bug" \
  --body "$(cat <<'EOF'
## Bug Report

**Found during verification of:** Issue #<original_number>
**Branch:** `issue-<original_number>`

## Summary
<brief description of the bug>

## Root Cause Analysis
**Location:** `<file_path>:<line_number>`
**Cause:** <explanation of why the bug occurs>
**Code Path:**
1. <step 1 in code execution>
2. <step 2>
3. <failure point>

## Steps to Reproduce
1. Start services: `<command>`
2. <step 2>
3. <step 3>
4. Observe: <unexpected behavior>

## Expected Behavior
<what should happen>

## Actual Behavior
<what actually happens>

## Error Output
```
<stack trace or error message>
```

## Failing Test
```python
<test code that demonstrates the bug>
```

## Suggested Fix
<if apparent, suggest how to fix>

## Environment
- Branch: `issue-<original_number>`
- Python version: <version>
- Node version: <version>

## Related Issues
- Parent issue: #<original_number>
EOF
)"
```

##### Step 4: Update Original Issue

```bash
gh issue comment <original_number> --body "## ⚠️ Verification Found Issues

Functional testing discovered the following bugs:

| Bug | Description | Severity |
|-----|-------------|----------|
| #<bug_number> | <description> | <high/medium/low> |

Verification cannot complete until these issues are resolved.
"

gh issue edit <original_number> --remove-label "ingested" --add-label "blocked"
```

### 4. Cleanup

After verification (pass or fail):
```bash
# Stop background services
pkill -f "uvicorn main:app"
pkill -f "npm run dev"

# Return to main branch
git checkout main
```

---

## Label Setup

Create labels if they don't exist:
```bash
gh label create "verified" --description "Issue has passed verification testing" --color "0E8A16"
gh label create "bug" --description "Bug or defect found" --color "D73A4A"
gh label create "blocked" --description "Issue is blocked by dependencies or bugs" --color "B60205"
```

## Directory Structure

```
parity-tests/
├── verification/
│   ├── conftest.py
│   ├── requirements.txt
│   ├── test_issue_<number>.py
│   ├── test_issue_<number>_ui.py
│   └── test_output_<number>.log
```

## Output

For each processed issue, report:
- Issue number and title
- Services started and health status
- Tests created and executed
- Test results (pass/fail counts)
- If bugs found:
  - Bug issue numbers created
  - Root cause summaries
  - Reproduction steps
- Final label status
