"""Summary + inter-rater agreement."""
from __future__ import annotations

from collections import Counter


def summarize(decisions: list[dict]) -> dict:
    if not decisions:
        return {"total": 0}

    overall = Counter(d["overall_decision"] for d in decisions)
    per_criterion: dict[str, Counter] = {}
    for d in decisions:
        for c in d["criteria"]:
            per_criterion.setdefault(c["id"], Counter())[c["decision"]] += 1

    return {
        "total": len(decisions),
        "by_overall_decision": dict(overall.most_common()),
        "by_criterion": {k: dict(v.most_common()) for k, v in per_criterion.items()},
    }


def agreement(decisions_a: list[dict], decisions_b: list[dict]) -> dict:
    by_id_a = {d["item_id"]: d for d in decisions_a}
    by_id_b = {d["item_id"]: d for d in decisions_b}
    common = sorted(set(by_id_a) & set(by_id_b))
    if not common:
        return {"common_items": 0}

    # Per-criterion agreement rate
    crit_ids: set = set()
    for d in decisions_a + decisions_b:
        for c in d["criteria"]:
            crit_ids.add(c["id"])

    crit_agreement: dict[str, dict] = {}
    for cid in crit_ids:
        total = 0
        agree = 0
        for item_id in common:
            ca = {c["id"]: c["decision"] for c in by_id_a[item_id]["criteria"]}
            cb = {c["id"]: c["decision"] for c in by_id_b[item_id]["criteria"]}
            if cid in ca and cid in cb:
                total += 1
                if ca[cid] == cb[cid]:
                    agree += 1
        if total:
            crit_agreement[cid] = {
                "total": total,
                "agree": agree,
                "rate": round(agree / total, 3),
            }

    # Overall agreement
    overall_total = len(common)
    overall_agree = sum(
        1 for i in common
        if by_id_a[i]["overall_decision"] == by_id_b[i]["overall_decision"]
    )

    return {
        "common_items": overall_total,
        "overall_agreement_rate": round(overall_agree / overall_total, 3) if overall_total else 0,
        "per_criterion": crit_agreement,
    }
