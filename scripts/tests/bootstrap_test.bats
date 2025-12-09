#!/usr/bin/env bats
# Unit tests for bootstrap.sh
# Run with: bats scripts/tests/bootstrap_test.bats

# Setup - runs before each test
setup() {
    # Get the directory where tests are located
    TESTS_DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" && pwd )"
    SCRIPTS_DIR="$(dirname "$TESTS_DIR")"
    BOOTSTRAP_SCRIPT="$SCRIPTS_DIR/bootstrap.sh"

    # Create a temp directory for test artifacts
    TEST_TEMP_DIR="$(mktemp -d)"

    # Export for use in tests
    export TESTS_DIR SCRIPTS_DIR BOOTSTRAP_SCRIPT TEST_TEMP_DIR
}

# Teardown - runs after each test
teardown() {
    # Clean up temp directory
    if [ -d "$TEST_TEMP_DIR" ]; then
        rm -rf "$TEST_TEMP_DIR"
    fi
}

# =============================================================================
# HELP AND USAGE TESTS
# =============================================================================

@test "bootstrap.sh exists and is executable" {
    [ -f "$BOOTSTRAP_SCRIPT" ]
    [ -x "$BOOTSTRAP_SCRIPT" ]
}

@test "--help flag displays usage information" {
    run "$BOOTSTRAP_SCRIPT" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *"Yugastore Bootstrap Script"* ]]
    [[ "$output" == *"Usage:"* ]]
    [[ "$output" == *"Options:"* ]]
}

@test "-h flag displays usage information" {
    run "$BOOTSTRAP_SCRIPT" -h
    [ "$status" -eq 0 ]
    [[ "$output" == *"Yugastore Bootstrap Script"* ]]
    [[ "$output" == *"Usage:"* ]]
}

@test "--help shows --non-interactive option" {
    run "$BOOTSTRAP_SCRIPT" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *"--non-interactive"* ]]
}

@test "--help shows --yugabyte=docker option" {
    run "$BOOTSTRAP_SCRIPT" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *"--yugabyte=docker"* ]]
}

@test "--help shows --yugabyte=native option" {
    run "$BOOTSTRAP_SCRIPT" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *"--yugabyte=native"* ]]
}

@test "--help shows examples section" {
    run "$BOOTSTRAP_SCRIPT" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *"Examples:"* ]]
}

@test "--help shows supported operating systems" {
    run "$BOOTSTRAP_SCRIPT" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *"Supported Operating Systems:"* ]]
    [[ "$output" == *"macOS"* ]]
    [[ "$output" == *"Linux"* ]]
}

# =============================================================================
# ARGUMENT PARSING TESTS
# =============================================================================

@test "unknown option shows error and usage" {
    run "$BOOTSTRAP_SCRIPT" --unknown-option
    [ "$status" -eq 1 ]
    [[ "$output" == *"Unknown option: --unknown-option"* ]]
    [[ "$output" == *"Usage:"* ]]
}

@test "invalid yugabyte option shows error" {
    run "$BOOTSTRAP_SCRIPT" --yugabyte=invalid
    [ "$status" -eq 1 ]
    [[ "$output" == *"Unknown option"* ]]
}

# =============================================================================
# SCRIPT STRUCTURE TESTS
# =============================================================================

