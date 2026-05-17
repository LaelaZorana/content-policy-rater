"""Rubric loading + validation."""
from __future__ import annotations

import json
from pathlib import Path


VALID_AGGREGATIONS = {"worst_wins", "majority", "weighted"}


def load_rubric(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        rubric = json.load(f)
    validate_rubric(rubric)
    return rubric


def validate_rubric(rubric: dict) -> None:
    """Raise ValueError if the rubric is malformed."""
    if "criteria" not in rubric or not isinstance(rubric["criteria"], list):
        raise ValueError("rubric must have a 'criteria' list")
    if not rubric["criteria"]:
        raise ValueError("rubric must have at least one criterion")

    seen_ids = set()
    for c in rubric["criteria"]:
        for field in ("id", "label", "decisions"):
            if field not in c:
                raise ValueError(f"criterion missing '{field}': {c}")
        if c["id"] in seen_ids:
            raise ValueError(f"duplicate criterion id: {c['id']}")
        seen_ids.add(c["id"])
        if not c["decisions"]:
            raise ValueError(f"criterion '{c['id']}' has no decisions")

    agg = rubric.get("aggregation", "worst_wins")
    if agg not in VALID_AGGREGATIONS:
        raise ValueError(f"aggregation must be one of {VALID_AGGREGATIONS}; got {agg!r}")
