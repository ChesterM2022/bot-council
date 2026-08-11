# I made GPT and Claude disagree on purpose

I wanted two AI models to help me make a decision together. My first instinct was
to put them in a shared conversation and let them talk until they agreed.

That turns out to be the wrong mental model.

Agreement is cheap. One model sees the other's framing, anchors on it, smooths the
edges, and produces a polished consensus. It feels collaborative, but it may only
be correlated confidence.

So I built a small council protocol instead:

1. Write a neutral decision brief and a bounded evidence packet.
2. Ask each model for an independent proposal before either sees the other.
3. Exchange challenges, including the strongest point and weakest assumption.
4. Require explicit revisions and concessions—not just rebuttals.
5. Repeat only while a round changes the evidence or recommendation.
6. Give the full record to a named decision owner who decides by evidence,
   reversibility, and authority rather than majority vote.

The output is not a hidden transcript of model thoughts. The discussion leaves a
visible decision record—claims, sources, objections, changes of mind, and remaining
dissent—but the primary result is a self-contained implementation plan. Someone
new to the issue should be able to execute that plan without decoding the debate.

The first real test taught me something more important: a perfect deliberation
protocol cannot rescue the wrong brief. The models had a strong conversation—but
about how they should collaborate, not about the operating problem I actually
wanted them to solve.

That failure improved the design. The skill now separates the reusable council
from project-specific adapters. It does not require Todoist or any task tracker.
It can work from a self-contained evidence packet, or—when explicitly authorized—
read a named set of local source files with read-only tools.

Then I reran the council on the actual operating question. The first proposals
disagreed sharply about which system should own task mutations. One model also
made an unsafe suggestion based on a date-only checkpoint. The next round caught
the mistake, corrected the evidence, and narrowed the disagreement. After two full
challenge/revision cycles, both models converged on one operational writer, a
separate judgment layer, structured handoffs between them, and schemas that must
exist before scheduling changes.

That is the part I found most valuable: not that two models agreed, but that the
record showed where one changed its mind and why.

The principle I am keeping: use multiple models to preserve disagreement long
enough to improve a decision, not to manufacture certainty.

I’m publishing the skill, protocol, and restricted peer runner so others can test
the pattern on their own architectural and strategic decisions.
