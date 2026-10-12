#!/usr/bin/env bash
# Đưa website (course/output) lên Cloudflare: https://ai-canuc80k.ai-web-deploy-20261010.workers.dev
# Chạy từ bất kỳ đâu: bash "05. AI Canuc80k/course/tools/deploy_web.sh"
# Lần đầu trên máy mới: npx wrangler@4 login
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
OUT="$ROOT/05. AI Canuc80k/course/output"
STAGE="$ROOT/04. Workspace/ai-web-deploy"
rm -rf "$STAGE/site" && mkdir -p "$STAGE/site"
# Không đưa phần riêng của giáo viên và tệp vận hành nội bộ
(cd "$OUT" && tar --exclude=./teacher_private --exclude=./current --exclude=./smoke-final.pptx \
  --exclude=./HUONG_DAN_GIAO_VIEN.txt --exclude=./KE_HOACH_CONTEST.txt -cf - .) | (cd "$STAGE/site" && tar -xf -)
cp "$STAGE/site/START_HERE.html" "$STAGE/site/index.html"
cat > "$STAGE/wrangler.jsonc" <<'EOF'
{
  "name": "ai-canuc80k",
  "compatibility_date": "2026-10-06",
  "assets": { "directory": "site" }
}
EOF
cd "$STAGE" && npx -y wrangler@4 deploy
rm -rf "$STAGE/site"
