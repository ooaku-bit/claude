#!/bin/bash
# PII guard — detects personal information patterns in files being written
INPUT=$(cat)
TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
FILE=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# Skip source code files — focus on data files
case "$FILE" in
  *.py|*.js|*.ts|*.jsx|*.tsx|*.sh|*.bash|*.yaml|*.yml|*.md|*.html|*.css|*.go|*.rb|*.java|*.c|*.cpp|*.h|*.rs)
    exit 0 ;;
esac

# Extract content based on tool
case "$TOOL" in
  Write)  CONTENT=$(printf '%s' "$INPUT" | jq -r '.tool_input.content // empty' 2>/dev/null) ;;
  Edit)   CONTENT=$(printf '%s' "$INPUT" | jq -r '.tool_input.new_string // empty' 2>/dev/null) ;;
  *)      exit 0 ;;
esac

[ -z "$CONTENT" ] && exit 0

WARNINGS=()

# Japanese phone numbers: 03-1234-5678 / 090-1234-5678
if printf '%s' "$CONTENT" | grep -qE '0[0-9]{1,4}-[0-9]{1,4}-[0-9]{4}'; then
  WARNINGS+=("電話番号")
fi

# My Number (マイナンバー): 12-digit number
if printf '%s' "$CONTENT" | grep -qE '\b[0-9]{12}\b'; then
  WARNINGS+=("マイナンバー候補(12桁)")
fi

# Credit card: xxxx-xxxx-xxxx-xxxx
if printf '%s' "$CONTENT" | grep -qE '[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}'; then
  WARNINGS+=("クレジットカード番号候補")
fi

# Email addresses (exclude obvious test/example domains)
if printf '%s' "$CONTENT" | grep -qE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' && \
   ! printf '%s' "$CONTENT" | grep -qE '@(example|test|dummy|sample)\.(com|org|net|jp)'; then
  WARNINGS+=("メールアドレス")
fi

if [ ${#WARNINGS[@]} -gt 0 ]; then
  MSG=$(IFS=', '; echo "${WARNINGS[*]}")
  printf '{"systemMessage":"⚠️ 個人情報保護警告 [%s]: %s のパターンを検出しました。個人情報保護法の要件（利用目的・安全管理措置）を確認してください。ファイル: %s"}\n' \
    "$(date -u '+%H:%M:%SZ')" "$MSG" "$FILE"
fi
