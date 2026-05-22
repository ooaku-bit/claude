# Claude Code Workspace

Claude Code の自動化・運用ワークスペース。

## 構成

| パス | 用途 |
|------|------|
| `.claude/settings.json` | 権限・フック設定 |
| `.claude/skills/` | スキル定義（`/skill-name` で呼び出し） |
| `.claude/commands/` | カスタムスラッシュコマンド |
| `.claude/agents/` | サブエージェント定義 |
| `scripts/auto-push.sh` | Stopフック: コミット済み変更を自動push |
| `scripts/session-init.sh` | SessionStartフック: 環境整合性チェック |
| `scripts/auto-sync.ps1` | Windows用: GitHubから自動pull |
| `scripts/setup-task-scheduler.ps1` | Windows用: タスクスケジューラ登録 |

## 自動化フロー

```
SessionStart → session-init.sh（構成チェック・権限修復）
Stop         → auto-push.sh（未プッシュコミットを自動push）
```

## ローカル設定（gitignored）

- `.claude/settings.local.json` — マシン固有の設定
- `.claude/hooks/` — マシン固有のフック
- `scripts/push.log` / `scripts/session.log` — 実行ログ
