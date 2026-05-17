import argparse, json, sys
from pathlib import Path
from . import review as review_mod, rubric as rubric_mod, stats as stats_mod


def _read_jsonl(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def _append_jsonl(path, rec):
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")


def cmd_review(args):
    rubric = rubric_mod.load_rubric(args.rubric)
    for item in _read_jsonl(args.batch):
        d = review_mod.review_item(item, rubric, args.rater)
        _append_jsonl(args.out, d)
    return 0


def cmd_summary(args):
    print(json.dumps(stats_mod.summarize(_read_jsonl(args.decisions)), indent=2))
    return 0


def main():
    p = argparse.ArgumentParser(prog="policy_rater")
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("review")
    pr.add_argument("batch", type=Path); pr.add_argument("--rubric", required=True, type=Path)
    pr.add_argument("--rater", required=True); pr.add_argument("--out", required=True, type=Path)
    ps = sub.add_parser("summary"); ps.add_argument("decisions", type=Path)
    args = p.parse_args()
    return cmd_review(args) if args.cmd == "review" else cmd_summary(args)


if __name__ == "__main__":
    sys.exit(main())
