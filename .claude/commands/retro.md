# /retro — セッション振り返り

セッション終了時に振り返りを記録し、ナレッジベースを更新する。

## 実行手順

1. **セッション内容を確認**
   ```bash
   git log --oneline --since="8 hours ago"
   git diff HEAD~5..HEAD --stat 2>/dev/null || git diff --stat
   ```

2. **振り返りファイルを作成**
   - ファイル名: `.claude/knowledge/retrospectives/YYYY-MM-DD-<概要>.md`
   - テンプレート: `.claude/knowledge/retrospectives/README.md` 参照

3. **パターン化できる学びを抽出**
   - 再利用できそうなものは `patterns/PATTERNS.md` に追記

4. **スキルフィードバックを記録**
   - 使ったスキルへの知見を `skill-learnings/README.md` に追記

5. **INDEX統計を更新**
   - `.claude/knowledge/INDEX.md` のカウントを更新

6. **コミット**
   ```bash
   git add .claude/knowledge/
   git commit -m "retro: YYYY-MM-DD セッション振り返り"
   ```

## 振り返りテンプレート

```markdown
# 振り返り: YYYY-MM-DD — <タスク概要>

## やったこと
- 

## うまくいったこと (Keep)
- 

## 改善したいこと (Problem)
- 

## 次回試すこと (Try)
- 

## スキルへのフィードバック
- <スキル名>: 
```
