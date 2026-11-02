---
name: clean-architecture
description: "Write or review domain boundaries, ports and adapters, dependency direction and typed domain models."
---

# Clean Architecture

## Write a use case

1. Locate the boundary in the existing design. A typical dependency direction is domain and ports inward, adapters outside, and a composition root that wires dependencies. Respect a simpler existing design when an added layer has no benefit.
2. Start with an input-to-output domain test. Model meaningful values and invalid states, then implement the decision without I/O. Supply time, identifiers and randomness as inputs. For expected domain failures use an explicit result or discriminated union; unexpected invariant failures remain errors.
3. Parse untrusted data once at the boundary into domain types. Translate framework, database, SDK and transport objects in adapters; do not return them to the domain. Define small ports around what the client actually needs and inject implementations at composition.
4. Test boundary integration and errors separately. Check idempotency where repeated execution is possible and give independent work separate mutable state.

## Review

Read the whole diff and identify layers. Check dependency direction, raw values or framework types crossing boundaries, duplicated parsing, a port with extra methods, and adapter implementations narrowing a port contract. When an abstraction looks superfluous, try the deletion test as a hint. Imagine it removed and ask whether the complexity disappears or spreads to its callers. List the invariants, errors and configuration each caller would then have to know, and confirm the callers with a search before calling anything unused. A thin adapter over an SDK, an external type, the clock or another side effect stays even with a single consumer, and dependency direction rules win over the deletion test. Verify findings against callers. Report location, concrete failure or maintenance consequence, proposed fix and, where useful, a test or dependency rule that prevents recurrence.

In Python, `NewType` gives static distinctions but does not validate at runtime. Use a constructor or parser for values with invariants. `frozen` data classes help model immutable values; `TYPE_CHECKING` does not remove conceptual coupling. Strict Pydantic parsing can still have format-specific exceptions, so check its documented behavior. Python has no standard-library `Result`; use the project’s established convention.

For messages that must reach another system, an outbox gives at-least-once delivery, so duplicates are possible and the consumer must tolerate them. Marking an event as sent before it is emitted turns that into at-most-once, because a crash between the two loses it. An idempotent consumer records the dedupe key and does its work in the same transaction. Side effects outside that database, such as HTTP calls or emails, are not covered by the transaction and need their own idempotency key. When the work leaves the database, a claim with a lease and an expiry is the usual substitute. A store that fails open keeps at-least-once delivery at the cost of duplicates during the outage. Report that window as a trade-off and do not ask for exactly-once.

Do not force value objects or a multi-layer design onto a disposable spike or trivial script. For Python-specific tooling and errors see [python-idioms](../python-idioms/SKILL.md), if installed; otherwise follow the project conventions.

## Further reading

- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) for dependency direction and boundary data.
- [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/) for parsing into a more precise type.
- [Python typing documentation](https://docs.python.org/3/library/typing.html) and [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) for the language-specific limits.
