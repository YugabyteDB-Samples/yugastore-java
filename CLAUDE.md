# YugaStore

Spring Boot microservices eCommerce app backed by YugabyteDB. Seven Maven modules in a root aggregator POM.

@docs/architecture.md
@docs/gotchas.md
@docs/testing-strategy.md

## AI-SDLC conventions

Full design/rationale: `docs/ai-sdlc-roadmap.md`. This section is the load-bearing summary — read it before starting or resuming any work on this repo.

**Naming is the join key.** Branch and `specs/` folder are both `<issue-#>-<slug>`, e.g. branch `42-cart-idempotency` ↔ `specs/42-cart-idempotency/`. Never invent a different numbering scheme.

**Work-item artifacts** live at `specs/<issue-#>-<slug>/`, git-tracked:
- `spec.md` — written by `superpowers:brainstorming`, **required at every scope** (Spike/Bounded/Architectural), not only Architectural. This project does not use GitHub Spec Kit; superpowers covers it with this one addition (roadmap §6).
- `plan.md` — written by `superpowers:writing-plans`; override its default output location to this path. Task checkboxes inside `plan.md` are the **authoritative** task ledger — nothing else outranks them.

**Resume automatically at the start of any session on this repo** whose branch matches the naming convention: invoke the `resuming-work` skill (or run `/resume`). It owns the full reconstruction protocol — `.ai-local/` hot cache first, then the Session Handoff Record, verified against `git log` and `plan.md` before trusting either (roadmap §1.4).

**Named agents, two layers** (roadmap §7): a top-level roster you call by name — `architect` (brainstorming, specs, ADRs), `builder` (plans, implementation), `quality-engineer` (test strategy, verification), `platform-engineer` (CI/CD, infra, GitHub admin), `reviewer` (whole-branch review, no push, no write access) — plus `builder`'s internal, disposable workers (`implementer`, `task-reviewer`, `re-reviewer`) that you don't call directly.

**Auto-memory boundary:** Claude Code's local auto-memory may hold facts about *you*, never facts about this repo, its architecture, or any work item. On any conflict between auto-memory and a file in this repo, **the repo file wins, silently, always.**

**Project principles:** `docs/constitution.md`. Changes there require a PR (CODEOWNERS-gated).
