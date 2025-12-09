#!/bin/bash

# Bootstrap script for Yugastore Java application
# This script follows the "Build and run" and "Running the app on host" instructions from README.md
#
# Usage:
#   ./bootstrap.sh                     # Interactive mode, assumes Docker YugabyteDB
#   ./bootstrap.sh --non-interactive   # Non-interactive mode, assumes Docker YugabyteDB already running
#   ./bootstrap.sh --yugabyte=docker   # Use Docker for YugabyteDB (install if needed)
#   ./bootstrap.sh --yugabyte=native   # Use native install for YugabyteDB (install if needed)
#   ./bootstrap.sh --help              # Show help

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"  # Project root is one level up from scripts/
LOG_FILE="$BASE_DIR/bootstrap.log"
MISSING_PREREQS=()
INTERACTIVE=true
YUGABYTE_MODE="docker"  # Default: docker

# ============================================================================
# PARSE COMMAND LINE ARGUMENTS
# ============================================================================
show_help() {
    echo "Yugastore Bootstrap Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --non-interactive     Run without prompts (assumes YugabyteDB is ready)"
    echo "  --yugabyte=docker     Use Docker to run YugabyteDB (default)"
    echo "  --yugabyte=native     Use native package manager to install YugabyteDB"
    echo "  --help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                          # Interactive mode with Docker YugabyteDB"
    echo "  $0 --non-interactive        # Non-interactive, assumes Docker YugabyteDB running"
    echo "  $0 --yugabyte=native        # Install YugabyteDB via native package manager"
    echo ""
    echo "Supported Operating Systems:"
    echo "  - macOS (Homebrew)"
    echo "  - Linux (apt, yum, dnf)"
    echo "  - Windows (WSL required for this script)"
    echo ""
}

for arg in "$@"; do
    case $arg in
        --non-interactive)
            INTERACTIVE=false
            shift
            ;;
        --yugabyte=docker)
            YUGABYTE_MODE="docker"
            shift
            ;;
        --yugabyte=native)
            YUGABYTE_MODE="native"
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            show_help
            exit 1
            ;;
    esac
done

# ============================================================================
# DETECT OPERATING SYSTEM
# ============================================================================
detect_os() {
    case "$(uname -s)" in
        Darwin*)
            OS="macos"
            ;;
        Linux*)
            # Detect Linux distribution
            if [ -f /etc/os-release ]; then
                . /etc/os-release
                case "$ID" in
                    ubuntu|debian|linuxmint|pop)
                        OS="linux-debian"
                        ;;
                    fedora|rhel|centos|rocky|almalinux)
                        OS="linux-redhat"
                        ;;
                    arch|manjaro)
                        OS="linux-arch"
                        ;;
                    *)
                        OS="linux-unknown"
                        ;;
                esac
            else
                OS="linux-unknown"
            fi
            ;;
        CYGWIN*|MINGW*|MSYS*)
            OS="windows"
            ;;
        *)
            OS="unknown"
            ;;
    esac
    echo "$OS"
}

OS_TYPE=$(detect_os)

# Initialize log file
echo "=== Yugastore Bootstrap Log ===" > "$LOG_FILE"
echo "Started at: $(date)" >> "$LOG_FILE"
echo "Working directory: $BASE_DIR" >> "$LOG_FILE"
echo "Operating System: $OS_TYPE" >> "$LOG_FILE"
echo "Interactive Mode: $INTERACTIVE" >> "$LOG_FILE"
echo "YugabyteDB Mode: $YUGABYTE_MODE" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Function to map common exit codes to descriptions
get_exit_code_description() {
    local code=$1
    case $code in
        0) echo "Success" ;;
        1) echo "General error" ;;
        2) echo "Misuse of shell command" ;;
        126) echo "Command invoked cannot execute (permission problem or not executable)" ;;
        127) echo "Command not found" ;;
        128) echo "Invalid argument to exit" ;;
        130) echo "Script terminated by Ctrl+C" ;;
        137) echo "Process killed (SIGKILL)" ;;
        139) echo "Segmentation fault (SIGSEGV)" ;;
        143) echo "Process terminated (SIGTERM)" ;;
        255) echo "Exit status out of range" ;;
        *) echo "Unknown error code" ;;
    esac
}

# Function to log a message
log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" >> "$LOG_FILE"
    if [ "$level" = "ERROR" ] || [ "$level" = "WARNING" ]; then
        echo "[$level] $message"
    fi
}

# Function to check if a command exists
check_command() {
    local cmd="$1"
    local install_hint="$2"

    if command -v "$cmd" &> /dev/null; then
        log_message "INFO" "Prerequisite check: $cmd found at $(which $cmd)"
        return 0
    else
        log_message "ERROR" "Prerequisite check: $cmd NOT FOUND. Install with: $install_hint"
        MISSING_PREREQS+=("$cmd (install with: $install_hint)")
        return 1
    fi
}

