#!/usr/bin/env bash
# セッション開始時に公式から Claude Code 設定を自動同期
# 24時間以内の同期はスキップされる（sync-claude-settings.py 内判定）
python3 /home/user/claude/scripts/sync-claude-settings.py 2>&1 | \
    sed 's/^/[session-start] /' || true
