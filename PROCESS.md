# Process Guide

## 1. Choose the right problem

Use a council when disagreement could improve an architectural, strategic, or
expensive-to-reverse decision. Do not use it to make routine execution slower.

Write the decision as an outcome question. A good brief names:

- the decision owner;
- facts and canonical sources;
- constraints and approval gates;
- unknowns;
- required answer shape;
- acceptance criteria.

Do not embed the preferred recommendation in the question.

## 2. Set one evidence boundary

Give both models the same evidence. If they share a filesystem, pass canonical
paths and use read/search-only access; do not make copies. Use `--source-file`
attachments only when the peer cannot reach the shared filesystem.

Mark every claim as evidence or inference. If a source is missing, say so rather
than filling it from memory.

## 3. Preserve independent openings

Collect Model A and Model B proposals before either sees the other's position.
The providers may be Claude, Codex, Gemini, Kimi, a local model, or any configured
pair; provider identity does not change the protocol roles.
This prevents anchoring and makes real disagreement observable.

Each opening should state position, evidence, challenges, proposed ownership, and
confidence.

## 4. Exchange useful challenges

A challenge must do more than disagree. Ask each model for:

- the strongest point in the other proposal;
- its weakest assumption;
- missing or misread evidence;
- the exact revision required.

Factual corrections should happen before strategic debate continues.

## 5. Require revisions

Each model must state concessions and produce a revised recommendation. A defense
with no changed decision is not a revision.

Default to two challenge/revision cycles when a multi-turn discussion is wanted.
Stop when another round would add no evidence, change, or resolvable disagreement.
Four cycles is the normal ceiling, not a target.

## 6. Decide with accountable authority

The final owner decides by evidence, tradeoffs, reversibility, and authority—not
by vote. Preserve material dissent and the condition that would reopen it.

Use one disposition:

- `adopt` for reversible internal work already authorized;
- `recommend for owner` for consequential or approval-gated changes;
- `blocked on evidence` when a named missing input prevents a decision.

Record the ruling and material dissent in `decision.md`. Keep it concise; it is
the audit record, not the execution interface.

## 7. Produce the implementation plan

Write `implementation-plan.md` as the primary deliverable. It must be
self-contained and should read like the output of a strong planning model, not a
summary of a panel discussion. A new implementer should understand what to build,
in what order, where it belongs, how to verify it, and what still needs approval
without reading the transcript.

Include:

- outcome, current state, and non-goals;
- adopted architecture and consequential decisions;
- ordered implementation phases and concrete changes;
- one owner per deliverable;
- dependencies, migration or rollout notes, and approval gates;
- acceptance criteria and verification commands or evidence;
- risks, mitigations, unresolved questions, and explicit stop conditions;
- the first executable next action.

Do not preserve rejected alternatives in the plan body unless they constrain the
implementation. Link material dissent back to `decision.md` instead.

## 8. Separate planning from execution

Define deliverables, dependencies, owner, and acceptance evidence. Then choose the
runtime or person best suited to each package. A task tracker is optional. If one
exists, route only approved work into it; the council folder is a decision record,
not a second task queue.

The council creates the plan; it does not execute it unless the original request
also grants implementation authority.

## 9. Validate the council itself

Before closing, confirm:

- both openings were independent;
- requested exchanges occurred;
- sources are visible and bounded;
- factual corrections made it into later turns;
- the decision answers the original brief;
- `implementation-plan.md` is executable without reading the transcript;
- every phase has concrete outputs and acceptance evidence;
- ownership does not overlap;
- remaining approvals are explicit;
- no model's missing contribution was simulated.
