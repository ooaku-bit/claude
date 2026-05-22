# Claude Code Workspace

## プロジェクト概要
Claude Code の自動化・運用ワークスペース。

## アーキテクチャ / Architecture

```
/
├── CLAUDE.md            # プロジェクトルール（このファイル）
├── .claude/
│   ├── settings.json    # 権限・フック設定
│   ├── hooks/
│   │   └── auto-push.sh # Stop時の自動コミット&プッシュ
│   ├── skills/
│   │   ├── REGISTRY.md        # スキル索引（必ず最新に保つ）
│   │   ├── _template/         # 新スキル作成テンプレート
│   │   ├── code-review/
│   │   ├── testing/
│   │   ├── knowledge-capture/ # 学びをナレッジベースへ記録
│   │   └── skill-compose/     # スキル作成・改善
│   ├── commands/
│   │   ├── deploy.md
│   │   ├── retro.md           # /retro: セッション振り返り
│   │   ├── skill-new.md       # /skill-new: 新スキル作成
│   │   └── knowledge-add.md   # /knowledge-add: ナレッジ追加
│   ├── agents/
│   │   └── security-reviewer.md
│   └── knowledge/             # 組織ナレッジベース
│       ├── INDEX.md           # 全ナレッジの索引
│       ├── decisions/         # ADR（設計決定記録）
│       ├── patterns/          # 再利用可能なパターン集
│       ├── retrospectives/    # セッション振り返り
│       └── skill-learnings/   # スキル改善フィードバック
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

## ナレッジ管理ルール

- **気づいたらすぐ記録**: `/knowledge-add` で即時追記（後回し禁止）
- **セッション終了前に `/retro`**: 学びを振り返り・スキルフィードバックを記録
- **スキルREGISTRYを正とする**: スキル追加・更新時は `skills/REGISTRY.md` を必ず更新
- **スキル改善ループ**: `skill-learnings/` → `skill-compose` スキル → スキル更新

### ナレッジ改善サイクル

```
タスク実行
  → /knowledge-add でパターン・決定・学びを記録
  → /retro でセッション振り返りをまとめる
  → skill-compose スキルでスキルを改善
  → REGISTRYを更新して次のセッションへ
```

## セキュリティ

- `.env` ファイルや認証情報は絶対にコミットしない
- 外部副作用（DB操作・API呼び出し）は必ず確認してから実行
- `sudo` コマンドは原則禁止
