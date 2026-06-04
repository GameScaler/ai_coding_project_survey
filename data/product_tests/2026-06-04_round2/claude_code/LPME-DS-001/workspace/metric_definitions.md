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

