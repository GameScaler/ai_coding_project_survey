#!/usr/bin/env python3
"""
Fetch official AI coding product update pages and generate a lightweight daily digest.

This script intentionally avoids third-party dependencies so it can run in a fresh
workspace. It is a source-gathering helper; a human or Codex automation should add
the product-manager interpretation before publishing.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import html.parser
import argparse
import json
import pathlib
import re
import ssl
import sys
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = ROOT / "automation" / "product_sources.json"
DATA_DIR = ROOT / "data" / "daily_updates"
CACHE_PATH = DATA_DIR / "cache.json"


class TextExtractor(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
        if tag in {"h1", "h2", "h3", "p", "li", "time"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
        if tag in {"h1", "h2", "h3", "p", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            text = data.strip()
            if text:
                self.parts.append(text)

    def text(self) -> str:
        raw = " ".join(self.parts)
        raw = re.sub(r"\s+", " ", raw)
        return raw.strip()


def load_json(path: pathlib.Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def fetch_text(url: str, timeout: int = 20, insecure_ssl: bool = False) -> tuple[str, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ai-coding-product-survey/0.1",
            "Accept": "text/html,application/xhtml+xml,application/xml,text/plain;q=0.9,*/*;q=0.8",
        },
    )
    context = ssl._create_unverified_context() if insecure_ssl else None
    with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
        content_type = resp.headers.get("content-type", "")
        body = resp.read(2_000_000)
    text = body.decode("utf-8", errors="replace")
    if "html" in content_type or "<html" in text[:1000].lower():
        parser = TextExtractor()
        parser.feed(text)
        text = parser.text()
    else:
        text = re.sub(r"\s+", " ", text).strip()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text[:12000], digest


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    lowered = text.lower()
    return [kw for kw in keywords if kw.lower() in lowered]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--insecure-ssl",
        action="store_true",
        help="Disable TLS certificate verification for public changelog scraping. Use only behind trusted corporate proxies.",
    )
    args = parser.parse_args(argv)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    sources = load_json(SOURCES, {})
    cache = load_json(CACHE_PATH, {})
    today = dt.date.today().isoformat()
    report_path = DATA_DIR / f"{today}.md"

    rows = []
    new_cache = dict(cache)

    for product in sources.get("products", []):
        product_rows = []
        for url in product.get("official_sources", []):
            try:
                text, digest = fetch_text(url, insecure_ssl=args.insecure_ssl)
                previous = cache.get(url)
                changed = previous != digest
                new_cache[url] = digest
                hits = keyword_hits(text, product.get("watch_keywords", []))
                excerpt = text[:1200]
                product_rows.append(
                    {
                        "url": url,
                        "changed": changed,
                        "hits": hits,
                        "excerpt": excerpt,
                    }
                )
            except Exception as exc:  # noqa: BLE001
                product_rows.append(
                    {
                        "url": url,
                        "changed": False,
                        "error": str(exc),
                        "hits": [],
                        "excerpt": "",
                    }
                )
        rows.append((product, product_rows))

    lines = [
        f"# AI Coding 每日更新初筛 - {today}",
        "",
        "## Summary",
        "",
        "本文件是机器抓取草稿，只用于归档和人工复核。正式飞书推送必须只保留中文结论、PM 短评和来源链接，不直接推送网页原文摘录。",
        "",
    ]

    any_change = False
    for product, product_rows in rows:
        lines.append(f"## {product['name']}")
        lines.append("")
        changed_rows = [r for r in product_rows if r.get("changed")]
        if changed_rows:
            any_change = True
            lines.append(f"- 初筛状态：发现 {len(changed_rows)} 个官方来源内容变化。")
        else:
            lines.append("- 初筛状态：未发现官方来源内容变化。")
        for row in product_rows:
            lines.append(f"- 来源：{row['url']}")
            if row.get("error"):
                lines.append(f"  - 抓取状态：失败，{row['error']}")
                continue
            lines.append(f"  - 是否变化：{'是' if row['changed'] else '否'}")
            lines.append(f"  - 命中方向：{', '.join(row['hits']) if row['hits'] else '无'}")
        lines.append("")

    lines.insert(5, f"重大更新初筛：{'有变化，需要人工判断重要性' if any_change else '暂无明显变化'}")
    lines.append("## PM Notes")
    lines.append("")
    lines.append("- 今日 PM 短评：TODO")
    lines.append("- 对 TRAE SOLO 的启示：TODO")
    lines.append("- 是否更新 LPME benchmark：TODO")
    lines.append("")

    with CACHE_PATH.open("w", encoding="utf-8") as f:
        json.dump(new_cache, f, ensure_ascii=False, indent=2, sort_keys=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
