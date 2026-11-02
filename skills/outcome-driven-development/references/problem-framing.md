# Problem framing before construction

Use this when a request proposes a mechanism but the product result needs definition. Do enough
framing to choose a useful slice; do not turn a clear bug fix into a discovery program.

## Questions that change the implementation

Identify the beneficiary and the situation that should improve. Separate their problem from the
maintenance problems of the tool being proposed. For example, a product team needs to build and safely
change software; maintaining a framework is justified only if it reduces that work or protects an
outcome they need. More harness features are not themselves customer value.

Describe before/after behavior concretely. Include legitimate use, failure handling and the
boundary of the claim. A framework might reduce setup for a new project while making legacy
adoption expensive; a single “easy to use” claim would hide that tradeoff.

Check the premise. Could a small library, existing tool, configuration or example solve the
problem with less ownership? Which capability actually must be shared? What must remain specific
to a product, domain, transport or environment? Preserve the user's chosen direction, but make
material contradictions visible before building on them.

## Decision record proportional to the task

A useful short record contains:

| Field | Purpose |
|---|---|
| Problem and affected actor | Keeps tool-building connected to a real need |
| Outcome and scope | Prevents narrow implementation from masquerading as the whole result |
| Source and authority | Establishes who/what defines expected behavior |
| Alternatives and choice | Preserves the rejected option and the tradeoff that matters |
| Claim, evidence and limit | Chooses the right object to prove |
| Assumption or missing decision | Keeps uncertainty visible and assignable |
| Revisit condition | Explains what future change can invalidate the choice |

Use existing decisions when they still apply. A plan, draft, comment, source link or previous
experiment can inform the choice without becoming current authority. Conflicting requirements
need the relevant owner; choosing the latest or most repeated text is not adjudication.

## Staff-level frame check

Before a large step, check three connections: does this implement the actual need; does it fit
the architecture and ownership boundary; and does its cost make sense once adoption/upkeep are
included? If the frame is wrong, propose a smaller correction and continue authorized independent
work. Do not generate more tasks to disguise a premise that remains unresolved.
