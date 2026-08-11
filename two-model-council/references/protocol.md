# Council Protocol

## Visible turn

```markdown
## [Runtime] — Round [N]: [Proposal | Challenge | Revision]

### Position
[Recommendation in 1-3 sentences.]

### Evidence
- [Evidence] [Source and implication.]
- [Inference] [Decision-relevant inference.]

### Challenge
- [Specific weakness, conflict, or unanswered question.]

### Concession or revision
- [What changed, or "No revision" with a reason.]

### Proposed work split
- [Owner — deliverable — dependency — acceptance evidence.]

### Confidence
[High, medium, or low, plus what could change the answer.]
```

This is a visible decision record, not hidden chain-of-thought.

## Default exchange

1. Independent proposals.
2. Mutual challenges.
3. Mutual revisions.
4. Second mutual challenge on remaining disagreement.
5. Final revisions.
6. Accountable-owner synthesis.

Continue for material differences, checkable new evidence, overlapping ownership,
or unclear approval boundaries. Stop after the requested minimum when the models
converge, differences are merely preferences, or a round adds no revision. Four
cycles is the default ceiling.

## Decision record

```markdown
# Council Decision: [Topic]

**Disposition:** [adopt | recommend for owner | blocked on evidence]

## Recommendation
[One path and confidence.]

## Why
- [Decisive evidence and tradeoff.]

## Agreement
- [What both models agree on.]

## Preserved dissent
- [Concern, owner, and trigger to revisit.]

## Work packages
1. **[Deliverable]** — Owner: [role/runtime] — Depends on: [item] — Done when: [evidence]

## Owner decisions
- [Only approvals or choices that remain.]
```

Keep `decision.md` concise. It explains the ruling and preserves decision-relevant
dissent; it is not the implementation handoff.

## Implementation plan

Write this as `implementation-plan.md`. It is the primary output and must be
usable without reading any other council artifact.

```markdown
# Implementation Plan: [Outcome]

**Status:** [ready to implement | approval required | blocked]
**Decision owner:** [person or role]
**Implementation owner:** [person, role, or runtime]
**Last updated:** [date]

## Outcome
[What will be true when the plan is complete, and why it matters.]

## Current state
- [Only facts an implementer needs to understand the starting point.]

## Scope

### In scope
- [Included result.]

### Out of scope
- [Explicit non-goal.]

## Adopted approach
[The architecture or operating choice in direct language.]

### Decisions already made
- [Decision the implementer should not reopen without new evidence.]

## Implementation phases

### Phase 1: [Name]
**Owner:** [one owner]
**Depends on:** [dependency or none]

Changes:
1. [Concrete change, including component, file, interface, or workflow where known.]
2. [Concrete change.]

Done when:
- [Observable acceptance evidence.]

### Phase 2: [Name]
[Repeat as needed.]

## Interfaces and handoffs
- [Producer -> artifact or schema -> consumer.]

## Validation
- [Test, inspection, command, scenario, or evidence.]
- [Failure and stale-state behavior to verify.]

## Rollout and recovery
- [Sequence, compatibility, migration, rollback, or recovery condition.]

## Risks and mitigations
| Risk | Likelihood/impact | Mitigation | Owner |
|---|---|---|---|
| [Risk] | [Assessment] | [Action] | [Owner] |

## Approval gates and stop conditions
- [Approval required before consequential action.]
- [Condition that must stop implementation.]

## Open questions
- [Only unresolved questions that materially affect implementation; otherwise "None".]

## First executable action
[One bounded action that starts the plan once its gates are satisfied.]
```

Planning rules:

- Convert recommendations into imperative, ordered work.
- Use one canonical owner for every deliverable.
- Name likely files, components, data contracts, or workflows when the evidence
  supports them; do not invent paths or APIs.
- Make acceptance criteria observable and proportionate to risk.
- Distinguish `ready to implement`, `approval required`, and `blocked` honestly.
- Keep rejected alternatives and debate history in `decision.md` or
  `transcript.md`, not in the execution sequence.
