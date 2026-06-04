#!/usr/bin/env python3
"""Clean and analyze messy acquisition cohort data.

The script intentionally uses pandas plus standard-library SVG rendering so the
analysis can run in this workspace without optional plotting dependencies.
"""

from __future__ import annotations

import math
from datetime import datetime
from pathlib import Path
from typing import Callable
from xml.sax.saxutils import escape

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "acquisition_raw.csv"
OUTPUT_DIR = ROOT / "analysis" / "output"
SUMMARY_PATH = ROOT / "analysis" / "EXECUTIVE_SUMMARY.md"

CHANNEL_ALIASES = {"social": "paid_social"}
CHANNEL_ORDER = ["search", "paid_social", "affiliate"]
CHANNEL_COLORS = {
    "search": "#276fbf",
    "paid_social": "#c95f3f",
    "affiliate": "#4a8f5a",
    "Total": "#27313b",
}


def parse_dates(date_series: pd.Series) -> pd.Series:
    """Parse intentionally mixed date formats with a documented US month-first assumption."""
    try:
        return pd.to_datetime(
            date_series,
            errors="coerce",
            format="mixed",
            dayfirst=False,
        )
    except TypeError:
        return pd.to_datetime(date_series, errors="coerce", dayfirst=False)


def channel_sort_values(channels: pd.Series) -> pd.Series:
    rank = {channel: i for i, channel in enumerate(CHANNEL_ORDER)}
    return channels.map(lambda value: rank.get(value, len(rank) + sorted(set(channels)).index(value)))


def interpolate_by_channel(df: pd.DataFrame, column: str) -> pd.Series:
    ordered = df.sort_values(["channel", "date", "row_id"]).copy()
    interpolated = ordered.groupby("channel", group_keys=False)[column].transform(
        lambda values: values.interpolate(method="linear", limit_direction="both")
    )
    result = pd.Series(index=ordered.index, data=interpolated)
    return result.reindex(df.index)


def round_half_up(values: pd.Series) -> pd.Series:
    return np.floor(values.astype(float) + 0.5)


def format_money(value: float, decimals: int = 0) -> str:
    if pd.isna(value):
        return "n/a"
    return f"${value:,.{decimals}f}"


def format_pct(value: float) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{value * 100:.1f}%"


def format_ratio(value: float) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{value:.2f}x"


def nice_axis_max(max_value: float) -> float:
    if not math.isfinite(max_value) or max_value <= 0:
        return 1.0
    target = max_value * 1.08
    exponent = math.floor(math.log10(target))
    base = 10**exponent
    for multiplier in [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 7.5, 10]:
        candidate = multiplier * base
        if candidate >= target:
            return candidate
    return 10 * base


def svg_text(
    x: float,
    y: float,
    text: str,
    *,
    size: int = 13,
    weight: int = 400,
    anchor: str = "middle",
    fill: str = "#27313b",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}">{escape(text)}</text>'
    )


def make_bar_chart(
    values: dict[str, float],
    output_path: Path,
    *,
    title: str,
    subtitle: str,
    value_formatter: Callable[[float], str],
) -> None:
    width, height = 900, 520
    left, right, top, bottom_margin = 96, 36, 86, 92
    bottom = height - bottom_margin
    plot_width = width - left - right
    plot_height = bottom - top
    items = [(label, value) for label, value in values.items() if pd.notna(value)]
    y_max = nice_axis_max(max(value for _, value in items)) if items else 1

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(left, 34, title, size=22, weight=700, anchor="start"),
        svg_text(left, 58, subtitle, size=13, anchor="start", fill="#596572"),
    ]

    for tick in range(6):
        value = y_max * tick / 5
        y = bottom - (value / y_max) * plot_height
        stroke = "#d9dee5" if tick else "#9aa4af"
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" stroke="{stroke}" stroke-width="1"/>')
        parts.append(svg_text(left - 12, y + 4, value_formatter(value), size=12, anchor="end", fill="#596572"))

    if items:
        slot = plot_width / len(items)
        bar_width = min(130, slot * 0.52)
        for index, (label, value) in enumerate(items):
            x_center = left + slot * index + slot / 2
            bar_height = (value / y_max) * plot_height
            x = x_center - bar_width / 2
            y = bottom - bar_height
            color = CHANNEL_COLORS.get(label, "#596572")
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" '
                f'fill="{color}" rx="4"/>'
            )
            parts.append(svg_text(x_center, y - 10, value_formatter(value), size=13, weight=700))
            parts.append(svg_text(x_center, bottom + 28, label, size=13, weight=700))

    parts.extend(
        [
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#9aa4af" stroke-width="1"/>',
            f'<line x1="{left}" y1="{bottom}" x2="{width - right}" y2="{bottom}" stroke="#9aa4af" stroke-width="1"/>',
            "</svg>",
        ]
    )
    output_path.write_text("\n".join(parts), encoding="utf-8")


