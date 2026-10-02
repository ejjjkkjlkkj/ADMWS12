"""Minimal command line tool built directly on the ADMWS12 zero primitive."""

from __future__ import annotations

import argparse
import json
import sys

from .atom import Atom, AtomError, verify_envelope


def main() -> int:
    parser = argparse.ArgumentParser(prog="admws12-zero")
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("--kind", required=True)
    create.add_argument("--version", type=int, default=1)
    create.add_argument("--payload", required=True)
    create.add_argument("--provenance", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--file", required=True)
    args = parser.parse_args()
    try:
        if args.command == "create":
            atom = Atom(args.kind, args.version, json.loads(args.payload), json.loads(args.provenance))
            print(json.dumps(atom.envelope(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            return 0
        with open(args.file, "r", encoding="utf-8") as handle:
            verify_envelope(json.load(handle))
        print("atom: OK")
        return 0
    except (OSError, json.JSONDecodeError, AtomError) as exc:
        print("atom: ERROR: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
