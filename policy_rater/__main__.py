"""CLI: review / summary / agreement"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import review as review_mod
from . import rubric as rubric_mod
from . import stats as stats_mod


def _read_jsonl(path: Path) -> list[dict]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"{path} line {i}: invalid JSON: {e}") from e
    return out


def _append_jsonl(path: Path, record: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def cmd_review(args) -> int:
    rubric = rubric_mod.load_rubric(args.rubric)
    already = set()
    if args.out.exists():
        already = {d["item_id"] for d in _read_jsonl(args.out)}
        print(f"Resuming — {len(already)} items already reviewed.")

    n = 0
    try:
        for item in _read_jsonl(args.batch):
            if item.get("id") in already:
                continue
            dec = review_mod.review_item(item, rubric, args.rater)
            _append_jsonl(args.out, dec)
            n += 1
    except KeyboardInterrupt:
        print(f"\nStopped. Reviewed {n} item(s) this session.")
        return 0

    print(f"\nDone. Reviewed {n} item(s) → {args.out}")
    return 0


def cmd_summary(args) -> int:
    decisions = _read_jsonl(args.decisions)
    print(json.dumps(stats_mod.summarize(decisions), indent=2))
    return 0


def cmd_agreement(args) -> int:
    a = _read_jsonl(args.decisions_a)
    b = _read_jsonl(args.decisions_b)
    print(json.dumps(stats_mod.agreement(a, b), indent=2))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="policy_rater")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("review")
    pr.add_argument("batch", type=Path)
    pr.add_argument("--rubric", required=True, type=Path)
    pr.add_argument("--rater", required=True)
    pr.add_argument("--out", required=True, type=Path)

    ps = sub.add_parser("summary")
    ps.add_argument("decisions", type=Path)

    pa = sub.add_parser("agreement")
    pa.add_argument("decisions_a", type=Path)
    pa.add_argument("decisions_b", type=Path)

    args = p.parse_args(argv)
    if args.cmd == "review":
        return cmd_review(args)
    if args.cmd == "summary":
        return cmd_summary(args)
    if args.cmd == "agreement":
        return cmd_agreement(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
