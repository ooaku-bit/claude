# /skill-new — 新スキル作成

繰り返し登場する作業パターンを新しいスキルとして登録する。

## 使い方

```
/skill-new <スキル名> <一行説明>
```

## 実行手順

1. **REGISTRY確認**: 類似スキルが存在しないか確認
   ```bash
   cat .claude/skills/REGISTRY.md
   ```

2. **ディレクトリ作成**
   ```bash
   mkdir -p .claude/skills/<スキル名>
   ```

3. **テンプレートからコピー**
   ```bash
   cp .claude/skills/_template/SKILL.md .claude/skills/<スキル名>/SKILL.md
   ```

4. **SKILL.mdを編集**: フロントマター・手順・成功基準を具体化

5. **REGISTRY更新**: `skills/REGISTRY.md` の一覧に追記

6. **コミット**
   ```bash
   git add .claude/skills/<スキル名>/
   git add .claude/skills/REGISTRY.md
   git commit -m "feat(skill): <スキル名> スキル追加"
   ```

## チェックリスト

- [ ] description がトリガー条件を含んでいる（システムがスキルを自動選択できる）
- [ ] 手順が具体的で再現可能
- [ ] 200行未満
- [ ] REGISTRYに追記済み
