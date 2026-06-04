#!/usr/bin/env python3
"""
Create a Feishu/Lark group share link for a chat where the app bot is a member.

Required environment variables:
  FEISHU_APP_ID
  FEISHU_APP_SECRET

The script reads ignored local env files (.env.local / .env) just like
feishu_app_send.py. Do not commit secrets.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
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
    except Exception:
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


def tenant_access_token(app_id: str, app_secret: str) -> str:
    data = post_json(
        f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    if data.get("code") != 0:
        raise RuntimeError(f"tenant_access_token failed: {data}")
    return data["tenant_access_token"]


def create_chat_link(token: str, chat_id: str, validity_period: str) -> dict:
    encoded_chat_id = urllib.parse.quote(chat_id, safe="")
    return post_json(
        f"{FEISHU_BASE}/im/v1/chats/{encoded_chat_id}/link",
        {"validity_period": validity_period},
        token,
    )


def main() -> int:
    load_local_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("chat_id")
    parser.add_argument(
        "--validity-period",
        choices=["week", "year", "permanently"],
        default="permanently",
    )
    args = parser.parse_args()

    token = tenant_access_token(os.environ["FEISHU_APP_ID"], os.environ["FEISHU_APP_SECRET"])
    result = create_chat_link(token, args.chat_id, args.validity_period)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("code") != 0:
        raise SystemExit(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
