# Operations Runbook

Last reviewed: 2026-06-10

This runbook explains the daily / weekly update system, Feishu delivery chain, and troubleshooting workflow.

## What Should Happen Daily

Target behavior:

1. 11:00: Codex daily automation creates `data/daily_updates/YYYY-MM-DD.md`.
2. After creation: it runs `scripts/sync_and_run_feishu_delivery_guard.sh`.
3. 11:15 and 11:45: launchd daily fallback checks whether a public daily digest exists. If not, it creates a conservative "无新增产品级重大公开更新" digest and sends it.
4. Every 10 minutes: launchd Feishu delivery guard scans recent daily / weekly files and sends any pending cards.

This means a missing Codex run should not create a missing Feishu message. The fallback creates a safe digest, and the guard sends it.

## What Should Happen Weekly

Every Monday 11:20, Codex weekly automation should create the last completed Monday-Sunday review in `data/weekly_updates/`.

Weekly digest must not be generated for an in-progress week. For example, the week starting Monday should only be published after that Sunday has completed.

If the Codex weekly automation does not create the file, launchd weekly fallback runs Monday 11:50 and 12:30. It creates a conservative weekly digest from existing public daily digests and then sends it. After any weekly file exists, the same delivery guard sends it to Feishu subscribers.

## Important Files

- `automation/digest_format.md`: only daily / weekly format contract.
- `automation/product_sources.json`: official product source pool.
- `automation/feishu_subscribers.local.json`: local-only subscriber table, ignored by Git.
- `.env.local`: local-only Feishu credentials, ignored by Git.
- `data/daily_updates/YYYY-MM-DD.md`: public daily digest.
- `data/weekly_updates/YYYY-Www.md`: public weekly digest.
- `data/feishu/delivery_state.local.json`: repo-local delivery state, ignored by Git.
- `~/.ai_coding_survey_delivery_runtime/`: launchd runtime copy.

## Scripts

Create source-gathering draft:

```bash
python3 scripts/daily_update.py --insecure-ssl
```

Create conservative daily fallback:

```bash
python3 scripts/generate_daily_fallback.py
```

Sync runtime:

```bash
scripts/sync_delivery_runtime.sh
```

Sync and send pending cards:

```bash
scripts/sync_and_run_feishu_delivery_guard.sh
```

Run fallback generation and delivery:

```bash
scripts/run_daily_fallback_and_delivery.sh
```

Run weekly fallback generation and delivery:

```bash
scripts/run_weekly_fallback_and_delivery.sh
```

Direct delivery guard dry run:

```bash
python3 scripts/feishu_delivery_guard.py \
  --daily-lookback-days 7 \
  --weekly-lookback-weeks 3 \
  --dry-run
```

Direct delivery guard send:

```bash
python3 scripts/feishu_delivery_guard.py \
  --daily-lookback-days 7 \
  --weekly-lookback-weeks 3 \
  --attempts 4 \
  --backoff-seconds 20
```

## launchd Jobs

Installed plist templates:

- `automation/launchd/com.gamescaler.ai-coding-daily-fallback.plist`
- `automation/launchd/com.gamescaler.ai-coding-weekly-fallback.plist`
- `automation/launchd/com.gamescaler.ai-coding-feishu-delivery-guard.plist`

Install / reload:

```bash
scripts/sync_delivery_runtime.sh
mkdir -p "$HOME/Library/LaunchAgents"
cp automation/launchd/com.gamescaler.ai-coding-daily-fallback.plist "$HOME/Library/LaunchAgents/"
cp automation/launchd/com.gamescaler.ai-coding-weekly-fallback.plist "$HOME/Library/LaunchAgents/"
cp automation/launchd/com.gamescaler.ai-coding-feishu-delivery-guard.plist "$HOME/Library/LaunchAgents/"
uid=$(id -u)
for label in com.gamescaler.ai-coding-daily-fallback com.gamescaler.ai-coding-weekly-fallback com.gamescaler.ai-coding-feishu-delivery-guard; do
  launchctl bootout "gui/$uid" "$HOME/Library/LaunchAgents/$label.plist" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$uid" "$HOME/Library/LaunchAgents/$label.plist"
  launchctl enable "gui/$uid/$label"
done
```

Kickstart manually:

