"""Summary stats."""
from collections import Counter


def summarize(decisions):
    if not decisions:
        return {"total": 0}
    overall = Counter(d["overall_decision"] for d in decisions)
    per_criterion = {}
    for d in decisions:
        for c in d["criteria"]:
            per_criterion.setdefault(c["id"], Counter())[c["decision"]] += 1
    return {"total": len(decisions),
            "by_overall_decision": dict(overall.most_common()),
            "by_criterion": {k: dict(v.most_common()) for k, v in per_criterion.items()}}
