# Claims evidence and proof boundaries

Represent only the objects needed for the slice: requirement, authoritative source, assumption,
artifact, product surface, claim, witness, observer and decision. Stable references help people
refer to the same thing. A small file/table is sufficient; an ontology platform is optional.

Keep these distinct: an operation ran; an observation exists; the observation supports a claim;
the whole required outcome is demonstrated. Neither a typed evidence label nor a hash establishes
semantic adequacy. State the observed target, environment and boundary.

| Intended claim | Suitable proof in its scope | Inadequate substitution |
|---|---|---|
| Parser/core decision | Inputs, valid/invalid states and observable decisions under the actual contract | Naming, coverage or a test of an unrelated helper |
| API behavior | Request, interpreted response and actual endpoint/binding identity | Status code alone for a broader journey |
| Persisted state | Writer plus independent fresh read/reopen and pertinent failure/replay cases | Screenshot, in-memory counter, mock call or queued status |
| External effect | Observer at the promised stage, correlated identity and ambiguity/retry handling | Dispatch intent or successful local cancellation |
| User journey | Required steps, legitimate completion and failure recovery in the relevant composition | A passing backend unit test |
| Developer experience | Actual install/create/adopt/change/debug/upgrade workflow and observed friction | Existence of commands or a pleasant README |
| Upgrade compatibility | Old/new version on the same consumer/corpus, change report and explicit adoption | A new wheel built successfully |
| Operational identity/recovery | Artifact→runtime observation and an authorized relevant recovery drill | Desired SHA, health200 or image rollback as database restore |
| Resource bound | Admission/dispatch/payload/attempt/exposure observation for a supported profile | A timeout, estimate or usage summary as a financial cap |

Reuse an existing witness that proves the obligation. Add or strengthen one when there is a
demonstrated gap. Where practical, show that the relevant broken behavior is rejected and a
legitimate behavior accepted. A test can use raises/properties/observers without a literal
assert. Do not require full suites, E2E, mutation or a new test for every implementation detail.

Independent proof means the observation is not simply the system under test restating its own
answer. Consider whether candidate code can alter the verifier, selector, oracle, configuration
or attestation. An unsandboxed subprocess can be useful local feedback, but cannot support a
stronger trust claim merely because it is a different process.

If evidence is partial, narrow the claim or complete the missing boundary. If the instrument
fails or no applicable work ran, record that state. Do not translate missing/unknown/skipped into
success. Preserve real nonapplicability with a verifiable reason. Do not “fix” a failure by
relaxing the source, oracle, required policy, baseline or threshold being judged.
