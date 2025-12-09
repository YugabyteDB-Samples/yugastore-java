## Enhanced Specification Verifier with Deep Source Analysis

### Overview

The enhanced specification verifier adds **deep source document analysis** capability. When violations are detected, it can automatically fetch and analyze the original source documents (meeting transcripts, emails, design documents) to provide deeper insights.

### What's New

#### 🔍 Deep Analysis Features

1. **Automatic Source Document Fetching**
   - Fetches original documents via API when violations found
   - Analyzes transcripts, emails, design docs, meeting notes
   - Provides context from original discussions

2. **Enhanced Violation Reports**
   - Shows which source documents were analyzed
   - Includes insights from original content
   - Helps understand WHY requirements are missing or ambiguous

3. **Smart Document References**
   - Requirements link to their source documents
   - Format: `[SRC:doc-id]`, `[SOURCE:doc-id]`, `[DOC:doc-id]`
   - Automatic extraction and tracking

### How It Works

#### 1. Document Format with Source References

In your human input documents, reference original sources:

```
REQ-001: Users must search by title, author, ISBN [SRC:transcript-meeting-2024-01-15]
REQ-002: Cart must persist across sessions [SOURCE:email-product-owner-001]
REQ-003: Passwords must be encrypted [DOC:security-requirements-v2]
```

#### 2. API Configuration

Create `api_config.json`:

```json
{
  "enabled": true,
  "base_url": "http://your-api-server.com",
  "api_key": "your-api-key",
  "timeout": 30,
  "max_retries": 3
}
```

#### 3. Run with Deep Analysis

```bash
./spec_verifier_enhanced.py \
  --human-input input.txt \
  --requirements reqs.txt \
  --constitution principles.txt \
  --specification spec.md \
  --deep-analysis \
  --api-config api_config.json
```

### Example Output

#### Without Deep Analysis (Original Tool)
```
[CRITICAL] COVERAGE: 4 requirements have NO coverage
  Evidence:
    - REQ_abc123: Password reset functionality needed
```

#### With Deep Analysis (Enhanced Tool)
```
[CRITICAL] COVERAGE: 4 requirements have NO coverage
  Evidence:
    - REQ_abc123: Password reset functionality needed
  📄 Source Documents Analyzed: 2
    - email: User Feedback - Password Reset Feature Request
    - transcript: Security Review Meeting
  🔍 Deep Analysis:
    Analyzed 2 source document(s):
      In User Feedback - Password Reset Feature Request (email):
        - 'password': ...CRITICAL: Password reset functionality via email...
        - 'reset': ...Users are getting locked out and we have no automated way...
      In Security Review Meeting (transcript):
        - 'password': ...bcrypt with appropriate cost factor. NO plaintext storage...
```

### API Specification

#### Endpoint Format

```
GET /documents/{doc_id}
Authorization: Bearer {api_key}
```

#### Response Format

```json
{
  "id": "transcript-meeting-2024-01-15",
  "type": "transcript",
  "title": "Stakeholder Meeting - Product Requirements",
  "date": "2024-01-15",
  "participants": ["John Doe", "Jane Smith"],
  "content": "Full text content of the document..."
}
```

#### Document Types

- `transcript` - Meeting/call transcripts
- `email` - Email threads
- `design_doc` - Design documents
- `meeting_notes` - Meeting notes
- `interview` - User interviews
- `other` - Other document types

### Demo Usage

#### 1. Start the Mock API Server

```bash
cd examples/
python3 mock_source_api.py
```

This starts a mock API server on `http://localhost:8888` with example documents.

#### 2. Run the Enhanced Demo

In another terminal:

```bash
cd examples/
./run_demo_enhanced.sh
```

This runs the verifier with deep analysis enabled.

### Command-Line Options

```bash
# Basic options (same as original)
-i, --human-input FILES       Human input documents
-r, --requirements FILES      Requirements documents
-c, --constitution FILE       Constitution/principles
-s, --specification FILE      Specification to verify
-o, --output FILE            Output file
--json                       JSON output format

# New deep analysis options
--deep-analysis              Enable deep source analysis
--api-config FILE            API configuration JSON file
--api-url URL                API base URL (alternative to config file)
--api-key KEY                API key (alternative to config file)
--api-timeout SECONDS        Request timeout (default: 30)
```

### Configuration Options

#### Via Config File (`--api-config`)

```json
{
  "enabled": true,
  "base_url": "http://localhost:8888",
  "api_key": "your-api-key",
  "timeout": 30,
  "max_retries": 3
}
```

#### Via Command-Line Arguments

```bash
./spec_verifier_enhanced.py \
  [...] \
  --deep-analysis \
  --api-url http://localhost:8888 \
  --api-key your-api-key \
  --api-timeout 30
```

### Use Cases

#### 1. Understanding Missing Requirements

**Problem**: Specification doesn't address a requirement

**Deep Analysis**: Fetches original discussions to understand:
- What stakeholders actually said
- Why the requirement was important
- Context that might clarify the intent

#### 2. Resolving Ambiguity

**Problem**: Specification uses vague language

**Deep Analysis**: Looks at source documents to find:
- Specific numbers or criteria mentioned
- Detailed explanations
- Examples discussed

