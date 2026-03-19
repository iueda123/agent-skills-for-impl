# Agent Skills for Implementation

Claude Code 向けの汎用実装スキル集です。  
Issue の作成・修正、計画作成、実装（単一/並列）、PR 作成までの一連フローをカバーする。

## ディレクトリ構成

- `skills/`: スキル定義のソース（`SKILL.md`、references、scripts）
- `docs/gh-issues/`: Issue 編集時のローカル Markdown 置き場
- `docs/plans/`: 計画ドキュメント置き場
- `docs/refs/`: 参照資料

## スキル一覧

| スキル | コマンド | 説明 |
| --- | --- | --- |
| [create-issue](skills/create-issue/SKILL.md) | `/create-issue` | 雑な要件メモから GitHub Issue を構造化して起票 |
| [refine-issue](skills/refine-issue/SKILL.md) | `/refine-issue` | Issue を Markdown 化し、対話で編集して GitHub に反映 |
| [refine-issue-with-research](skills/refine-issue-with-research/SKILL.md) | `/refine-issue-with-research` | コードベース等の詳細調査を含めて Issue を再構成して反映 |
| [create-plan](skills/create-plan/SKILL.md) | `/create-plan` | Issue 群から Plan Only の実行プロンプト集を生成 |
| [refine-plan](skills/refine-plan/SKILL.md) | `/refine-plan` | 生成済み plan (`docs/plans/{name}.md`) を対話で改善 |
| [impl-single](skills/impl-single/SKILL.md) | `/impl-single` | 単一作業ツリーで段階的に実装・検証 |
| [impl-multi](skills/impl-multi/SKILL.md) | `/impl-multi` | `git gtr` を使って worktree 並列実装 |
| [pull-request](skills/pull-request/SKILL.md) | `/pull-request` | コミット済み差分から PR 本文を作成し `gh pr create` |

## 標準フロー

```text
要件整理
  ↓
/create-issue
  ↓
/refine-issue または /refine-issue-with-research
  ↓
/create-plan
  ↓
/refine-plan
  ↓
/impl-single または /impl-multi
  ↓
/pull-request
```

## 主要な出力先

- Issue 編集用 Markdown: `docs/gh-issues/{issue_number}/{slug}.md`
- 複数 Issue の計画プロンプト集（親）: `docs/plans/{name}.md`
- Issue 単位の計画書（子）: `docs/plans/{name}/issues/{issue_number}-{slug}.md`
- 子ファイルは `issues/` 配下にまとめ、同一 plan の成果物を一覧しやすくする（親子関係を明示する）

## インストール

```bash
npx skills add iueda123/agent-skills-for-impl -y
```

このスキル集を導入したいリポジトリのルートでこのコマンドを実行すると、
配下の `.claude/skills/` に  `.claude/skills/*/SKILL.md` のようにインストールされる。

## 前提条件

- Claude Code が利用可能
- GitHub CLI (`gh`) がインストール済みかつ認証済み
- 対象リポジトリで実行していること

## 補足

- `refine-issue` / `refine-issue-with-research` は `skills/*/scripts/issue_refine.py` を使って Issue の fetch/push を行います。
- `create-plan` と `refine-plan` は「計画作成専用」です（実装は行いません）。
