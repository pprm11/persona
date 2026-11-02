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

Read the whole diff and identify layers. Check dependency direction, raw values or framework types crossing boundaries, duplicated parsing, a port with extra methods, and adapter implementations narrowing a port contract. Verify findings against callers. Report location, concrete failure or maintenance consequence, proposed fix and, where useful, a test or dependency rule that prevents recurrence.

In Python, `NewType` gives static distinctions but does not validate at runtime. Use a constructor or parser for values with invariants. `frozen` data classes help model immutable values; `TYPE_CHECKING` does not remove conceptual coupling. Strict Pydantic parsing can still have format-specific exceptions, so check its documented behavior. Python has no standard-library `Result`; use the project’s established convention.

Do not force value objects or a multi-layer design onto a disposable spike or trivial script. For Python-specific tooling and errors see [python-idioms](../python-idioms/SKILL.md), if installed; otherwise follow the project conventions.

## Further reading

- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) for dependency direction and boundary data.
- [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/) for parsing into a more precise type.
- [Python typing documentation](https://docs.python.org/3/library/typing.html) and [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) for the language-specific limits.
