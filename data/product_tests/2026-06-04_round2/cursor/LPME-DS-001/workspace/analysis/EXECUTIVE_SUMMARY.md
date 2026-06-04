# Acquisition Cohort Analysis — Executive Summary

**Period:** 2026-01-01 to 2026-01-04 (4 days, 12 raw rows)  
**Reproducibility:** Run `python3 analysis/acquisition_analysis.py` from the workspace root. Charts and tables are written under `analysis/output/`.

---

## Headline findings

| Channel | Typical CAC | Activation rate (complete rows) | 30d payback proxy (complete rows) |
|---------|-------------|-----------------------------------|-----------------------------------|
| **search** | ~$5.0–5.3 | ~46–52% | **>1.0** on all days with known spend |
| **paid_social** | ~$3.8–4.4 | ~34–39% | **<1.0** on all days with known spend |
| **affiliate** | ~$4.4 (excl. $0-spend day) | ~58–60% | **>1.5** when spend > 0 |

1. **Search** is the most expensive per signup but the only paid channel that consistently recovers spend within 30 days (`payback_proxy` 1.29–1.31 on complete days). Jan 4 CAC ticked up to **$5.31** while activation improved to **52.2%**.
2. **Paid social** (after normalizing `social` → `paid_social`) has the **lowest CAC** but **does not reach 30-day payback** (proxy 0.81–0.95). Activation **declined** from 38% (Jan 1) to 34% (Jan 3) before a partial rebound to 40% (Jan 4).
3. **Affiliate** shows the **strongest payback proxy** (1.52–1.55) when spend is recorded, with high activation (~58–60%), but **two rows break efficiency metrics** (zero spend, missing activations).

**Cohort revenue (all channels, daily sum):** $2,940 → $2,920 → $2,760 → **$3,210** (Jan 1–4). The Jan 3 dip aligns with weaker paid-social performance and a search row with missing spend (revenue still recorded).

---

## Artifacts produced

| Output | Path |
|--------|------|
| Cleaning + metrics script | `analysis/acquisition_analysis.py` |
| Row-level cleaned data | `analysis/output/cleaned_acquisition.csv` |
| Daily channel roll-up | `analysis/output/daily_channel_metrics.csv` |
| Data quality log | `analysis/output/data_quality_report.json` |
| CAC chart | `analysis/output/cac_by_channel.png` |
| Activation chart | `analysis/output/activation_rate_by_channel.png` |
| Payback proxy chart | `analysis/output/payback_proxy_by_channel.png` |
| Cohort revenue chart | `analysis/output/cohort_revenue_trend.png` |

---

## Assumptions

1. **Channel aliasing:** `social` and `paid_social` are treated as one channel **`paid_social`**, because `metric_definitions.md` states they may represent the same paid-social bucket. Original labels are preserved in `channel_raw`.
2. **Date parsing:** All date strings are parsed with `pandas.to_datetime(..., format="mixed")` and stored as `YYYY-MM-DD`. Formats in source included `2026-01-01`, `01/02/2026`, `2026/01/03`, and `Jan 03 2026`.
3. **Metric formulas** (per definitions file):
   - `CAC = spend_usd / signups`
   - `activation_rate = activated_users / signups`
   - `payback_proxy = revenue_30d_usd / spend_usd`
4. **Missing spend:** Not imputed as zero. Rows with missing `spend_usd` are flagged `spend_missing=True`; **CAC and payback_proxy are left blank** for those rows.
5. **Zero spend:** `affiliate` on 2026-01-02 has `spend_usd = 0` as recorded. CAC is computed as 0; **payback_proxy is undefined** (division by zero avoided).
6. **Missing activations:** Not imputed. `activation_rate` is blank when `activated_users` is missing.
7. **Aggregation:** One row per `date × channel`. Sums are used only when no row in the group has a missing flag for that field.

---

## Caveats

| Issue | Rows affected | Impact |
|-------|---------------|--------|
| Missing **spend** (search, Jan 3) | 1 | CAC/payback not plotted for that point; do not infer zero spend |
| Missing **activated_users** (affiliate, Jan 3) | 1 | Activation trend has a gap for affiliate |
| **Zero spend** (affiliate, Jan 2) | 1 | Payback undefined; CAC = $0 is misleading as “free acquisition” without ops context |
| **Short window** | 4 days | No statistical significance; trends are illustrative only |
| **payback_proxy ≠ ROI** | All | Uses 30-day cohort revenue only; ignores margin, refunds, and LTV beyond 30 days |
| **Channel merge** | 2 rows | If `social` were a distinct organic line, paid-social CAC/activation would be overstated |

---

## Verification notes

- **Source vs cleaned row count:** 12 → 12 (no rows dropped; quality flags added).
- **Parsed dates:** All 12 rows received valid `date` values; none flagged `unparseable_date`.
- **Issues logged in** `data_quality_report.json`: 4 (2 channel aliases, 1 missing spend, 1 missing activation).
- **Excluded from charts (by design):** 1 row from CAC series, 2 from payback series, 1 from activation series (see quality report counts).
- **Manual spot-check (Jan 1 search):** CAC = 1200/240 = **$5.00**; activation = 120/240 = **50%**; payback = 1560/1200 = **1.30** — matches cleaned output.

---

## Recommended next experiments

1. **Backfill Jan 3 search spend** from ad platform exports; re-run payback — current gap blocks channel-level efficiency comparison on the weakest revenue day.
2. **Holdout test on paid social:** Reduce spend 20% for 2 weeks in one geo; measure whether CAC rise is offset by activation/payback (validates whether sub-1.0 payback is structural).
3. **Affiliate contract audit:** Clarify Jan 2 zero-spend day (bonus inventory vs tracking bug) and fix activation tracking on Jan 3 before scaling affiliate spend.
4. **Extend cohort window:** Add `revenue_60d_usd` / `revenue_90d_usd` to test whether paid social reaches payback with longer horizons.
5. **Unify channel taxonomy** in the ingestion pipeline (`social` vs `paid_social`) to remove alias assumptions.
6. **Activation funnel deep-dive:** Search ~50% vs paid social ~35–40% suggests onboarding or audience mismatch — run event-level funnel by channel.

---

## How to re-run

```bash
cd /path/to/workspace
export MPLCONFIGDIR=analysis/output/.matplotlib   # optional; avoids matplotlib cache warnings
python3 analysis/acquisition_analysis.py
```

Dependencies: `pandas`, `matplotlib`.
