# Plan Template For Issues

複数 Issue の計画作成を 1 ファイルにまとめるためのテンプレート。
`manual`（プロンプト集として利用）と `auto`（同一セッションで直接生成）の両方に対応する。

## 目的

- 直列/並列の実行順序を先に明示する
- 各 Issue の計画作成指示を同じ構造で並べる
- 計画フェーズ（未実装）であることを全体に徹底する

## 出力フォーマット

````markdown
# {プロジェクト名} — Phase 2 Plan Pack

## この文書の前提

- この文書は計画作成専用（未実装）
- 各 Issue の `docs/plans/{name}/issues/*.md` を作るための指示をまとめる
- 実装は次フェーズで `/impl-single` または `/impl-multi` を使って行う

## 実行モード

- mode: `{manual|auto}`
- manual: 下記 `text` ブロックを新規セッションに投入して使う
- auto: 下記 `text` ブロックの内容をこのセッションで順に実行し、個別計画書まで作成する

## 実行順序（Wave）

```text
Wave 1（直列）: #12 → #13
Wave 2（並列）: #14, #15
Wave 3: #16
```

## Waveの進め方

1. Wave 1 の Issue について計画書を作る
2. Wave 1 の計画レビューが完了したら Wave 2 に進む
3. 並列 Wave は担当を分けて同時に進める
4. すべての計画レビューが完了したら実装フェーズへ移る

---

## Wave 1（直列）

### Issue #12 {Issueタイトル}

```text
{Issue #12 向け計画作成指示}
```

### Issue #13 {Issueタイトル}

```text
{Issue #13 向け計画作成指示}
```

---

## Wave 2（並列 2本）

### Issue #14 {Issueタイトル}

```text
{Issue #14 向け計画作成指示}
```

### Issue #15 {Issueタイトル}

```text
{Issue #15 向け計画作成指示}
```

---

## Wave 3

### Issue #16 {Issueタイトル}

```text
{Issue #16 向け計画作成指示}
```

---

## 計画完了のチェックリスト

- [ ] 全Issueで `docs/plans/{name}/issues/*.md` が作成済み
- [ ] 各計画に ToDo がある
- [ ] 不明点が質問として洗い出されている
- [ ] 依存関係の矛盾がない
- [ ] 実装フェーズ移行可否を判断済み
````

## Wave表記ルール

- 直列: `#A → #B`（A完了後にB）
- 並列: `#A, #B, #C`（同時進行可）
- 並列 N本: 見出しに本数を記載（例: `Wave 2（並列 3本）`）
- 1件だけの Wave は `Wave 3` のように簡潔表記

## 記述ルール

- 各 Issue 指示は [plan-template-for-an-issue.md](plan-template-for-an-issue.md) 準拠
- 実装指示（コード変更・PR作成）は含めない
- ユーザーが注釈レビューしやすいよう、見出し構造を固定する
