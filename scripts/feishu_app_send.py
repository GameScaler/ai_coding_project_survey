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
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass


FEISHU_BASE = "https://open.feishu.cn/open-apis"


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
