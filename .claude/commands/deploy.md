# Deploy Command

デプロイ前チェックリストを実行し、安全にデプロイする。

## 手順

1. **テスト実行**: 全テストがパスすることを確認
2. **Lint**: コード品質チェック
3. **セキュリティ**: 機密情報がコミットされていないか確認
4. **ブランチ確認**: `main` または `release/*` ブランチであることを確認
5. **変更差分確認**: `git diff main` で変更内容を最終確認
6. **タグ付け**: バージョンタグを付与
7. **プッシュ**: リモートにプッシュ

## 実行コマンド例

```bash
# テスト
npm test

# Lint
npm run lint

# 機密情報チェック
git diff --name-only | xargs grep -l "SECRET\|PASSWORD\|API_KEY" 2>/dev/null && echo "WARNING: Possible secrets found"

# タグ付け & プッシュ
git tag -a v$(date +%Y%m%d) -m "Release $(date +%Y-%m-%d)"
git push -u origin HEAD --tags
```
