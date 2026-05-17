"""Aggregate per-criterion decisions into an overall decision."""
from collections import Counter

SEVERITY_ORDER = {"PASS": 0, "FLAG": 1, "BLOCK": 2}


def aggregate(criteria_decisions, rubric):
    agg = rubric.get("aggregation", "worst_wins")
    decisions = [c["decision"] for c in criteria_decisions]
    if not decisions:
        return "PASS"
    if agg == "worst_wins":
        return max(decisions, key=lambda d: SEVERITY_ORDER.get(d, 0))
    if agg == "majority":
        return Counter(decisions).most_common(1)[0][0]
    raise ValueError(f"unknown aggregation: {agg}")
