# Enhanced Specification Verifier - Quick Start

## What's Different?

The enhanced version **fetches original source documents** (transcripts, emails, design docs) when it finds problems in your specification. This provides deeper insights into WHY issues exist.

## 5-Minute Demo

### Terminal 1: Start Mock API Server

```bash
cd examples/
python3 mock_source_api.py
```

You should see:
```
================================================================
Mock Source Document API Server
================================================================
Server running on http://localhost:8888

Available documents (8):
  - transcript-stakeholder-meeting-2024-01-15 (transcript): Stakeholder Meeting
  - email-product-owner-001 (email): RE: Search Results Display
  ...
```

### Terminal 2: Run Enhanced Verification

```bash
cd examples/
./run_demo_enhanced.sh
```

## What You'll See

### Regular Violation (Original Tool)
```
[CRITICAL] COVERAGE: 4 requirements have NO coverage
  Evidence:
    - REQ_abc123 [HUMAN_INPUT:input.txt]: Password reset functionality...
```

### Enhanced Violation (With Deep Analysis) 🔍
```
[CRITICAL] COVERAGE: 4 requirements have NO coverage
  Evidence:
    - REQ_abc123 [HUMAN_INPUT:input.txt]: Password reset functionality...
  📄 Source Documents Analyzed: 2
    - email: User Feedback - Password Reset Feature Request  
    - design_doc: Security Requirements Document v2
  🔍 Deep Analysis:
    Analyzed 2 source document(s):
      In User Feedback - Password Reset Feature Request (email):
        - 'password': ...CRITICAL: Password reset functionality via email...
        - 'reset': ...Users are getting locked out, no automated way to help...
      In Security Requirements Document v2 (design_doc):
        - 'password': ...Reset tokens valid for 1 hour maximum...
        - 'reset': ...Support password reset via email...
```

## Document Format

Add source references to your requirements:

```
REQ-001: Users must search by title [SRC:transcript-meeting-2024-01-15]
REQ-002: Cart persists across sessions [SOURCE:email-product-owner-001]
REQ-003: Passwords encrypted [DOC:security-requirements-v2]
```

Three formats supported:
- `[SRC:document-id]`
- `[SOURCE:document-id]`
- `[DOC:document-id]`

## API Configuration

Create `api_config.json`:

```json
{
  "enabled": true,
  "base_url": "http://localhost:8888",
  "api_key": "your-api-key",
  "timeout": 30
}
```

## Usage

### Basic (No Deep Analysis)
```bash
./spec_verifier_enhanced.py \
  -i input.txt \
  -r reqs.txt \
  -c principles.txt \
  -s spec.md
```

### With Deep Analysis
```bash
./spec_verifier_enhanced.py \
  -i input.txt \
  -r reqs.txt \
  -c principles.txt \
  -s spec.md \
  --deep-analysis \
  --api-config api_config.json
```

### Alternative: Command-Line Config
```bash
./spec_verifier_enhanced.py \
  [...] \
  --deep-analysis \
  --api-url http://localhost:8888 \
  --api-key your-api-key
```

## When to Use Each Version

### Use Original (`spec_verifier.py`)
- ✅ Quick local verification
- ✅ Offline work
- ✅ No source documents available
- ✅ Basic CI/CD checks

### Use Enhanced (`spec_verifier_enhanced.py`)
- ✅ Deep investigation of violations
- ✅ Understanding context from original discussions
- ✅ Resolving ambiguous requirements
- ✅ When source documents are available via API
- ✅ Post-finding analysis

## API Integration

Your API should return this format:

```json
{
  "id": "document-id",
  "type": "transcript|email|design_doc|meeting_notes",
  "title": "Document Title",
  "date": "2024-01-15",
  "participants": ["Person 1", "Person 2"],
  "content": "Full text content of the document..."
}
```

Endpoint: `GET /documents/{doc_id}`  
Auth: `Authorization: Bearer {api_key}`

## Benefits

### 1. Understand WHY Requirements Are Missing

**Before**:
> "Password reset not in spec"

**After**:
> "Password reset not in spec. Source analysis shows: Support team requested this in email-support-feedback because users are getting locked out. Security doc specifies 1-hour token validity."

### 2. Clarify Ambiguous Specifications

**Before**:
> "Spec uses vague term 'fast'"

**After**:
> "Spec uses vague term 'fast'. CTO email specifies: 'API response times must be under 200ms for 95th percentile'"

### 3. Validate Principle Violations

**Before**:
> "Spec logs passwords, violating security principle"

**After**:
> "Spec logs passwords, violating security principle. Security meeting transcript explicitly states: 'We must NEVER log passwords. Ever.'"

## Complete Example

### 1. Create requirement with source reference

`input.txt`:
```
REQ-001: System must handle 500 concurrent users [SRC:email-cto-performance]
```

### 2. Specification doesn't address it

`spec.md`:
```
# System will handle users appropriately
```

### 3. Run enhanced verifier

```bash
./spec_verifier_enhanced.py [...] --deep-analysis --api-config api_config.json
```

### 4. Get deep analysis

```
[CRITICAL] COVERAGE: REQ-001 not covered
  📄 Source Documents Analyzed: 1
    - email: Performance Requirements and SLAs
  🔍 Deep Analysis:
    In Performance Requirements and SLAs (email):
      - 'concurrent': ...System must handle minimum 500 concurrent users...
      - 'users': ...Support up to 1000 concurrent users as target...
      - 'performance': ...These are non-negotiable for production launch...
```

Now you know:
- The exact number required (500 minimum, 1000 target)
- It's from the CTO
- It's non-negotiable for launch
- You need to add this to the spec

## Comparison

| Feature | Original | Enhanced |
|---------|----------|----------|
| Find missing reqs | ✅ | ✅ |
| Find violations | ✅ | ✅ |
| Offline | ✅ | ✅* |
| Fast | ✅ | ✅ |
| Shows context | ❌ | ✅ |
| Fetches sources | ❌ | ✅ |
| Deep analysis | ❌ | ✅ |

*Enhanced works offline too, deep analysis is optional

## Tips

1. **Start Simple**: Use original version first, add deep analysis later
2. **Add References Incrementally**: Don't need to reference every requirement
3. **Reference Critical Items**: Focus on security, performance, compliance requirements
4. **Use Consistent IDs**: Keep document ID format consistent
5. **Test API First**: Verify API works before running verifier

## Troubleshooting

### "API server not running"
```bash
# Start it:
cd examples && python3 mock_source_api.py
```

### "Document not found"
- Check document ID spelling in `[SRC:...]` tags
- Verify document exists in API
- Try without prefix: `doc-id` not `SRC:doc-id`

### "Deep analysis not showing"
- Ensure `--deep-analysis` flag is set
- Verify API config is provided
- Check that requirements have `[SRC:...]` references
- Confirm violations were found (deep analysis only runs for violations)

## Next Steps

1. ✅ Run the demo (`./run_demo_enhanced.sh`)
2. ✅ Review output with deep analysis
3. ✅ Read full documentation (`SPEC_VERIFIER_ENHANCED_README.md`)
4. ✅ Add source references to your requirements
5. ✅ Set up your document API (or use mock for testing)
6. ✅ Run on your specifications

---

**Quick Demo**: 
```bash
# Terminal 1
cd examples && python3 mock_source_api.py

# Terminal 2  
cd examples && ./run_demo_enhanced.sh
```


