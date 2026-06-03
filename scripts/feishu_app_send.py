#!/usr/bin/env python3
"""
Send a Feishu/Lark bot message through an internal Feishu app.

Required environment variables:
  FEISHU_APP_ID
  FEISHU_APP_SECRET
  FEISHU_RECEIVE_ID

Optional:
  FEISHU_RECEIVE_ID_TYPE: chat_id, open_id, user_id, email, or union_id.
    Defaults to chat_id.

Do not store secrets in this repository. Keep app secrets in local shell
environment, Codex automation secrets, or a deployment secret manager.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import urllib.parse
import urllib.request


FEISHU_BASE = "https://open.feishu.cn/open-apis"


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
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def tenant_access_token(app_id: str, app_secret: str) -> str:
    data = post_json(
        f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    if data.get("code") != 0:
        raise RuntimeError(f"tenant_access_token failed: {data}")
    return data["tenant_access_token"]


def build_card(title: str, body: str, doc_url: str | None, github_url: str | None) -> dict:
    elements: list[dict] = [{"tag": "markdown", "content": body[:6000]}]
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
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_file", type=pathlib.Path)
    parser.add_argument("--title", default="AI Coding Daily Update")
    parser.add_argument("--doc-url", default="https://my.feishu.cn/docx/GVk4d22dSo3jEXxst72cRjMfntg")
    parser.add_argument("--github-url", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    body = args.markdown_file.read_text(encoding="utf-8")
    card = build_card(args.title, body, args.doc_url, args.github_url or None)

    if args.dry_run:
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return 0

    app_id = os.environ["FEISHU_APP_ID"]
    app_secret = os.environ["FEISHU_APP_SECRET"]
    receive_id = os.environ["FEISHU_RECEIVE_ID"]
    receive_id_type = os.environ.get("FEISHU_RECEIVE_ID_TYPE", "chat_id")

    token = tenant_access_token(app_id, app_secret)
    result = send_interactive_message(token, receive_id_type, receive_id, card)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("code") != 0:
        raise SystemExit(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
