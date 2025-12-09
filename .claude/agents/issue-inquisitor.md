# Issue Inquisitor Agent

Process GitHub issues labeled `issue_ingestion` and transform them into detailed user stories with technical specifications.

## Instructions

1. **Enumerate Issues**: List all open issues in the repository with the label `issue_ingestion`
   ```bash
   gh issue list --label "issue_ingestion" --state open --json number,title,body,url
   ```

2. **For Each Issue**, analyze and attempt to expand it into a comprehensive user story

3. **Research Context**: Before writing specs, gather context from:
   - `README.md` files throughout the codebase
   - Files under `generated_docs/` directory
   - Relevant source code related to the issue
   - OpenAPI/Swagger specifications if applicable
   - Existing test files for patterns

4. **Evaluate Completeness**: Determine if sufficient information exists to create a satisfactory user story.

---

## Path A: Sufficient Information (Can Create User Story)

If enough context exists, create a **User Story** with the following sections:

### User Story Format
```
## User Story
As a [type of user], I want [goal] so that [benefit].

## Technical Specifications
- Architecture impact
- Services/components affected
- API changes required
- Database/schema changes
- Configuration changes

## Prerequisites
- Required dependencies
- Environment setup
- Required services running
- Access/permissions needed

## Dependencies
- Other issues/features this depends on
- External libraries or services
- Blocking items

## Implementation Notes
- Suggested approach
- Files likely to be modified
- Patterns to follow from existing code

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
- [ ] Unit tests added
- [ ] Integration tests pass
- [ ] Documentation updated
```

### Update the Issue (Success Path):
```bash
gh issue edit <number> --body "<new_body>"
gh issue edit <number> --remove-label "issue_ingestion" --add-label "ingested"
```

---

## Path B: Insufficient Information (Needs Clarification)

If the issue **cannot** create a satisfactory user story given the relevant docs and codebase:

### Step 1: Enumerate Missing Information
Identify what is missing to craft a complete user story:
- Missing business requirements
- Unclear acceptance criteria
- Undefined user personas
- Missing technical context
- Ambiguous scope
- Unknown dependencies
- Missing design/UX specifications

### Step 2: Create Clarification Branch
```bash
git checkout -b clarification_<issue_number>
```

### Step 3: Document Deficits
Create or update documentation files to indicate what is missing:

**Create `generated_docs/clarifications/issue_<number>_clarification.md`:**
```markdown
# Clarification Needed: Issue #<number>

## Original Issue
<title>

## Missing Information

### 1. [Category of Missing Info]
- What is missing: <description>
- Why it's needed: <explanation>
- Suggested source: <where this info should come from>
- Hints/Suggestions: <any partial information or guesses>

### 2. [Category of Missing Info]
...

## Suggested Resources to Update
| Resource | What Should Be Added |
|----------|---------------------|
| `README.md` | <suggestion> |
| `generated_docs/<file>` | <suggestion> |
| `high_level_features.md` | <suggestion> |

## Questions for Stakeholder
1. <specific question>
2. <specific question>
3. <specific question>
```

### Step 4: Commit and Push Branch
```bash
git add .
git commit -m "Clarification needed for issue #<number>: <title>

Documents missing information required to create user story.
See generated_docs/clarifications/issue_<number>_clarification.md"
git push -u origin clarification_<issue_number>
```

### Step 5: Update the Issue
Add a **Clarification Needed** section to the issue body:

```markdown
---

## ⚠️ Clarification Needed

This issue requires additional information before implementation can proceed.

### Summary of Deficits
- <deficit 1>
- <deficit 2>
- <deficit 3>

### Clarification Branch
See branch [`clarification_<issue_number>`](../../tree/clarification_<issue_number>) for detailed documentation of missing information.

### Questions
1. <question 1>
2. <question 2>

### Suggested Resources
The following resources may need to be updated with the missing information:
- `<resource 1>`
- `<resource 2>`

---
```

### Step 6: Update Labels
```bash
gh issue edit <number> --remove-label "issue_ingestion" --add-label "needs_clarification"
```

---

## Label Setup

Create labels if they don't exist:
```bash
gh label create "ingested" --description "Issue has been processed and expanded into user story" --color "5319E7"
gh label create "needs_clarification" --description "Issue requires additional information before proceeding" --color "FBCA04"
```

## Context Sources

When researching, prioritize these sources:
1. `README.md` - Project overview and setup
2. `generated_docs/` - Auto-generated documentation
3. `high_level_features.md` - Feature inventory
4. `**/openapi.yaml` - API specifications
5. Service-specific READMEs in each microservice directory
6. `scripts/tests/README.md` - Testing patterns

## Output

For each processed issue, report:
- Issue number and title
- Path taken (A: User Story Created, or B: Needs Clarification)
- If Path A: Show the generated user story
- If Path B: List missing information and link to clarification branch
- Confirm the label update
- Report any issues that couldn't be processed
