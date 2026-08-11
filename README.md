# Two-Model Council

A portable, provider-agnostic protocol for making two AI models disagree productively, revise their
positions, and leave behind an auditable decision rather than a blended answer.

It is designed for architectural choices, strategy, ambiguous plans, and
expensive-to-reverse work. It is intentionally unnecessary for routine tasks.

## What it is

One model acts as orchestrator and artifact writer. A second model acts as an
independent peer. They receive the same neutral brief, propose independently,
challenge each other's evidence and assumptions, revise, and then hand the record
to a named decision owner or arbiter. The arbiter turns the result into one
self-contained implementation plan; readers do not need to reconstruct the plan
from the debate.

This captures visible conclusions, evidence, objections, concessions, and
decisions. It does not request or expose hidden chain-of-thought.

## The protocol

```text
neutral brief
   ├── model A independent proposal
   └── model B independent proposal
             ↓
       mutual challenge
             ↓
       mutual revision
             ↓
   repeat only while decision-relevant
             ↓
   accountable-owner decision
             ↓
   implementation plan
```

Default: two challenge/revision cycles, with a four-cycle ceiling. Stop earlier
only after the requested minimum and when another exchange would add no evidence,
revision, or resolvable disagreement.

## Why independent openings matter

If Model B sees Model A's answer before forming its own position, the exercise
becomes critique or editing—not independent judgment. The orchestrator should
therefore create one neutral evidence boundary and obtain both opening proposals
before exchanging them.

## Evidence options

When both models run on the same machine, give the peer canonical file paths and
use `--allow-workspace-read`; do not copy or inline the files. The prompt should
name the exact allowed paths, and the runner enables read/search tools only—never
writes or shell commands. Repeat `--source-file` only when the peer does not share
the filesystem.

## Task trackers are optional

The council ends with a decision record. It does not require Todoist, Linear,
GitHub Issues, or any task tracker. If a project already has a canonical execution
system, approved work can be routed there afterward. The council artifacts should
not become a competing task queue.

## Files produced

Each issue should preserve:

- `brief.md` — neutral question, evidence boundary, constraints, authority;
- `<provider-a>.md` — first model's turns;
- `<provider-b>.md` — second model's turns;
- `transcript.md` — visible exchange in order;
- `decision.md` — concise ruling, rationale, and preserved dissent;
- `implementation-plan.md` — primary handoff: ordered work, ownership,
  dependencies, acceptance tests, risks, and approval gates.

`implementation-plan.md` is the end product. It must stand alone as if a capable
model had been asked to inspect the problem and produce an execution-ready plan.
The other files explain how that plan was reached.

## Install as a Codex skill

Copy `two-model-council/` into your Codex skills directory. Keep the folder name
and `SKILL.md` name unchanged. Install and authenticate the CLIs for the providers
you select. Gemini support is built in; additional CLIs use a vetted adapter.

## Example

```bash
python3 two-model-council/scripts/run_peer.py \
  --provider claude \
  --prompt decisions/new-data-model/prompt.md \
  --output decisions/new-data-model/claude-round-1.md \
  --cwd . \
  --allow-workspace-read
```

Do not use permission-bypass flags. If a peer cannot run, record the failure;
never invent the missing model's contribution.

## Select providers and control cost

Claude, Codex, and Gemini are built in. The two council roles may use any
combination:

```bash
python3 two-model-council/scripts/run_peer.py \
  --provider gemini --model '<gemini-model>' \
  --prompt decisions/topic/prompt.md \
  --output decisions/topic/gemini.md --cwd . --allow-workspace-read
```

Kimi, Ollama, or another CLI can be registered with `--adapter-config`; see
`references/provider-adapters.md`. In a hosted product, keep this registry
server-owned and allowlisted—never run arbitrary user-supplied commands.

The runner otherwise inherits each CLI's configured default. Set a model and
reasoning effort explicitly:

```bash
# Claude: economical challenge/revision round
python3 two-model-council/scripts/run_peer.py \
  --peer claude --model haiku --effort low --max-budget-usd 1 \
  --prompt decisions/topic/prompt.md \
  --output decisions/topic/claude.md --cwd . --allow-workspace-read

# Codex: select an available model explicitly
python3 two-model-council/scripts/run_peer.py \
  --peer codex --model '<codex-model>' --effort low \
  --prompt decisions/topic/prompt.md \
  --output decisions/topic/codex.md --cwd . --allow-workspace-read
```

Use a capable economical model for independent proposals, a cheaper model for
challenge/revision rounds, and one stronger model for final synthesis. Do not run
both frontier models for every exchange. Also keep one peer session alive or
resume it when supported; repeatedly booting a CLI and resending unchanged context
can consume more tokens than the visible answer.

## Repository contents

- `two-model-council/SKILL.md` — portable skill entry point;
- `two-model-council/references/protocol.md` — turn and decision schemas;
- `two-model-council/scripts/run_peer.py` — restricted peer runner;
- `POST-DRAFT.md` — a public write-up based on the first real use.

No license has been selected. Add one before distributing if appropriate.
