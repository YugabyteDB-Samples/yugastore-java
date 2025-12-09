Implement a specific GitHub issue by number.

Ask the user: **What is the issue number to implement?**

Then follow the instructions in `.claude/agents/issue-implementor.md` to:

1. **Fetch the specified issue** (skip complexity prioritization)
2. **Create a branch** named `issue-<number>`
3. **Implement the feature**:
   - Backend changes in `python_services/`
   - Frontend changes in `nextjs-frontend/`
4. **Write unit tests first** (TDD approach)
5. **Iterate** until:
   - All tests pass
   - Coverage > 80% for files touched
6. **Commit changes** with a message referencing the issue
7. **Update label** from `ingested` to `implemented`

Report the final test results, coverage percentage, and files modified.
