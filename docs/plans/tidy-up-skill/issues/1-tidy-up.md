# Issue #1 計画書: feat: tidy-up スキルの新規作成

> **まだ実装しないでください。この文書は計画書のみです。**

---

## 1. 目的とスコープ

### やること

- Claude Code スキル `tidy-up` を新規作成する
- 実装完了後の振り返りフローで呼び出し、計画と実装の整合性を記録する報告書を自動生成する
- 以下の3軸で整合性を確認する
  - GitHub Issue の DoD/タスク vs 実装コード
  - plan ファイル vs 実装コード
  - テスト実行結果（Java/Gradle）または整合性評価（R/Python/Bash/Markdown等）
- 報告書を PR コメントとして投稿する（識別子 `<!-- tidy-up-report -->` 付き）
- 報告書を `gh-pr-log/<number>/comments.md` にローカル保存する

### やらないこと

- 実装コードの修正・提案
- PR の作成・更新

---

## 2. 現状整理

### 既存スキル構成

`skills/` 配下（開発対象）と `.claude/skills/` 配下（利用対象）は対称構造をとる。

```
skills/{skill-name}/
  SKILL.md          # スキル定義（frontmatter + 手順）
  references/       # 参照テンプレート群（任意）
```

`SKILL.md` の frontmatter 形式:

```yaml
---
name: {skill-name}
description: |
  1〜3行の説明。
  スキルが発動するトリガー表現を含める。
---
```

### 設計パターン

- スキルは Markdown の手順書として実装し、Claude がそれを読んで実行する
- `gh` CLI・`git` コマンドを組み合わせて動作する
- テンプレートは `references/` に分離し、`SKILL.md` から参照する
- 複雑なワークフロー（ステップが多い、テンプレートが必要）は `references/` を活用する例として `create-plan` が参考になる

### 前提

- `gh` CLI 認証済み
- スキル呼び出しは PR 作成後（`/tidy-up` コマンド）
- 対象プロジェクト種別は多様で、プロジェクトによって Axis 3 の評価方法が変わる
  - Java アプリケーション: `./gradlew test`
  - R スクリプト（数値解析）: テスト機構なし → Issue/Plan との整合性評価
  - Python スクリプト（数値解析）: テスト機構なし → Issue/Plan との整合性評価
  - Bash スクリプト（画像処理）: テスト機構なし → Issue/Plan との整合性評価
  - Markdown 文書（学術論文）: テストなし → 章・節の構成・内容の整合性評価
- `tidy-up` スキル呼び出し時点でカレントブランチが feature ブランチであること

---

## 3. 実施ステップ（順序つき）

1. **報告書テンプレートを設計する**
   - 3軸チェック（Issue DoD、plan ファイル、テスト結果）の出力フォーマットを決定する
   - `skills/tidy-up/references/report-template.md` として定義する

2. **スキルディレクトリ・SKILL.md を作成する**
   - `skills/tidy-up/SKILL.md` を作成する
   - 以下のワークフローを記述する（§5 参照）

3. **`.claude/skills/` への同期**
   - `skills/tidy-up/` を `.claude/skills/tidy-up/` にコピーして利用可能にする
   - （既存スキルと同様の運用）

---

## 4. 変更対象

| ファイルパス | 操作 | 内容 |
|---|---|---|
| `skills/tidy-up/SKILL.md` | 新規作成 | スキル本体（ワークフロー定義） |
| `skills/tidy-up/references/report-template.md` | 新規作成 | 報告書テンプレート |
| `.claude/skills/tidy-up/SKILL.md` | 新規作成 | `skills/` からのコピー（利用可能化） |
| `.claude/skills/tidy-up/references/report-template.md` | 新規作成 | 同上 |

---

## 5. SKILL.md のワークフロー設計

### Step 1: 対象 PR の特定

- `gh pr view --json number,body` で PR 情報を取得
- PR 本文の `Closes #xxx` / `close #xxx` / `Fix #xxx` / `Resolves #xxx` 等から Issue 番号を正規表現で抽出
- 抽出した Issue 番号をユーザーに提示して確認を取る

### Step 2: 対象 plan ファイルの特定

- スキル呼び出し時の引数から plan ファイルパスを取得
- 引数がない場合: ユーザーに尋ねる（`docs/plans/` 配下を候補として提示）

