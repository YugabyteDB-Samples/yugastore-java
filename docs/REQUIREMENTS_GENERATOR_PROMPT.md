# Requirements Document Generator Prompt

> **Purpose:** This prompt template generates a standardized Requirements.md document from various input sources. The output is designed to be combined with a constitution/principles document to create formal Software Design Document (SDD) specifications.

---

## PROMPT TEMPLATE

```
You are a senior business analyst and requirements engineer. Your task is to synthesize input materials into a comprehensive, standardized Requirements Document. This document will be used as an input to generate formal Software Design Document (SDD) specifications when combined with architectural principles and constraints.

---

## INPUT MATERIALS

### Source Type Definitions
Classify each input as one of:
- **STAKEHOLDER_TRANSCRIPT**: Summarized meeting notes, interview transcripts
- **EMAIL_THREAD**: Email correspondence with requirements discussions
- **EXISTING_FUNCTIONALITY**: Documentation of current system capabilities
- **TECHNICAL_DISCUSSION**: Engineering team discussions, technical constraints
- **BUSINESS_DOCUMENT**: Strategy docs, roadmaps, business cases

### Provided Sources

{{SOURCES}}

---

## OUTPUT FORMAT

{{FORMAT_TEMPLATE}}

---

## ANALYSIS INSTRUCTIONS

### Phase 1: Source Extraction
For each input source:
1. Identify explicit requirements (directly stated needs)
2. Identify implicit requirements (inferred from context, complaints, or workarounds)
3. Extract constraints and limitations mentioned
4. Note stakeholder priorities and urgency indicators
5. Capture success metrics or acceptance criteria mentioned

### Phase 2: Requirement Classification
Categorize each extracted requirement as:
- **FUNCTIONAL**: Features and capabilities the system must provide
- **NON_FUNCTIONAL**: Performance, security, scalability, usability requirements
- **TECHNICAL**: Architecture, technology stack, integration requirements
- **BUSINESS**: Business rules, compliance, regulatory requirements
- **UX**: User experience, accessibility, design requirements

### Phase 3: Cross-Reference Analysis
1. Compare extracted requirements against existing functionality documentation
2. Identify **NEW** requirements (not currently implemented)
3. Identify **ENHANCEMENT** requirements (improvements to existing features)
4. Identify **MIGRATION** requirements (changing how something works)
5. Identify **DEPRECATION** candidates (features to be removed or replaced)

### Phase 4: Conflict Detection
Flag and document any conflicts:
- Contradictory requirements from different stakeholders
- Technical constraints that conflict with business requirements
- Timeline conflicts (dependencies, sequencing issues)
- Resource conflicts (competing priorities)
- Scope conflicts (feature creep vs. MVP)

For each conflict, provide:
- Conflict ID (e.g., CONFLICT-001)
- Sources involved
- Nature of the conflict
- Recommended resolution or escalation path

### Phase 5: Prioritization
Apply MoSCoW prioritization based on stakeholder input:
- **MUST**: Critical for launch/MVP
- **SHOULD**: Important but not blocking
- **COULD**: Nice to have if time permits
- **WON'T**: Explicitly out of scope (for this phase)

---

## DOCUMENT GENERATION RULES

1. **Traceability**: Every requirement must cite its source(s)
2. **Testability**: Requirements should be verifiable with clear acceptance criteria
3. **Atomicity**: Each requirement should be single-purpose
4. **Consistency**: Use consistent terminology throughout
5. **Completeness**: Flag gaps where requirements are implied but underspecified

### Requirement ID Schema
- FR-XXX: Functional Requirements
- NFR-XXX: Non-Functional Requirements  
- TR-XXX: Technical Requirements
- BR-XXX: Business Requirements
- UX-XXX: User Experience Requirements

### Status Indicators
Use these status markers:
- [NEW]: Not in current system
- [ENHANCE]: Improving existing capability
- [MIGRATE]: Changing implementation approach
- [VERIFIED]: Confirmed with stakeholders
- [DRAFT]: Needs stakeholder validation
- [CONFLICT]: Has unresolved conflicts (see Conflicts section)

---

## ADDITIONAL CONTEXT

{{CONSTITUTION_PRINCIPLES}}

---

Now analyze the provided sources and generate the Requirements Document following the specified format.
```

