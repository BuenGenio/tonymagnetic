#!/usr/bin/env bash
# Render the site to a single PDF. Needs chromium + poppler (pdfunite).
#   tools/build-pdf.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist"
PORT="${PORT:-4321}"
PAGES=(index work about contact)

mkdir -p "$OUT/pages"

# chromium under snap confinement cannot write outside $HOME
case "$OUT" in "$HOME"/*) ;; *) echo "dist/ must live under \$HOME for snap chromium"; exit 1;; esac

started=""
if ! curl -sf -o /dev/null "http://127.0.0.1:$PORT/index.html"; then
  ( cd "$ROOT" && python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 & )
  started=1; sleep 1
fi

for p in "${PAGES[@]}"; do
  echo "  rendering $p"
  chromium --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --virtual-time-budget=12000 --run-all-compositor-stages-before-draw \
    --no-pdf-header-footer --print-to-pdf="$OUT/pages/$p.pdf" \
    "http://127.0.0.1:$PORT/$p.html" 2>/dev/null
done

rm -f "$OUT/tony-magnetic-website.pdf"
pdfunite $(printf "$OUT/pages/%s.pdf " "${PAGES[@]}") "$OUT/tony-magnetic-website.pdf"
[ -n "$started" ] && pkill -f "http.server $PORT" || true
echo "  -> dist/tony-magnetic-website.pdf ($(pdfinfo "$OUT/tony-magnetic-website.pdf" | awk '/^Pages/{print $2}') pages)"
