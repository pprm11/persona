---
name: python-idioms
description: "Write or review idiomatic Python: types, errors, async, configuration, tests and I/O."
---

# Python Idioms

## Working rules

Follow the repository's supported Python versions and existing configuration. Prefer consistency with the surrounding module over a new style rule. Use context managers for resources, avoid mutable default arguments, and choose readable loops over dense comprehensions. Keep mutable state scoped and injected where it affects tests or concurrency.

At input boundaries prefer precise types and parsing; accept appropriate abstract interfaces and return concrete documented types. Avoid `Any` when an expressive type exists. Use immutable data classes or explicit unions where they represent real invariants. `assert` is not input validation: optimization can remove it. See [clean-architecture](../clean-architecture/SKILL.md) for domain boundaries when installed.

## Failures, logging and I/O

Catch the narrowest expected exceptions around the smallest operation. Preserve causal context with `raise ... from exc`; do not silently swallow broad exceptions. Log an error once where handled, without secrets or unnecessary personal information. Libraries should not configure application logging. Parse configuration once and do not embed credentials in defaults.

Set timeouts on remote calls. Retry only failures that can safely be retried, with a bounded budget, backoff and jitter, at one layer; check idempotency. In async code avoid blocking the event loop, retain task ownership and propagate cancellation. Close clients and files on all paths.

## Verify

Test observable behavior, error paths and relevant invariants. Inject a clock instead of relying on sleeps; use fakes at external boundaries when appropriate. Property tests are useful for parser round trips and idempotency when meaningful.

Flag a tautological test: its expected value recomputes the implementation (the same formula, the same filter, a hash of the same expression), so the test stays green when the logic is wrong. Expect a literal or an independently derived oracle, or properties the specification states. Flag a vacuous property: a strategy or `assume()` filter that rejects almost every input, so the body rarely runs; generate valid inputs directly and keep `assume` for rare residue. Accept a determinism check (same valid input, same output) on code that could hold hidden state, such as a cache, a seeded generator or a digest, and say why; companion assertions that pin something independent make it a sound test.

Run the project’s configured tests, formatter, lint and type checks; report unavailable checks. Do not impose heavyweight tooling on a throwaway script merely for consistency. For review findings include location, consequence, evidence and a specific correction.

## Further reading

- [PEP 8](https://peps.python.org/pep-0008/) for consistency and Python conventions.
- [Python logging HOWTO](https://docs.python.org/3/howto/logging.html) for library logging and lazy formatting.
- [Python asyncio tasks](https://docs.python.org/3/library/asyncio-task.html) for task lifetime and cancellation.
- [Timeouts, retries and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) for retry tradeoffs.
