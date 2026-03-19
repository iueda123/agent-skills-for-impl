---
name: refine-issue
description: |
  既存のGitHub Issueを一覧表示し、対象IssueをローカルのMarkdownファイルへ書き出し、
  Claude と対話しながら Markdown 編集を支援し、最後に GitHub へ反映するスキル。
  `/refine-issue`、`Issueを修正したい`、`Issueに追記したい`、`IssueをMarkdownで編集したい`
  のような依頼で使う。`/create-issue` 後の追記・修正フローに使う。
---

# Issue Refine

既存の GitHub Issue をローカル Markdown に落とし、Claude が編集作業を対話で支援しながら GitHub 上の Issue を更新する。

コマンドはこの `SKILL.md` があるディレクトリ（`skills/refine-issue/`）を基準に実行する。

## ワークフロー

### Step 1: 対象Issueを決める

Issue番号が指定されていればそれを使う。
指定がなければ、まず一覧を表示する。

```bash
python3 scripts/issue_refine.py list
```

必要に応じて `--state all` や `--limit 100` を付ける。
一覧を見せたら、ユーザーに Issue 番号を選ばせる。

### Step 2: IssueをMarkdownに書き出す

まず、対象 Issue に対応するローカル Markdown が残っていないか確認する。

```bash
python3 scripts/issue_refine.py local 123
```

`gh-issues/{number}/*.md` が存在する場合は、必ず次の趣旨で確認する。

```text
この Issue のローカル Markdown が残っています。ローカルの Markdown を元に修正を続けますか？
それとも GitHub から最新の Issue を再取得して、ローカル Markdown を更新してから始めますか？
```

- ローカル Markdown を使う場合は、そのファイルを正本として編集を続ける
- GitHub から再取得する場合は、上書きしてローカル Markdown を更新する

ローカル Markdown がない場合、または GitHub 再取得が選ばれた場合は、対象 Issue をローカルファイルへ保存する。

```bash
python3 scripts/issue_refine.py fetch 123
```

GitHub から再取得して既存 Markdown を更新する場合は `--overwrite` を使う。

```bash
python3 scripts/issue_refine.py fetch 123 --overwrite
```

出力先は `gh-issues/{number}/{slug}.md`。
ファイルは YAML frontmatter に `number` と `title` を持ち、frontmatter の後ろ全体が Issue 本文になる。

### Step 3: ユーザーに編集してもらう

書き出し後、保存先パスをユーザーに伝える。
その直後に、必ず次の趣旨で編集支援を申し出る。

```text
どのような編集を手伝いますか？
背景の整理、要件の言い換え、DoD の具体化、スコープ整理、未確定事項の洗い出し、文章の整形などを一緒に進められます。
```

その後は待機せず、Markdown 編集そのものを対話で支援する。
例えば以下を行う。

- 追記したい内容をヒアリングして、Markdown に入れる文面案を作る
- 背景・目的、要件、DoD、未確定事項のどこを直すべきか提案する
- ユーザーが貼った文章を Issue 向けの構造に整える
- 必要なら対象 Markdown ファイルを編集する
- 相談・依頼内容が小規模なものとなってきたら、曖昧な点や不明な点がなくなるまで、ユーザーに1問ずつ確認して進める。

数往復のやりとりで内容がまとまってきたら、次の趣旨で反映確認を行う。

```text
GitHub に反映しましょうか？
```

### Step 4: 編集内容をGitHubへ反映する

ユーザーが反映を希望したら、ローカル Markdown から title/body を読み取り、Issue を更新する。

```bash
python3 scripts/issue_refine.py push gh-issues/123/example.md
```

`gh issue edit <number> --title ... --body-file ...` を使って反映する。
反映成功後は、当該 Markdown ファイルを削除する。

## ルール

- Issue に書かれていない仕様を勝手に補わない
- 追記・修正は必ずローカル Markdown を正本として扱う
- `gh-issues/{number}/*.md` が残っている場合は、ローカル継続か GitHub 再取得かを必ず確認する
- 書き出し直後に「どのような編集を手伝いますか？」と尋ねる
- 編集支援の区切りで「GitHub に反映しましょうか？」と確認する
- 「注釈に対応して」と依頼された場合、注釈はユーザーがAIに文書への追記・修正を依頼するためのものとして扱う
- 「注釈に対応して」と依頼された場合、回答は注釈を使わず本文へ統合した形で提示する
- ユーザーが反映を明示する前に push しない
- push 成功後は当該 Markdown ファイルを削除する
- 大きな仕様変更なら既存 Issue を膨らませすぎず、新規 Issue 化も検討する

## 前提条件

- GitHub CLI (`gh`) がインストールされ、認証済み
- 現在のディレクトリが対象リポジトリ
- 対象リポジトリに対する Issue の閲覧・更新権限がある

## 参照

- Markdown ファイル構造: [references/issue-markdown-format.md](references/issue-markdown-format.md)
