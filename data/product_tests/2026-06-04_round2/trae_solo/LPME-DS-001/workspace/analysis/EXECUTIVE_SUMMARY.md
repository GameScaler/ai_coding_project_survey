# EXECUTIVE SUMMARY — LPME-DS-001
## Inputs
- acquisition_raw.csv
- metric_definitions.md

## Metric definitions (as provided)
以下为输入文件中的定义（原文）：

```text
# Metric Definitions

- spend_usd: daily paid acquisition spend.
- signups: new user signups attributed to the channel.
- activated_users: users who completed the activation event within 7 days.
- revenue_30d_usd: revenue from the signup cohort within 30 days.
- CAC: spend_usd / signups.
- activation_rate: activated_users / signups.
- payback_proxy: revenue_30d_usd / spend_usd.

## Ambiguities

- Some rows use `channel = social` and others use `channel = paid_social`; treat them as the same channel only if you document the assumption.
- Rows with missing spend may mean either tracking failure or zero spend. Do not silently treat them as zero without caveat.
```

## Key computed results (overall)
- Total spend: $8,400
- Total signups: 2,167
- Total activated users: 956
- Total 30D revenue: $11,830
- Overall CAC: $4 per signup
- Overall activation rate: 44.1%
- Overall payback proxy: 1.408
- Best payback proxy channel: affiliate (2.008)
- Best activation rate channel: search (49.8%)

## Cohort trend readout
- Total 30D revenue from first to last cohort_date moved up by $270 (first=$2,940, last=$3,210).

## Assumptions
- 日期解析：对类似 01/02/2026 的格式按 month-first（Jan 02, 2026）优先解析；仅对解析失败项再尝试 day-first。
- 渠道合并：将 channel_raw='social' 与 'paid_social' 在汇总/图表中合并为 channel='paid_social'，同时在 cleaned 数据中保留 channel_raw 以便追溯。
- 指标口径：CAC、activation_rate、payback_proxy 采用 metric_definitions.md 中定义（分子/分母先按 channel 汇总，再相除）。
- payback_proxy：当 spend_usd<=0 或缺失时，不计算 payback_proxy（置为 NA），避免 inf/误读。

## Caveats
- spend_usd 缺失行可能代表 tracking failure 或 0 spend：本分析未将其自动填为 0；因此 channel 汇总时的 total_signups 仍包含这些行，但 total_spend 不包含，可能导致 CAC / payback 的偏差。
- activated_users 缺失会导致 activation_rate 无法计算（NA）；如需补齐需进一步澄清埋点/回填策略。
- 数据粒度为“按日 * 渠道”的聚合；cohort revenue trend 这里等同于“以日期作为 cohort key 的 30D revenue 汇总趋势”，并非用户级别留存曲线。

## Data-quality issues
- spend_usd 存在缺失：按定义可能是 tracking failure 或 0 spend；本分析不自动填 0。
- 存在 spend_usd=0 的行：payback_proxy（revenue/spend）不适用，已置为 NaN 避免 inf。
- activated_users 存在缺失：activation_rate 对应行将为 NaN。
- 渠道 social 与 paid_social 在汇总中已合并为 paid_social（保留 channel_raw 以便回溯）。

**Data-quality counters**

```json
{
  "input_rows":12,
  "output_rows":12,
  "parsed_date_nulls":0,
  "missing_spend_rows":1,
  "zero_spend_rows":1,
  "missing_activated_rows":1,
  "invalid_payback_rows":2,
  "channel_variants":{
    "search":4,
    "affiliate":4,
    "social":2,
    "paid_social":2
  },
  "notes":[
    "spend_usd 存在缺失：按定义可能是 tracking failure 或 0 spend；本分析不自动填 0。",
    "存在 spend_usd=0 的行：payback_proxy（revenue\/spend）不适用，已置为 NaN 避免 inf。",
    "activated_users 存在缺失：activation_rate 对应行将为 NaN。",
    "渠道 social 与 paid_social 在汇总中已合并为 paid_social（保留 channel_raw 以便回溯）。"
  ]
}
```

## Verification notes
- 已输出 analysis/output/channel_summary.csv：可直接核对每个 channel 的 total_spend/total_signups/total_activated/total_revenue 以及由此计算出的指标。
- cleaned_acquisition.csv 保留 channel_raw 与计算后的逐行指标（cac/activation_rate/payback_proxy），便于 spot check。

## Next experiment recommendations
- 补齐 spend 缺失的归因链路：区分“确实 0 spend”与“tracking failure”，并在原始表中引入 spend_imputed_flag 以支持敏感性分析。
- 将 social vs paid_social 的定义写入规范（或在数据侧统一枚举值），避免渠道拆分/合并导致的指标波动。
- 引入更长的 revenue window（如 60d/90d）与毛利口径，替代 payback_proxy 作为更接近真实回本周期的指标。
- 增加按 cohort_date 的趋势监控：例如 CAC 与 revenue_per_signup_30d 的时间序列/控制图，以识别渠道或漏斗结构的系统性漂移。
