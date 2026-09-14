# AI-SDLC Practice: Architecture & Roadmap

**Status:** Proposal. `yugastore-java` is the pilot repo for this practice — conventions set here are meant to be load-bearing, not throwaway.

## Executive Summary

We're standing up a spec-driven, agent-executed SDLC entirely on the already-installed `superpowers` Claude Code skill set — for spec/plan artifacts, the build-execute-review loop, and a two-layer named-agent model (§7): a top-level roster (Architect, Builder, Quality Engineer, Platform Engineer, Reviewer) matching real SDLC roles, each bound to a skill and trusted with feature-branch push except Reviewer, sitting above Builder's internal, more-restricted execution workers — plus GitHub Issues + Projects as the single Kanban board that both humans and agents work from, with a small set of GitHub Actions guardrails (§8) enforcing the conventions rather than participating in them. [GitHub Spec Kit](https://github.com/github/spec-kit) was evaluated and deliberately not adopted as a separate tool (see §6) — superpowers covers what it offered, once we close two small gaps with plain project conventions.

The problem that forces real design work here isn't the happy path — it's interruption. A session can die at any point: power loss, stepping away, `/clear`, a laptop swap, a different teammate picking up the same issue. Nothing today guarantees the next session can resume with full fidelity, and there's a second, related gap: no durable, versioned context that every session should start from before touching any task.

**Governing rule for everything below: intent lives in git; progress lives in the Issue; nothing lives in both.** Every artifact in this document is assigned to exactly one tier, and each tier has exactly one owner.

| Tier | Answers | Store | Owner |
|---|---|---|---|
| Project context | What must anyone know before touching this repo? | `docs/constitution.md`, `CLAUDE.md`, `docs/` (incl. `docs/adr/`) | PR review / CODEOWNERS |
| Work-item intent | What are we building, by what steps? | `specs/<issue-#>-<slug>/{spec.md,plan.md}` | Feature branch author |
| Work-item progress | Where exactly did we stop, what's true right now? | One edited-in-place GitHub Issue comment (the **Session Handoff Record**) + board column/labels | The agent, at defined checkpoints |
| Local hot cache | What's true *right now*, on *this machine*, without a network call? | `.ai-local/<issue-#>-<slug>/{state.md,decisionlog.md}` (gitignored) | The agent, written continuously; subordinate to the SHR and to `plan.md` |
| Scratch | High-frequency intra-session bookkeeping during plan execution only | superpowers' existing git-ignored SDD ledger | superpowers, unchanged |

## 1. Individual Session Resume: The Session Handoff Record (SHR)

### 1.1 Where it lives, and why not in git

The SHR is a single GitHub Issue comment, maintained in place via `gh`, marked by a machine-findable sentinel — **not** a committed file.

This cuts against instinct ("everything should be version-controlled"), but a committed-but-unpushed file is unreachable after "I lose power to my laptop," and forcing a push on every checkpoint means either checkpoint noise in the branch history or push failures mid-rebase. A `gh issue comment` edit is a single atomic network call with no dependency on working-tree cleanliness. **Progress is not a reviewable artifact, so it doesn't belong in a reviewable store.**

### 1.2 Format

One comment per Issue. First line is a sentinel (`<!-- AI-SDLC:HANDOFF v1 -->`) so an agent can find and replace it deterministically:

```
<!-- AI-SDLC:HANDOFF v1 -->
## Session Handoff Record
- updated: 2026-09-14T15:02:11Z  by: dele.olowoyo  host: MBP-dele  session: 610f4571
- branch: 014-cart-idempotency
- local HEAD: 9f2c1ab   remote HEAD: origin/014-cart-idempotency @ 9f2c1ab   ahead/behind: 0/0
- baseline: `./mvnw -pl cart-microservice test` -> 18/18 pass @ 9f2c1ab

### Task state (authoritative copy is plan.md checkboxes @ the sha above)
- Task 1 Idempotency key column - COMPLETE (commits 3a1f..7bd2, review clean)
- Task 2 Repository upsert - COMPLETE (commits 7bd2..9f2c1ab, review clean)
- Task 3 Controller wiring - IN FLIGHT, fix round 2/5, no commit yet
- Tasks 4-6 - NOT STARTED

### What was tried and rejected
- Unique index on (cart_id, sku): rejected, YCQL has no unique secondary index (see docs/gotchas.md)
- @Transactional across cart + products: rejected, cross-service

### Next concrete action
Re-dispatch Task 3 implementer with the open finding: magic number 100 in CartController:88.

### Blockers / risky ops pending
None. (Next risky op: schema change to cart table - requires local YB restart.)
```

Non-negotiable content rules:
- **Every claim about code is anchored to a sha.** "Task 2 complete" alone is a lie waiting to happen.
- **"What was tried and rejected" is mandatory.** This is the highest-value field and the one most likely to get skipped. Without it, a resumer re-derives dead ends — the expensive failure, not forgetting the goal.
- **No local filesystem paths are trusted.** Reconstruction always re-creates isolation from the branch, never from a recorded local path.

### 1.3 Who writes it, and when

Always the controlling agent, never a subagent (subagents have no authority over shared state; concurrent writes would clobber). Checkpoints:

1. Session start / claim on the issue
2. After each task completes
3. After each subagent returns a non-trivial result
4. Before any risky/irreversible operation (schema change, dependency bump, rebase, force-push)
5. On blocker or handing back to a human
6. On context compaction (flush before losing context)
7. On session end

### 1.4 Reconstruction protocol (assume zero access to the old transcript)

0. **Fast path, same machine only**: check `.ai-local/<issue-#>-<slug>/state.md` and `decisionlog.md`. If present and their `updated:` timestamp is recent, this is the cheapest and freshest source — no network call needed (this is exactly the `/clear` case). Treat it as a starting hypothesis, not ground truth; still perform steps 2-4 below to verify.
1. `gh issue view <N> --comments` → read the SHR.
2. `git fetch` → confirm the shas named in the SHR (or in `.ai-local/`) exist. If not, that source is stale-but-not-wrong-in-kind: fall back to `git log origin/<branch>` as ground truth and rewrite both.
3. Re-create isolation from the branch, run the recorded baseline command, compare to the recorded result. **A baseline mismatch invalidates the task state in both `.ai-local/` and the SHR.**
4. Read `specs/<issue-#>-<slug>/spec.md` and `plan.md` at HEAD. **Checkboxes in `plan.md` are authoritative** over both the SHR and `.ai-local/`'s task lists when they disagree — the file was reviewed, the others were not.
5. Re-hydrate the live todo list from `plan.md`.

### 1.5 Automatic discovery — no human has to remember

Three layers, deliberately redundant:
- **`SessionStart` hook** (`.claude/hooks/`, registered in `.claude/settings.json`) — derives the issue number from the branch name, first checks `.ai-local/<issue-#>-<slug>/` on disk (instant, offline), then checks `gh` health and surfaces the first ~40 lines of the SHR. If `gh` is unavailable, it says so loudly rather than silently emitting nothing — but a present `.ai-local/state.md` still gives the agent something to work from even offline.
- **Project skill `resuming-work`** — owns the full reconstruction protocol (§1.4). Composes with `superpowers:using-superpowers`, which already mandates checking for relevant skills before any response.
- **`CLAUDE.md`** states the convention as a backstop in case the hook breaks or is misconfigured.

**Branch naming is the join key**: `<issue-#>-<slug>`, matching the `specs/<issue-#>-<slug>/` folder. This lets a hook mechanically join git ↔ files ↔ Issue with no separate registry — the GitHub Issue number is used directly rather than an independent sequence, to avoid a lookup table that will drift.

## 2. Local Session Hot Cache

The SHR (§1) is durable across machines but expensive: it's a network call, and it's deliberately trimmed to avoid comment bloat. Verified investigation of the `superpowers` plugin found a real gap this fills: its local execution ledger (`.superpowers/sdd/.../progress.md`) only exists **while `subagent-driven-development` is actively running a plan** — plain brainstorming, `systematic-debugging`, and ad hoc work have no scratch mechanism at all today.

**Convention: `.ai-local/<issue-#>-<slug>/` — gitignored, two files, written continuously:**
- `state.md` — current point-in-time snapshot only: branch, HEAD sha, per-task status, next concrete action, open blockers. Overwritten in place, not appended.
- `decisionlog.md` — append-only, untrimmed record of "what was tried and rejected, and why." The SHR carries a trimmed ~10-entry excerpt of this; the full history lives here.

**Relationship rule (keeps "one owner per tier" intact):** `.ai-local/` is the fastest and most current source available, but it is **never authoritative** — the SHR remains the only source that survives a dead laptop or a machine swap, and `plan.md`'s checkboxes remain authoritative over both for actual task-completion state. The SHR is generated *from* `.ai-local/`'s current contents at the checkpoints defined in §1.3.

**Why this matters for the original ask:** after `/clear`, the files are still sitting on disk in the same repo checkout. The `SessionStart` hook reads `state.md` immediately — no `gh` round-trip, no latency, works offline — and the agent is oriented before it even checks GitHub. The SHR exists for the harder case (different machine, or this one is gone); `.ai-local/` exists for the common case (you're still at your desk, you just cleared context or stepped away).

If something in `decisionlog.md` turns out to matter beyond this one work item (a genuine architectural finding, not a task-specific dead end), it gets promoted into `docs/gotchas.md` or an ADR — the same promotion discipline as the auto-memory boundary in §3, and for the same reason: a fact's storage tier should match how long it stays true, not where it happened to get written first.

## 3. Project-Level Context

| Location | Holds | Discipline |
|---|---|---|
| `docs/constitution.md` | 10-20 durable, non-negotiable principles (TDD mandatory, no DataStax driver in YCQL modules, agents never push to `master`, definition of done) | PR + named approver to change; kept short enough to actually be read |
| `CLAUDE.md` | Thin router: doc pointers, plan-path override, branch/issue naming convention, resume convention, auto-memory boundary | Hard-capped (~60 lines) — it loads every session and competes for context budget |
| `docs/architecture.md`, `docs/gotchas.md` | Descriptive knowledge (already good models of this) | Extended, not replaced |
| `docs/adr/NNNN-title.md` (new) | Decisions with consequences (why YCQL, why Eureka, why no unique index) | Append-only, immutable once accepted; superseding = a new ADR |
| GitHub Projects board + labels | Active initiative state | Never mirrored into a file — this is the one thing meant to change hourly |
| ~~Wiki~~ | — | **Not used.** Unreviewed, unversioned, uncheckable — where drift goes to live |

**Anti-drift forcing functions** (staleness is the default outcome unless something forces correction):
1. Discovery-repairs-docs rule: if an agent burns time on something that should've been documented, fixing the doc is part of the same PR — not a follow-up issue.
2. PR template checkbox: "constitution/docs/ADR impact considered."
3. CODEOWNERS on `docs/constitution.md`, `CLAUDE.md`, `docs/`.
4. Recurring drift-review session: an agent diffs `docs/architecture.md` against actual reality and opens a PR.

## 4. The Local Auto-Memory Boundary

Claude Code's per-machine auto-memory system is **demoted, not deprecated**. Bright line: *who is the fact about?*

- Auto-memory holds facts about **the individual** (preferred verbosity, local Docker quirks, review style) — never facts about the repo, team, or work.
- **Precedence rule**: on any conflict, the repo file wins, silently and always. Auto-memory is a preference cache, not an authority.
- **Promotion path**: when auto-memory accumulates something team-relevant, that's a signal to open a PR promoting it into `docs/`, the constitution, or an SHR — then stop relying on the memory copy.

**Named risk:** this boundary is convention-only; nothing technical stops a teammate's stale local memory from asserting an outdated fact, and that failure is invisible — it looks like the agent just "knowing" something. The mitigation is cultural (this rule, stated in the file that loads every session), not technical. Not oversold as solved.

This is a different store from the `.ai-local/` hot cache in §2, and they stay separate — **decided**: auto-memory is per-machine and per-user across *every* repo and *every* task; `.ai-local/` is per-repo and per-work-item, gitignored but committed-adjacent (it lives in the working tree, dies with a `git clean` or fresh clone, same as the SDD ledger). One is identity-scoped, the other is task-scoped, and folding them together would blur that boundary rather than simplify anything.

## 5. GitHub Issue / File Split

| Written to the Issue | Kept in repo files | Kept locally only (never committed, never posted) |
|---|---|---|
| Problem statement, acceptance criteria (Issue body, human-authored) | — | — |
| Session Handoff Record (one edited-in-place comment) | — | — |
| Milestone comments ("Task 3 complete @ sha", "blocked on X") | — | — |
| Labels: `ai:in-progress`, `ai:blocked`, `ai:needs-human`, `ai:spec-ready` | — | — |
| Board column = work-item state | — | — |
| — | `spec.md`, `plan.md` (checkboxes = authoritative task ledger) | — |
| — | Code, tests, ADRs, gotchas | — |
| — | — | `.ai-local/<issue-#>-<slug>/{state.md,decisionlog.md}` |

Explicit non-duplications: the task list is never also an Issue checklist (two checkbox sets with no owner is a drift trap); acceptance criteria live in `spec.md` once it exists, the Issue body just links to it; work-item state is only the board column + labels, never a `status:` field in a file; `.ai-local/` content never gets posted verbatim to the Issue — only the SHR's distilled summary does.

## 6. Why We're Not Adopting the Spec Kit Tool

Spec Kit gave us three things: a constitution, a per-feature spec artifact, and a plan/tasks split. Verified against the actual `superpowers` skill files rather than assumed:

- **Constitution**: superpowers has no equivalent — no file, convention, or skill produces one. Closed with a plain file, `docs/constitution.md` (§3) — no CLI, no `.specify/` directory needed.
- **Per-item spec**: superpowers' `brainstorming` skill only writes a design-doc artifact for **Architectural**-scope work; **Bounded** and **Spike** scope (most day-to-day issues) produce no written artifact at all today — approval happens in chat and evaporates with the session. Closed with one project rule: **brainstorming must always produce a minimal `specs/<issue-#>-<slug>/spec.md`, at every scope**, before `writing-plans` runs. This is a small addition to how the skill is used here, not a fork of the skill itself.
- **Plan/tasks**: `writing-plans` already produces a single combined file — richer than Spec Kit's plan.md/tasks.md split (inline test code, per-task file lists, a "no placeholders" rule) — at a location the skill lets us override. Redirected here to `specs/<issue-#>-<slug>/plan.md`, with the task checkboxes living inside it. There is no separate `tasks.md`.
- Execution is `superpowers:subagent-driven-development` / `executing-plans`, unchanged.

**Net effect: the Spec Kit tool/CLI is dropped entirely.** Everything it was providing is either already native to superpowers or closed with a one-line project convention. This also removes a cost the first draft of this document flagged: v1 proposed partially adopting Spec Kit (`/specify`, `/plan`) while declining its `/tasks`/`/implement`, which meant forking away from Spec Kit's own documentation and absorbing upgrade risk for no longer benefit. Dropping the tool removes that risk — this is a simplification, not just a substitution.

## 7. Named Agents: A Two-Layer Model

Superpowers itself has no persistent role personas — one continuous session follows skills directly (brainstorming, then writing-plans, then optionally subagent-driven-development, then requesting-code-review), and only forks off disposable subagents where a skill needs isolation. The first cut of this section mapped that internal machinery 1:1 onto named agents and stopped there. **Revised**: that machinery stays, but it's not the roster a human or orchestrator thinks in terms of. On top of it sits a second layer — named, addressable roles matching real SDLC job functions, each bound to a skill (or cluster), each a standing, trusted actor rather than a disposable one.

### Layer 1: the top-level roster (call these by name)

| Agent | Bound to | Push? | Notes |
|---|---|---|---|
| `.claude/agents/architect.md` | `superpowers:brainstorming` | Feature branch only | Owns `spec.md` (every scope, per §6) and `docs/adr/` |
| `.claude/agents/builder.md` | `superpowers:writing-plans` + `subagent-driven-development` (or `executing-plans` for small work) | Feature branch only | Owns `plan.md`; internally dispatches Layer 2 |
| `.claude/agents/quality-engineer.md` | `superpowers:test-driven-development` + `verification-before-completion` | Feature branch only | Test strategy/coverage broadly, not one diff |
| `.claude/agents/platform-engineer.md` | No single skill — domain-scoped (CI/CD, infra/env config, GitHub repo admin) | Feature branch only | Live GitHub mutations still require a human checkpoint, same as everywhere else in this document |
| `.claude/agents/reviewer.md` | `superpowers:requesting-code-review` | **None** — pull/fetch only, plus `gh` write for posting verdicts | No `Edit`/`Write`, no `Agent` — an agent that can edit the code it's reviewing can't be trusted to judge it (`docs/constitution.md` rule 11) |

"Feature branch only" means: commit and push freely to the issue's own branch; never `master`, never a force-push on a shared branch (`docs/constitution.md` rule 3 — unchanged by this revision). None of the five merges to `master` unilaterally; that still goes through a PR.

### Layer 2: Builder's internal workers (unchanged from the first cut — don't call these directly)

| Agent | Wraps | Toolset | Dispatched by |
|---|---|---|---|
| `.claude/agents/implementer.md` | `subagent-driven-development`'s `implementer-prompt.md` | Read, Edit, Write, Grep, Glob, Bash — no `Agent` | Builder, one per task |
| `.claude/agents/task-reviewer.md` | `task-reviewer-prompt.md` | Read, Grep, Glob, Bash — no `Edit`/`Write`, no `Agent` | Builder, one per task |
| `.claude/agents/re-reviewer.md` | `re-review-prompt.md` | Same as `task-reviewer` | Builder, per fix round |

These exist so review stays independent of implementation *within* one execution run — a reviewer subagent that didn't write the code is the whole point, and it needs to be structurally unable to spawn its own replacement or push around the controller. Builder is the controller; these are never addressed by a human or by another top-level role.

### Why the split, and the one place the two principles are in tension

The top-level roster needs to be trusted with real repo access to actually do the job a human would recognize as "the Builder" or "the Architect" — that's Layer 1. The internal workers need to be *more* restricted than that, specifically so Builder's own execution loop can't quietly undermine its own review step — that's Layer 2, and it's a different property from Layer 1's role-based trust model. The one deliberate exception either way: **`reviewer` (Layer 1) is stricter than the general Layer-1 pattern** — no push at all, matching Layer 2's `task-reviewer`/`re-reviewer` — because review independence is a property of the *job*, not of which layer an agent happens to sit in (`docs/constitution.md` rule 11).

## 8. GitHub Actions Guardrails (Revisited)

Earlier in this process, agent-to-Issue interaction was scoped to `gh` CLI only, with no Actions-based sync layer — **that stands**: agents still read/write Issues directly, and the SHR is still written by the agent, never a bot. What's back on the table is a *separate* concern the team is now open to: CI-enforced guardrails that don't touch agent behavior, they just fail a check when a convention in this document is violated. Recommended, low-risk, and useful even before the rest of this rolls out:

- **Naming-convention check** — fails if a branch's name doesn't match `<issue-#>-<slug>`, or if `specs/<issue-#>-<slug>/` is missing for a branch with non-trivial changes. This is the join key the entire resume architecture depends on (§1.5); worth making un-skippable rather than trusting habit.
- **Definition-of-done check** — fails the PR if the "constitution/docs/ADR impact considered" template checkbox (§3) is left unchecked, rather than relying on a human noticing.
- **Scheduled drift-review trigger** — a cron workflow that opens the recurring drift-review PR (§3) automatically, instead of depending on someone remembering to kick it off.

**Deliberately excluded**: anything that writes the SHR, moves board columns, or otherwise acts as a second writer to state the agent already owns — that would reintroduce the exact two-owners-for-one-fact problem this document exists to avoid. These Actions enforce conventions; they don't participate in them.

## 9. Failure Modes

- **Two people/agents resume the same issue** — advisory locking only: label + SHR session id, and a session-start check that stops and asks a human if another session claimed it recently. `gh` has no compare-and-swap, so a true race (two claims within seconds) is undetectable. One worktree+branch per issue turns silent overwrite into a push rejection. **Decided: stay with advisory locking** — a hard, Actions-based lock is deferred until an actual collision occurs in practice, not built preemptively against a hypothetical one.
- **SHR goes stale / lies about branch state** — the verify-before-trust protocol (§1.4) is the mitigation: sha reachability + baseline test rerun before trusting task state.
- **Crash before any commit** — unavoidable loss window. Mitigated by WIP checkpoint commits pushed at task boundaries and the SHR's "next concrete action" field. We promise bounded loss (one task's work), not zero loss.
- **`git clean -fdx` / laptop swap destroys the local SDD ledger** — known and accepted by design; the SHR mirror is what makes this survivable across machines.
- **`gh` unavailable** (offline, expired auth, rate limit) — worst case, because the agent could proceed believing it's checkpointing. The `SessionStart` hook reports `gh` health loudly; on write failure the agent must surface it immediately, not fail silently. `.ai-local/state.md` still exists in this case, so the session isn't fully blind — just not durable across machines.
- **Hook silently breaking** — mitigated by `CLAUDE.md` stating the convention independently, and the hook printing a recognizable banner so its absence is noticeable.
- **Subagent given more capability than intended** — the "don't spawn subagents, don't do risky ops" rule inside `subagent-driven-development`'s prompts was originally enforced only by *prompt instruction*, not by an actual tool restriction — a safety property that shouldn't rest on prompt text alone. **Resolved** by §7: all four roles (implementer + three reviewer roles) are now named agents with an enforced, restricted toolset rather than a generic subagent with a fresh inline prompt.

## 10. Rollout Order

1. ✅ **Done** — Repo hygiene: `.github/` issue + PR templates, CODEOWNERS, `ai:*` labels, Projects board.
2. ✅ **Done** — Project context: expand `CLAUDE.md` into the thin router, write `docs/constitution.md`, seed `docs/adr/`.
3. ✅ **Done** — Branch/folder/issue naming convention — the join key; documented in `CLAUDE.md`, enforced by step 4's naming-convention check.
4. ✅ **Done** — GitHub Actions guardrails (§8): naming-convention check, DoD checkbox enforcement, scheduled drift-review trigger.
5. ✅ **Files done, not yet proven** — SHR convention + `.ai-local/` hot cache + `resuming-work` skill + `/resume` command, and all eight named agents from §7 (the top-level roster: `architect`, `builder`, `quality-engineer`, `platform-engineer`, `reviewer`; Builder's internal workers: `implementer`, `task-reviewer`, `re-reviewer`) all exist. **Still outstanding: the acceptance test** — have a teammate resume someone else's interrupted issue from a completely fresh clone, using only the SHR, `specs/`, and `git log`. Don't treat step 5 as truly complete until that drill has actually happened.
6. `SessionStart` hook — deliberately not started yet. Automate only once step 5's acceptance test has passed and the SHR/`.ai-local/` format has stabilized in real use.
7. **Pilot metrics**: time-to-productive-resume for a cold resumer, and number of rediscovered dead ends.

## 11. Decisions Log

All five items raised after the first draft are resolved:

- **Concurrent-resume locking**: stay with advisory locking (label + SHR session id); a hard Actions-based lock is deferred until an actual collision occurs, not built preemptively (§9).
- **Constitution ownership**: CODEOWNERS on `docs/constitution.md` is sufficient — no standing review cadence needed (§3).
- **Custom Actions automation**: revisited and adopted, scoped to CI guardrails only (naming/DoD/drift-review checks) — agent-to-Issue interaction stays `gh`-CLI-only, no bot writes to the SHR or board (§8).
- **Reviewer roles**: revised beyond the original ask — a full top-level roster (Architect, Builder, Quality Engineer, Platform Engineer, Reviewer) matching real SDLC job functions, not just reviewer roles treated like the implementer. Builder's internal implementer/task-reviewer/re-reviewer workers stay as-is underneath it (§7).
- **`.ai-local/` vs. auto-memory**: stay separate — identity-scoped vs. task-scoped stores serving different purposes (§4).

No open decisions remain from this round; new ones will be logged here as the rollout in §10 proceeds.
