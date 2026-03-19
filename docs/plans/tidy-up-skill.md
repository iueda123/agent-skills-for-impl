# tidy-up-skill — Phase 2 Plan Pack

## この文書の前提

- この文書は計画作成専用（未実装）
- Issue #1 の `docs/plans/tidy-up-skill/issues/*.md` を作るための指示をまとめる
- 実装は次フェーズで `/impl-single` または `/impl-multi` を使って行う

## 実行モード

- mode: `auto`
- manual: 下記 `text` ブロックを新規セッションに投入して使う
- auto: 下記 `text` ブロックの内容をこのセッションで順に実行し、個別計画書まで作成する

## 実行順序（Wave）

```text
Wave 1: #1
```

## Waveの進め方

1. Wave 1 の Issue について計画書を作る
2. 計画レビューが完了したら実装フェーズへ移る

---

## Wave 1

### Issue #1 feat: tidy-up スキルの新規作成

```text
技術計画モードで進めてください。
develop から plan/tidy-up-skill を作成して、Issue #1 の計画書を作ってください。

まず `gh issue view 1` で Issue を読んでください。
既存の .claude/skills/ 配下のスキル実装を読み、同じ設計パターンを前提に計画してください。

成果物として `docs/plans/tidy-up-skill/issues/1-tidy-up.md` を作成してください。
計画には以下を必ず含めてください。
1. 目的とスコープ（何をやる/やらない）
2. 現状整理（既存コード・既存文章・前提）
3. 実施ステップ（順序つき）
4. 変更対象（ファイルパス、または章・節の単位）
5. トレードオフと採用理由
6. リスクと回避策
7. 完了条件（DoD）
8. チェックボックス付き ToDo

不明点や不足情報は、作業開始前に質問として列挙してください。
まだ実装はしないでください。計画書の作成だけ行ってください。

将来の実行方法も末尾に1段落で記載してください。
- /impl-single または /impl-multi での実行想定
```

---

## 計画完了のチェックリスト

- [ ] `docs/plans/tidy-up-skill/issues/1-tidy-up.md` が作成済み
- [ ] 計画に ToDo がある
- [ ] 不明点が質問として洗い出されている
- [ ] 依存関係の矛盾がない
- [ ] 実装フェーズ移行可否を判断済み