---

## FORMAT TEMPLATES

### Option A: Standard PRD Format (Default)

```markdown
# [PROJECT_NAME] - Product Requirements Document

> **Version:** X.Y  
> **Status:** DRAFT | REVIEW | APPROVED  
> **Last Updated:** [DATE]  
> **Author:** [GENERATED FROM SOURCE ANALYSIS]

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| X.Y | [DATE] | [AUTHOR] | Initial generation from sources |

### Source Materials Analyzed
| Source ID | Type | Description | Date |
|-----------|------|-------------|------|
| SRC-001 | [TYPE] | [DESCRIPTION] | [DATE] |

---

## 1. Executive Summary

[2-3 paragraph summary of the project scope, key objectives, and high-level requirements. Include primary stakeholder goals and success criteria.]

### Key Objectives
1. [Primary objective]
2. [Secondary objective]
3. [Additional objectives...]

### Success Metrics
| Metric | Current State | Target State | Timeline |
|--------|---------------|--------------|----------|
| [Metric] | [Current] | [Target] | [Date] |

---

## 2. Stakeholder Analysis

### Primary Stakeholders
| Stakeholder | Role | Key Concerns | Priority Requirements |
|-------------|------|--------------|----------------------|
| [Name/Role] | [Description] | [Concerns] | [Refs to requirements] |

### Stakeholder Priority Matrix
| Requirement Area | [Stakeholder 1] | [Stakeholder 2] | [Stakeholder N] |
|------------------|-----------------|-----------------|-----------------|
| [Area] | HIGH/MED/LOW | HIGH/MED/LOW | HIGH/MED/LOW |

---

## 3. Current State Analysis

### Existing Functionality
[Summary of current system capabilities relevant to this requirements document]

| Feature | Current Status | Gap Analysis |
|---------|----------------|--------------|
| [Feature] | ✅ Implemented / ⚠️ Partial / ❌ Missing | [Gap description] |

### Technical Debt / Known Issues
| Issue ID | Description | Impact | Related Requirements |
|----------|-------------|--------|---------------------|
| [ID] | [Description] | [Impact] | [Requirement refs] |

---

## 4. Functional Requirements

### 4.1 [Feature Area 1]

#### [FR-001] [Requirement Title]
- **Priority:** MUST | SHOULD | COULD
- **Status:** [NEW] | [ENHANCE] | [MIGRATE]
- **Source(s):** SRC-XXX, SRC-YYY
- **Description:** [Detailed requirement description]
- **Acceptance Criteria:**
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
- **Dependencies:** [Related requirement IDs]
- **Notes:** [Additional context]

[Repeat for each functional requirement]

### 4.2 [Feature Area 2]
[...]

---

## 5. Non-Functional Requirements

### 5.1 Performance
| ID | Requirement | Metric | Target | Priority |
|----|-------------|--------|--------|----------|
| NFR-001 | [Requirement] | [Metric] | [Target] | MUST/SHOULD |

### 5.2 Security
| ID | Requirement | Compliance | Priority |
|----|-------------|------------|----------|
| NFR-0XX | [Requirement] | [Standard if applicable] | MUST/SHOULD |

### 5.3 Scalability
[...]

### 5.4 Usability/Accessibility
[...]

### 5.5 Reliability/Availability
[...]

---

## 6. Technical Requirements

| ID | Requirement | Rationale | Source |
|----|-------------|-----------|--------|
| TR-001 | [Requirement] | [Why needed] | SRC-XXX |

### Technology Stack Decisions
| Layer | Current | Target | Rationale |
|-------|---------|--------|-----------|
| [Layer] | [Current] | [Target] | [Reason] |

### Integration Requirements
| System | Integration Type | Requirements |
|--------|------------------|--------------|
| [System] | [API/Event/etc.] | [Details] |

---

## 7. User Experience Requirements

### 7.1 Design Principles
[Key UX principles extracted from stakeholder input]

### 7.2 Specific UX Requirements
| ID | Requirement | Rationale | Priority |
|----|-------------|-----------|----------|
| UX-001 | [Requirement] | [User need] | MUST/SHOULD |

### 7.3 Accessibility Requirements
[WCAG compliance level, specific accessibility needs]

---

## 8. Business Requirements

| ID | Requirement | Business Driver | Source |
|----|-------------|-----------------|--------|
| BR-001 | [Requirement] | [Business need] | SRC-XXX |

### Business Rules
| Rule ID | Description | Conditions | Actions |
|---------|-------------|------------|---------|
| BR-XXX | [Rule] | [When] | [Then] |

---

## 9. Constraints & Assumptions

### Constraints
| ID | Constraint | Type | Impact |
|----|------------|------|--------|
| CON-001 | [Constraint] | Technical/Business/Regulatory | [Impact] |

### Assumptions
| ID | Assumption | Risk if Invalid | Validation Plan |
|----|------------|-----------------|-----------------|
| ASM-001 | [Assumption] | [Risk] | [How to validate] |

---

## 10. Conflicts & Resolutions

### Identified Conflicts

#### CONFLICT-001: [Conflict Title]
- **Sources:** SRC-XXX vs SRC-YYY
- **Nature:** [Description of the conflict]
- **Option A:** [First resolution option]
- **Option B:** [Second resolution option]
- **Recommendation:** [Recommended resolution]
- **Status:** OPEN | RESOLVED | ESCALATED
- **Resolution:** [If resolved, document decision and rationale]

[Repeat for each conflict]

### Conflict Summary
| ID | Type | Severity | Status | Owner |
|----|------|----------|--------|-------|
| CONFLICT-001 | [Type] | HIGH/MED/LOW | [Status] | [Who decides] |

---

## 11. Phasing & Roadmap

### Phase Overview
| Phase | Scope | Target Date | Key Deliverables |
|-------|-------|-------------|------------------|
| Phase 1 | [Scope] | [Date] | [Deliverables] |
| Phase 2 | [Scope] | [Date] | [Deliverables] |

### Requirement Phasing
| Requirement | Phase | Rationale |
|-------------|-------|-----------|
| FR-XXX | Phase 1 | [Why this phase] |

---

## 12. Out of Scope

Items explicitly excluded from this requirements document:

| Item | Reason | Future Consideration |
|------|--------|---------------------|
| [Item] | [Why excluded] | Phase X / Never / TBD |

---

## 13. Open Questions

| ID | Question | Owner | Due Date | Status |
|----|----------|-------|----------|--------|
| Q-001 | [Question] | [Who] | [Date] | OPEN/ANSWERED |

---

## 14. Glossary

| Term | Definition |
|------|------------|
| [Term] | [Definition] |

---

## 15. Appendices

### A. Source Material Summaries
[Brief summaries of each input source]

### B. Requirement Traceability Matrix
| Requirement ID | Source(s) | Related Requirements | Test Cases |
|----------------|-----------|---------------------|------------|
| [ID] | [Sources] | [Related] | [Tests] |

### C. Change Log
[Track changes to this document]

---

*Document generated from source analysis*  
*Review required before SDD specification generation*
```