def make_line_chart(
    dates: list[pd.Timestamp],
    series: dict[str, list[float]],
    output_path: Path,
    *,
    title: str,
    subtitle: str,
    value_formatter: Callable[[float], str],
) -> None:
    width, height = 980, 560
    left, right, top, bottom_margin = 96, 170, 88, 84
    bottom = height - bottom_margin
    plot_width = width - left - right
    plot_height = bottom - top
    all_values = [value for values in series.values() for value in values if pd.notna(value)]
    y_max = nice_axis_max(max(all_values)) if all_values else 1
    x_step = plot_width / max(len(dates) - 1, 1)

    def point_x(index: int) -> float:
        return left + index * x_step if len(dates) > 1 else left + plot_width / 2

    def point_y(value: float) -> float:
        return bottom - (value / y_max) * plot_height

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        svg_text(left, 34, title, size=22, weight=700, anchor="start"),
        svg_text(left, 58, subtitle, size=13, anchor="start", fill="#596572"),
    ]

    for tick in range(6):
        value = y_max * tick / 5
        y = bottom - (value / y_max) * plot_height
        stroke = "#d9dee5" if tick else "#9aa4af"
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" stroke="{stroke}" stroke-width="1"/>')
        parts.append(svg_text(left - 12, y + 4, value_formatter(value), size=12, anchor="end", fill="#596572"))

    for index, date in enumerate(dates):
        x = point_x(index)
        parts.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" stroke="#edf0f3" stroke-width="1"/>')
        parts.append(svg_text(x, bottom + 30, date.strftime("%b %d"), size=12, fill="#596572"))

    for label, values in series.items():
        color = CHANNEL_COLORS.get(label, "#596572")
        width_attr = 3 if label == "Total" else 2
        points = " ".join(f"{point_x(i):.1f},{point_y(value):.1f}" for i, value in enumerate(values))
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="{width_attr}" stroke-linejoin="round"/>')
        for i, value in enumerate(values):
            parts.append(f'<circle cx="{point_x(i):.1f}" cy="{point_y(value):.1f}" r="4" fill="{color}"/>')

    legend_x = width - right + 28
    legend_y = top + 6
    for offset, label in enumerate(series.keys()):
        y = legend_y + offset * 26
        color = CHANNEL_COLORS.get(label, "#596572")
        parts.append(f'<line x1="{legend_x}" y1="{y}" x2="{legend_x + 22}" y2="{y}" stroke="{color}" stroke-width="3"/>')
        parts.append(svg_text(legend_x + 30, y + 4, label, size=13, anchor="start"))

    parts.extend(
        [
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#9aa4af" stroke-width="1"/>',
            f'<line x1="{left}" y1="{bottom}" x2="{width - right}" y2="{bottom}" stroke="#9aa4af" stroke-width="1"/>',
            "</svg>",
        ]
    )
    output_path.write_text("\n".join(parts), encoding="utf-8")


