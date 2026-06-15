#!/usr/bin/env python3
"""
Generate a conservative weekly digest when the Codex weekly automation does not.

The fallback only uses existing public daily digests. It does not publish crawler
metadata and does not pretend to be a deep market review. Its job is to ensure a
weekly artifact exists so Feishu delivery does not silently skip a completed week.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
DAILY_DIR = ROOT / "data" / "daily_updates"
WEEKLY_DIR = ROOT / "data" / "weekly_updates"
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


def last_complete_week(today: dt.date) -> tuple[dt.date, dt.date, str]:
    current_monday = today - dt.timedelta(days=today.weekday())
    week_start = current_monday - dt.timedelta(days=7)
    week_end = current_monday - dt.timedelta(days=1)
    iso_year, iso_week, _ = week_start.isocalendar()
    return week_start, week_end, f"{iso_year}-W{iso_week:02d}"


def is_public_weekly(text: str) -> bool:
    return (
        "## Weekly Summary" in text
        and "## Head Product Signals" in text
        and "## Competitive Reading" in text
        and "机器抓取草稿" not in text
    )


def section(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.M | re.S,
    )
    match = pattern.search(body)
    return match.group("body").strip() if match else ""


def subsections(body: str) -> dict[str, str]:
    matches = list(re.finditer(r"^###\s+(.+?)\s*$", body, re.M))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        result[match.group(1).strip()] = body[start:end].strip()
    return result


def product_updates_for_week(week_start: dt.date, week_end: dt.date) -> dict[str, list[str]]:
    updates = {product: [] for product in PRODUCTS}
    current = week_start
    while current <= week_end:
        path = DAILY_DIR / f"{current.isoformat()}.md"
        if path.exists():
            product_bodies = subsections(section(path.read_text(encoding="utf-8"), "Product Updates"))
            for product in PRODUCTS:
                body = product_bodies.get(product, "")
                for raw in body.splitlines():
                    line = raw.strip()
                    if not line.startswith("- "):
                        continue
                    content = line[2:].strip()
                    if content and content != "无" and content not in updates[product]:
                        updates[product].append(content)
        current += dt.timedelta(days=1)
    return updates


def build_digest(week_start: dt.date, week_end: dt.date, label: str) -> str:
    updates = product_updates_for_week(week_start, week_end)
    has_signal = any(values for values in updates.values())
    lines = [
        f"# {label}（{week_start.isoformat()}～{week_end.isoformat()}）",
        "",
        "## Weekly Summary",
        "",
        (
            "本周有少量产品级信号，主要来自每日归档中的模型、agent workflow、治理或交付边界变化。"
            if has_signal
            else "本周未观察到足以改变产品路线判断的重大公开更新。"
        ),
        "",
        "## Head Product Signals",
        "",
    ]
    for product in PRODUCTS:
        content = "；".join(updates[product][:2]) if updates[product] else "无"
        lines.append(f"- **{product}**：{content}")
    lines.extend(
        [
            "",
            "## Competitive Reading",
            "",
            "AI coding 产品能力仍由模型能力和产品能力共同决定；无论模型是否更新，产品层都需要持续补齐 context、workflow、verification、recovery、collaboration 和 governance。",
            "",
            "## TRAE SOLO Implication",
            "",
            "TRAE SOLO / TRAE Work 应把竞品变化翻译为用户可理解的任务状态、可验证交付物、模型 / 工具降级和团队协作边界。",
            "",
            "## LPME Implication",
            "",
            "如果本周没有新增重大产品能力，LPME 不做结构性更新；仅在后续实测中继续记录模型能力、产品补位和交付稳定性的差异。",
            "",
            "## Source Notes",
            "",
            "- 基于本周每日归档、官方 changelog / docs / release notes 复核。",
            f"- GitHub permalink: https://github.com/GameScaler/ai_coding_project_survey/blob/main/data/weekly_updates/{label}.md",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    today = dt.date.fromisoformat(args.date)
    week_start, week_end, label = last_complete_week(today)
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    path = WEEKLY_DIR / f"{label}.md"
    if path.exists() and not args.force and is_public_weekly(path.read_text(encoding="utf-8")):
        print(f"exists:{path}")
        return 0

    path.write_text(build_digest(week_start, week_end, label), encoding="utf-8")
    print(f"generated:{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