---

### Option B: Lean Requirements Format

```markdown
# [PROJECT_NAME] - Requirements Summary

> **Version:** X.Y | **Date:** [DATE] | **Status:** DRAFT

---

## Executive Summary
[1 paragraph summary]

## Key Requirements

### Must Have (MVP)
| ID | Requirement | Source | Status |
|----|-------------|--------|--------|
| [ID] | [Requirement] | [Source] | [Status] |

### Should Have
| ID | Requirement | Source | Status |
|----|-------------|--------|--------|

### Could Have
| ID | Requirement | Source | Status |
|----|-------------|--------|--------|

## Conflicts
| ID | Conflict | Resolution |
|----|----------|------------|

## Open Questions
| Question | Owner | Due |
|----------|-------|-----|

## Next Steps
1. [Action item]
2. [Action item]
```

---

### Option C: Technical Specification Focus

```markdown
# [PROJECT_NAME] - Technical Requirements Specification

> **Version:** X.Y | **Date:** [DATE]

---

## 1. System Overview
[Technical context and scope]

## 2. Functional Specifications

### 2.1 [Component/Service Name]

#### Endpoints/Interfaces
| Method | Path | Description | Request | Response |
|--------|------|-------------|---------|----------|

#### Business Logic
[Detailed logic specifications]

#### Data Models
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|

### 2.2 [Next Component]
[...]

## 3. Non-Functional Specifications
[Detailed NFRs with technical metrics]

## 4. Integration Specifications
[API contracts, event schemas, etc.]

## 5. Migration Specifications
[If applicable - current to future state mapping]

## 6. Security Specifications
[Authentication, authorization, data protection]

## 7. Appendices
[Schemas, diagrams, references]
```

