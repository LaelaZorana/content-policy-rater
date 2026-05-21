"""Aggregate per-criterion decisions into an overall decision."""
from __future__ import annotations

from collections import Counter

SEVERITY_ORDER = {"PASS": 0, "FLAG": 1, "BLOCK": 2}


def aggregate(criteria_decisions: list[dict], rubric: dict) -> str:
    """Return the overall decision string given per-criterion decisions and rubric."""
    agg = rubric.get("aggregation", "worst_wins")

    decisions = [c["decision"] for c in criteria_decisions]
    if not decisions:
        return "PASS"

    if agg == "worst_wins":
        return max(decisions, key=lambda d: SEVERITY_ORDER.get(d, 0))

    if agg == "majority":
        return Counter(decisions).most_common(1)[0][0]

    if agg == "weighted":
        # Each criterion contributes weight × severity; rank by total weighted severity.
        weights = {c["id"]: c.get("weight", 1) for c in rubric["criteria"]}
        score = {"PASS": 0.0, "FLAG": 0.0, "BLOCK": 0.0}
        for cd in criteria_decisions:
            w = weights.get(cd["id"], 1)
            score[cd["decision"]] = score.get(cd["decision"], 0.0) + w
        # If any BLOCK exists with weight >= threshold, BLOCK wins
        if score["BLOCK"] >= score["PASS"]:
            return "BLOCK"
        if score["FLAG"] >= score["PASS"]:
            return "FLAG"
        return "PASS"

    raise ValueError(f"unknown aggregation: {agg}")
