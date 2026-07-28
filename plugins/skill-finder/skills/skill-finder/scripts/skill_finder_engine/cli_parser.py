"""Argument parser for the evidence-engine CLI."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect capabilities, plan routes, and write run bundles."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    _add_doctor_parser(subparsers)
    _add_plan_parser(subparsers)
    _add_render_parser(subparsers)
    return parser


def _add_doctor_parser(subparsers) -> None:
    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--json", action="store_true")


def _add_plan_parser(subparsers) -> None:
    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("--goal", required=True)
    plan_parser.add_argument("--depth", choices=("quick", "deep"), default="quick")
    plan_parser.add_argument("--host", default="codex")
    plan_parser.add_argument(
        "--data-classification",
        choices=("public", "private", "secret"),
        default="public",
    )
    plan_parser.add_argument("--available", default="local-source")
    plan_parser.add_argument("--authorized", default="")
    plan_parser.add_argument("--require-family", action="append")
    plan_parser.add_argument("--exclude-family", action="append")
    plan_parser.add_argument("--local-only", action="store_true")


def _add_render_parser(subparsers) -> None:
    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("--output", required=True)
    render_parser.add_argument("--recommendation", required=True)
    render_parser.add_argument("--install-command", default="")
    render_parser.add_argument("--install-verified", action="store_true")
    render_parser.add_argument("--confidence-rationale", default="")
    render_parser.add_argument("--near-miss", default="")
    render_parser.add_argument("--unresolved", action="append")
