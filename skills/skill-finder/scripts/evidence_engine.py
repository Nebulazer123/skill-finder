#!/usr/bin/env python3
"""Inspect capabilities, plan routes, and write Skill Finder run bundles."""

from __future__ import annotations

import json
import sys

from skill_finder_engine.cli_commands import doctor, run_plan, run_render
from skill_finder_engine.cli_parser import build_parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        payload = doctor()
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if not payload["required_missing"] else 1
    if args.command == "plan":
        print(json.dumps(run_plan(args), indent=2, sort_keys=True))
        return 0
    if args.command == "render":
        run_render(args)
        print(f"Wrote run bundle to {args.output}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
