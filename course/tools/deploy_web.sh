#!/usr/bin/env bash
# Đưa website (course/output) lên Cloudflare: https://ai-canuc80k.pages.dev (Cloudflare Pages)
# Chạy từ bất kỳ đâu: bash "05. AI Canuc80k/course/tools/deploy_web.sh"
# Lần đầu trên máy mới: npx wrangler@4 login
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
OUT="$ROOT/05. AI Canuc80k/course/output"
STAGE="$ROOT/04. Workspace/ai-web-deploy"
# Lõi chung (tools/site-kit) phải khớp trước khi đưa lên
if [ -f "$ROOT/tools/site-kit/sync.py" ]; then python -B -X utf8 "$ROOT/tools/site-kit/sync.py" --check; fi
python -B -X utf8 "$ROOT/05. AI Canuc80k/course/tools/split_site.py"
rm -rf "$STAGE/site" && mkdir -p "$STAGE/site"
# Không đưa phần riêng của giáo viên và tệp vận hành nội bộ
(cd "$OUT" && tar --exclude=./teacher_private --exclude=./current --exclude=./smoke-final.pptx \
  --exclude=./HUONG_DAN_GIAO_VIEN.txt --exclude=./KE_HOACH_CONTEST.txt \
  --exclude=./ui/kit.lock.json --exclude=./ui/theory.js --exclude=./ui/course-data.js --exclude=./ui/code-examples.js -cf - .) | (cd "$STAGE/site" && tar -xf -)
cp "$STAGE/site/START_HERE.html" "$STAGE/site/index.html"
# Link cũ *.workers.dev do Worker chuyển hướng tools/site-kit/redirect-worker lo
rm -f "$STAGE/wrangler.jsonc"
cd "$STAGE" && npx -y wrangler@4.150.0 pages deploy site --project-name ai-canuc80k --branch main --commit-dirty=true
rm -rf "$STAGE/site"
