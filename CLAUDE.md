# Claude Code Workspace

## プロジェクト概要
Claude Code の自動化・運用ワークスペース。

## アーキテクチャ / Architecture

```
/
├── CLAUDE.md            # プロジェクトルール（このファイル）
├── README.md            # リポジトリ概要
├── .claude/
│   ├── settings.json    # 権限・フック設定（コミット済み）
│   ├── settings.local.json  # ローカル専用設定（gitignored）
│   ├── hooks/           # ローカル専用フック（gitignored）
│   ├── skills/          # スキル定義
│   ├── commands/        # カスタムコマンド（スラッシュコマンド）
│   └── agents/          # サブエージェント定義
├── scripts/             # 自動化スクリプト
│   ├── auto-push.sh     # Stopフック: 未プッシュコミットを自動push
│   ├── auto-sync.ps1    # Windows: GitHubから自動pull
│   └── setup-task-scheduler.ps1  # Windows: タスクスケジューラ設定
└── .gitignore
```

## ワークフロールール / Workflow Rules

- **Plan Modeを使う**: 調査と実装を明確に分離する
- **小さく実装してすぐ検証**: 小さく → 検証 → 改善を繰り返す
- **TodoリストでWork管理**: 優先順位と進捗を常に明確に
- **Commit頻繁に**: 一度に1タスクに集中し、完了したらすぐコミット
- **ブランチ戦略**: `master` / `feature/*` / `spike/*` を使い分ける
- **/compactを定期的に**: コンテキストを圧縮して余白を確保

## コンテキスト管理

- 重要な情報・ルール・約束事は必ずこのCLAUDE.mdに書く
- サブフォルダには `.claude/` や `CLAUDE.md` を追加してローカルコンテキストを追加
- 各ファイルは200行未満に保つ
- `/compact` は戻せないので事前にCLAUDE.mdへ退避

## 自律最適化ルール / Self-Optimization Rules

この構成は常に自律的に最適な状態を維持する。以下のルールを自動的に適用すること。

### 構成変更時の必須作業
- ファイル・フォルダを追加/削除した場合 → **このCLAUDE.mdのアーキテクチャ図を即座に更新**
- `settings.json` のフック参照を変更した場合 → **参照先スクリプトが存在することを確認**
- スクリプトを追加した場合 → **実行権限（chmod +x）を付与し、scripts/ に配置**
- gitignore に追加した場合 → **CLAUDE.mdの該当箇所にも反映**

### 定期チェック項目（セッション開始時）
- `scripts/session-init.sh` が自動実行され、構成の整合性を検証する
- ログは `scripts/session.log` / `scripts/push.log` に蓄積される

### 構成最適化の判断基準
- **壊れた参照は即修正**: settings.jsonのフックが存在しないファイルを指していたら直す
- **ドキュメントと実態の乖離は即修正**: CLAUDE.mdが現実と合わなくなったら更新する
- **スクリプトはscripts/に集約**: ルートや.claude/直下にスクリプトを置かない

## セキュリティ

- `.env` ファイルや認証情報は絶対にコミットしない
- 外部副作用（DB操作・API呼び出し）は必ず確認してから実行
- `sudo` コマンドは原則禁止
