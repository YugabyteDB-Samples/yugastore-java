# ADR-0001: Record architecture decisions

**Status:** Accepted
**Date:** 2026-09-14

## Context

Decisions with real consequences (why a datastore, why a driver, why a service boundary) were previously made implicitly — visible only in code, a PR description, or a gotcha someone eventually wrote down. Once made and not revisited, they're easy to accidentally contradict later without anyone knowing why the original choice was made.

## Decision

We record architecturally significant decisions as ADRs in `docs/adr/`, one file per decision, using `docs/adr/template.md`. ADRs are append-only: superseding a decision means writing a new ADR that references the old one, not editing history.

## Consequences

Anyone — human or agent — touching an area with a documented ADR can check *why* before changing it. This is a small amount of overhead per decision, in exchange for not silently relitigating settled questions. See `docs/ai-sdlc-roadmap.md` §3 for how this fits into the broader project-context model.
