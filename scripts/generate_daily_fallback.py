#!/usr/bin/env python3
"""
Generate a conservative daily digest when the Codex daily automation does not.

This script is deliberately boring. It never publishes crawler details or raw
source excerpts; it only creates the canonical daily shape so the Feishu delivery
watchdog always has a daily artifact to send.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
DAILY_DIR = ROOT / "data" / "daily_updates"
PRODUCTS = [
    "OpenAI Codex",
    "Claude Code",
    "Cursor",
    "TRAE SOLO",
    "GitHub Copilot",
    "Windsurf / Devin Desktop",
    "OpenClaw",
    "Kimi Code",
    "Zhipu GLM Coding Plan / CodeGeeX",
]


def is_public_digest(text: str) -> bool:
    return (
        "## Summary" in text
        and "## Product Updates" in text
        and "## PM Notes" in text
        and "每日更新初筛" not in text
        and "机器抓取草稿" not in text
    )


def build_digest(day: str) -> str:
    lines = [
        f"# AI Coding Daily Update - {day}",
        "",
        "## Summary",
        "",
        "无新增产品级重大公开更新。",
        "",
        "## Product Updates",
        "",
    ]
    for product in PRODUCTS:
        lines.extend([f"### {product}", "- 无", ""])
    lines.extend(
        [
            "## PM Notes",
            "",
            "- **产品官短评**：无新增产品级重大公开更新。",
            "- **对 TRAE SOLO 的启示**：只记录真正改变用户 workflow 的新 feature、模型迭代、agent workflow、治理、定价和交付物边界变化。",
            "- **LPME 是否更新**：不更新。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        raise SystemExit("--date must be YYYY-MM-DD")

    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    path = DAILY_DIR / f"{args.date}.md"
    if path.exists() and not args.force and is_public_digest(path.read_text(encoding="utf-8")):
        print(f"exists:{path}")
        return 0

    path.write_text(build_digest(args.date), encoding="utf-8")
    print(f"generated:{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
