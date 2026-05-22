# /knowledge-add — ナレッジ即時追加

作業中に気づいた学びをすぐに記録する。後回しにすると忘れる。

## 使い方

```
/knowledge-add pattern   # パターンを追加
/knowledge-add decision  # 設計決定を記録（ADR作成）
/knowledge-add learning  # スキル学習を記録
```

## 実行手順（パターン）

1. `.claude/knowledge/patterns/PATTERNS.md` を開く
2. 以下の形式で追記:
   ```markdown
   ### [パターン名]
   **状況**: 
   **解決策**: 
   **注意**: 
   **出典**: YYYY-MM-DD
   ```
3. `INDEX.md` のパターン件数を +1

## 実行手順（設計決定 ADR）

1. 既存ADRの最大連番を確認: `ls .claude/knowledge/decisions/`
2. `ADR-NNNN-タイトル.md` を作成（テンプレートは `decisions/README.md` 参照）
3. `decisions/README.md` の一覧に追記
4. `INDEX.md` の決定記録件数を +1

## 実行手順（スキル学習）

1. `.claude/knowledge/skill-learnings/README.md` に追記:
   ```markdown
   ## <スキル名> — YYYY-MM-DD
   **コンテキスト**: 
   **うまくいったこと**: 
   **うまくいかなかったこと**: 
   **提案する変更**: 
   ```
2. `INDEX.md` のスキル学習件数を +1
3. 蓄積量が多い場合は `/retro` で `skill-compose` に引き継ぐ
