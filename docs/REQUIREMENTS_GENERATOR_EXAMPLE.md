# Example: Using the Requirements Generator Prompt

> This example shows how to use the Requirements Generator Prompt with the Bookstore-R-Us stakeholder materials.

---

## Complete Prompt Example

Copy and paste this into your AI assistant to generate a requirements document:

---

```
You are a senior business analyst and requirements engineer. Your task is to synthesize input materials into a comprehensive, standardized Requirements Document. This document will be used as an input to generate formal Software Design Document (SDD) specifications when combined with architectural principles and constraints.

---

## INPUT MATERIALS

### Provided Sources

#### SRC-001: Stakeholder Interview - VP Digital Experience - Modernization (STAKEHOLDER_TRANSCRIPT)
**Date:** December 9, 2024
**Participant:** Sarah Mitchell, VP of Digital Experience

**Key Points Extracted:**
- Homepage hero section is static PNG, needs animations and interactivity
- Product cards lack hover effects and microinteractions
- "Add to cart" has no satisfying visual feedback
- Typography is generic (Roboto everywhere), wants distinctive bookish feel
- Hardcoded user ID "u1001" in checkout is a security concern
- Login uses BCrypt (good) but lacks modern features (OAuth, MFA, JWT)
- Mobile experience is poor - cramped nav, hard-to-tap cart, bad product grid
- No search functionality (6,000+ products, customers can't find things)
- Wants "warm bookstore" visual identity, not generic corporate look
- Phase 1 target: Q2 2024 (board presentation)
- Phased approach preferred: MVP first, iterate

**Stated Priorities:**
1. Visual modernization + security fixes (tied for #1)
2. Mobile experience improvements
3. Navigation and discovery (category browsing, eventually search)
4. Nice-to-haves: wishlists, profiles, order history

#### SRC-002: Stakeholder Interview - VP Digital Experience - Mobile Strategy (STAKEHOLDER_TRANSCRIPT)
**Date:** December 12, 2024
**Participant:** Sarah Mitchell, VP of Digital Experience

**Key Metrics Revealed:**
- Mobile traffic: 31% (industry average: 65-70%)
- Mobile conversion: 0.8% (desktop: 3.2%)
- Mobile cart abandonment: 78% (desktop: 45%)
- Page load time: 6 seconds on 4G (target: <3 seconds)
- Mobile ad campaigns paused due to poor ROI
- Missing Gen Z/younger millennial demographic (mobile-first shoppers)

**Strategic Direction:**
- Mobile-first design approach (design for mobile, scale to desktop)
- Progressive Web App (PWA) for Android benefits without native app cost
- No native app (for now) - revisit if metrics don't improve
- Target metrics: 60%+ mobile traffic, 2-2.5% conversion, <50% abandonment

**Technical Requirements Discussed:**
- Minimum 44px touch targets
- Bottom navigation bar for thumb accessibility
- Apple Pay and Google Pay integration (high priority)
- Vertical feed-style product browsing
- Preserved scroll position on back navigation
- Cross-device wishlist/cart sync

#### SRC-003: Technical Team Discussion - Stack Migration (TECHNICAL_DISCUSSION)
**Date:** December 11, 2024
**Participants:** Mike (Tech Lead), Priya (Backend), Jordan (Full-Stack), Alex (DevOps)

**Architecture Mandate:**
- Organization directive: Python/FastAPI for all new development
- React frontends (already aligned)
- Strangler fig migration pattern for gradual replacement

**Service Migration Plan:**
| Service | Current | Target | Complexity | Owner |
|---------|---------|--------|------------|-------|
| Products | Spring Boot + JPA | FastAPI + SQLModel | Medium | Priya |
| Cart | Spring Boot (session-scoped) | FastAPI (stateless) | Low | Jordan |
| Checkout | Spring Boot + raw CQL | FastAPI + SQLAlchemy | High | Priya |
| Login | Spring Security | FastAPI + JWT | Medium | Jordan |
| API Gateway | Spring Cloud + Feign | FastAPI/lightweight proxy | Medium | Alex |
| Eureka | Spring Cloud Netflix | Remove (use env vars/k8s) | Low | Alex |

**Frontend Migration:**
- React class components → Next.js with hooks
- Scattered CSS → Tailwind CSS
- Old component libraries → shadcn/ui

**Critical Security Issues Identified:**
1. Order.setUser_id(1) - hardcoded to 1 regardless of actual user
2. Checkout always uses "u1001" - no real user flows through
3. SQL/CQL injection risk - string concatenation in transactions
4. No CSRF protection - explicitly disabled
5. Session-scoped beans may fail with load balancing

**Timeline:** Q2 for frontend + security fixes, Q2-Q3 for full backend migration

#### SRC-004: Current System Documentation (EXISTING_FUNCTIONALITY)
**Source:** Reverse-engineered from existing REQUIREMENTS.md

**Implemented Features:**
- Product catalog with pagination (limit/offset)
- Product details by ASIN
- Category browsing (Books, Music, Beauty, Electronics)
- Sales rankings within categories
- Star rating display
- Shopping cart: add, view, remove, clear
- Cart total calculation
- Checkout with inventory validation
- Transactional inventory updates
- Order creation with confirmation number

**Known Gaps (TODO items from existing docs):**
- Product search
- Product filtering (price, brand, rating)
- Update quantity in cart
- Wishlist / save for later
- Payment processing
- Shipping address/method
- Order confirmation emails
- Tax calculation
- Guest checkout
- Order history
- User profile management

**Technical Debt:**
- Hardcoded user ID "u1001"
- Deprecated React patterns (componentWillReceiveProps, componentWillMount)
- HTTP only (no HTTPS)
- Raw CQL string concatenation

---

## OUTPUT FORMAT

Use Standard PRD Format (Option A from the template) with these modifications:
- Include a dedicated "Mobile Requirements" section under Non-Functional Requirements
- Add a "Migration Requirements" section under Technical Requirements
- Emphasize the Conflicts section given the stakeholder vs. technical team input

---

## ADDITIONAL CONTEXT

### Constitution Principles (Architectural Constraints)

1. **Technology Stack Mandate:**
   - Backend: Python 3.11+, FastAPI, SQLModel/SQLAlchemy
   - Frontend: Next.js 14+, React 18+, TypeScript, Tailwind CSS
   - Database: PostgreSQL (YSQL) - consolidate away from YCQL
   - Authentication: JWT-based, with path to OAuth2

2. **Architecture Patterns:**
   - Microservices with clear bounded contexts
   - Stateless services (no session-scoped beans)
   - Environment-based service discovery (no Eureka)
   - API Gateway pattern for frontend-to-backend communication

3. **Security Principles:**
   - No hardcoded credentials or user IDs
   - Parameterized queries only (no string concatenation)
   - Proper authentication flow through all services
   - HTTPS in production

4. **UX Principles:**
   - Mobile-first responsive design
   - Minimum 44px touch targets
   - Page load under 3 seconds on 4G
   - Progressive Web App capabilities

5. **Development Approach:**
   - Strangler fig pattern for migration
   - Phased delivery with working increments
   - Parallel deployment during transition

---

Now analyze the provided sources and generate the Requirements Document following the specified format.
```

