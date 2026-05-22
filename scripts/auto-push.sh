#!/bin/bash
# Push committed changes to origin after Claude stops.
# Only pushes if local is ahead of remote — never force-pushes.

REPO_DIR="/home/user/claude"
LOG_FILE="$REPO_DIR/scripts/push.log"

ts() { date "+%Y-%m-%d %H:%M:%S"; }

BRANCH=$(git -C "$REPO_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -z "$BRANCH" ]; then
    echo "$(ts) [SKIP] Not a git repo or no branch." >> "$LOG_FILE"
    exit 0
fi

LOCAL=$(git -C "$REPO_DIR" rev-parse HEAD 2>/dev/null)
REMOTE=$(git -C "$REPO_DIR" rev-parse "origin/$BRANCH" 2>/dev/null)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "$(ts) [OK] Nothing to push on $BRANCH." >> "$LOG_FILE"
    exit 0
fi

git -C "$REPO_DIR" push -u origin "$BRANCH" >> "$LOG_FILE" 2>&1
STATUS=$?
if [ $STATUS -eq 0 ]; then
    echo "$(ts) [OK] Pushed $BRANCH to origin." >> "$LOG_FILE"
else
    echo "$(ts) [ERROR] Push failed (exit $STATUS)." >> "$LOG_FILE"
fi
exit $STATUS