### Step 3: Axis 1 — GitHub Issue vs 実装コード

- `gh issue view {number}` で Issue を取得し、DoD チェックリストを抽出
- 対象ブランチの差分（`git diff develop..HEAD`）を確認
- 各 DoD 項目について「実装済み / 未実装 / 不明」を判定する

### Step 4: Axis 2 — plan ファイル vs 実装コード

- 指定された plan ファイルを読む
- 計画書の「実施ステップ」「変更対象」「ToDo」と差分を照合する
- 計画からの逸脱・未実施項目を列挙する

### Step 5: Axis 3 — テスト実行 or 整合性評価

プロジェクト種別を自動検出し（`build.gradle` の有無など）、動作を切り替える。

**テスト実行モード（Java/Gradle）:**

- `./gradlew test` を実行する
- テスト結果（PASS/FAIL 件数、失敗テスト名）を取得する
- 失敗がある場合はその内容を報告書に含める

**整合性評価モード（R / Python / Bash / Markdown 等）:**

- テスト実行の代わりに、Issue・Plan と成果物の内容的整合性を評価する
- 確認観点の例:
  - 想定していた出力ファイル・図表・スクリプトが実際に存在するか
  - Markdown 文章の場合: 章・節の構成が plan の設計通りか
  - データ解析の場合: 使用データ・手法・出力形式が Issue/Plan の記述と一致するか
- 評価結果を「一致 / 逸脱 / 不明」で報告書に記載する

**種別判定ロジック（案）:**

| 条件 | 判定種別 |
|------|---------|
| `build.gradle` が存在する | Java/Gradle |
| `*.R` が主体 | R スクリプト |
| `*.py` が主体 | Python スクリプト |
| `*.sh` が主体 | Bash スクリプト |
| `*.md` が主体 | Markdown 文書 |
| 判定不能 | ユーザーに確認 |

### Step 6: 報告書生成・投稿

- `report-template.md` に沿って報告書を生成する
- `gh pr comment {number} --body "..."` で PR コメントとして投稿する（識別子 `<!-- tidy-up-report -->` を冒頭に付与）
- `gh-pr-log/{number}/comments.md` に同内容をローカル保存する
- `comments.md` 冒頭に「この内容は PR コメントとして GitHub 上に記録済みのため破棄しても構わない」旨を付記する

---

## 6. 報告書テンプレートの設計

```markdown
<!-- tidy-up-report -->
# tidy-up レポート

PR: #{number}
実行日時: {datetime}

## Axis 1: Issue DoD チェック

| # | DoD項目 | 状態 | 備考 |
|---|---------|------|------|
| 1 | {dod_item} | ✅ 実装済み / ❌ 未実装 / ❓ 不明 | {note} |

## Axis 2: plan ファイル整合性チェック

plan ファイル: `{plan_file_path}`

| ステップ | 状態 | 備考 |
|---------|------|------|
| {step} | ✅ 完了 / ❌ 未完了 / ➖ スコープ外 | {note} |

## Axis 3: テスト結果 / 整合性評価

プロジェクト種別: {project_type}

<!-- Java/Gradle の場合 -->
```
{gradle_test_output_summary}
```
- 合計: {total} 件 / 成功: {passed} 件 / 失敗: {failed} 件

<!-- テストなし（R/Python/Bash/Markdown等）の場合 -->
| 確認項目 | 状態 | 備考 |
|---------|------|------|
| {item} | ✅ 一致 / ❌ 逸脱 / ❓ 不明 | {note} |

## 総合評価

{overall_assessment}
```

---

## 7. トレードオフと採用理由

| 選択肢 | 採用理由 |
|--------|---------|
| `gh pr comment` で投稿（採用） | PR スレッドにインラインで記録でき、レビュアーが参照しやすい |
| Issue コメントで投稿 | PR との紐付けが薄くなる。不採用 |
| ローカルファイルのみ | GitHub 上に記録が残らない。不採用 |
| プロジェクト種別に応じて Axis 3 を切り替える（採用） | テストのないプロジェクト（R/Python/Bash/Markdown）でも整合性評価を提供できる |
| テストがない場合は Axis 3 をスキップ | 評価なしでは振り返りの価値が下がる。不採用 |

---

## 8. リスクと回避策

