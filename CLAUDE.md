# Claude Code Workspace

## プロジェクト概要
Claude Code の自動化・運用ワークスペース。

## アーキテクチャ / Architecture

```
/
├── CLAUDE.md            # プロジェクトルール（このファイル）
├── .claude/
│   ├── settings.json    # 権限・フック設定（gitignored）
│   ├── skills/          # スキル定義
│   ├── commands/        # カスタムコマンド
│   └── agents/          # エージェント定義
└── .gitignore
```

## ワークフロールール / Workflow Rules

- **Plan Modeを使う**: 調査と実装を明確に分離する
- **小さく実装してすぐ検証**: 小さく → 検証 → 改善を繰り返す
- **TodoリストでWork管理**: 優先順位と進捗を常に明確に
- **Commit頻繁に**: 一度に1タスクに集中し、完了したらすぐコミット
- **ブランチ戦略**: `main` / `feature/*` / `spike/*` を使い分ける
- **/compactを定期的に**: コンテキストを圧縮して余白を確保

## コンテキスト管理

- 重要な情報・ルール・約束事は必ずこのCLAUDE.mdに書く
- サブフォルダには `.claude/` や `CLAUDE.md` を追加してローカルコンテキストを追加
- 各ファイルは200行未満に保つ
- `/compact` は戻せないので事前にCLAUDE.mdへ退避

## セキュリティ

- `.env` ファイルや認証情報は絶対にコミットしない
- 外部副作用（DB操作・API呼び出し）は必ず確認してから実行
- `sudo` コマンドは原則禁止
