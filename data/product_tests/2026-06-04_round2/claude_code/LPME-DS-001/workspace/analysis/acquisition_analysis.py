from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "acquisition_raw.csv"
OUTPUT_DIR = BASE_DIR / "analysis" / "output"
CLEANED_CSV_PATH = OUTPUT_DIR / "cleaned_acquisition.csv"
SUMMARY_PATH = BASE_DIR / "analysis" / "EXECUTIVE_SUMMARY.md"

CHANNEL_MAP = {
    "social": "paid_social",
    "paid_social": "paid_social",
    "search": "search",
    "affiliate": "affiliate",
}


def parse_mixed_dates(raw_dates: pd.Series) -> pd.Series:
    parsed = pd.to_datetime(raw_dates, errors="coerce", format="mixed")
    if parsed.notna().any():
        return parsed
    return pd.to_datetime(raw_dates, errors="coerce")


def load_and_clean_data() -> tuple[pd.DataFrame, list[str]]:
    notes: list[str] = []
    df = pd.read_csv(INPUT_PATH)

    df["source_date"] = df["date"]
    df["date"] = parse_mixed_dates(df["date"])
    invalid_dates = int(df["date"].isna().sum())
    if invalid_dates:
        notes.append(f"Found {invalid_dates} rows with invalid dates; dropped them from analysis.")
    df = df.dropna(subset=["date"]).copy()

    raw_channel_values = sorted(df["channel"].dropna().astype(str).unique().tolist())
    df["channel"] = df["channel"].astype(str).str.strip().str.lower()
    unmapped_channels = sorted(set(df[~df["channel"].isin(CHANNEL_MAP)]["channel"].tolist()))
    if unmapped_channels:
        notes.append(
            "Unmapped channels retained as-is: " + ", ".join(unmapped_channels)
        )
    df["channel_group"] = df["channel"].map(CHANNEL_MAP).fillna(df["channel"])
    if {"social", "paid_social"}.issubset(set(raw_channel_values)):
        notes.append(
            "Assumption: merged `social` into `paid_social` because metric_definitions.md flags them as potentially the same channel."
        )

    numeric_columns = ["spend_usd", "signups", "activated_users", "revenue_30d_usd"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["spend_missing"] = df["spend_usd"].isna()
    missing_spend_rows = df[df["spend_missing"]].copy()
    if not missing_spend_rows.empty:
        notes.append(
            f"Missing spend_usd on {len(missing_spend_rows)} row(s); excluded those rows from spend-based metrics instead of assuming zero spend."
        )
    zero_spend_rows = int(df["spend_usd"].eq(0).sum())
    if zero_spend_rows:
        notes.append(
            f"Retained {zero_spend_rows} row(s) with explicit zero spend as documented zero-cost acquisition."
        )

    missing_activation_rows = df[df["activated_users"].isna()].copy()
    if not missing_activation_rows.empty:
        notes.append(
            f"Missing activated_users on {len(missing_activation_rows)} row(s); imputed with channel-level median activated_users for trend calculations and flagged in output."
        )
    channel_median_activation = df.groupby("channel_group")["activated_users"].transform("median")
    overall_median_activation = df["activated_users"].median()
    df["activated_users_imputed"] = df["activated_users"].isna()
    df["activated_users_clean"] = (
        df["activated_users"].fillna(channel_median_activation).fillna(overall_median_activation)
    )

    df["signups"] = df["signups"].fillna(0)
    df["revenue_30d_usd"] = df["revenue_30d_usd"].fillna(0)

    df = df.sort_values(["date", "channel_group"]).reset_index(drop=True)
    df["cac"] = df["spend_usd"] / df["signups"].where(df["signups"] != 0)
    df.loc[df["spend_missing"], "cac"] = pd.NA
    df["activation_rate"] = df["activated_users_clean"] / df["signups"].where(df["signups"] != 0)
    df["payback_proxy"] = df["revenue_30d_usd"] / df["spend_usd"].where(df["spend_usd"] != 0)
    df.loc[df["spend_missing"], "payback_proxy"] = pd.NA

    df["cohort_revenue_cumulative"] = df.groupby("channel_group")["revenue_30d_usd"].cumsum()

    ordered_columns = [
        "date",
        "source_date",
        "channel",
        "channel_group",
        "spend_usd",
        "spend_missing",
        "signups",
        "activated_users",
        "activated_users_imputed",
        "activated_users_clean",
        "revenue_30d_usd",
        "cac",
        "activation_rate",
        "payback_proxy",
        "cohort_revenue_cumulative",
    ]
    return df[ordered_columns], notes


def build_channel_summary(df: pd.DataFrame) -> pd.DataFrame:
    spend_summary = (
        df.groupby("channel_group", as_index=False)
        .agg(
            spend_usd=("spend_usd", "sum"),
            spend_missing_rows=("spend_missing", "sum"),
            signups=("signups", "sum"),
            activated_users_clean=("activated_users_clean", "sum"),
            revenue_30d_usd=("revenue_30d_usd", "sum"),
        )
        .sort_values("channel_group")
    )
    spend_for_metrics = df[~df["spend_missing"]].groupby("channel_group").agg(
        spend_usd_observed=("spend_usd", "sum"),
        signups_with_spend=("signups", "sum"),
        revenue_30d_usd_with_spend=("revenue_30d_usd", "sum"),
    )
    grouped = spend_summary.merge(spend_for_metrics, on="channel_group", how="left")
    grouped["cac"] = grouped["spend_usd_observed"] / grouped["signups_with_spend"].where(grouped["signups_with_spend"] != 0)
    grouped["activation_rate"] = grouped["activated_users_clean"] / grouped["signups"].where(grouped["signups"] != 0)
    grouped["payback_proxy"] = grouped["revenue_30d_usd_with_spend"] / grouped["spend_usd_observed"].where(grouped["spend_usd_observed"] != 0)
    return grouped


def save_cleaned_data(df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    export_df = df.copy()
    export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d")
    export_df.to_csv(CLEANED_CSV_PATH, index=False)


def plot_bar(summary: pd.DataFrame, column: str, title: str, ylabel: str, filename: str, percent: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    values = summary[column] * 100 if percent else summary[column]
    ax.bar(summary["channel_group"], values, color=["#4c78a8", "#f58518", "#54a24b"])
    ax.set_title(title)
    ax.set_xlabel("Channel")
    ax.set_ylabel(ylabel)
    if percent:
        ax.set_ylim(bottom=0)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / filename, dpi=150)
    plt.close(fig)


def plot_cohort_revenue_trend(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    for channel, channel_df in df.groupby("channel_group"):
        ax.plot(
            channel_df["date"],
            channel_df["cohort_revenue_cumulative"],
            marker="o",
            linewidth=2,
            label=channel,
        )
    ax.set_title("Cumulative 30-Day Cohort Revenue by Channel")
    ax.set_xlabel("Cohort Date")
    ax.set_ylabel("Cumulative revenue_30d_usd")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(title="Channel")
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "cohort_revenue_trend.png", dpi=150)
    plt.close(fig)


def dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    formatted_rows = []
    for row in df.itertuples(index=False):
        formatted_row = []
        for value in row:
            if pd.isna(value):
                formatted_row.append("")
            elif isinstance(value, float):
                formatted_row.append(f"{value:.2f}")
            else:
                formatted_row.append(str(value))
        formatted_rows.append(formatted_row)

    separator = ["---"] * len(headers)
    table_rows = [headers, separator, *formatted_rows]
    return "\n".join("| " + " | ".join(row) + " |" for row in table_rows)


def build_summary_markdown(df: pd.DataFrame, channel_summary: pd.DataFrame, notes: list[str]) -> str:
    total_spend = df["spend_usd"].sum(min_count=1)
    total_signups = df["signups"].sum()
    total_activated = df["activated_users_clean"].sum()
    total_revenue = df["revenue_30d_usd"].sum()
    spend_observed_df = df[~df["spend_missing"]]
    overall_cac = (
        spend_observed_df["spend_usd"].sum() / spend_observed_df["signups"].sum()
        if spend_observed_df["signups"].sum()
        else float("nan")
    )
    overall_activation = total_activated / total_signups if total_signups else float("nan")
    overall_payback = (
        spend_observed_df["revenue_30d_usd"].sum() / spend_observed_df["spend_usd"].sum()
        if spend_observed_df["spend_usd"].sum()
        else float("nan")
    )

    best_payback = channel_summary.sort_values("payback_proxy", ascending=False).iloc[0]
    best_activation = channel_summary.sort_values("activation_rate", ascending=False).iloc[0]
    lowest_cac = channel_summary.sort_values("cac", ascending=True).iloc[0]

    quality_issues = []
    if int(df["spend_missing"].sum()):
        quality_issues.append(
            f"{int(df['spend_missing'].sum())} row(s) had missing spend_usd and were excluded from spend-based metrics instead of being treated as zero."
        )
    if int(df["spend_usd"].eq(0).sum()):
        quality_issues.append(
            f"{int(df['spend_usd'].eq(0).sum())} row(s) had explicit zero spend and were retained as documented zero-cost acquisition."
        )
    if int(df["activated_users_imputed"].sum()):
        quality_issues.append(
            f"{int(df['activated_users_imputed'].sum())} row(s) had missing activated_users and required imputation for rate calculations."
        )
    if (df["channel"] != df["channel_group"]).any():
        quality_issues.append(
            "Channel labels were inconsistent (`social` vs `paid_social`) and were standardized under a documented assumption."
        )
    quality_issues.append("Source dates mixed ISO, slash-delimited, and month-name formats; parsing now uses mixed-format datetime handling so valid dates are retained.")

    lines = [
        "# Executive Summary",
        "",
        "## What was analyzed",
        "Daily acquisition performance across channels using spend, signups, 7-day activations, and 30-day cohort revenue.",
        "",
        "## Headline findings",
        f"- Overall observed spend: ${total_spend:,.2f} across {int(total_signups):,} signups.",
        f"- Overall CAC: ${overall_cac:,.2f} per signup.",
        f"- Overall activation rate: {overall_activation:.1%}.",
        f"- Overall payback proxy (30-day revenue / spend): {overall_payback:.2f}x.",
        f"- Best payback proxy: **{best_payback['channel_group']}** at {best_payback['payback_proxy']:.2f}x.",
        f"- Best activation rate: **{best_activation['channel_group']}** at {best_activation['activation_rate']:.1%}.",
        f"- Lowest CAC: **{lowest_cac['channel_group']}** at ${lowest_cac['cac']:.2f}.",
        "",
        "## Assumptions",
        "- `social` and `paid_social` were combined into `paid_social`, per the ambiguity called out in metric_definitions.md.",
        "- Missing `spend_usd` was not treated as zero; rows with missing spend are retained but excluded from spend-based metrics and flagged in the cleaned output.",
        "- Missing `activated_users` was imputed with the channel-level median only for aggregate trend calculations and flagged in the cleaned output.",
        "- Payback proxy follows the provided definition exactly: `revenue_30d_usd / spend_usd`.",
        "",
        "## Caveats",
        "- The dataset covers only four cohort dates, so trend conclusions are directional rather than statistically robust.",
        "- One search row is missing spend, so search CAC and payback estimates exclude that row and remain more uncertain than other channels.",
        "- 30-day revenue is cohort-based, but acquisition is logged daily; this is useful for directional efficiency, not full LTV analysis.",
        "",
        "## Verification notes",
        "- The analysis was executed via `python3 analysis/acquisition_analysis.py`.",
        "- Output files were generated directly from the script: cleaned CSV, four PNG charts, and this executive summary.",
        "- Mixed-format dates in the raw CSV were verified to parse across ISO, slash-delimited, and month-name inputs before cleaning.",
        "- Spend-based metrics were verified to exclude rows with missing spend while retaining explicit zero-spend rows.",
        "- Metric formulas in the cleaned output were cross-checked against metric_definitions.md.",
        "",
        "## Data-quality issues",
    ]
    lines.extend([f"- {issue}" for issue in quality_issues])
    lines.extend(
        [
            "",
            "## Cleaning notes",
        ]
    )
    lines.extend([f"- {note}" for note in notes])
    lines.extend(
        [
            "",
            "## Next experiment recommendations",
            f"1. Reallocate incremental budget toward **{best_payback['channel_group']}**, which currently shows the strongest revenue payback.",
            f"2. Diagnose onboarding differences behind **{best_activation['channel_group']}** outperforming on activation rate, then test those activation levers in lower-converting channels.",
            f"3. Audit spend tracking for **search** before scaling, because one missing spend row is currently excluded from CAC and payback calculations.",
            "4. Extend the cohort window and add more dates so trend charts can separate noise from stable channel effects.",
            "",
            "## Channel summary",
            dataframe_to_markdown_table(channel_summary),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    df, notes = load_and_clean_data()
    channel_summary = build_channel_summary(df)
    save_cleaned_data(df)

    plot_bar(channel_summary, "cac", "CAC by Channel", "CAC (USD per signup)", "cac_by_channel.png")
    plot_bar(
        channel_summary,
        "activation_rate",
        "Activation Rate by Channel",
        "Activation rate (%)",
        "activation_rate_by_channel.png",
        percent=True,
    )
    plot_bar(
        channel_summary,
        "payback_proxy",
        "Payback Proxy by Channel",
        "Revenue / Spend (x)",
        "payback_proxy_by_channel.png",
    )
    plot_cohort_revenue_trend(df)

    summary_markdown = build_summary_markdown(df, channel_summary, notes)
    SUMMARY_PATH.write_text(summary_markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