def clean_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(RAW_PATH, dtype=str, keep_default_na=False)
    raw.insert(0, "row_id", range(1, len(raw) + 1))

    df = raw.copy()
    df["date_raw"] = df["date"].astype(str)
    df["date"] = parse_dates(df["date_raw"].str.strip())
    df["date_parse_failed"] = df["date"].isna()

    df["channel_raw"] = df["channel"].astype(str).str.strip()
    df["channel"] = df["channel_raw"].str.lower().replace(CHANNEL_ALIASES)
    df["channel_was_normalized"] = df["channel_raw"].str.lower() != df["channel"]

    for column in ["spend_usd", "signups", "activated_users", "revenue_30d_usd"]:
        df[f"{column}_raw"] = df[column].replace("", pd.NA)
        df[column] = pd.to_numeric(df[column].replace("", pd.NA), errors="coerce")

    df["spend_usd_was_missing"] = df["spend_usd"].isna()
    spend_interpolated = interpolate_by_channel(df, "spend_usd")
    spend_global_median = df["spend_usd"].median(skipna=True)
    df["spend_usd_imputation_method"] = ""
    df.loc[df["spend_usd_was_missing"] & spend_interpolated.notna(), "spend_usd_imputation_method"] = (
        "linear_interpolation_within_channel"
    )
    df.loc[df["spend_usd_was_missing"] & spend_interpolated.isna(), "spend_usd_imputation_method"] = (
        "global_median_fallback"
    )
    df["spend_usd"] = df["spend_usd"].fillna(spend_interpolated).fillna(spend_global_median)

    df["activated_users_was_missing"] = df["activated_users"].isna()
    activated_interpolated = interpolate_by_channel(df, "activated_users")
    activation_rate_median = (df["activated_users"] / df["signups"]).median(skipna=True)
    activated_fallback = df["signups"] * activation_rate_median
    activated_imputed = activated_interpolated.fillna(activated_fallback)
    df["activated_users_imputation_method"] = ""
    df.loc[
        df["activated_users_was_missing"] & activated_interpolated.notna(),
        "activated_users_imputation_method",
    ] = "linear_interpolation_within_channel_rounded"
    df.loc[
        df["activated_users_was_missing"] & activated_interpolated.isna(),
        "activated_users_imputation_method",
    ] = "median_activation_rate_fallback_rounded"
    df["activated_users"] = df["activated_users"].fillna(round_half_up(activated_imputed))
    df["activated_users"] = df[["activated_users", "signups"]].min(axis=1)

    df["cac"] = np.where(df["signups"] > 0, df["spend_usd"] / df["signups"], np.nan)
    df["activation_rate"] = np.where(df["signups"] > 0, df["activated_users"] / df["signups"], np.nan)
    df["payback_proxy"] = np.where(df["spend_usd"] > 0, df["revenue_30d_usd"] / df["spend_usd"], np.nan)
    df["payback_proxy_undefined_reason"] = np.where(df["spend_usd"] == 0, "zero_spend", "")

    def row_notes(row: pd.Series) -> str:
        notes: list[str] = []
        if row["date_parse_failed"]:
            notes.append("date_parse_failed")
        if row["channel_was_normalized"]:
            notes.append("channel_normalized_from_social")
        if row["spend_usd_was_missing"]:
            notes.append(f"spend_imputed:{row['spend_usd_imputation_method']}")
        if row["activated_users_was_missing"]:
            notes.append(f"activated_users_imputed:{row['activated_users_imputation_method']}")
        if row["spend_usd"] == 0:
            notes.append("zero_spend_payback_undefined")
        return "; ".join(notes)

    df["data_quality_notes"] = df.apply(row_notes, axis=1)
    df["channel_sort"] = channel_sort_values(df["channel"])
    df = df.sort_values(["date", "channel_sort", "row_id"]).drop(columns=["channel_sort"]).reset_index(drop=True)

    quality = pd.DataFrame(
        [
            {
                "check": "raw_row_count",
                "count": len(raw),
                "handling": "cleaned output preserves one row per raw cohort row",
            },
            {
                "check": "unparsed_dates",
                "count": int(df["date_parse_failed"].sum()),
                "handling": "mixed-format parser with month-first assumption for slash dates",
            },
            {
                "check": "normalized_channel_rows",
                "count": int(df["channel_was_normalized"].sum()),
                "handling": "mapped social to paid_social",
            },
            {
                "check": "missing_spend_rows",
                "count": int(df["spend_usd_was_missing"].sum()),
                "handling": "imputed with within-channel linear interpolation when possible",
            },
            {
                "check": "missing_activated_users_rows",
                "count": int(df["activated_users_was_missing"].sum()),
                "handling": "imputed with within-channel linear interpolation and rounded",
            },
            {
                "check": "zero_spend_rows",
                "count": int((df["spend_usd"] == 0).sum()),
                "handling": "left spend at zero; row-level payback_proxy set to blank/undefined",
            },
        ]
    )
    return df, quality


