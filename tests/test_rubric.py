import pytest

from policy_rater import rubric as rubric_mod


VALID = {
    "name": "test", "version": "1.0",
    "criteria": [
        {"id": "a", "label": "A", "decisions": ["PASS", "FLAG"]},
        {"id": "b", "label": "B", "decisions": ["PASS", "BLOCK"], "weight": 2},
    ],
    "aggregation": "worst_wins",
}


def test_valid_rubric_loads(tmp_path):
    import json
    p = tmp_path / "r.json"
    p.write_text(json.dumps(VALID))
    r = rubric_mod.load_rubric(p)
    assert r == VALID


def test_missing_criteria_raises():
    with pytest.raises(ValueError, match="criteria"):
        rubric_mod.validate_rubric({})


def test_empty_criteria_raises():
    with pytest.raises(ValueError, match="at least one"):
        rubric_mod.validate_rubric({"criteria": []})


def test_duplicate_id_raises():
    bad = {**VALID, "criteria": [VALID["criteria"][0], VALID["criteria"][0]]}
    with pytest.raises(ValueError, match="duplicate"):
        rubric_mod.validate_rubric(bad)


def test_unknown_aggregation_raises():
    bad = {**VALID, "aggregation": "average"}
    with pytest.raises(ValueError, match="aggregation"):
        rubric_mod.validate_rubric(bad)


def test_criterion_missing_decisions_raises():
    bad = {**VALID, "criteria": [{"id": "a", "label": "A", "decisions": []}]}
    with pytest.raises(ValueError, match="no decisions"):
        rubric_mod.validate_rubric(bad)
