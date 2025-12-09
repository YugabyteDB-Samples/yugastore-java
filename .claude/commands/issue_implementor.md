Implement the least complex GitHub issue labeled `ingested`.

Follow the instructions in `.claude/agents/issue-implementor.md` to:

1. **List all `ingested` issues** and analyze their complexity
2. **Select the least complex** issue to implement
3. **Create a branch** named `issue-<number>`
4. **Implement the feature**:
   - Backend changes in `python_services/`
   - Frontend changes in `nextjs-frontend/`
5. **Write unit tests first** (TDD approach)
6. **Iterate** until:
   - All tests pass
   - Coverage > 80% for files touched
7. **Commit changes** with a message referencing the issue
8. **Update label** from `ingested` to `implemented`

Report the final test results, coverage percentage, and files modified.