# ============================================================================
# OS-SPECIFIC PACKAGE INSTALLATION FUNCTIONS
# ============================================================================

# Install package based on OS
install_package() {
    local package_name="$1"
    local macos_package="${2:-$1}"
    local debian_package="${3:-$1}"
    local redhat_package="${4:-$1}"

    log_message "INFO" "Attempting to install $package_name for $OS_TYPE..."
    echo "Installing $package_name..."

    case "$OS_TYPE" in
        macos)
            if command -v brew &> /dev/null; then
                brew install "$macos_package" 2>&1 | tee -a "$LOG_FILE"
                return ${PIPESTATUS[0]}
            else
                log_message "ERROR" "Homebrew not found. Please install Homebrew first."
                return 1
            fi
            ;;
        linux-debian)
            if command -v apt-get &> /dev/null; then
                sudo apt-get update && sudo apt-get install -y "$debian_package" 2>&1 | tee -a "$LOG_FILE"
                return ${PIPESTATUS[0]}
            else
                log_message "ERROR" "apt-get not found."
                return 1
            fi
            ;;
        linux-redhat)
            if command -v dnf &> /dev/null; then
                sudo dnf install -y "$redhat_package" 2>&1 | tee -a "$LOG_FILE"
                return ${PIPESTATUS[0]}
            elif command -v yum &> /dev/null; then
                sudo yum install -y "$redhat_package" 2>&1 | tee -a "$LOG_FILE"
                return ${PIPESTATUS[0]}
            else
                log_message "ERROR" "Neither dnf nor yum found."
                return 1
            fi
            ;;
        linux-arch)
            if command -v pacman &> /dev/null; then
                sudo pacman -S --noconfirm "$debian_package" 2>&1 | tee -a "$LOG_FILE"
                return ${PIPESTATUS[0]}
            else
                log_message "ERROR" "pacman not found."
                return 1
            fi
            ;;
        windows)
            if command -v choco &> /dev/null; then
                choco install -y "$package_name" 2>&1 | tee -a "$LOG_FILE"
                return ${PIPESTATUS[0]}
            elif command -v winget &> /dev/null; then
                winget install --accept-package-agreements --accept-source-agreements "$package_name" 2>&1 | tee -a "$LOG_FILE"
                return ${PIPESTATUS[0]}
            else
                log_message "ERROR" "Neither Chocolatey nor winget found. Please install packages manually."
                return 1
            fi
            ;;
        *)
            log_message "ERROR" "Unsupported OS: $OS_TYPE"
            return 1
            ;;
    esac
}

# Install Java 17 (required version for this application)
install_java() {
    log_message "INFO" "Installing Java 17..."
    echo "Installing OpenJDK 17..."

    case "$OS_TYPE" in
        macos)
            # Install OpenJDK 17 via Homebrew
            brew install openjdk@17 2>&1 | tee -a "$LOG_FILE"

            # Create symlink so system java wrappers find this JDK
            if [ -d "/opt/homebrew/opt/openjdk@17" ]; then
                sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk 2>/dev/null || true
                export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
                export JAVA_HOME="/opt/homebrew/opt/openjdk@17"
                log_message "INFO" "Java 17 installed via Homebrew and symlinked"
            elif [ -d "/usr/local/opt/openjdk@17" ]; then
                # Intel Mac path
                sudo ln -sfn /usr/local/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk 2>/dev/null || true
                export PATH="/usr/local/opt/openjdk@17/bin:$PATH"
                export JAVA_HOME="/usr/local/opt/openjdk@17"
                log_message "INFO" "Java 17 installed via Homebrew (Intel) and symlinked"
            fi
            ;;
        linux-debian)
            sudo apt-get update 2>&1 | tee -a "$LOG_FILE"
            sudo apt-get install -y openjdk-17-jdk 2>&1 | tee -a "$LOG_FILE"
            # Set JAVA_HOME
            export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
            [ -d "$JAVA_HOME" ] || export JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
            log_message "INFO" "Java 17 installed via apt-get"
            ;;
        linux-redhat)
            if command -v dnf &> /dev/null; then
                sudo dnf install -y java-17-openjdk-devel 2>&1 | tee -a "$LOG_FILE"
            else
                sudo yum install -y java-17-openjdk-devel 2>&1 | tee -a "$LOG_FILE"
            fi
            export JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
            log_message "INFO" "Java 17 installed via dnf/yum"
            ;;
        linux-arch)
            sudo pacman -S --noconfirm jdk17-openjdk 2>&1 | tee -a "$LOG_FILE"
            export JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
            log_message "INFO" "Java 17 installed via pacman"
            ;;
        windows)
            # Try Chocolatey first, then winget
            if command -v choco &> /dev/null; then
                choco install -y openjdk17 2>&1 | tee -a "$LOG_FILE"
                log_message "INFO" "Java 17 installed via Chocolatey"
            elif command -v winget &> /dev/null; then
                winget install --accept-package-agreements --accept-source-agreements Microsoft.OpenJDK.17 2>&1 | tee -a "$LOG_FILE"
                log_message "INFO" "Java 17 installed via winget"
            else
                log_message "ERROR" "Neither Chocolatey nor winget available. Please install Java 17 manually."
                echo "ERROR: Please install Java 17 manually from https://adoptium.net/"
                return 1
            fi
            ;;
        *)
            log_message "ERROR" "Unsupported OS for Java installation: $OS_TYPE"
            echo "ERROR: Please install Java 17 manually from https://adoptium.net/"
            return 1
            ;;
    esac

    return 0
}