---

## Expected Output Structure

When you run this prompt, you should get a document with:

1. **Executive Summary** - Synthesizing modernization + mobile + migration goals
2. **Stakeholder Analysis** - Sarah's business needs vs. technical team constraints
3. **Current State** - Gap analysis against existing functionality
4. **Functional Requirements** - Extracted from all sources with FR-XXX IDs
5. **Non-Functional Requirements** - Including dedicated Mobile section
6. **Technical Requirements** - Including Migration section
7. **UX Requirements** - Warm bookstore feel, modern interactions
8. **Conflicts Section** - e.g., timeline pressure vs. scope, mobile priority vs. backend migration

---

## Conflict Examples the Generator Should Surface

Based on these sources, the generator should identify conflicts like:

### CONFLICT-001: Timeline vs. Scope
- **Sources:** SRC-001 (Sarah wants May delivery) vs. SRC-003 (team says migration is complex)
- **Nature:** Phase 1 scope may be too large for Q2 delivery
- **Recommendation:** Prioritize frontend refresh + critical security fixes; defer full backend migration

### CONFLICT-002: Apple Pay Priority
- **Sources:** SRC-002 (Sarah says must-have) vs. SRC-003 (team says "might slip to phase 2")
- **Nature:** High-impact feature may not fit in phase 1 timeline
- **Recommendation:** Timebox integration effort; have fallback plan

### CONFLICT-003: PWA vs. Native App
- **Sources:** SRC-002 (PWA recommended) vs. implicit iOS limitations
- **Nature:** PWA limitations on iOS may not fully address mobile gaps
- **Recommendation:** Start with PWA, measure results, revisit native if metrics don't improve

---

## Tips for Your Workflow

1. **Before generating:** Summarize long transcripts into key points (like I did above)

2. **Include existing docs:** The REQUIREMENTS.md you already have is perfect as EXISTING_FUNCTIONALITY input

3. **Iterate:** Run the generator, review output, add clarifications, regenerate

4. **Version your requirements:** Keep dated versions as stakeholder input evolves

5. **Connect to SDD:** Once requirements are stable, feed them + constitution into SDD generator

---

## Quick Template (Copy-Paste Ready)

For future stakeholder materials, use this intake format:

```markdown
#### SRC-XXX: [Title] ([SOURCE_TYPE])
**Date:** [Date]
**Participant(s):** [Names and Roles]

**Key Points:**
- [Point 1]
- [Point 2]

**Priorities Stated:**
1. [Priority 1]
2. [Priority 2]

**Metrics/Data Mentioned:**
- [Metric]: [Value]

**Constraints/Concerns:**
- [Constraint 1]
```

