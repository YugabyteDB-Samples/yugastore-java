# Issue Implementor Agent

Implement GitHub issues that have been processed and labeled `ingested`.

## Instructions

### 1. Issue Selection (Auto-Prioritization Mode)

List all open issues with the `ingested` label:
```bash
gh issue list --label "ingested" --state open --json number,title,body,labels
```

Analyze each issue and score complexity based on:
- Number of files likely to be modified
- Number of services affected
- Dependencies on other features
- Estimated lines of code
- Integration complexity

Select the **least complex** issue to implement first.

### 2. Issue Selection (Chooser Mode)

Skip prioritization and implement the specific issue number provided by the user.

### 3. Branch Creation

Create a feature branch named after the issue number:
```bash
git checkout -b issue-<number>
```

### 4. Implementation

#### Backend Changes (Python)
All backend changes go in the `python_services/` directory:
- Follow existing patterns in the codebase
- Create or modify service files
- Update API endpoints as needed
- Add database migrations if required

#### Frontend Changes (Next.js)
All frontend changes go in the `nextjs-frontend/` directory:
- Follow existing component patterns
- Update pages/routes as needed
- Add/modify API client calls
- Update styles following existing conventions

### 5. Test-Driven Development

#### Unit Tests First
Before writing implementation code:
1. Create unit test files following project conventions
2. Write tests that cover:
   - Happy path scenarios
   - Edge cases
   - Error handling
   - Boundary conditions

#### Backend Tests (`python_services/`)
```python
# tests/test_<feature>.py
import pytest

class Test<Feature>:
    def test_<scenario>(self):
        # Arrange, Act, Assert
        pass
```

#### Frontend Tests (`nextjs-frontend/`)
```javascript
// __tests__/<component>.test.tsx
import { render, screen } from '@testing-library/react'

describe('<Component>', () => {
  it('should <behavior>', () => {
    // Test implementation
  })
})
```

### 6. Implementation Iteration

Iterate until:
- [ ] All unit tests pass
- [ ] Code coverage > 80% for files touched
- [ ] No linting errors
- [ ] Type checks pass (if applicable)

#### Check Coverage

**Python:**
```bash
cd python_services
pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

**Next.js:**
```bash
cd nextjs-frontend
npm run test -- --coverage --coverageThreshold='{"global":{"lines":80}}'
```

### 7. Verification Loop

```
while (tests_failing OR coverage < 80%):
    if tests_failing:
        analyze_failure()
        fix_code_or_test()
    if coverage < 80%:
        identify_uncovered_lines()
        add_tests_for_uncovered_code()
    run_tests()
```

### 8. Completion

Once all criteria are met:
1. Stage all changes: `git add .`
2. Create commit with descriptive message referencing the issue:
   ```bash
   git commit -m "Implement #<number>: <issue title>

   - <summary of changes>
   - Tests added with >80% coverage

   Closes #<number>"
   ```
3. Report summary of:
   - Files created/modified
   - Test count and pass rate
   - Coverage percentage
   - Any notes or follow-up items

### 9. Label Update

Update the issue label:
```bash
gh issue edit <number> --remove-label "ingested" --add-label "implemented"
```

Create the label if it doesn't exist:
```bash
gh label create "implemented" --description "Issue has been implemented and is ready for review" --color "0E8A16"
```

## Directory Structure Reference

```
python_services/
├── src/
│   └── <service>/
├── tests/
│   └── test_<feature>.py
└── requirements.txt

nextjs-frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── lib/
├── __tests__/
└── package.json
```

## Quality Gates

- [ ] All tests pass
- [ ] Coverage > 80% on touched files
- [ ] No new linting errors
- [ ] Code follows existing patterns
- [ ] Acceptance criteria from issue are met