# Check if Java version is 17 or higher
check_java_version() {
    if ! command -v java &> /dev/null; then
        return 1
    fi

    # Get Java version number
    java_version=$(java -version 2>&1 | head -n 1 | sed -E 's/.*"([0-9]+)\.?.*/\1/')

    if [ -z "$java_version" ]; then
        # Try alternate parsing for different java -version formats
        java_version=$(java -version 2>&1 | head -n 1 | grep -oE '[0-9]+' | head -1)
    fi

    if [ -n "$java_version" ] && [ "$java_version" -ge 17 ] 2>/dev/null; then
        log_message "INFO" "Java version $java_version detected (>= 17 required)"
        return 0
    else
        log_message "WARNING" "Java version $java_version detected, but Java 17+ is required"
        return 1
    fi
}

# Install Maven
install_maven() {
    log_message "INFO" "Installing Maven..."
    case "$OS_TYPE" in
        macos)
            brew install maven 2>&1 | tee -a "$LOG_FILE"
            ;;
        linux-debian)
            sudo apt-get update && sudo apt-get install -y maven 2>&1 | tee -a "$LOG_FILE"
            ;;
        linux-redhat)
            sudo dnf install -y maven 2>&1 | tee -a "$LOG_FILE" || \
            sudo yum install -y maven 2>&1 | tee -a "$LOG_FILE"
            ;;
        linux-arch)
            sudo pacman -S --noconfirm maven 2>&1 | tee -a "$LOG_FILE"
            ;;
        windows)
            choco install -y maven 2>&1 | tee -a "$LOG_FILE" || \
            winget install --accept-package-agreements Apache.Maven 2>&1 | tee -a "$LOG_FILE"
            ;;
    esac
}

# Install Python 3
install_python() {
    log_message "INFO" "Installing Python 3..."
    case "$OS_TYPE" in
        macos)
            brew install python@3 2>&1 | tee -a "$LOG_FILE"
            ;;
        linux-debian)
            sudo apt-get update && sudo apt-get install -y python3 python3-pip 2>&1 | tee -a "$LOG_FILE"
            ;;
        linux-redhat)
            sudo dnf install -y python3 python3-pip 2>&1 | tee -a "$LOG_FILE" || \
            sudo yum install -y python3 python3-pip 2>&1 | tee -a "$LOG_FILE"
            ;;
        linux-arch)
            sudo pacman -S --noconfirm python python-pip 2>&1 | tee -a "$LOG_FILE"
            ;;
        windows)
            choco install -y python3 2>&1 | tee -a "$LOG_FILE" || \
            winget install --accept-package-agreements Python.Python.3.11 2>&1 | tee -a "$LOG_FILE"
            ;;
    esac
}

# Install psql client
install_psql() {
    log_message "INFO" "Installing PostgreSQL client..."
    case "$OS_TYPE" in
        macos)
            brew install libpq 2>&1 | tee -a "$LOG_FILE"
            export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
            ;;
        linux-debian)
            sudo apt-get update && sudo apt-get install -y postgresql-client 2>&1 | tee -a "$LOG_FILE"
            ;;
        linux-redhat)
            sudo dnf install -y postgresql 2>&1 | tee -a "$LOG_FILE" || \
            sudo yum install -y postgresql 2>&1 | tee -a "$LOG_FILE"
            ;;
        linux-arch)
            sudo pacman -S --noconfirm postgresql-libs 2>&1 | tee -a "$LOG_FILE"
            ;;
        windows)
            choco install -y postgresql 2>&1 | tee -a "$LOG_FILE"
            ;;
    esac
}