#### 3. Investigating Principle Violations

**Problem**: Spec violates a security principle

**Deep Analysis**: Checks source documents to determine:
- Was this discussed and approved?
- Did stakeholders understand the security implications?
- Is there a business justification?

### Security Considerations

1. **API Keys**: Store API keys securely
   - Use environment variables in production
   - Don't commit keys to version control
   - Rotate keys regularly

2. **Network Security**:
   - Use HTTPS in production (not HTTP)
   - Validate SSL certificates
   - Consider VPN for internal APIs

3. **Data Privacy**:
   - Source documents may contain sensitive information
   - Ensure proper access controls
   - Consider data retention policies

### Performance

#### Caching

The tool caches fetched documents to avoid redundant API calls:
- Documents cached in memory during run
- Same document fetched once even if referenced multiple times
- Cache cleared between runs

#### Selective Analysis

Deep analysis only performed when:
- `--deep-analysis` flag is set
- API configuration is provided
- Violations are detected
- Requirements have source references

Typically adds 2-10 seconds depending on:
- Number of violations
- Number of source documents
- API response time
- Network latency

### Integration Examples

#### CI/CD Pipeline with Deep Analysis

```yaml
# GitHub Actions example
name: Verify Specification

on:
  pull_request:
    paths:
      - 'docs/specification.md'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Verify Specification
        env:
          API_KEY: ${{ secrets.SOURCE_DOC_API_KEY }}
        run: |
          ./spec_verifier_enhanced.py \
            -i docs/inputs/*.txt \
            -r docs/requirements/*.md \
            -c docs/principles.txt \
            -s docs/specification.md \
            --deep-analysis \
            --api-url https://api.company.com \
            --api-key $API_KEY \
            --json > violations.json
      
      - name: Upload Report
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: verification-report
          path: violations.json
```

#### Custom API Integration

If you have an existing document management system:

```python
# Your API should return documents in this format:
{
  "id": "unique-doc-id",
  "type": "transcript",  # or email, design_doc, etc.
  "title": "Document Title",
  "date": "2024-01-15",
  "participants": ["Person 1", "Person 2"],
  "content": "Full text content..."
}
```

Map your system's data to this format in your API endpoint.

### Troubleshooting

#### "API Error: HTTP 404"
- Check that document IDs in your input files match API document IDs
- Verify API base URL is correct
- Ensure documents exist in your system

#### "Network Error: Connection refused"
- API server not running
- Wrong port or URL
- Firewall blocking connection

#### "Unauthorized - Missing or invalid token"
- Check API key is correct
- Verify `Authorization: Bearer {key}` header format
- Ensure API key has necessary permissions

#### "Deep analysis not running"
- Verify `--deep-analysis` flag is set
- Check API configuration is provided
- Ensure requirements have `[SRC:...]` references
- Confirm violations were detected (deep analysis only runs for violations)

### Comparison: Original vs Enhanced

| Feature | Original | Enhanced |
|---------|----------|----------|
| Basic verification | ✅ | ✅ |
| Zero dependencies | ✅ | ✅ (stdlib only) |
| Offline operation | ✅ | ✅ (optional API) |
| Source doc fetching | ❌ | ✅ |
| Deep analysis | ❌ | ✅ |
| Context from originals | ❌ | ✅ |
| API integration | ❌ | ✅ |

### Best Practices

#### 1. Consistent Document Referencing

Be consistent with document ID format:
```
Good:
  [SRC:transcript-2024-01-15]
  [SOURCE:email-product-owner-001]

Avoid:
  [SRC:transcript 2024-01-15]  # No spaces
  [SRC:Transcript-2024-01-15]  # Be consistent with casing
```

#### 2. Reference Tracking

Maintain a document reference registry:
```
transcript-2024-01-15  → Stakeholder meeting on Jan 15
email-product-owner-001 → Search feature requirements
design-doc-v2          → Architecture decisions
```

#### 3. API Response Format

Ensure your API returns consistent JSON:
- Always include `id`, `type`, `title`, `content`
- Use standard `type` values
- Include `date` and `participants` when available

#### 4. Incremental Adoption

Start without deep analysis, add it later:
```bash
# Phase 1: Basic verification
./spec_verifier.py [...]

# Phase 2: Add source references to documents
# Edit files to add [SRC:...] tags

# Phase 3: Set up API integration
# Implement or configure document API

# Phase 4: Enable deep analysis
./spec_verifier_enhanced.py [...] --deep-analysis
```

### Future Enhancements

Potential improvements (not yet implemented):

- [ ] Semantic similarity search in source documents
- [ ] LLM integration for natural language analysis
- [ ] Automatic requirement extraction from transcripts
- [ ] Conflict detection across source documents
- [ ] Timeline visualization of requirement evolution
- [ ] Webhook support for real-time document updates
- [ ] Batch API calls for better performance
- [ ] Source document diff analysis (version comparison)

### License

Same as parent project

---

**Quick Start**: 
1. `cd examples && python3 mock_source_api.py` (in terminal 1)
2. `cd examples && ./run_demo_enhanced.sh` (in terminal 2)
3. See deep analysis in action!


