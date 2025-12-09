# Bootstrap Script Tests

This directory contains unit tests for the `bootstrap.sh` script using the BATS (Bash Automated Testing System) framework.

## Prerequisites

### Install BATS

**macOS (Homebrew):**
```bash
brew install bats-core
```

**Ubuntu/Debian:**
```bash
sudo apt-get install bats
```

**Fedora/RHEL:**
```bash
sudo dnf install bats
```

**From source:**
```bash
git clone https://github.com/bats-core/bats-core.git
cd bats-core
./install.sh /usr/local
```

## Running the Tests

From the repository root directory:

```bash
bats scripts/tests/bootstrap_test.bats
```

Or from the scripts directory:

```bash
cd scripts
bats tests/bootstrap_test.bats
```

### Verbose Output

For more detailed output showing each test:

```bash
bats --tap scripts/tests/bootstrap_test.bats
```

### Run Specific Tests

To run tests matching a pattern:

```bash
bats --filter "help" scripts/tests/bootstrap_test.bats
```

## Test Coverage

The test suite covers the following areas:

| Category | Description | Test Count |
|----------|-------------|------------|
| Help and Usage | `--help` and `-h` flag functionality | 8 |
| Argument Parsing | Command-line option handling and error cases | 2 |
| Script Structure | Presence of required functions | 8 |
| Default Values | Correct initialization of variables | 3 |
| Prerequisite Checks | Detection and installation of required tools (Java 17, mvn, python3, ycqlsh/cqlsh, psql) | 19 |
| Exit Code Mapping | Proper error code descriptions | 4 |
| YugabyteDB Mode | Docker and native installation functions | 4 |
| Microservice Startup | All 6 microservices are started | 6 |
| Build | Maven build configuration | 2 |
| Schema and Data | Database initialization steps | 3 |
| Logging | Log file and log levels | 4 |
| Output Information | Service URLs and stop instructions | 2 |
| Package Managers | Support for apt, yum, dnf, brew | 3 |
| Error Handling | Exit codes and missing prerequisites | 3 |
| Port Configuration | Correct ports for all services | 8 |
| Frontend URL Display | Clickable URL with OSC 8 escape sequence | 4 |

**Total: 83 tests**

## Test File Structure

```
scripts/
├── bootstrap.sh          # Main bootstrap script
└── tests/
    ├── README.md         # This file
    └── bootstrap_test.bats  # BATS test suite
```

## Writing Additional Tests

BATS tests follow this structure:

```bash
@test "description of test" {
    run command_to_test
    [ "$status" -eq 0 ]           # Check exit status
    [[ "$output" == *"expected"* ]] # Check output contains string
}
```

### Setup and Teardown

The test file includes `setup()` and `teardown()` functions that run before and after each test:

- `setup()`: Creates temp directories and sets up paths
- `teardown()`: Cleans up temp files

## Continuous Integration

To run tests in CI/CD pipelines, use:

```bash
bats --formatter tap scripts/tests/bootstrap_test.bats
```

This outputs TAP (Test Anything Protocol) format suitable for CI systems.

## Troubleshooting

### Tests not finding bootstrap.sh

Ensure you're running tests from the repository root:

```bash
cd /path/to/bookstore-r-us
bats scripts/tests/bootstrap_test.bats
```

### Permission denied

Make sure the test file is executable:

```bash
chmod +x scripts/tests/bootstrap_test.bats
```

### BATS not found

Verify BATS is installed and in your PATH:

```bash
which bats
bats --version
```