# Install Docker
install_docker() {
    log_message "INFO" "Installing Docker..."
    case "$OS_TYPE" in
        macos)
            echo "Please install Docker Desktop for macOS from https://www.docker.com/products/docker-desktop"
            echo "After installation, start Docker Desktop and re-run this script."
            log_message "ERROR" "Docker Desktop must be installed manually on macOS"
            return 1
            ;;
        linux-debian)
            sudo apt-get update
            sudo apt-get install -y docker.io 2>&1 | tee -a "$LOG_FILE"
            sudo systemctl start docker
            sudo systemctl enable docker
            sudo usermod -aG docker $USER
            ;;
        linux-redhat)
            sudo dnf install -y docker 2>&1 | tee -a "$LOG_FILE" || \
            sudo yum install -y docker 2>&1 | tee -a "$LOG_FILE"
            sudo systemctl start docker
            sudo systemctl enable docker
            sudo usermod -aG docker $USER
            ;;
        linux-arch)
            sudo pacman -S --noconfirm docker 2>&1 | tee -a "$LOG_FILE"
            sudo systemctl start docker
            sudo systemctl enable docker
            sudo usermod -aG docker $USER
            ;;
        windows)
            echo "Please install Docker Desktop for Windows from https://www.docker.com/products/docker-desktop"
            echo "After installation, start Docker Desktop and re-run this script."
            log_message "ERROR" "Docker Desktop must be installed manually on Windows"
            return 1
            ;;
    esac
}

# ============================================================================
# YUGABYTEDB INSTALLATION FUNCTIONS
# ============================================================================

# Install YugabyteDB via Docker
install_yugabyte_docker() {
    log_message "INFO" "Setting up YugabyteDB via Docker..."
    echo "Setting up YugabyteDB via Docker..."

    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        log_message "WARNING" "Docker not found. Attempting to install..."
        install_docker
        if ! command -v docker &> /dev/null; then
            log_message "ERROR" "Docker installation failed or requires manual intervention."
            echo "ERROR: Docker is required for --yugabyte=docker mode."
            echo "Please install Docker and re-run this script."
            return 1
        fi
    fi

    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        log_message "ERROR" "Docker daemon is not running."
        echo "ERROR: Docker daemon is not running. Please start Docker and re-run this script."
        return 1
    fi

    # Check if yugabyte container already exists
    if docker ps -a --format '{{.Names}}' | grep -q '^yugabyte$'; then
        # Check if it's running
        if docker ps --format '{{.Names}}' | grep -q '^yugabyte$'; then
            log_message "INFO" "YugabyteDB container is already running."
            echo "YugabyteDB container is already running."
            return 0
        else
            # Start existing container
            log_message "INFO" "Starting existing YugabyteDB container..."
            echo "Starting existing YugabyteDB container..."
            docker start yugabyte 2>&1 | tee -a "$LOG_FILE"
            sleep 10
            return 0
        fi
    fi

    # Run new YugabyteDB container
    log_message "INFO" "Starting new YugabyteDB Docker container..."
    echo "Starting new YugabyteDB Docker container..."
    docker run -d --name yugabyte \
        -p7000:7000 -p9000:9000 -p5433:5433 -p9042:9042 \
        yugabytedb/yugabyte:latest \
        bin/yugabyted start --daemon=false 2>&1 | tee -a "$LOG_FILE"

    if [ $? -ne 0 ]; then
        log_message "ERROR" "Failed to start YugabyteDB Docker container."
        return 1
    fi

    # Wait for YugabyteDB to be ready
    echo "Waiting for YugabyteDB to initialize (30 seconds)..."
    sleep 30

    log_message "INFO" "YugabyteDB Docker container started successfully."
    return 0
}