@test "script contains show_help function" {
    run grep -q "show_help()" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script contains detect_os function" {
    run grep -q "detect_os()" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script contains log_message function" {
    run grep -q "log_message()" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script contains run_command function" {
    run grep -q "run_command()" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script contains get_exit_code_description function" {
    run grep -q "get_exit_code_description()" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script handles Darwin (macOS) in detect_os" {
    run grep -q "Darwin" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script handles Linux in detect_os" {
    run grep -q "Linux" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script handles Windows/CYGWIN in detect_os" {
    run grep -q "CYGWIN\|MINGW\|MSYS" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# DEFAULT VALUES TESTS
# =============================================================================

@test "script sets default INTERACTIVE to true" {
    run grep -q 'INTERACTIVE=true' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script sets default YUGABYTE_MODE to docker" {
    run grep -q 'YUGABYTE_MODE="docker"' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script defines LOG_FILE variable" {
    run grep -q 'LOG_FILE=' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# PREREQUISITE CHECK TESTS
# =============================================================================

@test "script checks for java prerequisite" {
    run grep -q "java" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script has install_java function" {
    run grep -q "install_java()" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script has check_java_version function" {
    run grep -q "check_java_version()" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script requires Java 17 or higher" {
    run grep -q "17" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
    run grep -qi "java.*17\|openjdk.*17\|openjdk@17" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script installs Java via Homebrew on macOS" {
    run grep -q "brew install openjdk@17" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script installs Java via apt-get on Debian/Ubuntu" {
    run grep -q "apt-get.*openjdk-17-jdk" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script installs Java via dnf/yum on RedHat/Fedora" {
    run grep -q "dnf install.*java-17-openjdk\|yum install.*java-17-openjdk" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script installs Java via pacman on Arch Linux" {
    run grep -q "pacman.*jdk17-openjdk" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script installs Java via Chocolatey or winget on Windows" {
    run grep -q "choco install.*openjdk17\|winget install.*OpenJDK" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script sets JAVA_HOME after installation" {
    run grep -q "JAVA_HOME" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script creates symlink for Java on macOS" {
    run grep -q "JavaVirtualMachines" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script provides manual install instructions for Java" {
    run grep -q "adoptium.net" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script checks for mvn prerequisite" {
    run grep -q "mvn" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script checks for python3 prerequisite" {
    run grep -q "python3" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script checks for ycqlsh or cqlsh prerequisite" {
    run grep -q "ycqlsh\|cqlsh" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script prefers ycqlsh over cqlsh" {
    # Verify ycqlsh is checked first (preferred)
    run grep -q 'command -v ycqlsh' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses CQLSH_CMD variable for CQL operations" {
    run grep -q 'CQLSH_CMD' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script sets CQLSH_NO_BUNDLED to avoid library conflicts" {
    # This avoids incompatibility between bundled six 1.12.0 and Python 3.12+
    run grep -q 'CQLSH_NO_BUNDLED=1' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script checks for psql prerequisite" {
    run grep -q "psql" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# EXIT CODE MAPPING TESTS
# =============================================================================

@test "script maps exit code 0 to Success" {
    run grep -A1 'case.*code.*in' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
    run grep -q '"Success"' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script maps exit code 1 to General error" {
    run grep -q "General error" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script maps exit code 127 to Command not found" {
    run grep -q "Command not found" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script maps exit code 126 to permission problem" {
    run grep -q "permission problem\|cannot execute" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# YUGABYTE MODE TESTS
# =============================================================================

@test "script has install_yugabyte_docker function" {
    run grep -q "install_yugabyte_docker()" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script has install_yugabyte_native function" {
    run grep -q "install_yugabyte_native()" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses Docker for yugabyte when mode is docker" {
    run grep -q 'docker run.*yugabyte' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses homebrew for macOS native install" {
    run grep -q "brew.*yugabytedb\|brew tap yugabyte" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# MICROSERVICE STARTUP TESTS
# =============================================================================

@test "script starts eureka service" {
    run grep -qi "eureka" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script starts api-gateway microservice" {
    run grep -qi "api-gateway" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script starts products microservice" {
    run grep -qi "products" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script starts checkout microservice" {
    run grep -qi "checkout" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script starts cart microservice" {
    run grep -qi "cart" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script starts react-ui" {
    run grep -qi "react-ui" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# BUILD TESTS
# =============================================================================

@test "script runs maven build with -DskipTests" {
    run grep -q 'mvn.*-DskipTests.*package' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script skips docker build in native mode with -Dexec.skip" {
    run grep -q '\-Dexec.skip=true' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# SCHEMA AND DATA TESTS
# =============================================================================

@test "script creates CQL schema" {
    run grep -qi "schema.cql\|cqlsh.*-f" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script loads sample data" {
    run grep -qi "dataload\|sample.*data" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script creates SQL tables" {
    run grep -qi "schema.sql\|psql.*-f" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# LOGGING TESTS
# =============================================================================

@test "script logs to bootstrap.log" {
    run grep -q 'bootstrap.log' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script has INFO log level" {
    run grep -q '"INFO"' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script has ERROR log level" {
    run grep -q '"ERROR"' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script has WARNING log level" {
    run grep -q '"WARNING"' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# OUTPUT INFORMATION TESTS
# =============================================================================

@test "script displays service URLs on completion" {
    run grep -q "localhost:8761\|localhost:8080\|localhost:8081" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script shows how to stop services" {
    run grep -qi "pkill\|stop.*services" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# PACKAGE MANAGER TESTS
# =============================================================================

@test "script supports apt-get for Debian-based Linux" {
    run grep -q "apt-get\|apt " "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script supports yum/dnf for RedHat-based Linux" {
    run grep -q "yum\|dnf" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script supports brew for macOS" {
    run grep -q "brew install\|brew " "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

@test "script checks command exit codes" {
    run grep -q '\$?' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script exits on build failure" {
    run grep -q 'exit 1' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script handles missing prerequisites" {
    run grep -qi "missing\|not found\|installing" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# PORT CONFIGURATION TESTS
# =============================================================================

@test "script uses port 8761 for Eureka" {
    run grep -q "8761" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses port 8080 for React UI" {
    run grep -q "8080" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses port 8081 for API Gateway" {
    run grep -q "8081" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses port 8082 for Products" {
    run grep -q "8082" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses port 8083 for Cart" {
    run grep -q "8083" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses port 8086 for Checkout" {
    run grep -q "8086" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses port 9042 for YCQL/Cassandra" {
    run grep -q "9042" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses port 5433 for YSQL/PostgreSQL" {
    run grep -q "5433" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

# =============================================================================
# FRONTEND URL DISPLAY TESTS
# =============================================================================

@test "script displays prominent FRONTEND URL section" {
    run grep -q "FRONTEND URL" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses printf for clickable URL" {
    run grep -q 'printf.*http://localhost:8080' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script uses OSC 8 escape sequence for hyperlink" {
    # OSC 8 is the escape sequence for clickable hyperlinks in terminals
    run grep -q '\\033\]8;;' "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}

@test "script displays click to open hint" {
    run grep -qi "click to open" "$BOOTSTRAP_SCRIPT"
    [ "$status" -eq 0 ]
}
