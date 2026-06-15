#!/usr/bin/env python3
"""
Retry and track Feishu delivery for daily / weekly AI coding digests.

This guard is intentionally deterministic: it scans recent digest files, sends
missing deliveries recipient by recipient, and records successful message IDs in
an ignored local state file. It prevents one transient Feishu/DNS failure from
silently dropping the daily card.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
DAILY_DIR = ROOT / "data" / "daily_updates"
WEEKLY_DIR = ROOT / "data" / "weekly_updates"
DEFAULT_SUBSCRIBERS = ROOT / "automation" / "feishu_subscribers.local.json"
DEFAULT_STATE = ROOT / "data" / "feishu" / "delivery_state.local.json"
SEND_SCRIPT = ROOT / "scripts" / "feishu_app_send.py"
GITHUB_BASE = "https://github.com/GameScaler/ai_coding_project_survey/blob/main"


@dataclass(frozen=True)
class Recipient:
    name: str
    receive_id_type: str
    receive_id: str

    @property
    def key(self) -> str:
        return f"{self.receive_id_type}:{self.receive_id}"


@dataclass(frozen=True)
class Digest:
    key: str
    kind: str
    label: str
    path: pathlib.Path
    title: str
    github_url: str


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: pathlib.Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def load_subscribers(path: pathlib.Path, subscription: str) -> list[Recipient]:
    data = load_json(path, {"subscribers": []})
    recipients: list[Recipient] = []
    for row in data.get("subscribers", []):
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
                name=row.get("name") or receive_id,
                receive_id_type=row.get("receive_id_type", "chat_id"),
                receive_id=receive_id,
            )
        )
    return recipients


def monday_of_iso_week(year: int, week: int) -> dt.date:
    return dt.date.fromisocalendar(year, week, 1)


def candidate_digests(
    today: dt.date,
    daily_lookback_days: int,
    weekly_lookback_weeks: int,
    only: str,
    label_filter: str | None,
) -> list[Digest]:
    candidates: list[Digest] = []

    if only in {"all", "daily"}:
        start = today - dt.timedelta(days=daily_lookback_days)
        for path in sorted(DAILY_DIR.glob("????-??-??.md")):
            try:
                digest_date = dt.date.fromisoformat(path.stem)
            except ValueError:
                continue
            if start <= digest_date <= today:
                label = digest_date.isoformat()
                if label_filter and label != label_filter:
                    continue
                rel = path.relative_to(ROOT).as_posix()
                candidates.append(
                    Digest(
                        key=f"daily:{label}",
                        kind="daily",
                        label=label,
                        path=path,
                        title=f"AI Coding 产品更新｜{label}",
                        github_url=f"{GITHUB_BASE}/{rel}",
                    )
                )

    if only in {"all", "weekly"}:
        start = today - dt.timedelta(weeks=weekly_lookback_weeks)
        for path in sorted(WEEKLY_DIR.glob("????-W??.md")):
            match = re.fullmatch(r"(\d{4})-W(\d{2})", path.stem)
            if not match:
                continue
            year, week = int(match.group(1)), int(match.group(2))
            try:
                week_start = monday_of_iso_week(year, week)
            except ValueError:
                continue
            week_end = week_start + dt.timedelta(days=6)
            if start <= week_end <= today:
                if label_filter and path.stem != label_filter:
                    continue
                rel = path.relative_to(ROOT).as_posix()
                candidates.append(
                    Digest(
                        key=f"weekly:{path.stem}",
                        kind="weekly",
                        label=path.stem,
                        path=path,
                        title=f"AI Coding 周复盘｜{path.stem}",
                        github_url=f"{GITHUB_BASE}/{rel}",
                    )
                )

    return sorted(candidates, key=lambda item: (item.kind, item.label))


def delivery_record(state: dict[str, Any], digest: Digest) -> dict[str, Any]:
    deliveries = state.setdefault("deliveries", {})
    return deliveries.setdefault(
        digest.key,
        {
            "file": digest.path.relative_to(ROOT).as_posix(),
            "kind": digest.kind,
            "label": digest.label,
            "title": digest.title,
            "github_url": digest.github_url,
            "recipients": {},
        },
    )


def is_closed(state: dict[str, Any], digest: Digest, recipient: Recipient) -> bool:
    record = delivery_record(state, digest)
    recipient_record = record.get("recipients", {}).get(recipient.key, {})
    return recipient_record.get("status") in {"sent", "archived"}


def mark_sent(
    state: dict[str, Any],
    digest: Digest,
    recipient: Recipient,
    message_id: str,
    attempts: int,
) -> None:
    record = delivery_record(state, digest)
    recipients = record.setdefault("recipients", {})
    recipients[recipient.key] = {
        "attempts": attempts,
        "message_id": message_id,
        "name": recipient.name,
        "receive_id_type": recipient.receive_id_type,
        "sent_at": now_iso(),
        "status": "sent",
    }
    record["updated_at"] = now_iso()


def mark_failed(
    state: dict[str, Any],
    digest: Digest,
    recipient: Recipient,
    error: str,
    attempts: int,
) -> None:
    record = delivery_record(state, digest)
    recipients = record.setdefault("recipients", {})
    existing = recipients.get(recipient.key, {})
    recipients[recipient.key] = {
        **existing,
        "attempts": attempts,
        "last_error": error[:1000],
        "last_failed_at": now_iso(),
        "name": recipient.name,
        "receive_id_type": recipient.receive_id_type,
        "status": "failed",
    }
    record["updated_at"] = now_iso()


def mark_archived(state: dict[str, Any], digest: Digest, recipient: Recipient) -> None:
    record = delivery_record(state, digest)
    recipients = record.setdefault("recipients", {})
    recipients[recipient.key] = {
        "archived_at": now_iso(),
        "name": recipient.name,
        "receive_id_type": recipient.receive_id_type,
        "status": "archived",
    }
    record["updated_at"] = now_iso()


def send_once(digest: Digest, recipient: Recipient) -> tuple[bool, str, str]:
    env = os.environ.copy()
    env["FEISHU_RECEIVE_ID"] = recipient.receive_id
    env["FEISHU_RECEIVE_ID_TYPE"] = recipient.receive_id_type
    env["FEISHU_SUBSCRIBER_FILE"] = ""

    result = subprocess.run(
        [
            sys.executable,
            str(SEND_SCRIPT),
            str(digest.path),
            "--title",
            digest.title,
            "--github-url",
            digest.github_url,
            "--subscription",
            digest.kind,
        ],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return False, "", (result.stderr or result.stdout or f"exit={result.returncode}").strip()

    try:
        payload = json.loads(result.stdout)
        row = payload["results"][0]
        api_result = row["result"]
    except Exception as exc:  # noqa: BLE001
        return False, "", f"cannot parse send output: {exc}; output={result.stdout[:500]}"

    if api_result.get("code") != 0:
        return False, "", json.dumps(api_result, ensure_ascii=False)[:1000]

    message_id = api_result.get("data", {}).get("message_id", "")
    return True, message_id, "success"


def send_with_retries(
    digest: Digest,
    recipient: Recipient,
    attempts: int,
    backoff_seconds: int,
) -> tuple[bool, str, str, int]:
    last_error = ""
    for attempt in range(1, attempts + 1):
        ok, message_id, message = send_once(digest, recipient)
        if ok:
            return True, message_id, message, attempt
        last_error = message
        if attempt < attempts:
            time.sleep(backoff_seconds * attempt)
    return False, "", last_error, attempts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subscriber-file", type=pathlib.Path, default=DEFAULT_SUBSCRIBERS)
    parser.add_argument("--state-file", type=pathlib.Path, default=DEFAULT_STATE)
    parser.add_argument("--daily-lookback-days", type=int, default=7)
    parser.add_argument("--weekly-lookback-weeks", type=int, default=3)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--backoff-seconds", type=int, default=20)
    parser.add_argument("--only", choices=["all", "daily", "weekly"], default="all")
    parser.add_argument(
        "--label",
        help="Only deliver one digest label, for example 2026-06-12 or 2026-W24. Useful for precise correction resends.",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--archive-pending",
        action="store_true",
        help="Mark pending historical candidates as closed without sending. Use only when bootstrapping state after manual review/backfill.",
    )
    args = parser.parse_args(argv)

    state = load_json(args.state_file, {"version": 1, "deliveries": {}})
    today = dt.date.today()
    digests = candidate_digests(
        today=today,
        daily_lookback_days=args.daily_lookback_days,
        weekly_lookback_weeks=args.weekly_lookback_weeks,
        only=args.only,
        label_filter=args.label,
    )

    plan = []
    failed = False
    for digest in digests:
        recipients = load_subscribers(args.subscriber_file, digest.kind)
        for recipient in recipients:
            pending = args.force or not is_closed(state, digest, recipient)
            plan.append(
                {
                    "digest": digest.key,
                    "recipient": recipient.name,
                    "pending": pending,
                }
            )
            if args.dry_run or not pending:
                continue

            if args.archive_pending:
                mark_archived(state, digest, recipient)
                write_json(args.state_file, state)
                print(f"ARCHIVED {digest.key} -> {recipient.name}")
                continue

            ok, message_id, message, attempts = send_with_retries(
                digest=digest,
                recipient=recipient,
                attempts=args.attempts,
                backoff_seconds=args.backoff_seconds,
            )
            if ok:
                mark_sent(state, digest, recipient, message_id, attempts)
                write_json(args.state_file, state)
                print(f"SENT {digest.key} -> {recipient.name}: {message_id}")
            else:
                failed = True
                mark_failed(state, digest, recipient, message, attempts)
                write_json(args.state_file, state)
                print(f"FAILED {digest.key} -> {recipient.name}: {message}", file=sys.stderr)

    if args.dry_run:
        print(json.dumps({"plan": plan}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
