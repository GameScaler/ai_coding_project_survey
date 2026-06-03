#!/usr/bin/env python3
"""
Send an AI coding daily update to a Feishu/Lark custom bot webhook.

Environment variables:
  FEISHU_BOT_WEBHOOK: required
  FEISHU_BOT_SECRET: optional, required only if signature verification is enabled
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import pathlib
import time
import urllib.request


def sign(secret: str, timestamp: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(string_to_sign, b"", digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def build_card(title: str, body: str, doc_url: str | None, github_url: str | None) -> dict:
    elements = [
        {
            "tag": "markdown",
            "content": body[:6000],
        }
    ]
    actions = []
    if doc_url:
        actions.append(
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "Open Feishu Doc"},
                "type": "primary",
                "url": doc_url,
            }
        )
    if github_url:
        actions.append(
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "Open GitHub Digest"},
                "url": github_url,
            }
        )
    if actions:
        elements.append({"tag": "action", "actions": actions})

    return {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "blue",
            },
            "elements": elements,
        },
    }


def post_json(url: str, payload: dict) -> tuple[int, str]:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status, resp.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_file", type=pathlib.Path)
    parser.add_argument("--title", default="AI Coding Daily Update")
    parser.add_argument("--doc-url", default="https://my.feishu.cn/docx/GVk4d22dSo3jEXxst72cRjMfntg")
    parser.add_argument("--github-url", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    body = args.markdown_file.read_text(encoding="utf-8")
    payload = build_card(args.title, body, args.doc_url, args.github_url or None)

    secret = os.environ.get("FEISHU_BOT_SECRET")
    if secret:
        timestamp = str(int(time.time()))
        payload["timestamp"] = timestamp
        payload["sign"] = sign(secret, timestamp)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    webhook = os.environ.get("FEISHU_BOT_WEBHOOK")
    if not webhook:
        raise SystemExit("FEISHU_BOT_WEBHOOK is required unless --dry-run is used")

    status, text = post_json(webhook, payload)
    print(f"HTTP {status}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

