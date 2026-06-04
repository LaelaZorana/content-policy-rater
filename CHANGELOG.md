# Changelog

## 0.2.1: 2026-05-23

- Fix: `aggregate()` returned a string but `worst_wins` didn't handle empty
  decision lists. Now returns "PASS" for empty input.
- Fix: per-criterion agreement rate divided by total decisions, not common
  decisions. Fixed.

## 0.2.0: 2026-05-20

- Added `agreement` subcommand (per-criterion + overall agreement rates)
- Added `weighted` aggregation mode
- Resume support on `review`

## 0.1.0: 2026-05-16

- First working version. `review` + `summary` commands.
- 6-criterion default rubric (factual accuracy, safety, bias, PII, on-policy, clarity).
- worst_wins and majority aggregation.
