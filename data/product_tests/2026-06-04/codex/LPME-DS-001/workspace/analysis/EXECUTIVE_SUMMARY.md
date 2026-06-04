# Executive Summary: Acquisition Cohorts

## Scope

Analyzed `acquisition_raw.csv` daily signup cohorts from 2026-01-01 through 2026-01-04. The cleaned dataset preserves 12 raw cohort rows and writes derived metrics to `analysis/output/cleaned_acquisition.csv`.

## Assumptions and Metric Decisions

- Slash dates are parsed month-first, so `01/02/2026` is treated as January 2, 2026.
- `social` and `paid_social` are treated as the same channel and normalized to `paid_social`.
- The missing search spend on 2026-01-03 is imputed with within-channel linear interpolation: $1,240.
- The missing affiliate activation count on 2026-01-03 is imputed with within-channel linear interpolation and rounded: 55 users.
- Row-level payback proxy is undefined when spend is zero. The by-channel payback chart uses total 30-day revenue divided by total cleaned spend, so the affiliate value should be read with the zero-spend caveat.

## Cohort Trends

- Search produced the most 30-day revenue at $6,170 and ended at the highest daily cohort revenue ($1,700 on 2026-01-04). Its CAC is $5.20, activation rate is 49.8%, and payback proxy is 1.25x.
- Paid social has the weakest efficiency in this sample: CAC $4.08, activation rate 37.8%, and payback proxy 0.91x. It is below 1.0x 30-day payback.
- Affiliate shows the lowest CAC ($3.38) and highest activation rate (58.9%). Its aggregate payback proxy is 2.01x, but excluding the zero-spend row lowers it to 1.54x.
- Total cohort revenue moved from $2,940 on 2026-01-01 to $3,210 on 2026-01-04 (9.2%), with a dip on 2026-01-03 before rebounding on 2026-01-04.

## Data Quality Issues and Caveats

- Mixed date formats found: ISO, slash-delimited, and month-name strings.
- Normalized channel alias rows: 2.
- Missing spend rows: 1; this was imputed rather than treated as zero.
- Missing activated-user rows: 1; this was imputed and rounded to a whole user count.
- Zero-spend rows with revenue: 1; row-level payback is undefined and aggregate payback may overstate efficiency if this is a tracking issue.
- The sample covers only four cohort days, so these are directional trends rather than stable channel benchmarks.

## Next Experiment Recommendations

- Audit the affiliate zero-spend row and require spend-source validation before using affiliate payback for budget allocation.
- Run a paid-social activation experiment focused on the post-signup onboarding step, since activation trails other channels by more than 10 percentage points.
- Increase search budget in a controlled holdout or geo-split test to confirm whether the high January 4 revenue cohort repeats without degrading CAC.
- Add ETL checks for parseable dates, known channel names, missing spend, missing activation counts, and spend-zero/revenue-positive rows.

## Verification Notes

- Executed `python3 analysis/acquisition_analysis.py`.
- Verified the cleaned output row count matches the raw row count: 12 rows.
- Verified unparsed date count is 0.
- Generated charts:
- `analysis/output/cac_by_channel.svg`
- `analysis/output/activation_rate_by_channel.svg`
- `analysis/output/payback_proxy_by_channel.svg`
- `analysis/output/cohort_revenue_trend.svg`