# Install YugabyteDB natively based on OS
install_yugabyte_native() {
    log_message "INFO" "Installing YugabyteDB natively for $OS_TYPE..."
    echo "Installing YugabyteDB natively..."

    case "$OS_TYPE" in
        macos)
            echo "Installing YugabyteDB via Homebrew..."
            brew tap yugabyte/yugabytedb 2>&1 | tee -a "$LOG_FILE"
            brew install yugabytedb 2>&1 | tee -a "$LOG_FILE"
            if [ $? -ne 0 ]; then
                log_message "ERROR" "Failed to install YugabyteDB via Homebrew."
                return 1
            fi
            echo "Starting YugabyteDB..."
            yugabyted start 2>&1 | tee -a "$LOG_FILE"
            ;;

        linux-debian|linux-redhat|linux-arch|linux-unknown)
            echo "Installing YugabyteDB on Linux..."
            # Download and install YugabyteDB
            YUGABYTE_VERSION="2.20.1.0"
            YUGABYTE_TAR="yugabyte-${YUGABYTE_VERSION}-linux-x86_64.tar.gz"
            YUGABYTE_URL="https://downloads.yugabyte.com/releases/${YUGABYTE_VERSION}/${YUGABYTE_TAR}"

            echo "Downloading YugabyteDB ${YUGABYTE_VERSION}..."
            log_message "INFO" "Downloading from $YUGABYTE_URL"

            if command -v wget &> /dev/null; then
                wget -q "$YUGABYTE_URL" -O "/tmp/${YUGABYTE_TAR}" 2>&1 | tee -a "$LOG_FILE"
            elif command -v curl &> /dev/null; then
                curl -sL "$YUGABYTE_URL" -o "/tmp/${YUGABYTE_TAR}" 2>&1 | tee -a "$LOG_FILE"
            else
                log_message "ERROR" "Neither wget nor curl found. Cannot download YugabyteDB."
                return 1
            fi

            echo "Extracting YugabyteDB..."
            tar -xzf "/tmp/${YUGABYTE_TAR}" -C /opt 2>&1 | tee -a "$LOG_FILE" || \
            sudo tar -xzf "/tmp/${YUGABYTE_TAR}" -C /opt 2>&1 | tee -a "$LOG_FILE"

            YUGABYTE_HOME="/opt/yugabyte-${YUGABYTE_VERSION}"
            export PATH="$YUGABYTE_HOME/bin:$PATH"

            echo "Starting YugabyteDB..."
            "$YUGABYTE_HOME/bin/yugabyted" start 2>&1 | tee -a "$LOG_FILE"
            ;;

        windows)
            # ============================================================================
            # MANUAL INTERVENTION REQUIRED: Windows Native YugabyteDB
            # ============================================================================
            # NOTE: YugabyteDB does not have a native Windows installer.
            # Windows users must use Docker or WSL2 to run YugabyteDB.
            # ============================================================================
            log_message "ERROR" "Native YugabyteDB installation is not supported on Windows."
            echo ""
            echo "=========================================="
            echo "MANUAL STEP REQUIRED: Windows YugabyteDB"
            echo "=========================================="
            echo ""
            echo "YugabyteDB does not have a native Windows installer."
            echo "Please use one of these alternatives:"
            echo ""
            echo "  1. Docker Desktop for Windows:"
            echo "     docker run -d --name yugabyte -p7000:7000 -p9000:9000 -p5433:5433 -p9042:9042 yugabytedb/yugabyte:latest bin/yugabyted start --daemon=false"
            echo ""
            echo "  2. WSL2 (Windows Subsystem for Linux):"
            echo "     Run this script inside WSL2 with --yugabyte=native"
            echo ""
            log_message "INFO" "Windows users should use Docker or WSL2 for YugabyteDB."
            return 1
            ;;

        *)
            log_message "ERROR" "Unsupported OS for native YugabyteDB installation: $OS_TYPE"
            return 1
            ;;
    esac

    # Wait for YugabyteDB to be ready
    echo "Waiting for YugabyteDB to initialize (30 seconds)..."
    sleep 30

    return 0
}

# Function to run a command with logging
run_command() {
    local description="$1"
    local command="$2"
    local working_dir="${3:-$BASE_DIR}"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] RUNNING: $description" >> "$LOG_FILE"
    echo "  Command: $command" >> "$LOG_FILE"
    echo "  Directory: $working_dir" >> "$LOG_FILE"

    # Run command and capture output and exit code
    cd "$working_dir"
    output=$(eval "$command" 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "  Status: SUCCESS" >> "$LOG_FILE"
        echo "  Output: $output" >> "$LOG_FILE"
    else
        local error_desc=$(get_exit_code_description $exit_code)
        echo "  Status: FAILURE" >> "$LOG_FILE"
        echo "  Exit Code: $exit_code ($error_desc)" >> "$LOG_FILE"
        echo "  Error Output: $output" >> "$LOG_FILE"
    fi
    echo "" >> "$LOG_FILE"

    cd "$BASE_DIR"
    return $exit_code
}

# Function to run a background service with logging
run_service_background() {
    local description="$1"
    local command="$2"
    local working_dir="${3:-$BASE_DIR}"
    local log_prefix="$4"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] STARTING SERVICE: $description" >> "$LOG_FILE"
    echo "  Command: $command" >> "$LOG_FILE"
    echo "  Directory: $working_dir" >> "$LOG_FILE"

    cd "$working_dir"
    nohup $command > "${BASE_DIR}/${log_prefix}.out" 2>&1 &
    local pid=$!

    # Give the service a moment to start or fail immediately
    sleep 3

    if ps -p $pid > /dev/null 2>&1; then
        echo "  Status: SUCCESS (PID: $pid)" >> "$LOG_FILE"
        echo "  Service output logged to: ${log_prefix}.out" >> "$LOG_FILE"
        echo "  Started $description (PID: $pid)"
    else
        wait $pid 2>/dev/null
        exit_code=$?
        local error_desc=$(get_exit_code_description $exit_code)
        echo "  Status: FAILURE" >> "$LOG_FILE"
        echo "  Exit Code: $exit_code ($error_desc)" >> "$LOG_FILE"
        echo "  Error Output: $(tail -20 ${BASE_DIR}/${log_prefix}.out 2>/dev/null)" >> "$LOG_FILE"
        echo "  FAILED to start $description"
    fi
    echo "" >> "$LOG_FILE"

    cd "$BASE_DIR"
}

