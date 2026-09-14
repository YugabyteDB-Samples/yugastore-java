---
name: resuming-work
description: Use at the start of any session on a branch that matches the <issue-#>-<slug> convention, or when explicitly asked to resume/pick up an issue. Reconstructs full working state from .ai-local/, the GitHub Issue's Session Handoff Record, and git — verifying rather than trusting any single source. Also owns writing/updating the SHR and .ai-local/ files at the checkpoints defined below.
---

# Resuming Work

Full design: `docs/ai-sdlc-roadmap.md` §1-2. This skill is the only place the reconstruction protocol and the checkpoint-writing protocol live — don't reinvent either inline.

## When a branch has no issue number

If the current branch doesn't match `<issue-#>-<slug>` (e.g. `master`, or a scratch branch), this skill doesn't apply. Don't fabricate an issue number.

## Reconstruction protocol (run this before touching any code)

0. **Fast path, same machine.** Check `.ai-local/<issue-#>-<slug>/state.md` and `decisionlog.md`. If present, read them — this is a starting hypothesis, not ground truth. No network call yet.
1. `gh issue view <issue-#> --comments` — find the comment starting with `<!-- AI-SDLC:HANDOFF v1 -->`. That's the SHR.
2. `git fetch`, then confirm every sha named in the SHR (or `.ai-local/state.md`) is reachable. If not: that source is stale-but-not-wrong-in-kind — fall back to `git log origin/<branch>` as ground truth, and note that both sources need rewriting.
3. Re-create isolation from the branch (see `superpowers:using-git-worktrees` if not already on it). Run the baseline command recorded in the SHR/state.md. Compare the result. **A mismatch invalidates the task state in both sources** — don't trust either's task list until you've re-derived it.
4. Read `specs/<issue-#>-<slug>/spec.md` and `plan.md` at HEAD. **`plan.md`'s checkboxes are authoritative** over both the SHR and `.ai-local/` when they disagree.
5. Re-hydrate your live todo list from `plan.md`.
6. Summarize what you reconstructed back to the human in a few lines before proceeding — branch, what's done, what's next, and anything you had to fall back on (stale SHR, missing baseline, etc.).

## Finding the SHR comment programmatically

```bash
gh api repos/{owner}/{repo}/issues/<issue-#>/comments \
  --jq '.[] | select(.body | startswith("<!-- AI-SDLC:HANDOFF v1 -->")) | .id'
```

If a comment ID is returned, update it in place:

```bash
gh api repos/{owner}/{repo}/issues/<issue-#>/comments/<comment-id> -X PATCH -f body=@handoff.md
```

If nothing is returned, this is the first checkpoint for this issue — create it:

```bash
gh issue comment <issue-#> --body-file handoff.md
```

Never create a second SHR comment. Always search first.

## SHR format

```
<!-- AI-SDLC:HANDOFF v1 -->
## Session Handoff Record
- updated: <ISO 8601 UTC>  by: <git config user.email>  host: <hostname>  session: <short id, stable for this session>
- branch: <branch>
- local HEAD: <sha>   remote HEAD: origin/<branch> @ <sha>   ahead/behind: <n>/<n>
- baseline: `<command>` -> <result> @ <sha>

### Task state (authoritative copy is plan.md checkboxes @ the sha above)
<one line per task: name, status, commit range if complete>

### What was tried and rejected
<trimmed to the most recent ~10 entries; full history lives in .ai-local/decisionlog.md>

### Next concrete action
<one or two sentences, specific enough to act on with zero other context>

### Blockers / risky ops pending
<or "None.">
```

Every claim about code is anchored to a sha. "What was tried and rejected" is never skipped, even when there's nothing new — write "No new rejected approaches this session" rather than omitting the section.

## `.ai-local/` format (`.ai-local/<issue-#>-<slug>/`, gitignored)

**`state.md`** — overwritten in place, not appended. Same shape as the SHR's top block, but never trimmed and never posted anywhere.

**`decisionlog.md`** — append-only. One entry per rejected approach or significant finding:

```
## <ISO 8601 UTC>
<what was tried, why it was rejected, or what was learned>
```

If something here is a genuine, durable fact rather than something specific to this task, it doesn't stay here — promote it into `docs/gotchas.md` or a new `docs/adr/` entry in the same PR (constitution rule 6), and note the promotion in the log entry.

## Checkpoints — when to write

Write/update `.ai-local/state.md` continuously as you work (it's cheap — a local file write). Flush to the SHR (and append to `decisionlog.md` if there's a new rejected approach) at:

1. Session start / claim on the issue — add the `ai:in-progress` label. If it's already present with a different session id updated in the last ~4 hours, **stop and ask the human** before proceeding: possible concurrent work.
2. After each task completes.
3. After each subagent (implementer/reviewer) returns a non-trivial result.
4. Before any risky or irreversible operation (schema change, dependency bump, rebase, force-push).
5. On blocker, or handing back to a human — add `ai:blocked` or `ai:needs-human`.
6. On context compaction — flush before you lose context.
7. On session end.

Only the controlling agent writes the SHR — never a subagent. Subagents report back to the controller; the controller updates state.
