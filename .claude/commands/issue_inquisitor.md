Process GitHub issues labeled `issue_ingestion` and expand them into detailed user stories.

Follow the instructions in `.claude/agents/issue-inquisitor.md` to:

1. **List all issues** with the `issue_ingestion` label

2. **For each issue**, research context from `README.md` files, `generated_docs/`, and the codebase

3. **Evaluate if sufficient information exists** to create a complete user story

4. **If sufficient information (Path A)**:
   - Create a comprehensive user story including:
     - User story statement (As a... I want... so that...)
     - Technical specifications
     - Prerequisites
     - Dependencies
     - Implementation notes
     - Acceptance criteria with checkboxes
   - Update the issue body with the expanded content
   - Change the label from `issue_ingestion` to `ingested`

5. **If insufficient information (Path B)**:
   - Enumerate what information is missing
   - Create a branch named `clarification_<issue_number>`
   - Document deficits in `generated_docs/clarifications/issue_<number>_clarification.md`
   - Indicate which resources should contain the missing information
   - Include suggestions and hints for filling gaps
   - Push the branch to remote
   - Update the issue with a **Clarification Needed** section summarizing deficits
   - Reference the clarification branch in the issue
   - Change the label from `issue_ingestion` to `needs_clarification`

6. **Report** on all processed issues:
   - Which path was taken (user story created vs needs clarification)
   - Links to updated issues and any clarification branches created

Create labels (`ingested`, `needs_clarification`) if they don't exist.