# ============================================================================
# MAIN SCRIPT
# ============================================================================

echo "=========================================="
echo "Yugastore Bootstrap Script"
echo "=========================================="
echo "Log file: $LOG_FILE"
echo "Operating System: $OS_TYPE"
echo "Interactive Mode: $INTERACTIVE"
echo "YugabyteDB Mode: $YUGABYTE_MODE"
echo ""

# ============================================================================
# PREREQUISITE CHECKS
# ============================================================================
echo "Checking prerequisites..."
log_message "INFO" "=== PREREQUISITE CHECKS ==="

# Check for package manager based on OS
case "$OS_TYPE" in
    macos)
        if ! command -v brew &> /dev/null; then
            log_message "ERROR" "Homebrew is not installed. Please install it first:"
            log_message "ERROR" "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            echo ""
            echo "ERROR: Homebrew is not installed."
            echo "Please install Homebrew first by running:"
            echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            echo ""
            echo "Then re-run this script."
            exit 1
        fi
        log_message "INFO" "Prerequisite check: brew found at $(which brew)"
        ;;
    linux-debian)
        log_message "INFO" "Using apt-get package manager"
        ;;
    linux-redhat)
        log_message "INFO" "Using dnf/yum package manager"
        ;;
    windows)
        if ! command -v choco &> /dev/null && ! command -v winget &> /dev/null; then
            log_message "WARNING" "Neither Chocolatey nor winget found. Package installation may fail."
        fi
        ;;
esac

# Check for Java 17+
if ! command -v java &> /dev/null; then
    log_message "WARNING" "Java not found. Attempting to install OpenJDK 17..."
    install_java
elif ! check_java_version; then
    log_message "WARNING" "Java version is below 17. Attempting to install OpenJDK 17..."
    install_java
fi

# Verify Java is installed and version is correct
if command -v java &> /dev/null; then
    java_version_full=$(java -version 2>&1 | head -n 1)
    log_message "INFO" "Java version: $java_version_full"
    echo "  Java: $java_version_full"

    if ! check_java_version; then
        log_message "ERROR" "Java 17 or higher is required. Current version does not meet requirements."
        echo "ERROR: Java 17+ is required. Please install from https://adoptium.net/"
        exit 1
    fi
else
    log_message "ERROR" "Java installation failed. Please install Java 17 manually."
    echo "ERROR: Java 17 is required. Please install from https://adoptium.net/"
    exit 1
fi

# Check for Maven
if ! command -v mvn &> /dev/null; then
    log_message "WARNING" "Maven not found. Attempting to install..."
    install_maven
fi

if ! command -v mvn &> /dev/null; then
    log_message "ERROR" "Maven installation failed."
    exit 1
fi

# Check for Python 3 (needed for data loading)
if ! command -v python3 &> /dev/null; then
    log_message "WARNING" "Python 3 not found. Attempting to install..."
    install_python
fi

# Check for ycqlsh or cqlsh (Cassandra Query Language Shell)
# Prefer ycqlsh (YugabyteDB's bundled version) over cqlsh to avoid version warnings
# Install Python dependencies required by ycqlsh
log_message "INFO" "Installing Python dependencies for CQL shell..."
pip3 install six cassandra-driver geomet &>/dev/null || true

# Set CQLSH_NO_BUNDLED to avoid using outdated bundled libraries (six 1.12.0)
# that are incompatible with Python 3.12+
export CQLSH_NO_BUNDLED=1

if command -v ycqlsh &> /dev/null; then
    CQLSH_CMD="ycqlsh"
    log_message "INFO" "Using YugabyteDB's ycqlsh for CQL operations"
elif command -v cqlsh &> /dev/null; then
    CQLSH_CMD="cqlsh"
    log_message "WARNING" "Using generic cqlsh - may show version warnings with YugabyteDB"
else
    log_message "WARNING" "Neither ycqlsh nor cqlsh found. Will attempt to use ycqlsh after YugabyteDB install."
    CQLSH_CMD="ycqlsh"  # Default to ycqlsh, will be available after YugabyteDB native install
fi

# Check for psql (PostgreSQL client)
if ! command -v psql &> /dev/null; then
    log_message "WARNING" "psql not found. Attempting to install PostgreSQL client..."
    install_psql
fi

# Add libpq to PATH on macOS if needed
if [ "$OS_TYPE" = "macos" ] && [ -d "/opt/homebrew/opt/libpq/bin" ]; then
    export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
fi

# ============================================================================
# YUGABYTEDB SETUP
# ============================================================================
log_message "INFO" "=== YUGABYTEDB SETUP ==="
echo ""
echo "=========================================="
echo "Setting up YugabyteDB ($YUGABYTE_MODE mode)..."
echo "=========================================="

