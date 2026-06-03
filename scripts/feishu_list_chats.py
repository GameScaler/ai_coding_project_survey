#!/usr/bin/env python3
"""
List Feishu chats visible to the internal app bot.

Use this after the app bot has been enabled, approved, and added to the target
subscription group. It prints chat IDs that can be used as FEISHU_RECEIVE_ID.
Secrets must stay in local environment variables or ignored .env files.
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


FEISHU_BASE = "https://open.feishu.cn/open-apis"


def load_local_env() -> None:
    for path in (pathlib.Path(".env.local"), pathlib.Path(".env")):
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def request_json(method: str, url: str, payload: dict | None = None, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        if "CERTIFICATE_VERIFY_FAILED" not in str(exc):
            raise
        return request_json_with_curl(method, url, payload, token)


def request_json_with_curl(method: str, url: str, payload: dict | None, token: str | None) -> dict:
    cmd = [
        "curl",
        "--silent",
        "--show-error",
        "--fail-with-body",
        "--max-time",
        "20",
        "--request",
        method,
        "--header",
        "Content-Type: application/json; charset=utf-8",
    ]
    if token:
        cmd.extend(["--header", f"Authorization: Bearer {token}"])
    input_data = None
    if payload is not None:
        cmd.extend(["--data-binary", "@-"])
        input_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    cmd.append(url)
    result = subprocess.run(
        cmd,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8") or result.stdout.decode("utf-8"))
    return json.loads(result.stdout.decode("utf-8"))


def tenant_access_token(app_id: str, app_secret: str) -> str:
    data = request_json(
        "POST",
        f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    if data.get("code") != 0:
        raise RuntimeError(f"tenant_access_token failed: {data}")
    return data["tenant_access_token"]


def list_chats(token: str, page_size: int, limit: int) -> list[dict]:
    items: list[dict] = []
    page_token = ""
    while True:
        query = {"page_size": str(page_size)}
        if page_token:
            query["page_token"] = page_token
        url = f"{FEISHU_BASE}/im/v1/chats?{urllib.parse.urlencode(query)}"
        data = request_json("GET", url, token=token)
        if data.get("code") != 0:
            raise RuntimeError(f"list chats failed: {data}")
        body = data.get("data", {})
        items.extend(body.get("items", []))
        if len(items) >= limit:
            return items[:limit]
        if not body.get("has_more"):
            return items
        page_token = body.get("page_token") or ""
        if not page_token:
            return items


def main() -> int:
    load_local_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    token = tenant_access_token(os.environ["FEISHU_APP_ID"], os.environ["FEISHU_APP_SECRET"])
    chats = list_chats(token, args.page_size, args.limit)

    if args.json:
        print(json.dumps({"items": chats}, ensure_ascii=False, indent=2))
        return 0

    for chat in chats:
        print(
            "\t".join(
                [
                    chat.get("chat_id", ""),
                    chat.get("name", ""),
                    chat.get("chat_type", ""),
                    str(chat.get("member_count", "")),
                ]
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
