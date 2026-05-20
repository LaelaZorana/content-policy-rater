from policy_rater import decide


RUBRIC_WORST = {"aggregation": "worst_wins",
                "criteria": [{"id": "a"}, {"id": "b"}, {"id": "c"}]}
RUBRIC_MAJ = {"aggregation": "majority",
              "criteria": [{"id": "a"}, {"id": "b"}, {"id": "c"}]}


def _ds(*decisions):
    return [{"id": chr(ord("a") + i), "decision": d, "reason": "x"}
            for i, d in enumerate(decisions)]


def test_worst_wins_block_beats_flag():
    assert decide.aggregate(_ds("PASS", "FLAG", "BLOCK"), RUBRIC_WORST) == "BLOCK"


def test_worst_wins_all_pass():
    assert decide.aggregate(_ds("PASS", "PASS", "PASS"), RUBRIC_WORST) == "PASS"


def test_majority_picks_most_common():
    assert decide.aggregate(_ds("PASS", "FLAG", "FLAG"), RUBRIC_MAJ) == "FLAG"


def test_empty_decisions_pass():
    assert decide.aggregate([], RUBRIC_WORST) == "PASS"