if [ "$YUGABYTE_MODE" = "docker" ]; then
    install_yugabyte_docker
    yugabyte_result=$?
elif [ "$YUGABYTE_MODE" = "native" ]; then
    install_yugabyte_native
    yugabyte_result=$?
fi

if [ $yugabyte_result -ne 0 ]; then
    if [ "$INTERACTIVE" = true ]; then
        echo ""
        echo "YugabyteDB setup failed or requires manual intervention."
        read -p "Do you want to continue anyway (assuming YugabyteDB is already running)? (y/n): " continue_anyway
        if [ "$continue_anyway" != "y" ] && [ "$continue_anyway" != "Y" ]; then
            log_message "ERROR" "User chose not to continue after YugabyteDB setup failure."
            exit 1
        fi
    else
        log_message "ERROR" "YugabyteDB setup failed in non-interactive mode."
        echo "ERROR: YugabyteDB setup failed. Please ensure YugabyteDB is running and re-run this script."
        exit 1
    fi
fi

# Verify YugabyteDB connectivity
echo "Verifying YugabyteDB connectivity..."

# Re-check for ycqlsh after YugabyteDB installation (native install provides it)
if command -v ycqlsh &> /dev/null; then
    CQLSH_CMD="ycqlsh"
elif command -v cqlsh &> /dev/null; then
    CQLSH_CMD="cqlsh"
fi

if command -v $CQLSH_CMD &> /dev/null; then
    if $CQLSH_CMD -e "SELECT now() FROM system.local;" &>/dev/null; then
        log_message "INFO" "YugabyteDB YCQL connection verified using $CQLSH_CMD"
        echo "  YCQL (Cassandra) connection: OK (using $CQLSH_CMD)"
    else
        log_message "WARNING" "Could not connect to YugabyteDB YCQL on localhost:9042"
        echo "  WARNING: Could not connect to YCQL on localhost:9042"
    fi
else
    log_message "WARNING" "No CQL shell found (ycqlsh or cqlsh)"
    echo "  WARNING: No CQL shell available"
fi

if command -v psql &> /dev/null; then
    if psql -h localhost -p 5433 -U yugabyte -d yugabyte -c "SELECT 1;" &>/dev/null; then
        log_message "INFO" "YugabyteDB YSQL connection verified"
        echo "  YSQL (PostgreSQL) connection: OK"
    else
        log_message "WARNING" "Could not connect to YugabyteDB YSQL on localhost:5433"
        echo "  WARNING: Could not connect to YSQL on localhost:5433"
    fi
fi

# ============================================================================
# BUILD THE APPLICATION
# ============================================================================
echo ""
echo "=========================================="
echo "Building the application..."
echo "=========================================="
log_message "INFO" "=== BUILD PHASE ==="

# Skip Docker build if not using Docker mode (exec plugin runs docker build)
if [ "$YUGABYTE_MODE" = "docker" ]; then
    MVN_BUILD_CMD="mvn -DskipTests package"
else
    # Skip the exec plugin which runs docker build
    MVN_BUILD_CMD="mvn -DskipTests -Dexec.skip=true package"
    log_message "INFO" "Skipping Docker image builds (native mode)"
fi

run_command "Build application with Maven" "$MVN_BUILD_CMD"
if [ $? -ne 0 ]; then
    log_message "ERROR" "Build failed. Check $LOG_FILE for details."
    echo "ERROR: Build failed. Check $LOG_FILE for details."
    exit 1
fi
echo "Build completed successfully."

# ============================================================================
# STEP 1: INSTALL AND INITIALIZE YUGABYTEDB
# ============================================================================
echo ""
echo "=========================================="
echo "Step 1: Initializing YugabyteDB schemas..."
echo "=========================================="
log_message "INFO" "=== STEP 1: DATABASE INITIALIZATION ==="

# Create CQL schema using ycqlsh (preferred) or cqlsh
echo "Creating CQL schema..."
run_command "Create CQL schema ($CQLSH_CMD -f schema.cql)" "$CQLSH_CMD -f schema.cql" "$BASE_DIR/resources"
if [ $? -ne 0 ]; then
    log_message "WARNING" "CQL schema creation failed. Check $LOG_FILE for details."
    echo "WARNING: CQL schema creation failed."
fi

# Load sample data
echo "Loading sample data..."
run_command "Load sample data (./dataload.sh)" "./dataload.sh" "$BASE_DIR/resources"
if [ $? -ne 0 ]; then
    log_message "WARNING" "Data load failed. Check $LOG_FILE for details."
    echo "WARNING: Data load failed."
fi

# Create YSQL tables
echo "Creating YSQL tables..."
run_command "Create YSQL schema (psql -f schema.sql)" "psql -h localhost -p 5433 -U yugabyte -d yugabyte -f schema.sql" "$BASE_DIR/resources"
if [ $? -ne 0 ]; then
    log_message "WARNING" "YSQL schema creation failed. Check $LOG_FILE for details."
    echo "WARNING: YSQL schema creation failed."
