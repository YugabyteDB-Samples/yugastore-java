Create or update Python parity tests for all API endpoints.

Follow the instructions in `.claude/agents/parity-tests.md` to:

1. For each service in the Swagger documentation, create a test folder under `parity-tests/{service}-tests/`
2. Create Python pytest tests covering all endpoints
3. Include tests for success cases, error cases, and schema validation
4. Create `conftest.py` with fixtures and `requirements.txt` for dependencies
5. Create `run_all_tests.sh` script to execute all test suites

Run the tests and report the pass/fail summary.
