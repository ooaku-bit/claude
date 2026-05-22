# /sync-settings

公式ソースから Claude Code の最新設定情報を強制取得し `docs/claude-code-latest.md` に反映します。

## 使い方
```
/sync-settings
```

## 実行内容
1. npm registry から `@anthropic-ai/claude-code` の最新バージョンを取得
2. Anthropic 公式ドキュメントから設定・フック情報を取得
3. `docs/claude-code-latest.md` を更新
4. 変更があれば commit してリポジトリに保存

```bash
python3 /home/user/claude/scripts/sync-claude-settings.py --force
```

実行後、変更をコミットしてください：
```bash
cd /home/user/claude
git add docs/claude-code-latest.md .claude/.sync-timestamp
git diff --cached --stat
```
