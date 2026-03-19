---
name: create-plan
description: |
  GitHub Issue群から、Phase 2: Plan（計画のみ・未実装）用の実行プロンプト集を生成するスキル。
  「開発計画を作成して」「実行プロンプトを生成して」「create-planを作って」「プロンプト集を作って」
  「並列開発の計画を立てて」などのリクエストで発動。
  Issue番号リストを受け取り、依存関係のWave構造を対話で決定し、
  各Issueの plan 作成プロンプトを docs/plans/*.md に出力する。
---

# Create Plan — Phase 2 (Plan Only) Prompt Generator

GitHub Issue から Claude Code 用の「計画作成プロンプト集」を生成する。
このスキルの責務は計画書作成まで。**実装はしない**。

## 目的

- 各 Issue ごとに「plan を書かせるための実行プロンプト」を生成する
- 依存関係に基づく Wave（直列/並列）を明示する
- そのまま Claude セッションへ投入できる形で `docs/plans/*.md` にまとめる

## ワークフロー

### Step 1: Issue番号リストの取得

引数から Issue番号を抽出する。以下の形式を受け付ける。

- 範囲指定: `#3-10` → #3, #4, #5, #6, #7, #8, #9, #10
- カンマ区切り: `#2, #3, #4, #5`
- スペース区切り: `2 3 4 5`
- 混合: `#2, #4-8, #13` → #2, #4, #5, #6, #7, #8, #13

`#` プレフィックスは有無どちらでもOK。

引数がない場合は確認する。

```text
対象のIssue番号を教えてください（例: #3-10, #2,#4,#5）
```

### Step 2: Issue内容の取得

各 Issue の内容を `gh issue view N` で取得し、以下を抽出する。

- タイトル
- 本文（補足ドキュメント参照、既存コード参考、制約事項）
- 完了条件（DoD）の有無

### Step 3: plan用ブランチ名の自動生成

Issue タイトルから `plan/xxx` 形式のブランチ名を生成する。

ルール:

- 日本語タイトルは英訳してケバブケースに変換
- 例: 「データモデル変更」→ `plan/data-model`
- 例: 「ベンダー見積依頼画面」→ `plan/vendor-quotes`

### Step 4: ベースブランチの確認

確認する。

```text
ベースブランチはどれにしますか？（develop / main / その他）
```

### Step 5: Wave構造の提案と確定

1. Issue内容から依存関係を分析し、Wave構造を提案する
2. 提案は必ずユーザー確認してから確定する

提案例:

```text
Wave 1（直列）: #2 → #3
Wave 2（並列）: #4, #5, #6
Wave 3（並列）: #7, #8
```

判断基準:

- DB/スキーマ/基盤変更は前の Wave に置く
- 共通 UI/共通ライブラリ改修は早い Wave に置く
- 独立した作業（別画面・別章など）は並列化する
- 明示的依存（「〜の上に追加」「〜完了後」）は後ろに置く

### Step 6: 各Issueの plan 作成プロンプト生成

各 Issue に対し [references/plan-template-for-an-issue.md](references/plan-template-for-an-issue.md) を使ってプロンプトを生成する。

Issue 本文から以下を抽出して埋め込む。

- 補足ドキュメント: `docs/*.md`, `research*.md`, `plan*.md`, `SPEC-*`
- 既存コード参照: `src/`, `app/`, `main/java/` など
- 技術制約・方針（例: Java版、使用ライブラリ、論文フォーマット）

該当する記述がなければ該当行は省略する。

### Step 7: 実行順序つき計画書として出力

出力ファイル名を確認する。

```text
出力ファイル名を教えてください（例: docs/plans/project-x.md）
```

デフォルトは `docs/plans/{プロジェクト名}.md`。

出力構造は [references/plan-template-for-issues.md](references/plan-template-for-issues.md) を使う。

## ルール

- **実装は禁止**。このスキルは計画書作成だけを扱う
- 生成プロンプトには「まだ実装しないでください」を必ず含める
- Issue本文にない情報は推測で確定しない
- Wave構造はユーザー確認前に確定しない
- 後続フェーズの整合性として、必要に応じて `/impl-single` または `/impl-multi` への接続を明記する
- `gh` CLI が認証済みであることを前提とする
