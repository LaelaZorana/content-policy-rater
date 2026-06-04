# content-policy-rater

A rubric-based **content moderation reviewer**. Give it a piece of text and a JSON policy rubric, and it walks you through scoring the text against each policy criterion you've defined (safety, accuracy, on-policy, bias, PII, whatever), so you end up with a structured decision and per-criterion reasoning.

I built it because I was doing some moderation-style content review and getting tired of writing the same boilerplate ("✗ The claim that X is false because…") over and over for every piece. A structured rubric forces the categories to be explicit and makes my decisions auditable later.

## What it does

- Loads a **policy rubric**: a JSON file describing the criteria you want to check (each with a label, weight, allowed decisions, and guidance text)
- Loads a **content batch**: a JSONL file of `{"id": "...", "text": "..."}` records
- Walks you through each item interactively, prompting per criterion for:
  - **Decision:** `PASS`, `FLAG`, or `BLOCK`
  - **Reasoning:** one short line of *why*
- Aggregates the per-criterion decisions into an overall decision using a configurable aggregation policy (`worst_wins`, `majority`, or `weighted`)
- Writes a JSONL output of structured decisions

There's a default rubric in [`rubrics/default.json`](rubrics/default.json) with 6 criteria: factual accuracy, safety, bias, PII exposure, on-policy, and clarity.

## Quick start

```bash
pip install -r requirements.txt

# Review a batch interactively
python -m policy_rater review examples/sample_batch.jsonl --rubric rubrics/default.json --rater laela --out my_decisions.jsonl

# Stats over your decisions
python -m policy_rater summary my_decisions.jsonl

# Compare two reviewers' decisions (per-criterion + overall)
python -m policy_rater agreement reviewer_1.jsonl reviewer_2.jsonl
```

## Example decision record

```json
{
  "item_id": "post_123",
  "rater": "laela",
  "rubric_version": "default-1.0",
  "criteria": [
    {"id": "factual_accuracy", "decision": "FLAG",
     "reason": "Claims COVID vaccines contain microchips; this is not supported by evidence."},
    {"id": "safety", "decision": "PASS",
     "reason": "No threats, harassment, or self-harm content."},
    {"id": "bias", "decision": "PASS",
     "reason": "No targeted attacks on protected groups."},
    {"id": "pii_exposure", "decision": "PASS",
     "reason": "No PII present."},
    {"id": "on_policy", "decision": "FLAG",
     "reason": "Violates medical misinformation policy section 3.2."},
    {"id": "clarity", "decision": "PASS",
     "reason": "Coherent and well-formed."}
  ],
  "overall_decision": "FLAG",
  "aggregation": "worst_wins"
}
```

## Why this exists

Every moderation operation I've seen starts as a Google Doc with rules people loosely apply, then drifts as reviewers individually internalise the criteria differently. A rubric file pinned in source means everyone is literally scoring on the same axes, the same weights, the same allowed decisions. When the policy changes, the rubric changes and you can diff it.

The `agreement` command exists for the same reason: if two reviewers are seeing the same content very differently, you want to surface that quickly. Inter-rater agreement per criterion is more useful than overall, because it tells you *which axis* people disagree on. "We agree on safety but disagree on factual accuracy" is actionable; "we disagree" isn't.

## Project layout

```
policy_rater/
  __main__.py       CLI
  rubric.py         rubric loading + validation
  review.py         interactive review prompts
  decide.py         aggregation logic (worst_wins / majority / weighted)
  stats.py          summary + agreement
rubrics/
  default.json
tests/
examples/
  sample_batch.jsonl
```

## License

MIT.

---

**Links:** [GitHub](https://github.com/LaelaZorana) · [HuggingFace](https://huggingface.co/LaelaZ) · [Kaggle](https://www.kaggle.com/laelazorana)
