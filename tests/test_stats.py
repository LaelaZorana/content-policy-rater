from policy_rater import stats


def _dec(item_id, overall, criteria):
    return {"item_id": item_id, "rater": "x", "rubric_version": "v",
            "criteria": [{"id": cid, "decision": d, "reason": "x"}
                          for cid, d in criteria],
            "overall_decision": overall, "aggregation": "worst_wins"}


def test_summary_basic():
    decisions = [
        _dec("1", "PASS", [("safety", "PASS"), ("bias", "PASS")]),
        _dec("2", "FLAG", [("safety", "PASS"), ("bias", "FLAG")]),
        _dec("3", "BLOCK", [("safety", "BLOCK"), ("bias", "FLAG")]),
    ]
    s = stats.summarize(decisions)
    assert s["total"] == 3
    assert s["by_overall_decision"]["BLOCK"] == 1
    assert s["by_criterion"]["safety"]["PASS"] == 2
    assert s["by_criterion"]["bias"]["FLAG"] == 2


def test_agreement_per_criterion():
    a = [_dec("1", "PASS", [("safety", "PASS"), ("bias", "PASS")]),
         _dec("2", "FLAG", [("safety", "PASS"), ("bias", "FLAG")])]
    b = [_dec("1", "PASS", [("safety", "PASS"), ("bias", "PASS")]),
         _dec("2", "BLOCK", [("safety", "BLOCK"), ("bias", "FLAG")])]
    g = stats.agreement(a, b)
    assert g["common_items"] == 2
    # safety: 1/2 agree (item 1 same, item 2 different)
    assert g["per_criterion"]["safety"]["rate"] == 0.5
    # bias: 2/2 agree
    assert g["per_criterion"]["bias"]["rate"] == 1.0
    # overall: 1/2 agree
    assert g["overall_agreement_rate"] == 0.5


def test_no_common_items_returns_zero():
    a = [_dec("1", "PASS", [("safety", "PASS")])]
    b = [_dec("99", "FLAG", [("safety", "FLAG")])]
    assert stats.agreement(a, b) == {"common_items": 0}
