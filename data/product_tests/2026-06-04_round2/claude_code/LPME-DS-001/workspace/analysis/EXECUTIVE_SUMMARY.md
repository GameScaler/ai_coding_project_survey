# Executive Summary

## What was analyzed
Daily acquisition performance across channels using spend, signups, 7-day activations, and 30-day cohort revenue.

## Headline findings
- Overall observed spend: $8,400.00 across 2,167 signups.
- Overall CAC: $4.33 per signup.
- Overall activation rate: 46.6%.
- Overall payback proxy (30-day revenue / spend): 1.24x.
- Best payback proxy: **affiliate** at 2.01x.
- Best activation rate: **affiliate** at 58.6%.
- Lowest CAC: **affiliate** at $3.38.

## Assumptions
- `social` and `paid_social` were combined into `paid_social`, per the ambiguity called out in metric_definitions.md.
- Missing `spend_usd` was not treated as zero; rows with missing spend are retained but excluded from spend-based metrics and flagged in the cleaned output.
- Missing `activated_users` was imputed with the channel-level median only for aggregate trend calculations and flagged in the cleaned output.
- Payback proxy follows the provided definition exactly: `revenue_30d_usd / spend_usd`.

## Caveats
- The dataset covers only four cohort dates, so trend conclusions are directional rather than statistically robust.
- One search row is missing spend, so search CAC and payback estimates exclude that row and remain more uncertain than other channels.
- 30-day revenue is cohort-based, but acquisition is logged daily; this is useful for directional efficiency, not full LTV analysis.

## Verification notes
- The analysis was executed via `python3 analysis/acquisition_analysis.py`.
- Output files were generated directly from the script: cleaned CSV, four PNG charts, and this executive summary.
- Mixed-format dates in the raw CSV were verified to parse across ISO, slash-delimited, and month-name inputs before cleaning.
- Spend-based metrics were verified to exclude rows with missing spend while retaining explicit zero-spend rows.
- Metric formulas in the cleaned output were cross-checked against metric_definitions.md.

## Data-quality issues
- 1 row(s) had missing spend_usd and were excluded from spend-based metrics instead of being treated as zero.
- 1 row(s) had explicit zero spend and were retained as documented zero-cost acquisition.
- 1 row(s) had missing activated_users and required imputation for rate calculations.
- Channel labels were inconsistent (`social` vs `paid_social`) and were standardized under a documented assumption.
- Source dates mixed ISO, slash-delimited, and month-name formats; parsing now uses mixed-format datetime handling so valid dates are retained.

## Cleaning notes
- Assumption: merged `social` into `paid_social` because metric_definitions.md flags them as potentially the same channel.
- Missing spend_usd on 1 row(s); excluded those rows from spend-based metrics instead of assuming zero spend.
- Retained 1 row(s) with explicit zero spend as documented zero-cost acquisition.
- Missing activated_users on 1 row(s); imputed with channel-level median activated_users for trend calculations and flagged in output.

## Next experiment recommendations
1. Reallocate incremental budget toward **affiliate**, which currently shows the strongest revenue payback.
2. Diagnose onboarding differences behind **affiliate** outperforming on activation rate, then test those activation levers in lower-converting channels.
3. Audit spend tracking for **search** before scaling, because one missing spend row is currently excluded from CAC and payback calculations.
4. Extend the cohort window and add more dates so trend charts can separate noise from stable channel effects.

## Channel summary
| channel_group | spend_usd | spend_missing_rows | signups | activated_users_clean | revenue_30d_usd | spend_usd_observed | signups_with_spend | revenue_30d_usd_with_spend | cac | activation_rate | payback_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| affiliate | 1250.00 | 0 | 370 | 217.00 | 2510 | 1250.00 | 370 | 2510 | 3.38 | 0.59 | 2.01 |
| paid_social | 3470.00 | 0 | 851 | 322.00 | 3150 | 3470.00 | 851 | 3150 | 4.08 | 0.38 | 0.91 |
| search | 3680.00 | 1 | 946 | 471.00 | 6170 | 3680.00 | 721 | 4780 | 5.10 | 0.50 | 1.30 |
