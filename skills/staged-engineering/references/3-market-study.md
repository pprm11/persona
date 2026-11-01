# Stage 3: market study (prior art and benchmarks)

Reader: a reviewer who wants to know whether the series reinvents something the market already solved. It is a stage of its own, with the full analysis; stages 4, 5 and 6 carry only a 3-line summary with a link here.

## Skeleton

```
# Market study: prior art and benchmarks
Series: ...
## In one minute            verdict, the ask, what the market covers, what it does not, the numbers that drive decisions
## Method                   how sources were read; label each claim: independent measurement, vendor claim, search-only
## Prior art and market practices
### <family 1> (e.g. experimentation platforms: Statsig, LaunchDarkly, GrowthBook, Eppo)
### <family 2> (e.g. progressive delivery: Argo Rollouts, Flagger, Istio/Envoy, AppConfig)
### <family 3> (e.g. agent platforms, the channel provider's own features)
## Adopted, adapted or rejected   table: practice · source · verdict · where in the series · why
## Public benchmarks        table: number · what it measures · source with date · label · where the series uses it
## Gaps                     what has no public number and how the test environment will measure it
## Open questions · ## Next steps
```

## How to do it

1. Start from the requirements R# and the constraints AS#: for each one, who in the market solves it and how (sticky bucketing, exposure log, kill switch, stage ladder, holdout).
2. Web research in rounds (standard first; extended only for a hard or recent number). Every source with title, publisher, URL and access date. A vendor talking about itself, on a page read in full, is a "vendor claim". A page read only through a summary or snippet is "search-only", whoever the publisher is. A WebFetch of the page counts as a page read when the claim comes from the fetched text; only the search result alone is "search-only".
3. A benchmark enters only if a decision uses it (cold start, latency, cost per million, the provider's retry policy). A number with no use leaves.
4. Market names feed the stage 1 glossary (a changed term is a cascade).

## Done when

Every practice cited in the later stages has a row in the adopted/adapted/rejected table, and every benchmark number used in a decision has a source, a date and a label.
