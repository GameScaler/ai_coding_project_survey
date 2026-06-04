#!/usr/bin/env python3
"""Acquisition cohort analysis: clean raw data and produce metric charts."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

WORKSPACE = Path(__file__).resolve().parents[1]
RAW_PATH = WORKSPACE / "acquisition_raw.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
CLEANED_PATH = OUTPUT_DIR / "cleaned_acquisition.csv"
QUALITY_REPORT_PATH = OUTPUT_DIR / "data_quality_report.json"

# Map legacy channel labels to a single paid-social bucket (documented in EXECUTIVE_SUMMARY).
CHANNEL_ALIASES = {"social": "paid_social"}


def parse_dates(series: pd.Series) -> pd.Series:
    """Parse heterogeneous date strings into normalized datetime."""
    return pd.to_datetime(series, format="mixed", dayfirst=False)


def clean_raw(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Clean acquisition data; return frame and quality metadata."""
    issues: list[dict] = []
    out = df.copy()

    out["date_raw"] = out["date"].astype(str)
    parsed = parse_dates(out["date"])
    unparseable = parsed.isna() & out["date"].notna()
    if unparseable.any():
        for idx in out.index[unparseable]:
            issues.append({"row": int(idx), "field": "date", "issue": "unparseable_date"})
    out["date"] = parsed.dt.strftime("%Y-%m-%d")

    out["channel_raw"] = out["channel"].astype(str)
    remapped = out["channel"].isin(CHANNEL_ALIASES.keys())
    out["channel"] = out["channel"].replace(CHANNEL_ALIASES)
    for idx in out.index[remapped]:
        issues.append(
            {
                "row": int(idx),
                "field": "channel",
                "issue": "channel_alias_applied",
                "from": out.loc[idx, "channel_raw"],
                "to": out.loc[idx, "channel"],
            }
        )

    numeric_cols = ["spend_usd", "signups", "activated_users", "revenue_30d_usd"]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    for col in numeric_cols:
        missing = out[col].isna()
        for idx in out.index[missing]:
            issues.append({"row": int(idx), "field": col, "issue": "missing_value"})

    # spend_usd == 0 is explicit zero spend (e.g. affiliate row); do not impute missing spend.
    out["spend_missing"] = out["spend_usd"].isna()
    out["activated_missing"] = out["activated_users"].isna()

    out["cac_usd"] = out.apply(
        lambda r: r["spend_usd"] / r["signups"]
        if pd.notna(r["spend_usd"]) and pd.notna(r["signups"]) and r["signups"] > 0
        else pd.NA,
        axis=1,
    )
    out["activation_rate"] = out.apply(
        lambda r: r["activated_users"] / r["signups"]
        if pd.notna(r["activated_users"]) and pd.notna(r["signups"]) and r["signups"] > 0
        else pd.NA,
        axis=1,
    )
    out["payback_proxy"] = out.apply(
        lambda r: r["revenue_30d_usd"] / r["spend_usd"]
        if pd.notna(r["revenue_30d_usd"])
        and pd.notna(r["spend_usd"])
        and r["spend_usd"] > 0
        else pd.NA,
        axis=1,
    )

    quality = {
        "source_rows": len(df),
        "cleaned_rows": len(out),
        "issues": issues,
        "rows_excluded_from_cac": int(out["cac_usd"].isna().sum()),
        "rows_excluded_from_payback": int(out["payback_proxy"].isna().sum()),
        "rows_excluded_from_activation_rate": int(out["activation_rate"].isna().sum()),
    }
    return out, quality


