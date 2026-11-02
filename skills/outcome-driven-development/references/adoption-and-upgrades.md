# New projects legacy adoption and framework propagation

Treat adoption and evolution as observable product behavior. This guidance extends the article's
maintenance/context principles to shared frameworks, as requested by the user.

## Define four separate outcomes

| Scenario | Questions that determine the design | Evidence |
|---|---|---|
| New project | What must the developer decide? What useful behavior appears first? Which generated parts are examples/drafts? | Fresh install and create/change/debug workflow; meaningful result; command/edit/config count and failures |
| Legacy project | Can existing code, test runner and layout remain? What protection/detection exists today? Which map is necessary? | Actual mapping/adoption in a representative fixture; before/after hashes; existing behavior and its defect control |
| Framework upgrade | Which API/schema/rule/runtime behavior changes? Who approves adoption? Can the same consumer compare versions? | Immutable artifact/pin, compatibility matrix and old/new comparison on the same target/corpus |
| Release propagation | Which consumers have only been notified, installed, migrated, validated or activated? What is stale or unknown? | Per-consumer status with version/config/policy/target and evidence, not a single “published” flag |

## Separate ownership

Keep the shared deterministic mechanism separate from optional rule packs and domain/runtime
adapters. Consumer configuration declares its layout, sources, capabilities and exceptions.
Generated starter code generally belongs to the consumer; a shared engine should be updated as
a dependency rather than recopied. Validate this boundary with two genuinely different consumers,
not two clones of one template. If both require forks of the engine, reconsider the abstraction.

Track core, plugin API, schemas, rules/policy and runtime compatibility independently where their
changes have different meanings. A bug fix can alter a verdict; a semantically compatible API
does not imply unchanged policy. An authority change is not just another patch version.

## Upgrade and activation path

Produce a concrete release delta: changed claims/rules/API/schema, affected consumers, known
incompatibilities and migration/rollback instructions. Pin artifacts by immutable identity.
Consumer comparison should keep code, corpus, policy and environment comparable except for the
dimension being tested; disclose unavoidable differences.

Test both the new detection and legitimate behavior. A stricter release that catches an escape
but blocks a valid workflow still needs resolution. Show missing/unknown/unsupported cases.
Migration should be explicit and reviewable, preserve domain configuration and the history of
exceptions/baselines, and avoid overwriting custom code. Offer a dry-run/diff when it improves
reviewability. Keep the required policy in force until an authorized transition is proved.

Separate release availability, installed package, migrated config, validated result and active
protection. A bot can propose a version bump without proving adoption. Do not claim a whole fleet
updated from one successful canary. Record owner, deadline/staleness when applicable and unknown
consumers; do not silently force new semantics onto all users.

Rollback is compatibility-sensitive: reverting a package can restore an old bug; reverting an
image may not restore schema/data. State which guarantees return or disappear. A pin can be
changed technically without authorizing retirement of an existing required protection.

## Results and friction

For guided legacy adoption, distinguish mechanical fields that structure/imports can justify
from semantic choices such as the applicable source and prompt. Discovery may propose a technical
map without executing the candidate; it cannot authenticate a document or prove a test exercises
the mapped behavior. Show the selected code, test scope and material defaults before application.
Offer an explicit mapping when discovery cannot resolve the layout instead of forcing a reorganization.

Ask only the unresolved choice. Ambiguous code/test links should remain pending until selected;
a skipped choice should stop dependent questions and avoid partial application. Count meaningful
human selections separately from generated fields, review/apply commands and test execution.
Validate the reduction across different layouts with preservation hashes and a behavior defect
control. A two-choice synthetic success is useful evidence for that slice, not a universal onboarding
target or proof of usability, authority, complete suite selection or human preference.

Measure the actual path: first useful result, setup, hand edits, duplicated code/config, diagnostic
quality, rework, upgrade effort and recurring maintenance. Separate cold install from warm loop;
wall time from human attention; offline synthetic proof from model-backed business quality.
An initial scaffold that works only for a toy layout does not establish low legacy adoption cost.
Use a bounded prototype to decide whether to retain a package, a thinner shared helper, a template
or a central service; do not commit to operating a platform before that comparison.
