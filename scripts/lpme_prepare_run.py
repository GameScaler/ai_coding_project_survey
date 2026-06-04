#!/usr/bin/env python3
"""Prepare isolated LPME product test workspaces."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


TASKS = {
    "LPME-SE-001": "se_bugfix",
    "LPME-PM-001": "pm_prototype",
    "LPME-DS-001": "ds_acquisition",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product", required=True)
    parser.add_argument("--date", default="2026-06-04")
    parser.add_argument("--task", choices=sorted(TASKS), default=None)
    args = parser.parse_args()

    root = Path("data/product_tests") / args.date / args.product
    fixtures = Path("benchmark/lpme_v0.2/fixtures")
    tasks = [args.task] if args.task else sorted(TASKS)

    for task_id in tasks:
        fixture_name = TASKS[task_id]
        run_dir = root / task_id
        workspace = run_dir / "workspace"
        output = run_dir / "output_artifacts"
        screenshots = run_dir / "screenshots"
        for path in (workspace, output, screenshots):
            path.mkdir(parents=True, exist_ok=True)
        source = fixtures / fixture_name
        if workspace.exists():
            shutil.rmtree(workspace)
        shutil.copytree(source, workspace)
        (run_dir / "run_notes.md").write_text(
            f"# {args.product} {task_id} Run Notes\n\n"
            f"- Date: {args.date}\n"
            "- Status: prepared\n"
            "- Product/version:\n"
            "- Surface:\n"
            "- Model/account plan:\n"
            "- Time:\n"
            "- Cost/credits:\n"
            "- First usable artifact time:\n"
            "- Human correction loops:\n"
            "- Biggest delight:\n"
            "- Biggest failure:\n"
            "- Root cause hypothesis:\n"
            "- TRAE SOLO implication:\n",
            encoding="utf-8",
        )
        (run_dir / "raw_logs.txt").write_text("", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
