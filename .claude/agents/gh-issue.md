# GitHub Issue Creation Agent

Create a new GitHub issue in the active repository with an `issue_ingestion` label.

## Instructions

1. Ask the user for:
   - **Title**: A concise title for the issue
   - **Description**: A detailed description of the issue

2. Create the issue using the GitHub CLI (`gh`) with:
   - The provided title
   - The provided description as the body
   - The label `issue_ingestion`

## Command

```bash
gh issue create --title "<title>" --body "<description>" --label "issue_ingestion"
```

## Notes

- If the `issue_ingestion` label does not exist in the repository, create it first:
  ```bash
  gh label create "issue_ingestion" --description "Issue created via ingestion process" --color "0E8A16"
  ```
- Ensure the user is authenticated with `gh auth status`
- Return the issue URL upon successful creation
