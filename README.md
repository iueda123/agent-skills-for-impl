# Agent Skills

Claude Code の Skills（カスタムスラッシュコマンド）集です。

Issue 起票 → Issue の追記・修正 → 並列開発計画 → git worktree で並列実装 → PR 作成までを自動化するワークフローを提供します。

## スキル一覧

| スキル | コマンド | 説明 |
| --- | --- | --- |
| [create-issue](./create-issue/) | `/create-issue` | 雑な要件から GitHub Issue を構造化して起票 |
| [refine-issue](./refine-issue/) | `/refine-issue` | 既存 Issue を Markdown に書き出し、Claude が対話で編集支援した後に GitHub へ反映 |
| [refine-issue-with-research](./refine-issue-with-research/) | `/refine-issue-with-research` | 既存 Issue を Markdown に書き出し、コードベース調査結果に基づいて目的・要件・現状・選択肢・方針を再構成して反映 |
| [create-plan](./create-plan/) | `/create-plan` | 単体 Issue でも複数 Issue でも使える。依存関係を分析し、Wave 構造の並列開発プロンプトを生成（例: `/create-plan #5` `/create-plan #3-10`） |
| [refine-plan](./refine-plan/) | `/refine-plan` | create-plan で生成した plan ファイルを対話しながら改善 |
| [impl-multi](./impl-multi/) | `/impl-multi` | git worktree で隔離環境を作り並列開発 |
| [impl-single](./impl-single/) | `/impl-single` | 単一ツリーで1タスクずつ丁寧に実装を進める |
| [pull-request](./pull-request/) | `/pull-request` | 変更内容を分析して PR を自動作成 |

## ワークフロー

```text
要件定義
  ↓
/create-issue → GitHub Issue を起票
  ↓
/refine-issue → Issue 一覧表示 → 対象選択 → 既存 md の有無確認 → 必要なら再取得して gh-issues/{number}/{slug}.md を更新
  ↓
Claude が「どのような編集を手伝いますか？」と聞き、対話しながら Markdown を編集
  ↓
区切りで「GitHub に反映しましょうか？」と確認して反映
  ↓
反映後にローカル Markdown を削除
  ↓
/create-plan → docs/prompts/xxx.md（実行プロンプト集）
  ↓
プロンプトをコピペして複数の Claude Code セッションで実行
  ↓
/impl-multi → worktree 作成 → 実装 → /pull-request → PR 作成
```

## 典型フロー

1. Claude Code と対話しながら要件定義を固める
2. `/create-issue` で最初の Issue を起票する
3. `/refine-issue` で既存 Issue 一覧を見て、修正したい Issue を選ぶ
4. `gh-issues/{number}/*.md` が残っていれば、ローカル継続か GitHub 再取得かを決める
5. 必要に応じて Issue を `gh-issues/{number}/{slug}.md` に書き出す、または更新する
6. Claude が「どのような編集を手伝いますか？」と尋ね、ユーザーと数往復しながら Markdown 編集を支援する
7. 内容がまとまったら Claude が「GitHub に反映しましょうか？」と確認し、合意後に GitHub に反映する
8. 反映後、当該 Markdown を削除する
9. 内容が固まった Issue 群に対して `/create-plan` を実行する
10. 生成されたプロンプトを使って `/impl-multi` と `/pull-request` で並列実装と PR 作成を進める

## インストール

全スキルを一括インストール：

```bash
npx skills add okazuki58/agent-skills -y
```

個別にインストール：

```bash
npx skills add okazuki58/agent-skills --skill <skill-name> -y
```

## 前提条件

- Claude Code がインストール済み
- GitHub CLI (`gh`) がインストール・認証済み
- git リポジトリ内で実行すること
