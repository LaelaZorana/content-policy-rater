from policy_rater import decide


RUBRIC_WORST = {"aggregation": "worst_wins",
                "criteria": [{"id": "a"}, {"id": "b"}, {"id": "c"}]}
RUBRIC_MAJ = {"aggregation": "majority",
              "criteria": [{"id": "a"}, {"id": "b"}, {"id": "c"}]}
RUBRIC_WEIGHTED = {"aggregation": "weighted",
                   "criteria": [{"id": "a", "weight": 1},
                                {"id": "b", "weight": 5},
                                {"id": "c", "weight": 1}]}


def _ds(*decisions):
    return [{"id": chr(ord("a") + i), "decision": d, "reason": "x"}
            for i, d in enumerate(decisions)]


def test_worst_wins_block_beats_flag():
    assert decide.aggregate(_ds("PASS", "FLAG", "BLOCK"), RUBRIC_WORST) == "BLOCK"


def test_worst_wins_all_pass():
    assert decide.aggregate(_ds("PASS", "PASS", "PASS"), RUBRIC_WORST) == "PASS"


def test_majority_picks_most_common():
    assert decide.aggregate(_ds("PASS", "FLAG", "FLAG"), RUBRIC_MAJ) == "FLAG"


def test_weighted_b_heavy_dominates():
    # b has weight 5; if b says BLOCK it should win even if a+c both say PASS
    assert decide.aggregate(_ds("PASS", "BLOCK", "PASS"), RUBRIC_WEIGHTED) == "BLOCK"


def test_weighted_heavy_pass_beats_light_flags():
    # b has weight 5 and says PASS; a + c are weight 1 each and say FLAG.
    # Weighted total: PASS=5, FLAG=2 → PASS wins.
    assert decide.aggregate(_ds("FLAG", "PASS", "FLAG"), RUBRIC_WEIGHTED) == "PASS"


def test_empty_decisions_pass():
    assert decide.aggregate([], RUBRIC_WORST) == "PASS"
