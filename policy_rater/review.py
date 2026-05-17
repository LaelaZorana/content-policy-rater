"""Interactive review prompts."""
from __future__ import annotations

from .decide import aggregate


def _menu(prompt: str, options: list[str]) -> str:
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        raw = input("Choice (number): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("  Invalid choice.")


def review_item(item: dict, rubric: dict, rater: str) -> dict:
    print("\n" + "=" * 70)
    print(f"Item: {item.get('id', '?')}")
    print(f"\nTEXT:\n{item.get('text', '')}")
    print("-" * 70)

    criteria_decisions = []
    for crit in rubric["criteria"]:
        print(f"\n[{crit['label']}]")
        if crit.get("guidance"):
            print(f"  guidance: {crit['guidance']}")
        decision = _menu("  Decision:", crit["decisions"])
        reason = input("  Reason (one line): ").strip()
        while len(reason) < 3:
            reason = input("  Please give a real reason: ").strip()
        criteria_decisions.append({
            "id": crit["id"],
            "decision": decision,
            "reason": reason,
        })

    overall = aggregate(criteria_decisions, rubric)

    return {
        "item_id": item.get("id"),
        "rater": rater,
        "rubric_version": f"{rubric.get('name', 'unnamed')}-{rubric.get('version', '0')}",
        "criteria": criteria_decisions,
        "overall_decision": overall,
        "aggregation": rubric.get("aggregation", "worst_wins"),
    }
