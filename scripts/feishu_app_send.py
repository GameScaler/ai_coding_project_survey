#!/usr/bin/env python3
"""
Send a Feishu/Lark bot message through an internal Feishu app.

Required environment variables:
  FEISHU_APP_ID
  FEISHU_APP_SECRET

Optional:
  FEISHU_RECEIVE_ID: required for single-target sends unless --subscriber-file is used
  FEISHU_RECEIVE_ID_TYPE: chat_id, open_id, user_id, email, or union_id.
    Defaults to chat_id.
  FEISHU_SUBSCRIBER_FILE: JSON subscriber file for multi-recipient sends.

Do not store secrets in this repository. Keep app secrets in local shell
environment, Codex automation secrets, or a deployment secret manager.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass


FEISHU_BASE = "https://open.feishu.cn/open-apis"
URL_RE = re.compile(r"https?://[^\s)>\"]+")
FIXED_PRODUCTS = [
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


@dataclass(frozen=True)
class Recipient:
    receive_id: str
    receive_id_type: str
    name: str = ""


def load_subscribers(path: pathlib.Path, subscription: str) -> list[Recipient]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("subscribers", [])
    recipients: list[Recipient] = []
    for row in rows:
        if row.get("status", "active") != "active":
            continue
        row_subscription = row.get("subscription", "daily")
        if subscription != "all" and row_subscription not in {subscription, "all"}:
            continue
        receive_id = row.get("receive_id")
        if not receive_id:
            continue
        recipients.append(
            Recipient(
                receive_id=receive_id,
                receive_id_type=row.get("receive_id_type", "chat_id"),
                name=row.get("name", receive_id),
            )
        )
    return recipients


def post_json(url: str, payload: dict, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        if "CERTIFICATE_VERIFY_FAILED" not in str(exc):
            raise
        return post_json_with_curl(url, payload, token)


def post_json_with_curl(url: str, payload: dict, token: str | None = None) -> dict:
    cmd = [
        "curl",
        "--silent",
        "--show-error",
        "--fail-with-body",
        "--max-time",
        "20",
        "--request",
        "POST",
        "--header",
        "Content-Type: application/json; charset=utf-8",
        "--data-binary",
        "@-",
        url,
    ]
    if token:
        cmd[-1:-1] = ["--header", f"Authorization: Bearer {token}"]
    result = subprocess.run(
        cmd,
        input=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8") or result.stdout.decode("utf-8"))
    return json.loads(result.stdout.decode("utf-8"))


def load_local_env() -> None:
    """Load ignored local env files when present, without overriding shell env."""
    for path in (pathlib.Path(".env.local"), pathlib.Path(".env")):
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def tenant_access_token(app_id: str, app_secret: str) -> str:
    data = post_json(
        f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    if data.get("code") != 0:
        raise RuntimeError(f"tenant_access_token failed: {data}")
    return data["tenant_access_token"]


def section(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.M | re.S,
    )
    match = pattern.search(body)
    return match.group("body").strip() if match else ""


def compact_text(text: str) -> str:
    text = re.sub(r"^#+\s+.*$", "", text, flags=re.M)
    text = re.sub(r"自动抓取已完成。.*", "", text)
    text = re.sub(r"发布前需要补充.*", "", text)
    text = re.sub(r"本文件是机器抓取草稿.*", "", text)
    text = re.sub(r"重大更新初筛[：:].*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def product_sections(body: str) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_name = ""
    current_lines: list[str] = []
    ignored = {"Summary", "PM Notes", "Product Updates"}

    for raw in body.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", raw.strip())
        if heading:
            if current_name and current_name not in ignored:
                sections.append((current_name, current_lines))
            current_name = heading.group(1).strip()
            current_lines = []
            continue
        if current_name:
            current_lines.append(raw)

    if current_name and current_name not in ignored:
        sections.append((current_name, current_lines))
    return sections


def subsections(body: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^###\s+(.+?)\s*$", body, re.M))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections.append((match.group(1).strip(), body[start:end].strip()))
    return sections


def normalize_hits(text: str, limit: int = 8) -> str:
    if not text or text.lower() in {"none", "无"}:
        return "无"
    parts = re.split(r"[,，、/]\s*", text)
    seen: set[str] = set()
    cleaned: list[str] = []
    for part in parts:
        value = part.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        cleaned.append(value)
        if len(cleaned) >= limit:
            break
    return "、".join(cleaned) if cleaned else "无"


def draft_product_summary(body: str) -> tuple[list[str], int]:
    product_names: list[str] = []
    changed_source_count = 0

    for product, lines in product_sections(body):
        text = "\n".join(lines)
        count = 0
        for pattern in (
            r"初筛[：:]\s*发现\s*(\d+)\s*个",
            r"初筛状态[：:]\s*发现\s*(\d+)\s*个",
        ):
            match = re.search(pattern, text)
            if match:
                count = int(match.group(1))
                break
        if not count:
            count = len(re.findall(r"(?:Changed:\s*True|是否变化：是)", text))
        if count:
            product_names.append(product)
            changed_source_count += count

    return product_names, changed_source_count


def summary_text(body: str) -> str:
    summary = compact_text(section(body, "Summary"))
    if summary:
        return summary

    product_names, changed_source_count = draft_product_summary(body)
    if product_names:
        shown = "、".join(product_names[:5])
        suffix = "等" if len(product_names) > 5 else ""
        return (
            f"今日 {shown}{suffix} 有候选更新，需要人工判断是否构成产品级重大变化。"
            "正式发布前请完善 Summary / Product Updates / PM Notes。"
        )
    return "无新增产品级重大公开更新。"


def product_signal_lines(body: str, limit: int = 10) -> list[str]:
    signals: list[str] = []

    product_updates = section(body, "Product Updates")
    if product_updates:
        current = ""
        for raw in product_updates.splitlines():
            line = raw.strip()
            heading = re.match(r"^###\s+(.+)$", line)
            if heading:
                current = heading.group(1).strip()
                continue
            if current and line.startswith("- "):
                content = line[2:].strip()
                signals.append(f"- **{current}**：{content}")
                current = ""
            if len(signals) >= limit:
                return signals

    for product, lines in product_sections(body):
        explicit_count = 0
        changed_count = 0
        hits: list[str] = []
        for raw in lines:
            line = raw.strip()
            count_match = re.search(r"初筛(?:状态)?[：:]\s*发现\s*(\d+)\s*个", line)
            if count_match:
                explicit_count = int(count_match.group(1))
            if re.search(r"(?:Changed:\s*True|是否变化：是)", line):
                changed_count += 1
            hits_match = re.search(r"(?:Keyword hits|命中方向)[：:]\s*(.+)$", line)
            if hits_match:
                hit_text = hits_match.group(1).strip()
                if hit_text and hit_text.lower() not in {"none", "无"}:
                    hits.append(hit_text)
        count = explicit_count or changed_count
        if not count:
            continue
        hit_summary = normalize_hits("、".join(hits))
        if hit_summary == "无":
            signals.append(f"- **{product}**：发现 {count} 个官方来源变化，需复核是否构成产品级更新。")
        else:
            signals.append(
                f"- **{product}**：发现 {count} 个官方来源变化；关注方向：{hit_summary}。"
            )
        if len(signals) >= limit:
            break
    return signals


def pm_note_lines(body: str) -> list[str]:
    notes = section(body, "PM Notes")
    lines: list[str] = []
    for raw in notes.splitlines():
        line = raw.strip()
        if not line or "TODO" in line:
            continue
        if line.startswith("- "):
            lines.append(line)
    return lines[:3]


def clean_markdown_text(text: str) -> str:
    text = re.sub(r"^[-*]\s+", "", text.strip())
    text = text.replace("**", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def compact_section_lines(text: str) -> list[str]:
    bullet_lines: list[str] = []
    paragraphs: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- "):
            bullet_lines.append(clean_markdown_text(line))
        elif not line.startswith("#"):
            paragraphs.append(clean_markdown_text(line))
    return bullet_lines or paragraphs[:2]


def first_section_text(body: str, heading: str, default: str = "无") -> str:
    lines = compact_section_lines(section(body, heading))
    return lines[0] if lines else default


def fixed_product_update_lines(body: str) -> list[str]:
    product_updates = section(body, "Product Updates")
    product_bodies = dict(subsections(product_updates))
    lines: list[str] = []
    for product in FIXED_PRODUCTS:
        product_body = product_bodies.get(product, "")
        updates: list[str] = []
        for raw in product_body.splitlines():
            line = raw.strip()
            if not line.startswith("- "):
                continue
            content = clean_markdown_text(line)
            if not content or content.startswith("来源") or URL_RE.match(content):
                continue
            updates.append(content)
        content = "；".join(updates[:2]) if updates else "无"
        lines.append(f"**{product}**：{content}")
    return lines


def fixed_weekly_signal_lines(body: str) -> list[str]:
    raw_signals = compact_section_lines(section(body, "Head Product Signals"))
    signals: dict[str, str] = {}
    for raw in raw_signals:
        cleaned = clean_markdown_text(raw)
        match = re.match(r"^(.+?)[：:](.*)$", cleaned)
        if not match:
            continue
        product = match.group(1).strip()
        value = match.group(2).strip() or "无"
        if product in FIXED_PRODUCTS:
            signals[product] = value
    return [f"**{product}**：{signals.get(product, '无')}" for product in FIXED_PRODUCTS]


def source_lines(body: str, github_url: str | None) -> list[str]:
    urls: list[str] = []
    if github_url:
        urls.append(github_url)
    urls.extend(URL_RE.findall(body))

    seen: set[str] = set()
    deduped: list[str] = []
    for url in urls:
        url = url.rstrip(".,，。")
        if url in seen:
            continue
        seen.add(url)
        deduped.append(url)

    labels = {
        "github.com/GameScaler": "GitHub 归档",
        "developers.openai.com/codex": "OpenAI Codex",
        "github.com/openai/codex": "OpenAI Codex",
        "code.claude.com": "Claude Code",
        "github.com/anthropics/claude-code": "Claude Code",
        "cursor.com/changelog": "Cursor",
        "cursor.com/blog": "Cursor",
        "docs.trae.ai": "TRAE SOLO",
        "trae.cn": "TRAE 中国更新日志",
        "trae.ai/solo-web": "TRAE SOLO",
        "github.blog": "GitHub Copilot",
        "github.com/github/copilot-cli": "GitHub Copilot",
        "windsurf.com": "Windsurf",
        "devin.ai": "Devin",
        "docs.openclaw.ai": "OpenClaw",
        "github.com/openclaw": "OpenClaw",
        "raw.githubusercontent.com/openclaw": "OpenClaw",
        "kimi.com/code": "Kimi Code",
        "kimi.com/ai-models": "Kimi Code",
        "github.com/MoonshotAI/kimi-code": "Kimi Code",
        "raw.githubusercontent.com/MoonshotAI/kimi-code": "Kimi Code",
        "docs.bigmodel.cn/cn/coding-plan": "Zhipu GLM Coding Plan",
        "docs.bigmodel.cn/cn/update": "Zhipu GLM Coding Plan",
        "z.ai/subscribe": "Zhipu GLM Coding Plan",
        "codegeex.cn": "CodeGeeX",
        "marketplace.visualstudio.com/items?itemName=aminer.codegeex": "CodeGeeX VS Code",
        "github.com/THUDM/CodeGeeX": "CodeGeeX",
    }

    output: list[str] = []
    seen_labels: set[str] = set()
    for url in deduped:
        label = "来源"
        for key, value in labels.items():
            if key in url:
                label = value
                break
        if label in seen_labels:
            continue
        seen_labels.add(label)
        output.append(f"- [{label}]({url})")
        if len(output) >= 14:
            break
    return output


def build_digest_markdown(body: str, github_url: str | None) -> str:
    if section(body, "Weekly Summary"):
        return build_weekly_digest_markdown(body)

    summary = summary_text(body)

    product_updates = fixed_product_update_lines(body)

    notes = pm_note_lines(body)
    if not notes:
        notes = [
            "- **产品官短评**：无新增产品级重大公开更新。",
            "- **对 TRAE SOLO 的启示**：只记录真正改变用户 workflow 的新 feature、模型迭代、agent workflow、治理、定价和交付物边界变化。",
            "- **LPME 是否更新**：不更新。",
        ]

    parts = [
        "**Summary**",
        summary,
        "",
        "**Product Updates**",
        *product_updates,
        "",
        "**PM Notes**",
        *notes,
    ]
    return "\n".join(parts)


def build_weekly_digest_markdown(body: str) -> str:
    competitive = compact_section_lines(section(body, "Competitive Reading"))
    source_notes = compact_section_lines(section(body, "Source Notes"))
    parts = [
        "**Weekly Summary**",
        first_section_text(body, "Weekly Summary"),
        "",
        "**Head Product Signals**",
        *fixed_weekly_signal_lines(body),
        "",
        "**Competitive Reading**",
        *(competitive or ["无"]),
        "",
        "**TRAE SOLO Implication**",
        first_section_text(body, "TRAE SOLO Implication"),
        "",
        "**LPME Implication**",
        first_section_text(body, "LPME Implication"),
        "",
        "**Source Notes**",
        *(source_notes or ["无"]),
    ]
    return "\n".join(parts)


def build_card(title: str, body: str, doc_url: str | None, github_url: str | None) -> dict:
    card_body = build_digest_markdown(body, github_url or None)
    elements: list[dict] = [{"tag": "markdown", "content": card_body[:6000]}]
    actions = []
    if doc_url:
        actions.append(
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "打开飞书文档"},
                "type": "primary",
                "url": doc_url,
            }
        )
    if github_url:
        actions.append(
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "打开 GitHub Digest"},
                "url": github_url,
            }
        )
    if actions:
        elements.append({"tag": "action", "actions": actions})
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "blue",
        },
        "elements": elements,
    }


def send_interactive_message(
    token: str,
    receive_id_type: str,
    receive_id: str,
    card: dict,
) -> dict:
    query = urllib.parse.urlencode({"receive_id_type": receive_id_type})
    return post_json(
        f"{FEISHU_BASE}/im/v1/messages?{query}",
        {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(card, ensure_ascii=False),
        },
        token,
    )


def main() -> int:
    load_local_env()

    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_file", type=pathlib.Path)
    parser.add_argument("--title", default="AI Coding Daily Update")
    parser.add_argument("--doc-url", default="https://my.feishu.cn/docx/GVk4d22dSo3jEXxst72cRjMfntg")
    parser.add_argument("--github-url", default="")
    parser.add_argument("--subscriber-file", type=pathlib.Path, default=None)
    parser.add_argument("--subscription", choices=["daily", "weekly", "major-only", "all"], default="daily")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    body = args.markdown_file.read_text(encoding="utf-8")
    card = build_card(args.title, body, args.doc_url, args.github_url or None)

    subscriber_file = args.subscriber_file
    if subscriber_file is None and os.environ.get("FEISHU_SUBSCRIBER_FILE"):
        subscriber_file = pathlib.Path(os.environ["FEISHU_SUBSCRIBER_FILE"])

    recipients: list[Recipient]
    if subscriber_file:
        recipients = load_subscribers(subscriber_file, args.subscription)
    else:
        receive_id = os.environ.get("FEISHU_RECEIVE_ID")
        if not receive_id and not args.dry_run:
            raise SystemExit("FEISHU_RECEIVE_ID is required unless --subscriber-file is used")
        recipients = [
            Recipient(
                receive_id=receive_id or "dry_run_receive_id",
                receive_id_type=os.environ.get("FEISHU_RECEIVE_ID_TYPE", "chat_id"),
            )
        ]

    if args.dry_run:
        print(
            json.dumps(
                {
                    "recipient_count": len(recipients),
                    "recipients": [
                        {
                            "name": recipient.name,
                            "receive_id_type": recipient.receive_id_type,
                            "receive_id": recipient.receive_id,
                        }
                        for recipient in recipients
                    ],
                    "card": card,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    app_id = os.environ["FEISHU_APP_ID"]
    app_secret = os.environ["FEISHU_APP_SECRET"]
    token = tenant_access_token(app_id, app_secret)

    results = []
    failed = False
    for recipient in recipients:
        result = send_interactive_message(
            token,
            recipient.receive_id_type,
            recipient.receive_id,
            card,
        )
        results.append(
            {
                "name": recipient.name,
                "receive_id_type": recipient.receive_id_type,
                "receive_id": recipient.receive_id,
                "result": result,
            }
        )
        if result.get("code") != 0:
            failed = True

    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
