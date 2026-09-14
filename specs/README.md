# specs/

One folder per work item: `specs/<issue-#>-<slug>/`, matching the GitHub Issue number and the git branch name — this is the join key the whole AI-SDLC resume architecture depends on. See `docs/ai-sdlc-roadmap.md` for the full design.

Each folder holds:
- `spec.md` — written by `superpowers:brainstorming`, required at every scope (Spike/Bounded/Architectural).
- `plan.md` — written by `superpowers:writing-plans`; task checkboxes inside it are the authoritative task ledger.

Nothing else goes here. Session progress lives on the GitHub Issue (Session Handoff Record) and in the gitignored `.ai-local/<issue-#>-<slug>/` hot cache, not in this directory.
