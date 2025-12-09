# Bootstrap Script Agent

Create a bash script that automates the setup and running of this application.

## Instructions

1. Follow the README.md file and create a bash script called `bootstrap.sh` saved in the `/scripts` folder
2. The script should follow all commands under "Running the app on host" and "Build and run" sections
3. For each command, write out a log that appends a line indicating:
   - The command to be run
   - Success or failure of that command
   - If there was an error, write the error or error code to that line
   - If it is an error code, attempt to map that to the text of the error code

## Requirements

- Add the option to run non-interactively, passing a flagged override variable
- Create logic to determine which operating system is running (macOS, Windows, Linux)
- Provide usage information when given a `-h` or `--help` flag
- If any prerequisites are missing, add those to the script
- If there are steps that require human intervention, note that as a comment and log message

## Testing

- Create a `/tests` directory under `/scripts`
- Create a suite of unit tests that covers all script functionality, input options, and error cases
- Use BATS (Bash Automated Testing System) or similar shell testing framework
- Execute tests and report the pass rate

## Documentation

- Update the README.md to use the shell script as an alternative to running all steps manually
- Document any prerequisites or steps that require human intervention
- Add a README.md under `scripts/tests` describing setup, install steps, and how to execute tests