def summarize_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("channel", as_index=False)
        .agg(
            rows=("row_id", "count"),
            spend_usd=("spend_usd", "sum"),
            signups=("signups", "sum"),
            activated_users=("activated_users", "sum"),
            revenue_30d_usd=("revenue_30d_usd", "sum"),
            missing_spend_rows=("spend_usd_was_missing", "sum"),
            missing_activated_users_rows=("activated_users_was_missing", "sum"),
            zero_spend_rows=("spend_usd", lambda values: int((values == 0).sum())),
        )
        .assign(
            cac=lambda data: data["spend_usd"] / data["signups"],
            activation_rate=lambda data: data["activated_users"] / data["signups"],
            payback_proxy=lambda data: data["revenue_30d_usd"] / data["spend_usd"],
        )
    )

    nonzero = (
        df[df["spend_usd"] > 0]
        .groupby("channel")
        .agg(nonzero_revenue_30d_usd=("revenue_30d_usd", "sum"), nonzero_spend_usd=("spend_usd", "sum"))
    )
    nonzero["payback_proxy_excluding_zero_spend_rows"] = (
        nonzero["nonzero_revenue_30d_usd"] / nonzero["nonzero_spend_usd"]
    )
    summary = summary.join(nonzero["payback_proxy_excluding_zero_spend_rows"], on="channel")
    summary["channel_sort"] = channel_sort_values(summary["channel"])
    return summary.sort_values("channel_sort").drop(columns=["channel_sort"]).reset_index(drop=True)


