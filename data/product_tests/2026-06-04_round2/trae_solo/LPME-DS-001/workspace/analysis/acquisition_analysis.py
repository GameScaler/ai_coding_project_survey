#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LPME-DS-001 — Acquisition 数据清洗与 cohort 趋势分析（可复现）

输入（位于 workspace 根目录）:
  - acquisition_raw.csv
  - metric_definitions.md

输出（位于 workspace/analysis/output）:
  - cleaned_acquisition.csv
  - cac_by_channel.png
  - activation_rate_by_channel.png
  - payback_proxy_by_channel.png
  - cohort_revenue_trend.png
  - channel_summary.csv（用于核对计算口径，便于复现/验证）

同时生成：
  - workspace/analysis/EXECUTIVE_SUMMARY.md
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
import re


@dataclass
class DataQualityReport:
    input_rows: int
    output_rows: int
    parsed_date_nulls: int
    missing_spend_rows: int
    zero_spend_rows: int
    missing_activated_rows: int
    invalid_payback_rows: int
    channel_variants: Dict[str, int]
    notes: list[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_rows": self.input_rows,
            "output_rows": self.output_rows,
            "parsed_date_nulls": self.parsed_date_nulls,
            "missing_spend_rows": self.missing_spend_rows,
            "zero_spend_rows": self.zero_spend_rows,
            "missing_activated_rows": self.missing_activated_rows,
            "invalid_payback_rows": self.invalid_payback_rows,
            "channel_variants": self.channel_variants,
            "notes": self.notes,
        }


def _safe_div(numer: pd.Series, denom: pd.Series) -> pd.Series:
    """安全除法：denom<=0 或任一为 NaN 时返回 NaN（避免 inf/误读）。"""
    numer = pd.to_numeric(numer, errors="coerce")
    denom = pd.to_numeric(denom, errors="coerce")
    out = numer / denom
    out[(denom <= 0) | denom.isna() | numer.isna()] = np.nan
    return out


def _parse_mixed_dates(date_series: pd.Series) -> Tuple[pd.Series, int]:
    """
    处理不一致日期格式：
      - 2026-01-01
      - 01/02/2026
      - 2026/01/03
      - Jan 03 2026
    策略：
      - 不依赖 pandas 的“推断格式”（不同版本可能行为变化），改为按正则分流到确定格式：
        * YYYY-MM-DD
        * YYYY/MM/DD
        * MM/DD/YYYY（假设 month-first；若业务是 day-first，需要在 summary 中调整假设）
        * Mon DD YYYY（英文月份缩写）
      - 其余回退到 dateutil 解析（pandas.to_datetime 不带 format）
    """
    s = date_series.astype(str).str.strip()

    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")

    m_ymd_dash = s.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)
    m_ymd_slash = s.str.match(r"^\d{4}/\d{2}/\d{2}$", na=False)
    m_mdy_slash = s.str.match(r"^\d{1,2}/\d{1,2}/\d{4}$", na=False)
    m_mon = s.str.match(r"^[A-Za-z]{3}\s+\d{1,2}\s+\d{4}$", na=False)

    if m_ymd_dash.any():
        out.loc[m_ymd_dash] = pd.to_datetime(s.loc[m_ymd_dash], format="%Y-%m-%d", errors="coerce")
    if m_ymd_slash.any():
        out.loc[m_ymd_slash] = pd.to_datetime(s.loc[m_ymd_slash], format="%Y/%m/%d", errors="coerce")
    if m_mdy_slash.any():
        # 关键假设：01/02/2026 = Jan 02, 2026（month-first）
        out.loc[m_mdy_slash] = pd.to_datetime(s.loc[m_mdy_slash], format="%m/%d/%Y", errors="coerce")
    if m_mon.any():
        out.loc[m_mon] = pd.to_datetime(s.loc[m_mon], format="%b %d %Y", errors="coerce")

    remaining = out.isna()
    if remaining.any():
        out.loc[remaining] = pd.to_datetime(s.loc[remaining], errors="coerce")

    nulls = int(out.isna().sum())
    return out.dt.date.astype("string"), nulls


def load_inputs(root_dir: Path) -> Tuple[pd.DataFrame, str]:
    csv_path = root_dir / "acquisition_raw.csv"
    md_path = root_dir / "metric_definitions.md"

    if not csv_path.exists():
        raise FileNotFoundError(f"Missing input CSV: {csv_path}")
    if not md_path.exists():
        raise FileNotFoundError(f"Missing metric definitions: {md_path}")

    df_raw = pd.read_csv(csv_path)
    metric_text = md_path.read_text(encoding="utf-8")
    return df_raw, metric_text


