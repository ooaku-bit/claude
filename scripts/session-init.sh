#!/bin/bash
# Run on every SessionStart to validate and repair workspace structure.

REPO_DIR="/home/user/claude"
LOG_FILE="$REPO_DIR/scripts/session.log"

ts() { date "+%Y-%m-%d %H:%M:%S"; }
log() { echo "$(ts) $*" | tee -a "$LOG_FILE"; }

log "[SessionStart] Initializing workspace..."

# Ensure scripts are executable
for script in "$REPO_DIR/scripts/"*.sh; do
    [ -f "$script" ] && chmod +x "$script"
done

# Validate Stop hook target exists
HOOK_REF=$(grep -o '"command": "bash [^"]*"' "$REPO_DIR/.claude/settings.json" 2>/dev/null | awk '{print $3}' | tr -d '"')
if [ -n "$HOOK_REF" ] && [ ! -f "$HOOK_REF" ]; then
    log "[WARN] Stop hook target not found: $HOOK_REF"
else
    log "[OK] Stop hook target verified."
fi

# Check for uncommitted changes from previous session
cd "$REPO_DIR" || exit 1
STAGED=$(git diff --cached --name-only 2>/dev/null)
UNSTAGED=$(git diff --name-only 2>/dev/null)
if [ -n "$STAGED" ] || [ -n "$UNSTAGED" ]; then
    log "[WARN] Uncommitted changes detected. Review before proceeding."
fi

# Show current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
log "[OK] Branch: $BRANCH"
log "[SessionStart] Done."