---

## USAGE EXAMPLES

### Example 1: Basic Usage

```
You are a senior business analyst...

---

## INPUT MATERIALS

### Provided Sources

#### SRC-001: Stakeholder Interview - VP Digital Experience (STAKEHOLDER_TRANSCRIPT)
[Paste summarized transcript here]

#### SRC-002: Technical Team Discussion (TECHNICAL_DISCUSSION)  
[Paste meeting notes here]

#### SRC-003: Current System Documentation (EXISTING_FUNCTIONALITY)
[Paste existing requirements/docs here]

---

## OUTPUT FORMAT

[Use Standard PRD Format - Option A]

---

## ADDITIONAL CONTEXT

### Constitution Principles
- All systems must use Python/FastAPI for backend services
- Security-first approach: all user data must be properly authenticated
- Mobile-first design philosophy
- Microservices architecture with clear service boundaries
```

### Example 2: With Custom Format

```
...

## OUTPUT FORMAT

Generate using this custom format:

# Requirements Brief
## Problem Statement
## Proposed Solution  
## Requirements Table (ID | Priority | Description | Acceptance Criteria)
## Dependencies
## Risks

...
```

---

## PROMPT CUSTOMIZATION OPTIONS

### A. Add Domain-Specific Sections
Modify the format template to include industry-specific sections:
- **E-commerce**: Payment processing, inventory management, fulfillment
- **Healthcare**: HIPAA compliance, patient data, clinical workflows
- **Finance**: Regulatory compliance, audit trails, transaction processing

### B. Adjust Detail Level
- **Executive Brief**: High-level summary for leadership
- **Product Spec**: Detailed for product managers
- **Technical Spec**: Implementation-ready for engineers

### C. Include Specific Analysis
Add instructions for specific analysis needs:
```
### Additional Analysis Required
- Competitive feature comparison
- Regulatory compliance checklist
- Accessibility audit
- Performance baseline comparison
```

---

## TIPS FOR BEST RESULTS

1. **Summarize transcripts well**: Raw transcripts work but summarized versions with key points highlighted produce better results

2. **Include existing documentation**: The more context about current state, the better the gap analysis

3. **Specify stakeholder roles**: Help the model understand whose voice carries which weight

4. **Define your terms**: Include a glossary of domain-specific terms if relevant

5. **Be explicit about constraints**: Technology mandates, timeline, budget, team size

6. **Provide the constitution upfront**: If you have architectural principles or constraints, include them

---

## INTEGRATION WITH SDD GENERATION

This Requirements Document is designed to be an input for SDD generation. When feeding into SDD creation:

1. **Requirements.md** provides the WHAT (features, capabilities, constraints)
2. **Constitution.md** provides the HOW (architectural patterns, technology choices, principles)
3. **SDD** synthesizes both into implementation specifications

### Recommended Flow
```
[Stakeholder Sources] → [Requirements Generator Prompt] → [Requirements.md]
                                                              ↓
[Architecture Principles] → [Constitution.md] ────────────────┤
                                                              ↓
                                          [SDD Generator Prompt] → [SDD.md]
```

