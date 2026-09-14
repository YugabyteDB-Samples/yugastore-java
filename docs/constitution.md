# Constitution

Durable, non-negotiable principles for this repo. This is not the place for anything that might be true only for a while — see `docs/ai-sdlc-roadmap.md` for the full context-tier design. Changes to this file require a PR (CODEOWNERS-gated — see `.github/CODEOWNERS`).

1. **Spec before plan, always.** `superpowers:brainstorming` must produce a written `specs/<issue-#>-<slug>/spec.md` before `superpowers:writing-plans` runs — at every scope (Spike, Bounded, Architectural), not only Architectural.
2. **TDD is mandatory** for application code changes (not for docs/config-only changes). Tests are written before implementation, per `superpowers:test-driven-development`.
3. **No agent pushes to `master` or force-pushes a shared branch.** All work lands via PR.
4. **`plan.md`'s task checkboxes are the authoritative task ledger** for any work item. If the Session Handoff Record or local `.ai-local/state.md` disagrees with `plan.md`, `plan.md` wins.
5. **Use the Yugabyte Java Driver (`com.yugabyte:java-driver-core`), never the DataStax OSS driver**, in any module talking to YCQL (`products-microservice`, `checkout-microservice`) — see `docs/gotchas.md` and `docs/adr/0002-yugabyte-driver-over-datastax.md`.
6. **Discovery repairs docs, in the same PR.** If an agent burns time on something that should already have been documented, updating `docs/gotchas.md`, `docs/architecture.md`, or a new ADR is part of that PR, not a follow-up issue.
7. **Definition of done** for any PR: tests pass, `plan.md` checkboxes current, constitution/docs/ADR impact considered (see PR template), and the linked Issue's Session Handoff Record reflects final state or the issue is closed.
8. **Architecture decisions with real consequences get an ADR** (`docs/adr/`), not just a Slack message or a PR description. ADRs are append-only; superseding a decision means a new ADR, not an edit.
9. **Local-only stores never outrank git or the Issue.** Claude Code's per-machine auto-memory and this repo's `.ai-local/` hot cache may inform an agent's next action, but neither is authoritative over a committed file or the Session Handoff Record.
10. **One owner per fact.** Work-item progress lives on the GitHub Issue (Session Handoff Record, labels, board column); work-item intent lives in `specs/`; project-level context lives in this file, `CLAUDE.md`, and `docs/`. Nothing is intentionally duplicated across tiers — see `docs/ai-sdlc-roadmap.md` for the full model.
11. **The reviewer role never writes code.** An agent that can edit the code it's reviewing cannot be trusted to judge it. This applies to the `reviewer` agent and the internal `task-reviewer`/`re-reviewer` workers alike — none of them get `Edit`/`Write` tools, regardless of how much other trust (push access, etc.) a role otherwise carries.