| リスク | 回避策 |
|--------|--------|
| `Closes #xxx` の抽出漏れ（大文字小文字、複数記法） | 正規表現で `close[sd]?`, `fix(e[sd])?`, `resolve[sd]?` をまとめてカバー |
| Gradle テストが長時間かかる | タイムアウト指定（例: `--tests` で絞り込みオプションをユーザーに提示） |
| プロジェクト種別の自動判定が誤る | 判定できない場合はユーザーに確認する。判定ロジックは種別表で管理し拡張しやすくする |
| plan ファイルが指定されない | Step 2 でユーザーに確認必須とする |
| PR コメント投稿に失敗する（auth エラー等） | エラー内容を表示し、ローカル保存には成功するよう切り離す |
| `develop` ブランチが存在しない | `git diff develop..HEAD` の代替として `git diff $(git merge-base HEAD origin/master)..HEAD` を使う |

---

## 9. 完了条件（DoD）

Issue #1 の DoD をそのまま記載:

- [ ] `tidy-up` スキルが `/tidy-up` コマンドで呼び出せる
- [ ] PR 本文から対象 Issue 番号を自動抽出できる
- [ ] GitHub Issue vs 実装コードの整合性チェックが動作する
- [ ] plan ファイルをスキル呼び出し時に指定でき、未指定時はスキルが尋ねる
- [ ] plan ファイル vs 実装コードの整合性チェックが動作する
- [ ] プロジェクト種別を自動検出し、Axis 3 の動作（テスト実行 or 整合性評価）を切り替えられる
- [ ] Java/Gradle プロジェクトでテストを実行し、結果を報告書に含められる
- [ ] テストのないプロジェクト（R/Python/Bash/Markdown等）で整合性評価を実施し、結果を報告書に含められる
- [ ] 報告書のフォーマット（テンプレート）が定義されている
- [ ] 報告書が PR コメントとして投稿される（識別子付き）
- [ ] `gh-pr-log/<number>/comments.md` にローカル出力される
- [ ] `comments.md` 冒頭に破棄可能である旨が付記されている

---

## 10. チェックボックス付き ToDo

### 計画フェーズ（このドキュメント）

- [x] ワークフロー設計（Step 1〜6）
- [x] 報告書テンプレート設計
- [x] 変更対象ファイルの列挙
- [x] トレードオフ整理
- [x] リスクと回避策の洗い出し

### 実装フェーズ（次フェーズで実施）

- [ ] `skills/tidy-up/references/report-template.md` を作成する
- [ ] `skills/tidy-up/SKILL.md` を作成する（ワークフロー全ステップ記述）
- [ ] プロジェクト種別判定ロジックを設計し `SKILL.md` に記述する
- [ ] `./gradlew test` 実行のコマンドとオプションを実際のプロジェクトで確認する
- [ ] 整合性評価モードの確認観点リストを `report-template.md` に定義する
- [ ] `.claude/skills/tidy-up/` に同期する
- [ ] 動作確認: `/tidy-up` コマンドで呼び出せることを確認する
- [ ] 動作確認: Issue 番号の自動抽出が動作することを確認する
- [ ] 動作確認: plan ファイル未指定時にユーザーへの確認が行われることを確認する
- [ ] 動作確認: 報告書が PR コメントとして投稿されることを確認する

---

## 11. 作業前に確認すべき質問

1. **Gradle プロジェクトのルートパス**: テスト対象プロジェクトで `./gradlew test` を実行するディレクトリはどこか？スキルは作業ディレクトリを固定して実行するか、ユーザーに尋ねるか？
2. **`develop` ブランチの扱い**: `git diff develop..HEAD` を使う想定だが、`develop` が存在しないリポジトリでの fallback 動作はどうするか？（現リポジトリは `master` のみ）
3. **既存の PR コメント更新**: 同一 PR に複数回 `/tidy-up` を実行した場合、コメントを新規追加するか上書き（edit）するか？
4. **plan ファイルの指定形式**: 引数として受け取るのはファイルパスのみか、`docs/plans/` からの相対パスか？

---

## 12. 将来の実行方法

このスキルの実装は単一ファイルの新規作成が中心であり、他スキルへの依存もないため `/impl-single` による単一ツリー実装が適している。実装フェーズでは `develop` ブランチから `feat/tidy-up-skill` ブランチを切り、`SKILL.md` と `report-template.md` を作成し、動作確認後に PR を作成する流れを推奨する。
