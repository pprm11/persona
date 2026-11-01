# Seed B: LLM gateway with model A/B (test seed, not a real task)

Use the skill `staged-engineering` to do this task.

I want to understand where and how to put an LLM gateway in front of the Acme order assistant v2 that falls back between models when the primary one fails and allows a per-customer model A/B (a customer always stays on the same model). Today v2 calls `llm.example.com` directly. Do the problem domain first and send me the questions for Dana and Pat. Then do the rest of the series: as-is, market study with benchmarks, solution domain, HLA with the cost as a decided 1-3-1, and HLD. You may build a POC.

Not allowed: deploy, creating resources, changing config, commit, push, PR, messages. Read-only. No secret printed.

Setup for this test run:
- Repository: the current folder is a checkout of `acme-org/order-assistant`. Read code only at commit `abc1234` (`git show abc1234:<path>`).
- The as-is may use files and public documentation only. No live checks against any cloud, database or API in this test: write NOT VERIFIED where a live check would be needed, with the command that would verify it.
- Write every output under `skill-test/` in the current folder. Do not touch any other file.
- Owner answers: when your problem domain draft lists its questions for the owners, and only then, read `answers-b.md` (next to this seed, path given in your task message). Those are simulated owner answers for this test. Apply them as the skill says.
- Prices: the AWS public price list JSON files may be downloaded with curl from `https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/<Service>/current/sa-east-1/index.json` into `skill-test/prices/`.
- When done, write `skill-test/REPORT.md`: what you produced, what you could not do, and every place where the skill's instructions were unclear or missing.
