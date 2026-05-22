#!/bin/bash
# Compliance audit log — records all Bash/Write/Edit/Read operations
INPUT=$(cat)
TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
LOG=/home/user/claude/.claude/audit.log

case "$TOOL" in
  Bash)
    CMD=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
    [ -n "$CMD" ] && printf '[%s] BASH: %s\n' "$TIMESTAMP" "$CMD" >> "$LOG"
    ;;
  Write|Edit)
    FILE=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
    [ -n "$FILE" ] && printf '[%s] %s: %s\n' "$TIMESTAMP" "$TOOL" "$FILE" >> "$LOG"
    ;;
  Read)
    FILE=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
    [ -n "$FILE" ] && printf '[%s] READ: %s\n' "$TIMESTAMP" "$FILE" >> "$LOG"
    ;;
esac
