#!/bin/bash
# Auto-push committed changes on session stop
cd /home/user/claude || exit 0
BRANCH=$(git branch --show-current 2>/dev/null)
[ -z "$BRANCH" ] && exit 0

# Only push if there are commits ahead of remote
AHEAD=$(git rev-list "origin/$BRANCH..HEAD" 2>/dev/null | wc -l)
if [ "$AHEAD" -gt 0 ]; then
  git push -u origin "$BRANCH" 2>/dev/null || true
fi
