#!/usr/bin/env bash
# セッション終了時に変更を自動コミット & プッシュ
set -euo pipefail

REPO=/home/user/claude
cd "$REPO"

# 変更がなければ終了
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "[auto-push] 変更なし。スキップ。"
    exit 0
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
TS=$(date '+%Y-%m-%d %H:%M')

git add -A
git commit -m "auto: セッション終了時の自動保存 (${TS})"

# リトライ付きプッシュ (exponential backoff)
for wait in 2 4 8 16; do
    if git push -u origin "$BRANCH"; then
        echo "[auto-push] push 完了: $BRANCH"
        exit 0
    fi
    echo "[auto-push] push 失敗。${wait}秒後にリトライ..."
    sleep "$wait"
done

echo "[auto-push] push 失敗 (4回リトライ後)。" >&2
exit 1
