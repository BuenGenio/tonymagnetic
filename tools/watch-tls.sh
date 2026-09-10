#!/usr/bin/env bash
# Poll GitHub Pages until the Let's Encrypt certificate for the custom domain is
# issued, then turn on Enforce HTTPS. Exits when done, or after MAX_HOURS.
REPO="${REPO:-BuenGenio/tonymagnetic}"
LOG="${LOG:-/home/buengenio/Projects/tonymagnetic/dist/tls-watch.log}"
MAX_HOURS="${MAX_HOURS:-8}"
INTERVAL=300

mkdir -p "$(dirname "$LOG")"
say(){ echo "$(date '+%H:%M:%S')  $*" | tee -a "$LOG"; }

say "watching $REPO for certificate issuance (every ${INTERVAL}s, up to ${MAX_HOURS}h)"
end=$(( $(date +%s) + MAX_HOURS*3600 ))

while [ "$(date +%s)" -lt "$end" ]; do
  state=$(gh api "repos/$REPO/pages" 2>/dev/null \
    | python3 -c "import json,sys;c=json.load(sys.stdin).get('https_certificate') or {};print(c.get('state','none'))" 2>/dev/null)

  case "$state" in
    approved|issued)
      say "certificate $state — enabling Enforce HTTPS"
      gh api -X PUT "repos/$REPO/pages" -F https_enforced=true >/dev/null 2>&1
      sleep 10
      enforced=$(gh api "repos/$REPO/pages" 2>/dev/null \
        | python3 -c "import json,sys;print(json.load(sys.stdin).get('https_enforced'))")
      code=$(curl -sI --max-time 20 https://tonymagnetic.com/ -o /dev/null -w '%{http_code}')
      say "https_enforced=$enforced  https://tonymagnetic.com -> $code"
      say "DONE"
      exit 0
      ;;
    none|"")  say "not issued yet" ;;
    *)        say "state: $state" ;;
  esac
  sleep "$INTERVAL"
done

say "gave up after ${MAX_HOURS}h — cert still not issued. Check DNS in Cloudflare."
exit 1