def aggregate_by_date_channel(df: pd.DataFrame) -> pd.DataFrame:
    """Roll up to one row per date × channel (sum counts, recompute rates)."""
    rows: list[dict] = []
    for (date, channel), grp in df.groupby(["date", "channel"], sort=False):
        spend_missing = bool(grp["spend_missing"].any())
        activated_missing = bool(grp["activated_missing"].any())
        spend = pd.NA if spend_missing or grp["spend_usd"].isna().any() else grp["spend_usd"].sum()
        activated = (
            pd.NA
            if activated_missing or grp["activated_users"].isna().any()
            else grp["activated_users"].sum()
        )
        signups = grp["signups"].sum()
        revenue = grp["revenue_30d_usd"].sum()

        row = {
            "date": date,
            "channel": channel,
            "spend_usd": spend,
            "signups": signups,
            "activated_users": activated,
            "revenue_30d_usd": revenue,
            "spend_missing": spend_missing,
            "activated_missing": activated_missing,
        }
        if pd.notna(spend) and signups > 0:
            row["cac_usd"] = spend / signups
        else:
            row["cac_usd"] = pd.NA
        if pd.notna(activated) and signups > 0:
            row["activation_rate"] = activated / signups
        else:
            row["activation_rate"] = pd.NA
        if pd.notna(spend) and pd.notna(revenue) and spend > 0:
            row["payback_proxy"] = revenue / spend
        else:
            row["payback_proxy"] = pd.NA
        rows.append(row)

    return pd.DataFrame(rows).sort_values(["date", "channel"])


def plot_metric(
    df: pd.DataFrame,
    metric_col: str,
    title: str,
    ylabel: str,
    filename: str,
    as_percent: bool = False,
) -> None:
    """Line chart by channel over date."""
    plot_df = df.dropna(subset=[metric_col]).copy()
    if plot_df.empty:
        return

    plot_df["date_dt"] = pd.to_datetime(plot_df["date"])
    channels = sorted(plot_df["channel"].unique())

    fig, ax = plt.subplots(figsize=(10, 5))
    for channel in channels:
        sub = plot_df[plot_df["channel"] == channel].sort_values("date_dt")
        y = sub[metric_col]
        if as_percent:
            y = y * 100
        ax.plot(sub["date_dt"], y, marker="o", label=channel)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    ax.legend(title="Channel")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / filename, dpi=150)
    plt.close(fig)


def plot_cohort_revenue(df: pd.DataFrame) -> None:
    """Stacked area of 30d revenue by channel over cohort signup date."""
    plot_df = df.dropna(subset=["revenue_30d_usd"]).copy()
    plot_df["date_dt"] = pd.to_datetime(plot_df["date"])
    pivot = (
        plot_df.pivot_table(
            index="date_dt", columns="channel", values="revenue_30d_usd", aggfunc="sum"
        )
        .sort_index()
        .fillna(0)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.stackplot(
        pivot.index,
        [pivot[c] for c in pivot.columns],
        labels=pivot.columns,
        alpha=0.85,
    )
    ax.set_title("Cohort 30-Day Revenue Trend by Channel")
    ax.set_xlabel("Cohort date")
    ax.set_ylabel("Revenue (USD)")
    ax.legend(title="Channel", loc="upper left")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "cohort_revenue_trend.png", dpi=150)
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(RAW_PATH)
    cleaned, quality = clean_raw(raw)
    cleaned.to_csv(CLEANED_PATH, index=False)

    agg = aggregate_by_date_channel(cleaned)
    agg.to_csv(OUTPUT_DIR / "daily_channel_metrics.csv", index=False)

    with open(QUALITY_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(quality, f, indent=2)

    plot_metric(
        agg,
        "cac_usd",
        "Customer Acquisition Cost (CAC) by Channel",
        "CAC (USD per signup)",
        "cac_by_channel.png",
    )
    plot_metric(
        agg,
        "activation_rate",
        "Activation Rate by Channel",
        "Activation rate (%)",
        "activation_rate_by_channel.png",
        as_percent=True,
    )
    plot_metric(
        agg,
        "payback_proxy",
        "30-Day Payback Proxy by Channel",
        "Revenue / spend (ratio)",
        "payback_proxy_by_channel.png",
    )
    plot_cohort_revenue(agg)

    print(f"Wrote {CLEANED_PATH}")
    print(f"Quality issues logged: {len(quality['issues'])}")
    print("Charts:", ", ".join(p.name for p in sorted(OUTPUT_DIR.glob("*.png"))))


if __name__ == "__main__":
    main()
