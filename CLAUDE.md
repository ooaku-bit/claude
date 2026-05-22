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

## 経営者サポート部署構成 / Executive Support Structure

### エージェント（.claude/agents/）
| エージェント | 部署名 | 役割 |
|---|---|---|
| executive-secretary | 秘書室 | 文書起草・議事録・要約・スケジュール整理 |
| strategy-analyst | 経営企画室 | 事業分析・戦略立案・KPI設計・競合調査 |
| risk-advisor | リスク管理室 | リスク洗い出し・契約確認・コンプライアンス |
| pr-director | 広報室 | プレスリリース・スピーチ・SNS・危機対応文 |
| security-reviewer | セキュリティ審査室 | OWASP準拠コードセキュリティレビュー |

### スキル（.claude/skills/）
| スキル | 用途 |
|---|---|
| report-writing | 経営レポート・月次報告書作成 |
| meeting-prep | 会議準備・アジェンダ・議事録 |
| market-research | 市場・競合・トレンド調査 |
| risk-assessment | リスクマトリクス評価・対策立案 |
| press-release | 広報文書・スピーチ原稿作成 |

### コマンド（.claude/commands/）
| コマンド | 用途 |
|---|---|
| /brief | 今日の経営ブリーフィングシート作成 |
| /minutes | 議事録の即時作成 |
| /report | 経営レポート（月次・週次・案件）作成 |
| /research | 市場・競合調査レポート作成 |
| /press | プレスリリース・広報文作成 |
| /deploy | デプロイ前チェックリスト実行 |

## セキュリティ

- `.env` ファイルや認証情報は絶対にコミットしない
- 外部副作用（DB操作・API呼び出し）は必ず確認してから実行
- `sudo` コマンドは原則禁止
