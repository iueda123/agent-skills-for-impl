---
name: tidy-up
description: |
  実装完了後の振り返りフローで呼び出す。
  GitHub Issue DoD・plan ファイル・テスト結果（またはプロジェクト整合性）の3軸で
  実装との整合性を確認し、報告書を PR コメントとして投稿する。
  `/tidy-up` または「tidy-up して」で発動。
---

# tidy-up Workflow

このスキルは **PR 作成後** に呼び出す。
実装コードの修正・提案・PR の作成/更新は行わない。

引数として plan ファイルパスを受け取ることができる。例: `/tidy-up docs/plans/foo/issues/1-bar.md`

---

## Step 1: 対象 PR の特定

```bash
gh pr view --json number,title,body,headRefName
```

- PR 本文の `Closes #xxx` / `closes #xxx` / `close #xxx` / `Fix #xxx` / `Resolves #xxx` 等から Issue 番号を正規表現で抽出する
  - パターン: `(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#(\d+)` (大文字小文字無視)
- 抽出した Issue 番号とブランチ名をユーザーに提示して確認を取る
- Issue が複数ある場合はすべて列挙し、対象を確認する

確認メッセージ例:
```
PR #42「feat: tidy-up スキルの新規作成」を対象にします。
関連 Issue: #1
よろしいですか？
```

---

## Step 2: plan ファイルの特定

- スキル呼び出し時の引数（例: `/tidy-up docs/plans/foo/issues/1-bar.md`）が指定されている場合はそれを使う
- 引数がない場合: `docs/plans/` 配下の `*.md` を列挙して候補を提示し、ユーザーに選んでもらう

```bash
find docs/plans -name "*.md" | sort
```

確認メッセージ例:
```
plan ファイルを指定してください。
候補:
- docs/plans/tidy-up-skill/issues/1-tidy-up.md
- docs/plans/other-feature/issues/2-foo.md
```

---

## Step 3: Axis 1 — GitHub Issue vs 実装コード

```bash
gh issue view {issue_number} --json title,body
```

- Issue 本文から DoD チェックリスト（`- [ ]` または `- [x]`）を抽出する
- 対象ブランチの差分を確認する:

```bash
# develop ブランチが存在する場合
git diff develop..HEAD --stat
git diff develop..HEAD

# develop が存在しない場合の fallback
git diff $(git merge-base HEAD origin/master)..HEAD --stat
git diff $(git merge-base HEAD origin/master)..HEAD
```

- 差分を読み、各 DoD 項目について「✅ 実装済み / ❌ 未実装 / ❓ 不明」を判定する
- 判定できない場合は ❓ とし、備考に理由を記載する

---

## Step 4: Axis 2 — plan ファイル vs 実装コード

- Step 2 で特定した plan ファイルを読む
- 「実施ステップ」「変更対象」「ToDo」の各項目と差分を照合する
- 計画からの逸脱・未実施項目を列挙する
- 状態は「✅ 完了 / ❌ 未完了 / ➖ スコープ外」で記録する

---

## Step 5: Axis 3 — テスト実行 or 整合性評価

まずプロジェクト種別を自動検出する:

```bash
# build.gradle の存在確認
ls build.gradle 2>/dev/null && echo "gradle"

# 主要ファイル種別の確認（対象ブランチの変更ファイルから推定）
git diff develop..HEAD --name-only 2>/dev/null || git diff $(git merge-base HEAD origin/master)..HEAD --name-only
```

| 条件 | 判定種別 |
|------|---------|
| `build.gradle` が存在する | Java/Gradle |
| 変更ファイルに `*.R` が多い | R スクリプト |
| 変更ファイルに `*.py` が多い | Python スクリプト |
| 変更ファイルに `*.sh` が多い | Bash スクリプト |
| 変更ファイルに `*.md` が多い | Markdown 文書 |
| 判定不能 | ユーザーに確認 |

### テスト実行モード（Java/Gradle）

```bash
./gradlew test
```

- テスト結果（PASS/FAIL 件数、失敗テスト名）を取得する
- 実行時間が長い場合はユーザーに通知する

### 整合性評価モード（R / Python / Bash / Markdown 等）

Issue・Plan の記述と成果物の整合性を評価する。
[references/report-template.md](references/report-template.md) の「整合性評価モードの確認観点」を参考に確認項目を列挙し、各項目を「✅ 一致 / ❌ 逸脱 / ❓ 不明」で評価する。

確認観点の例:
- 想定していた出力ファイル・図表・スクリプトが存在するか
- 使用データ・手法・出力形式が Issue/Plan の記述と一致するか
- Markdown 文書の場合: 章・節の構成が plan の設計通りか
- スクリプトの場合: 主要な処理ステップが意図通りか

---

## Step 6: 報告書生成・投稿

1. [references/report-template.md](references/report-template.md) に従い報告書を生成する
2. PR コメントとして投稿する（識別子 `<!-- tidy-up-report -->` を冒頭に付与）:

```bash
gh pr comment {number} --body "$(cat <<'REPORT'
{報告書の内容}
REPORT
)"
```

3. `gh-pr-log/{number}/` ディレクトリを作成し、`comments.md` にローカル保存する:

```bash
mkdir -p gh-pr-log/{number}
```

`gh-pr-log/{number}/comments.md` の冒頭に次の注記を付ける:

```
> この内容は PR コメントとして GitHub 上に記録済みのため、このファイルは破棄しても構いません。
```

4. 投稿完了後、PR コメントの URL または投稿確認メッセージをユーザーに表示する

---

## エラーハンドリング

- `develop` ブランチが存在しない場合: `git merge-base HEAD origin/master` を使う
- PR コメント投稿に失敗した場合: エラー内容を表示し、ローカル保存は独立して実施する
- `gh pr view` で PR が見つからない場合: 現在ブランチの PR を確認し、なければユーザーに PR 番号を入力してもらう
- プロジェクト種別の自動判定が不明な場合: 判定理由をユーザーに説明してから確認を取る
