Create or update the bootstrap script for this application.

Follow the instructions in `.claude/agents/bootstrap-script.md` to:

1. Create a bash script (`scripts/bootstrap.sh`) that automates the setup and running of the application
2. Follow all commands from the README.md "Running the app on host" and "Build and run" sections
3. Add logging for each command with success/failure status
4. Support cross-platform execution (macOS, Windows, Linux)
5. Add `-h`/`--help` flag for usage information
6. Create unit tests in `scripts/tests/` using BATS framework
7. Update documentation as needed

Run the script and tests, fixing any issues until all tests pass.
