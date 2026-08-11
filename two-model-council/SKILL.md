---
name: two-model-council
description: Run a visible, bounded two-model deliberation with independent proposals, mutual challenge, revision, an accountable decision, and a self-contained implementation plan. Use for consequential decisions, architecture, strategy, second-model review, or requests for models to discuss an issue and produce an execution-ready plan.
---

# Two-Model Council

Use any two independently selected models as advisers, not as a consensus machine.
Preserve evidence, useful disagreement, and clear ownership.

## Read first

1. Project governance files that exist.
2. The named decision owner or arbiter role, if one exists.
3. `references/protocol.md`.
4. Only the canonical sources needed for this decision.

## Output

Create one stable issue folder under the project's chosen decision-record root.
Default to `30-OUTPUT/council/<issue-name>/` when no convention exists. Write:

- `brief.md`
- `<provider-a>.md`
- `<provider-b>.md`
- `transcript.md`
- `decision.md`
- `implementation-plan.md`

Preserve visible reasoning summaries and evidence, never hidden chain-of-thought.
Treat `implementation-plan.md` as the primary user-facing result. It must be
self-contained; the other files are its audit trail.

## Method

1. Name the orchestrator and decision owner. Frame the question neutrally.
2. Separate facts, constraints, assumptions, approval gates, and unknowns.
3. Give both models the same minimal evidence boundary. When both runtimes share
   a filesystem, pass canonical paths and grant bounded read/search access; do not
   copy files or inline their contents. Use `--source-file` only when the peer
   cannot access the shared filesystem.
4. Collect independent proposals before either model sees the other's position.
5. Exchange challenges: strongest point, weakest assumption, missing evidence,
   and requested revision.
6. Exchange revisions with explicit concessions. Default to two complete
   challenge/revision cycles when multiple exchanges are requested.
7. Stop after the requested minimum when no new evidence or revision appears;
   default ceiling is four cycles.
8. The named decision owner synthesizes by evidence, tradeoffs, authority, and
   reversibility—not by vote. Preserve material dissent.
9. Write a concise `decision.md` with the ruling, rationale, confidence, and
   material dissent.
10. Write `implementation-plan.md` using the schema in
    `references/protocol.md`. Translate the ruling into ordered, concrete work
    with owners, dependencies, acceptance evidence, risks, gates, and a first
    executable action. Do not make the implementer infer tasks from the debate.
11. Route approved execution to the project's canonical tracker only when one
    exists and routing is authorized. A tracker is never required.

## Peer runner

By default, `scripts/run_peer.py` isolates the peer from the workspace. When both
runtimes share a trusted workspace and the requester authorizes named sources, use
`--allow-workspace-read` and put the canonical paths in the prompt. The flag
permits only read/search access. Do not stage copies. Repeat `--source-file` only
as a fallback for runtimes without shared filesystem access.

Never use permission-bypass flags. If the peer cannot run, record the failure and
continue as a one-model analysis; do not simulate the missing voice.

Built-ins are Claude, Codex, and Gemini. Use `--provider`; `--peer` remains an
alias. Read `references/provider-adapters.md` before adding Kimi, Ollama, or
another CLI through `--adapter-config`.

Choose model and effort per call with `--model` and `--effort`. Claude calls may
also set `--max-budget-usd`. Use economical models for challenges and revisions;
escalate only the final synthesis or a genuinely unresolved high-stakes round.
Expose model names as configuration rather than hardcoding provider defaults.

## Boundaries

- One canonical owner per deliverable or file.
- No broad vault access, secrets, or unrelated private context.
- Peer review does not authorize rewriting another owner's work.
- `adopt` applies only to reversible internal work already authorized.
- External sends, publishing, deployment, spending, destructive actions, and
  reserved decisions always require the appropriate approval.
- Running a council never authorizes task creation by itself.
- Producing an implementation plan never authorizes executing it.