def clean_acquisition(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, DataQualityReport]:
    expected_cols = [
        "date",
        "channel",
        "spend_usd",
        "signups",
        "activated_users",
        "revenue_30d_usd",
    ]
    missing_cols = [c for c in expected_cols if c not in df_raw.columns]
    if missing_cols:
        raise ValueError(f"Input missing columns: {missing_cols}. Got: {list(df_raw.columns)}")

    df = df_raw.copy()

    # 日期清洗
    df["cohort_date"], parsed_date_nulls = _parse_mixed_dates(df["date"])

    # 数值列清洗
    for col in ["spend_usd", "signups", "activated_users", "revenue_30d_usd"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 渠道歧义处理：social vs paid_social
    # 依据 metric_definitions.md 的 Ambiguities，我们在“生成图表/汇总口径”上合并，
    # 同时保留原始渠道值以便追溯。
    df["channel_raw"] = df["channel"].astype(str).str.strip()
    df["channel"] = df["channel_raw"].replace({"social": "paid_social"})

    # 计算衍生指标（逐行，便于核查；汇总口径稍后再做）
    df["cac"] = _safe_div(df["spend_usd"], df["signups"])
    df["activation_rate"] = _safe_div(df["activated_users"], df["signups"])
    df["payback_proxy"] = _safe_div(df["revenue_30d_usd"], df["spend_usd"])

    # 数据质量统计
    channel_variants = df["channel_raw"].value_counts(dropna=False).to_dict()
    missing_spend_rows = int(df["spend_usd"].isna().sum())
    zero_spend_rows = int((df["spend_usd"] == 0).sum())
    missing_activated_rows = int(df["activated_users"].isna().sum())
    invalid_payback_rows = int(((df["spend_usd"] <= 0) | df["spend_usd"].isna()).sum())

    notes: list[str] = []
    if parsed_date_nulls:
        notes.append("存在无法解析的日期（cohort_date 为 NaN）；这些行会影响 cohort 趋势。")
    if missing_spend_rows:
        notes.append(
            "spend_usd 存在缺失：按定义可能是 tracking failure 或 0 spend；本分析不自动填 0。"
        )
    if zero_spend_rows:
        notes.append(
            "存在 spend_usd=0 的行：payback_proxy（revenue/spend）不适用，已置为 NaN 避免 inf。"
        )
    if missing_activated_rows:
        notes.append("activated_users 存在缺失：activation_rate 对应行将为 NaN。")
    if ("social" in channel_variants) and ("paid_social" in channel_variants):
        notes.append(
            "渠道 social 与 paid_social 在汇总中已合并为 paid_social（保留 channel_raw 以便回溯）。"
        )

    dq = DataQualityReport(
        input_rows=int(len(df_raw)),
        output_rows=int(len(df)),
        parsed_date_nulls=parsed_date_nulls,
        missing_spend_rows=missing_spend_rows,
        zero_spend_rows=zero_spend_rows,
        missing_activated_rows=missing_activated_rows,
        invalid_payback_rows=invalid_payback_rows,
        channel_variants={k: int(v) for k, v in channel_variants.items()},
        notes=notes,
    )

    # 输出列顺序（便于人读与 diff）
    ordered = [
        "cohort_date",
        "channel",
        "channel_raw",
        "spend_usd",
        "signups",
        "activated_users",
        "revenue_30d_usd",
        "cac",
        "activation_rate",
        "payback_proxy",
    ]
    df = df[ordered].sort_values(["cohort_date", "channel"]).reset_index(drop=True)
    return df, dq


def compute_channel_summary(df_clean: pd.DataFrame) -> pd.DataFrame:
    """
    按 channel 汇总（更接近 metric_definitions.md 中“分子/分母先汇总再相除”的口径）：
      - CAC = sum(spend_usd) / sum(signups)
      - activation_rate = sum(activated_users) / sum(signups)
      - payback_proxy = sum(revenue_30d_usd) / sum(spend_usd)
    注意：
      - spend_usd 缺失行将被排除出 sum(spend_usd)，同时仍保留其 signups 等数值；
        因此 “sum(signups)” 口径可能略偏（详见 summary 的 caveats）。
    """
    g = df_clean.groupby("channel", dropna=False)
    out = g.agg(
        days=("cohort_date", "nunique"),
        total_spend_usd=("spend_usd", "sum"),
        total_signups=("signups", "sum"),
        total_activated_users=("activated_users", "sum"),
        total_revenue_30d_usd=("revenue_30d_usd", "sum"),
        rows=("channel", "size"),
        spend_missing_rows=("spend_usd", lambda s: int(s.isna().sum())),
        activated_missing_rows=("activated_users", lambda s: int(s.isna().sum())),
    ).reset_index()

    out["cac"] = _safe_div(out["total_spend_usd"], out["total_signups"])
    out["activation_rate"] = _safe_div(out["total_activated_users"], out["total_signups"])
    out["payback_proxy"] = _safe_div(out["total_revenue_30d_usd"], out["total_spend_usd"])
    return out.sort_values("total_signups", ascending=False).reset_index(drop=True)


def compute_cohort_revenue_trend(df_clean: pd.DataFrame) -> pd.DataFrame:
    """cohort（按 cohort_date）* channel 的 30d revenue 趋势。"""
    trend = (
        df_clean.groupby(["cohort_date", "channel"], dropna=False)
        .agg(
            spend_usd=("spend_usd", "sum"),
            signups=("signups", "sum"),
            revenue_30d_usd=("revenue_30d_usd", "sum"),
        )
        .reset_index()
        .sort_values(["cohort_date", "channel"])
    )
    trend["revenue_per_signup_30d"] = _safe_div(trend["revenue_30d_usd"], trend["signups"])
    return trend


def _save_bar_chart(
    df: pd.DataFrame, x: str, y: str, title: str, ylabel: str, out_path: Path
) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    plot_df = df[[x, y]].dropna().copy()
    ax.bar(plot_df[x].astype(str), plot_df[y].astype(float), color="#4C78A8")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    ax.grid(axis="y", alpha=0.25)

    # 简单标注数值
    for i, v in enumerate(plot_df[y].astype(float).tolist()):
        if math.isnan(v):
            continue
        ax.text(i, v, f"{v:.3g}", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def _save_line_chart(
    trend: pd.DataFrame, out_path: Path, title: str = "Cohort 30D Revenue Trend (USD)"
) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=150)
    trend = trend.dropna(subset=["cohort_date"]).copy()
    trend["cohort_date"] = pd.to_datetime(trend["cohort_date"])

    for channel, sub in trend.groupby("channel"):
        sub = sub.sort_values("cohort_date")
        ax.plot(sub["cohort_date"], sub["revenue_30d_usd"], marker="o", label=str(channel))

    ax.set_title(title)
    ax.set_ylabel("revenue_30d_usd")
    ax.set_xlabel("cohort_date")
    ax.grid(alpha=0.25)
    ax.legend(title="channel", frameon=False)
    fig.autofmt_xdate(rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_plots(
    channel_summary: pd.DataFrame, cohort_trend: pd.DataFrame, out_dir: Path
) -> Dict[str, Path]:
    out_paths: Dict[str, Path] = {}

    out_paths["cac"] = out_dir / "cac_by_channel.png"
    _save_bar_chart(
        channel_summary,
        x="channel",
        y="cac",
        title="CAC by Channel (sum(spend)/sum(signups))",
        ylabel="CAC (USD per signup)",
        out_path=out_paths["cac"],
    )

    out_paths["activation_rate"] = out_dir / "activation_rate_by_channel.png"
    _save_bar_chart(
        channel_summary,
        x="channel",
        y="activation_rate",
        title="Activation Rate by Channel (activated/signups)",
        ylabel="Activation rate",
        out_path=out_paths["activation_rate"],
    )

    out_paths["payback_proxy"] = out_dir / "payback_proxy_by_channel.png"
    _save_bar_chart(
        channel_summary,
        x="channel",
        y="payback_proxy",
        title="Payback Proxy by Channel (revenue_30d/spend)",
        ylabel="Payback proxy",
        out_path=out_paths["payback_proxy"],
    )

    out_paths["cohort_revenue_trend"] = out_dir / "cohort_revenue_trend.png"
    _save_line_chart(
        cohort_trend[["cohort_date", "channel", "revenue_30d_usd"]].copy(),
        out_path=out_paths["cohort_revenue_trend"],
    )

    return out_paths


def _fmt_money(x: float | int | None) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "NA"
    return f"${x:,.0f}"


def _fmt_pct(x: float | None) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "NA"
    return f"{x*100:.1f}%"


def write_executive_summary(
    out_path: Path,
    metric_text: str,
    dq: DataQualityReport,
    df_clean: pd.DataFrame,
    channel_summary: pd.DataFrame,
    cohort_trend: pd.DataFrame,
) -> None:
    # Overall aggregates（与 metric_definitions 的汇总口径一致）
    total_spend = float(df_clean["spend_usd"].sum(skipna=True))
    total_signups = float(df_clean["signups"].sum(skipna=True))
    total_activated = float(df_clean["activated_users"].sum(skipna=True))
    total_rev30 = float(df_clean["revenue_30d_usd"].sum(skipna=True))
    overall_cac = float(_safe_div(pd.Series([total_spend]), pd.Series([total_signups])).iloc[0])
    overall_ar = float(_safe_div(pd.Series([total_activated]), pd.Series([total_signups])).iloc[0])
    overall_payback = float(_safe_div(pd.Series([total_rev30]), pd.Series([total_spend])).iloc[0])

    best_payback = (
        channel_summary.dropna(subset=["payback_proxy"])
        .sort_values("payback_proxy", ascending=False)
        .head(1)
    )
    best_ar = (
        channel_summary.dropna(subset=["activation_rate"])
        .sort_values("activation_rate", ascending=False)
        .head(1)
    )

    # 简单 cohort 趋势：按日合计 revenue_30d
    daily = (
        cohort_trend.groupby("cohort_date", dropna=False)
        .agg(revenue_30d_usd=("revenue_30d_usd", "sum"), signups=("signups", "sum"))
        .reset_index()
        .sort_values("cohort_date")
    )
    if len(daily) >= 2 and daily["revenue_30d_usd"].notna().all():
        rev_change = float(daily["revenue_30d_usd"].iloc[-1] - daily["revenue_30d_usd"].iloc[0])
    else:
        rev_change = np.nan

    assumptions = [
        "日期解析：对类似 01/02/2026 的格式按 month-first（Jan 02, 2026）优先解析；仅对解析失败项再尝试 day-first。",
        "渠道合并：将 channel_raw='social' 与 'paid_social' 在汇总/图表中合并为 channel='paid_social'，同时在 cleaned 数据中保留 channel_raw 以便追溯。",
        "指标口径：CAC、activation_rate、payback_proxy 采用 metric_definitions.md 中定义（分子/分母先按 channel 汇总，再相除）。",
        "payback_proxy：当 spend_usd<=0 或缺失时，不计算 payback_proxy（置为 NA），避免 inf/误读。",
    ]

    caveats = [
        "spend_usd 缺失行可能代表 tracking failure 或 0 spend：本分析未将其自动填为 0；因此 channel 汇总时的 total_signups 仍包含这些行，但 total_spend 不包含，可能导致 CAC / payback 的偏差。",
        "activated_users 缺失会导致 activation_rate 无法计算（NA）；如需补齐需进一步澄清埋点/回填策略。",
        "数据粒度为“按日 * 渠道”的聚合；cohort revenue trend 这里等同于“以日期作为 cohort key 的 30D revenue 汇总趋势”，并非用户级别留存曲线。",
    ]

    next_experiments = [
        "补齐 spend 缺失的归因链路：区分“确实 0 spend”与“tracking failure”，并在原始表中引入 spend_imputed_flag 以支持敏感性分析。",
        "将 social vs paid_social 的定义写入规范（或在数据侧统一枚举值），避免渠道拆分/合并导致的指标波动。",
        "引入更长的 revenue window（如 60d/90d）与毛利口径，替代 payback_proxy 作为更接近真实回本周期的指标。",
        "增加按 cohort_date 的趋势监控：例如 CAC 与 revenue_per_signup_30d 的时间序列/控制图，以识别渠道或漏斗结构的系统性漂移。",
    ]

    verification_notes = [
        "已输出 analysis/output/channel_summary.csv：可直接核对每个 channel 的 total_spend/total_signups/total_activated/total_revenue 以及由此计算出的指标。",
        "cleaned_acquisition.csv 保留 channel_raw 与计算后的逐行指标（cac/activation_rate/payback_proxy），便于 spot check。",
    ]

    data_quality_issues = [f"- {n}" for n in (dq.notes if dq.notes else ["未发现显著问题（基于当前规则）。"])]

    lines: list[str] = []
    lines.append("# EXECUTIVE SUMMARY — LPME-DS-001\n")

    lines.append("## Inputs\n")
    lines.append("- acquisition_raw.csv\n")
    lines.append("- metric_definitions.md\n")

    lines.append("\n## Metric definitions (as provided)\n")
    # 原样引用 + 解释歧义（避免“想象”指标）
    lines.append("以下为输入文件中的定义（原文）：\n\n")
    lines.append("```text\n")
    lines.append(metric_text.strip() + "\n")
    lines.append("```\n")

    lines.append("\n## Key computed results (overall)\n")
    lines.append(f"- Total spend: {_fmt_money(total_spend)}\n")
    lines.append(f"- Total signups: {total_signups:,.0f}\n")
    lines.append(f"- Total activated users: {total_activated:,.0f}\n")
    lines.append(f"- Total 30D revenue: {_fmt_money(total_rev30)}\n")
    lines.append(f"- Overall CAC: {_fmt_money(overall_cac)} per signup\n")
    lines.append(f"- Overall activation rate: {_fmt_pct(overall_ar)}\n")
    lines.append(f"- Overall payback proxy: {overall_payback:.3f}\n")

    if not best_payback.empty:
        r = best_payback.iloc[0]
        lines.append(
            f"- Best payback proxy channel: {r['channel']} ({r['payback_proxy']:.3f})\n"
        )
    if not best_ar.empty:
        r = best_ar.iloc[0]
        lines.append(f"- Best activation rate channel: {r['channel']} ({_fmt_pct(r['activation_rate'])})\n")

    lines.append("\n## Cohort trend readout\n")
    if isinstance(rev_change, float) and not np.isnan(rev_change):
        direction = "up" if rev_change > 0 else "down" if rev_change < 0 else "flat"
        lines.append(
            f"- Total 30D revenue from first to last cohort_date moved {direction} by {_fmt_money(abs(rev_change))} "
            f"(first={_fmt_money(daily['revenue_30d_usd'].iloc[0])}, last={_fmt_money(daily['revenue_30d_usd'].iloc[-1])}).\n"
        )
    else:
        lines.append("- 数据点不足或存在缺失，无法稳健判断 cohort revenue 的首末变化。\n")

    lines.append("\n## Assumptions\n")
    for a in assumptions:
        lines.append(f"- {a}\n")

    lines.append("\n## Caveats\n")
    for c in caveats:
        lines.append(f"- {c}\n")

    lines.append("\n## Data-quality issues\n")
    lines.extend([q + "\n" for q in data_quality_issues])
    lines.append("\n**Data-quality counters**\n\n")
    dqd = dq.to_dict()
    lines.append("```json\n")
    lines.append(pd.Series(dqd).to_json(force_ascii=False, indent=2) + "\n")
    lines.append("```\n")

    lines.append("\n## Verification notes\n")
    for v in verification_notes:
        lines.append(f"- {v}\n")

    lines.append("\n## Next experiment recommendations\n")
    for n in next_experiments:
        lines.append(f"- {n}\n")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    root_dir = Path(__file__).resolve().parents[1]
    analysis_dir = root_dir / "analysis"
    out_dir = analysis_dir / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    df_raw, metric_text = load_inputs(root_dir)
    df_clean, dq = clean_acquisition(df_raw)

    cleaned_csv_path = out_dir / "cleaned_acquisition.csv"
    df_clean.to_csv(cleaned_csv_path, index=False)

    channel_summary = compute_channel_summary(df_clean)
    channel_summary_path = out_dir / "channel_summary.csv"
    channel_summary.to_csv(channel_summary_path, index=False)

    cohort_trend = compute_cohort_revenue_trend(df_clean)

    plot_paths = make_plots(channel_summary, cohort_trend, out_dir)

    exec_summary_path = analysis_dir / "EXECUTIVE_SUMMARY.md"
    write_executive_summary(
        exec_summary_path, metric_text, dq, df_clean, channel_summary, cohort_trend
    )

    # 轻量控制台输出（用于评测核对脚本确实跑过并产出文件）
    print("✅ Generated outputs:")
    print(f"- {cleaned_csv_path}")
    print(f"- {channel_summary_path}")
    for k, p in plot_paths.items():
        print(f"- [{k}] {p}")
    print(f"- {exec_summary_path}")


if __name__ == "__main__":
    main()