fi

# ============================================================================
# STEP 2: START EUREKA SERVICE DISCOVERY
# ============================================================================
echo ""
echo "=========================================="
echo "Step 2: Starting Eureka service discovery..."
echo "=========================================="
log_message "INFO" "=== STEP 2: EUREKA SERVICE DISCOVERY ==="

run_service_background "Eureka Service Discovery" "mvn spring-boot:run" "$BASE_DIR/eureka-server-local" "eureka-server"
echo "Waiting for Eureka to initialize (30 seconds)..."
sleep 30

# Verify Eureka is running
if curl -s http://localhost:8761 > /dev/null 2>&1; then
    log_message "INFO" "Eureka Service Discovery is responding on http://localhost:8761"
    echo "Eureka is running at http://localhost:8761"
else
    log_message "WARNING" "Eureka may not be fully started yet. Check eureka-server.out for details."
    echo "WARNING: Eureka may not be fully started. Check eureka-server.out"
fi

# ============================================================================
# STEP 2 (continued): START API GATEWAY MICROSERVICE
# ============================================================================
echo ""
echo "=========================================="
echo "Starting API Gateway microservice..."
echo "=========================================="
log_message "INFO" "=== API GATEWAY MICROSERVICE ==="

run_service_background "API Gateway Microservice" "mvn spring-boot:run" "$BASE_DIR/api-gateway-microservice" "api-gateway"
sleep 10

# ============================================================================
# STEP 3: START PRODUCTS MICROSERVICE
# ============================================================================
echo ""
echo "=========================================="
echo "Step 3: Starting Products microservice..."
echo "=========================================="
log_message "INFO" "=== STEP 3: PRODUCTS MICROSERVICE ==="

run_service_background "Products Microservice" "mvn spring-boot:run" "$BASE_DIR/products-microservice" "products"
sleep 10

# ============================================================================
# STEP 4: START CHECKOUT MICROSERVICE
# ============================================================================
echo ""
echo "=========================================="
echo "Step 4: Starting Checkout microservice..."
echo "=========================================="
log_message "INFO" "=== STEP 4: CHECKOUT MICROSERVICE ==="

run_service_background "Checkout Microservice" "mvn spring-boot:run" "$BASE_DIR/checkout-microservice" "checkout"
sleep 10

# ============================================================================
# STEP 5: START CART MICROSERVICE
# ============================================================================
echo ""
echo "=========================================="
echo "Step 5: Starting Cart microservice..."
echo "=========================================="
log_message "INFO" "=== STEP 5: CART MICROSERVICE ==="

run_service_background "Cart Microservice" "mvn spring-boot:run" "$BASE_DIR/cart-microservice" "cart"
sleep 10

# ============================================================================
# STEP 6: START THE UI
# ============================================================================
echo ""
echo "=========================================="
echo "Step 6: Starting React UI..."
echo "=========================================="
log_message "INFO" "=== STEP 6: REACT UI ==="

run_service_background "React UI" "mvn spring-boot:run" "$BASE_DIR/react-ui" "react-ui"
sleep 10

# ============================================================================
# COMPLETION
# ============================================================================
echo ""
echo "==========================================" | tee -a "$LOG_FILE"
echo "=== Bootstrap Complete ===" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"
echo "Completed at: $(date)" >> "$LOG_FILE"
echo ""
echo "Services should be available at:"
echo "  - Eureka Dashboard: http://localhost:8761/"
echo "  - API Gateway:      http://localhost:8081/"
echo "  - Products:         http://localhost:8082/"
echo "  - Cart:             http://localhost:8083/"
echo "  - Login:            http://localhost:8085/"
echo "  - Checkout:         http://localhost:8086/"
echo ""
echo "=========================================="
echo "  FRONTEND URL (click to open):"
echo ""
# Use OSC 8 hyperlink escape sequence for clickable URL in supported terminals
printf "  \033]8;;http://localhost:8080/\033\\http://localhost:8080/\033]8;;\033\\\n"
echo ""
echo "=========================================="
echo ""
echo "Log files:"
echo "  - Main log:         $LOG_FILE"
echo "  - Eureka:           eureka-server.out"
echo "  - API Gateway:      api-gateway.out"
echo "  - Products:         products.out"
echo "  - Checkout:         checkout.out"
echo "  - Cart:             cart.out"
echo "  - React UI:         react-ui.out"
echo ""
echo "To stop all services, run:"
echo "  pkill -f 'spring-boot:run'"
echo ""
if [ "$YUGABYTE_MODE" = "docker" ]; then
    echo "To stop YugabyteDB Docker container:"
    echo "  docker stop yugabyte"
    echo ""
fi
