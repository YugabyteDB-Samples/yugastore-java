Perform quality verification on GitHub issues labeled `ingested`.

Follow the instructions in `.claude/agents/verification.md` to:

1. **List all issues** with the `ingested` label

2. **For each issue**:
   - Checkout the implementation branch (`issue-<number>`)
   - Start required services:
     - Python backend services (`python_services/`)
     - Next.js frontend (`nextjs-frontend/`)
   - Wait for services to be healthy

3. **Create test assets** in `parity-tests/verification/`:
   - Functional tests based on acceptance criteria
   - API endpoint tests
   - UI flow tests (if applicable)
   - Edge case and error handling tests

4. **Execute and debug tests**:
   - Run pytest with verbose output
   - Debug failing tests
   - Iterate until tests pass or bugs are confirmed

5. **If all tests pass (Path A)**:
   - Comment on issue with test results
   - Update label from `ingested` to `verified`

6. **If bugs are found (Path B)**:
   - Perform root cause analysis
   - Document reproduction steps
   - Create new bug issues with:
     - Labels: `ingested`, `bug`
     - Root cause analysis
     - Reproduction steps
     - Error output
     - Suggested fix (if apparent)
   - Update original issue as `blocked`
   - Reference bug issues in original issue

7. **Cleanup**: Stop services and return to main branch

8. **Report** on all processed issues with test results and any bugs found.

Create labels (`verified`, `bug`, `blocked`) if they don't exist.