```bash
uid=$(id -u)
launchctl kickstart -k "gui/$uid/com.gamescaler.ai-coding-daily-fallback"
launchctl kickstart -k "gui/$uid/com.gamescaler.ai-coding-weekly-fallback"
launchctl kickstart -k "gui/$uid/com.gamescaler.ai-coding-feishu-delivery-guard"
```

Inspect:

```bash
uid=$(id -u)
launchctl print "gui/$uid/com.gamescaler.ai-coding-daily-fallback"
launchctl print "gui/$uid/com.gamescaler.ai-coding-weekly-fallback"
launchctl print "gui/$uid/com.gamescaler.ai-coding-feishu-delivery-guard"
```

Logs:

```bash
tail -120 ~/.ai_coding_survey_delivery_runtime/data/feishu/launchd_daily_fallback.out.log
tail -120 ~/.ai_coding_survey_delivery_runtime/data/feishu/launchd_daily_fallback.err.log
tail -120 ~/.ai_coding_survey_delivery_runtime/data/feishu/launchd_weekly_fallback.out.log
tail -120 ~/.ai_coding_survey_delivery_runtime/data/feishu/launchd_weekly_fallback.err.log
tail -120 ~/.ai_coding_survey_delivery_runtime/data/feishu/launchd_delivery_guard.out.log
tail -120 ~/.ai_coding_survey_delivery_runtime/data/feishu/launchd_delivery_guard.err.log
```

## Troubleshooting Decision Tree

### Case 1: Feishu has no daily message

Check whether today's digest exists:

```bash
date '+%Y-%m-%d'
ls -l data/daily_updates/$(date '+%Y-%m-%d').md
ls -l ~/.ai_coding_survey_delivery_runtime/data/daily_updates/$(date '+%Y-%m-%d').md
```

If no file exists:

```bash
python3 scripts/generate_daily_fallback.py
scripts/sync_and_run_feishu_delivery_guard.sh
```

Then check launchd daily fallback.

If the file exists but was not sent, inspect delivery state:

```bash
python3 - <<'PY'
import datetime as dt, json
day = dt.date.today().isoformat()
for p in [
    'data/feishu/delivery_state.local.json',
    '/Users/mvbj0638/.ai_coding_survey_delivery_runtime/data/feishu/delivery_state.local.json',
]:
    print(p)
    try:
        data = json.load(open(p, encoding='utf-8'))
    except FileNotFoundError:
        print('missing')
        continue
    print(json.dumps(data.get('deliveries', {}).get(f'daily:{day}', {}), ensure_ascii=False, indent=2)[:3000])
PY
```

If state is missing or failed:

```bash
scripts/sync_and_run_feishu_delivery_guard.sh
```

### Case 2: DNS / Feishu API fails

The sender has multiple fallbacks:

1. Python `urllib`;
2. plain `curl`;
3. public DNS resolver lookup;
4. `curl --resolve open.feishu.cn:443:<ip>`.

Check:

```bash
python3 - <<'PY'
import socket
print(socket.getaddrinfo('open.feishu.cn', 443))
PY
curl -I --max-time 10 https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
```

If API is down or network is blocked, leave the delivery state as failed. The launchd guard will retry.

### Case 3: Runtime sync fails

If `rsync` into `~/.ai_coding_survey_delivery_runtime` fails, recreate the runtime:

```bash
rm -rf ~/.ai_coding_survey_delivery_runtime
scripts/sync_delivery_runtime.sh
```

Then reload launchd jobs.

### Case 4: Digest revised after already sent

The guard will not resend a `sent` digest unless forced. To intentionally resend:

```bash
python3 scripts/feishu_delivery_guard.py \
  --only daily \
  --daily-lookback-days 1 \
  --force
```

Use force carefully. It will resend to all configured recipients.

## Public Content Guardrails

Do not publish:

- "automation failed";
- "DNS failed";
- "source changed";
- "crawler found N changed pages";
- raw source excerpts.

Public message should only say whether product capability changed.

If the fallback digest was sent and later a human / Codex creates a deep digest for the same day, decide whether to resend. For meaningful updates, resend with `--force`; for minor wording improvements, do not.

For a precise correction resend, target a single label:

```bash
python3 scripts/feishu_delivery_guard.py \
  --only daily \
  --label YYYY-MM-DD \
  --force \
  --attempts 4 \
  --backoff-seconds 20
```