def write_cleaned_outputs(df: pd.DataFrame, quality: pd.DataFrame, channel_summary: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cleaned = df.copy()
    cleaned["date"] = cleaned["date"].dt.strftime("%Y-%m-%d")
    ordered_columns = [
        "row_id",
        "date_raw",
        "date",
        "channel_raw",
        "channel",
        "channel_was_normalized",
        "spend_usd_raw",
        "spend_usd",
        "spend_usd_was_missing",
        "spend_usd_imputation_method",
        "signups",
        "activated_users_raw",
        "activated_users",
        "activated_users_was_missing",
        "activated_users_imputation_method",
        "revenue_30d_usd",
        "cac",
        "activation_rate",
        "payback_proxy",
        "payback_proxy_undefined_reason",
        "data_quality_notes",
    ]
    cleaned = cleaned[ordered_columns]
    for column in ["spend_usd", "cac", "activation_rate", "payback_proxy"]:
        cleaned[column] = cleaned[column].round(4)
    cleaned["activated_users"] = cleaned["activated_users"].round(0).astype("Int64")
    cleaned.to_csv(OUTPUT_DIR / "cleaned_acquisition.csv", index=False)

    summary_out = channel_summary.copy()
    for column in ["spend_usd", "revenue_30d_usd", "cac", "activation_rate", "payback_proxy", "payback_proxy_excluding_zero_spend_rows"]:
        summary_out[column] = summary_out[column].round(4)
    summary_out.to_csv(OUTPUT_DIR / "channel_summary.csv", index=False)
    quality.to_csv(OUTPUT_DIR / "data_quality_report.csv", index=False)


def write_charts(df: pd.DataFrame, channel_summary: pd.DataFrame) -> list[Path]:
    chart_paths = [
        OUTPUT_DIR / "cac_by_channel.svg",
        OUTPUT_DIR / "activation_rate_by_channel.svg",
        OUTPUT_DIR / "payback_proxy_by_channel.svg",
        OUTPUT_DIR / "cohort_revenue_trend.svg",
    ]

    summary_index = channel_summary.set_index("channel")
    ordered_channels = list(channel_summary["channel"])
    make_bar_chart(
        {channel: summary_index.loc[channel, "cac"] for channel in ordered_channels},
        chart_paths[0],
        title="CAC by Channel",
        subtitle="Total cleaned spend divided by total signups",
        value_formatter=lambda value: format_money(value, decimals=2),
    )
    make_bar_chart(
        {channel: summary_index.loc[channel, "activation_rate"] for channel in ordered_channels},
        chart_paths[1],
        title="Activation Rate by Channel",
        subtitle="Activated users within 7 days divided by signups",
        value_formatter=format_pct,
    )
    make_bar_chart(
        {channel: summary_index.loc[channel, "payback_proxy"] for channel in ordered_channels},
        chart_paths[2],
        title="Payback Proxy by Channel",
        subtitle="Total 30-day cohort revenue divided by total cleaned spend",
        value_formatter=format_ratio,
    )

    daily = (
        df.pivot_table(
            index="date",
            columns="channel",
            values="revenue_30d_usd",
            aggfunc="sum",
            fill_value=0,
        )
        .sort_index()
    )
    daily["Total"] = daily.sum(axis=1)
    dates = [pd.Timestamp(value) for value in daily.index]
    series: dict[str, list[float]] = {"Total": daily["Total"].astype(float).tolist()}
    for channel in ordered_channels:
        series[channel] = daily[channel].astype(float).tolist()

    make_line_chart(
        dates,
        series,
        chart_paths[3],
        title="Cohort Revenue Trend",
        subtitle="30-day revenue by signup cohort date after channel normalization",
        value_formatter=lambda value: format_money(value, decimals=0),
    )

    daily.reset_index().to_csv(OUTPUT_DIR / "daily_revenue_trend.csv", index=False)
    return chart_paths


def write_executive_summary(
    df: pd.DataFrame,
    quality: pd.DataFrame,
    channel_summary: pd.DataFrame,
    chart_paths: list[Path],
) -> None:
    summary = channel_summary.set_index("channel")
    daily_total = df.groupby("date")["revenue_30d_usd"].sum().sort_index()
    start_date = daily_total.index.min().strftime("%Y-%m-%d")
    end_date = daily_total.index.max().strftime("%Y-%m-%d")
    start_revenue = float(daily_total.iloc[0])
    end_revenue = float(daily_total.iloc[-1])
    revenue_change = (end_revenue / start_revenue - 1) if start_revenue else np.nan

    search = summary.loc["search"]
    paid_social = summary.loc["paid_social"]
    affiliate = summary.loc["affiliate"]

    quality_counts = quality.set_index("check")["count"].to_dict()
    chart_list = "\n".join(f"- `{path.relative_to(ROOT)}`" for path in chart_paths)

    markdown = f"""# Executive Summary: Acquisition Cohorts

## Scope

Analyzed `{RAW_PATH.name}` daily signup cohorts from {start_date} through {end_date}. The cleaned dataset preserves {len(df)} raw cohort rows and writes derived metrics to `analysis/output/cleaned_acquisition.csv`.

## Assumptions and Metric Decisions

- Slash dates are parsed month-first, so `01/02/2026` is treated as January 2, 2026.
- `social` and `paid_social` are treated as the same channel and normalized to `paid_social`.
- The missing search spend on 2026-01-03 is imputed with within-channel linear interpolation: {format_money(df.loc[df["spend_usd_was_missing"], "spend_usd"].iloc[0], decimals=0)}.
- The missing affiliate activation count on 2026-01-03 is imputed with within-channel linear interpolation and rounded: {int(df.loc[df["activated_users_was_missing"], "activated_users"].iloc[0])} users.
- Row-level payback proxy is undefined when spend is zero. The by-channel payback chart uses total 30-day revenue divided by total cleaned spend, so the affiliate value should be read with the zero-spend caveat.

## Cohort Trends

- Search produced the most 30-day revenue at {format_money(search["revenue_30d_usd"], decimals=0)} and ended at the highest daily cohort revenue ({format_money(df[(df["date"] == daily_total.index.max()) & (df["channel"] == "search")]["revenue_30d_usd"].sum(), decimals=0)} on {end_date}). Its CAC is {format_money(search["cac"], decimals=2)}, activation rate is {format_pct(search["activation_rate"])}, and payback proxy is {format_ratio(search["payback_proxy"])}.
- Paid social has the weakest efficiency in this sample: CAC {format_money(paid_social["cac"], decimals=2)}, activation rate {format_pct(paid_social["activation_rate"])}, and payback proxy {format_ratio(paid_social["payback_proxy"])}. It is below 1.0x 30-day payback.
- Affiliate shows the lowest CAC ({format_money(affiliate["cac"], decimals=2)}) and highest activation rate ({format_pct(affiliate["activation_rate"])}). Its aggregate payback proxy is {format_ratio(affiliate["payback_proxy"])}, but excluding the zero-spend row lowers it to {format_ratio(affiliate["payback_proxy_excluding_zero_spend_rows"])}.
- Total cohort revenue moved from {format_money(start_revenue, decimals=0)} on {start_date} to {format_money(end_revenue, decimals=0)} on {end_date} ({format_pct(revenue_change)}), with a dip on 2026-01-03 before rebounding on 2026-01-04.

## Data Quality Issues and Caveats

- Mixed date formats found: ISO, slash-delimited, and month-name strings.
- Normalized channel alias rows: {quality_counts["normalized_channel_rows"]}.
- Missing spend rows: {quality_counts["missing_spend_rows"]}; this was imputed rather than treated as zero.
- Missing activated-user rows: {quality_counts["missing_activated_users_rows"]}; this was imputed and rounded to a whole user count.
- Zero-spend rows with revenue: {quality_counts["zero_spend_rows"]}; row-level payback is undefined and aggregate payback may overstate efficiency if this is a tracking issue.
- The sample covers only four cohort days, so these are directional trends rather than stable channel benchmarks.

## Next Experiment Recommendations

- Audit the affiliate zero-spend row and require spend-source validation before using affiliate payback for budget allocation.
- Run a paid-social activation experiment focused on the post-signup onboarding step, since activation trails other channels by more than 10 percentage points.
- Increase search budget in a controlled holdout or geo-split test to confirm whether the high January 4 revenue cohort repeats without degrading CAC.
- Add ETL checks for parseable dates, known channel names, missing spend, missing activation counts, and spend-zero/revenue-positive rows.

## Verification Notes

- Executed `python3 analysis/acquisition_analysis.py`.
- Verified the cleaned output row count matches the raw row count: {len(df)} rows.
- Verified unparsed date count is {quality_counts["unparsed_dates"]}.
- Generated charts:
{chart_list}
"""

    SUMMARY_PATH.write_text(markdown, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cleaned, quality = clean_data()
    channel_summary = summarize_by_channel(cleaned)

    write_cleaned_outputs(cleaned, quality, channel_summary)
    chart_paths = write_charts(cleaned, channel_summary)
    write_executive_summary(cleaned, quality, channel_summary, chart_paths)

    assert len(cleaned) == len(pd.read_csv(RAW_PATH)), "cleaned row count does not match raw row count"
    assert int(cleaned["date_parse_failed"].sum()) == 0, "one or more dates failed to parse"
    for chart_path in chart_paths:
        assert chart_path.exists() and chart_path.stat().st_size > 500, f"chart missing or empty: {chart_path}"

    print(f"Wrote {OUTPUT_DIR / 'cleaned_acquisition.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'channel_summary.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'data_quality_report.csv'}")
    print(f"Wrote {SUMMARY_PATH}")
    for chart_path in chart_paths:
        print(f"Wrote {chart_path}")
    print(f"Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
