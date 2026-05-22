---
name: testing
description: テストを作成・実行する。describe + it + AAAパターンを使用し、ファクトリーモックを活用する。
allowed tools: Read, Bash, Edit, Write
---

# Testing Skill

## テストパターン

- `describe` + `it` + AAA (Arrange / Act / Assert) パターン
- ファクトリーモックを使用
- エッジケースを必ずカバー

## 手順

1. テスト対象のコードを `Read` で確認
2. テストケースを洗い出し（正常系・異常系・境界値）
3. テストファイルを作成・更新
4. テストを実行して全件パスを確認

## テンプレート

```python
def test_機能名_条件_期待結果():
    # Arrange
    ...
    # Act
    result = ...
    # Assert
    assert result == expected
```
