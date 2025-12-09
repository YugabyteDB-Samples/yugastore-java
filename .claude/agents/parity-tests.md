# Parity Tests Agent

Create functional/parity tests in Python to cover all API endpoints defined in the Swagger documentation.

## Instructions

1. For each service represented in the Swagger documentation, create a test folder
2. Folder naming convention: `parity-tests/{service}-tests/` where `{service}` is the name of the swagger document
3. Create Python unit tests to cover all endpoints

## Test Structure

For each service create:
- `test_{service}.py` - Main test file with all endpoint tests
- `conftest.py` - Pytest fixtures and configuration
- `requirements.txt` - Python dependencies (pytest, requests, etc.)

## Test Coverage

Each test file should include tests for:
- All GET endpoints with expected responses
- All POST endpoints with valid payloads
- Error cases (invalid input, missing parameters)
- Response schema validation against OpenAPI specs

## Requirements

- Use pytest as the testing framework
- Use requests library for HTTP calls
- Base URL should be configurable (default to localhost)
- Tests should be runnable independently
- Include setup/teardown for test data where needed

## Running Tests

Create a `run_all_tests.sh` script at the root of `parity-tests/` that:
- Sets up a Python virtual environment
- Installs dependencies
- Runs all test suites
- Reports pass/fail summary
