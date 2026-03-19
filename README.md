# Agent Skills for Implementation

Claude Code 向けの実装支援スキル集です。  
Issue 作成・Issue 精緻化・計画作成・実装・PR 作成・実装後レビュー（tidy-up）までを一連でカバーします。

## 収録スキル

| スキル | コマンド | 目的 |
| --- | --- | --- |
| [create-issue](skills/create-issue/SKILL.md) | `/create-issue` | 要件メモから GitHub Issue を構造化して作成 |
| [refine-issue](skills/refine-issue/SKILL.md) | `/refine-issue` | Issue を Markdown 化して対話編集し、GitHub へ反映 |
| [refine-issue-with-research](skills/refine-issue-with-research/SKILL.md) | `/refine-issue-with-research` | コードベース調査込みで Issue を再構成して反映 |
| [create-plan](skills/create-plan/SKILL.md) | `/create-plan` | Issue 群から Phase 2（計画のみ）の plan を作成 |
| [refine-plan](skills/refine-plan/SKILL.md) | `/refine-plan` | 生成済み plan（`docs/plans/{name}/issues/*.md`）を改善 |
| [impl-single](skills/impl-single/SKILL.md) | `/impl-single` | 単一作業ツリーで段階的に実装・検証 |
| [impl-multi](skills/impl-multi/SKILL.md) | `/impl-multi` | `git gtr` を使った worktree 並列実装 |
| [pull-request](skills/pull-request/SKILL.md) | `/pull-request` | コミット済み差分から PR 本文を作成し `gh pr create` |
| [tidy-up](skills/tidy-up/SKILL.md) | `/tidy-up` | PR 作成後に Issue/plan/テスト整合性を検証しレポート投稿 |

## 推奨フロー

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
  ↓
/tidy-up
```

## ディレクトリ構成

- `skills/`: スキル定義ソース（`SKILL.md`、`references/`、`scripts/`、`agents/`）
- `.claude/skills/`: Claude Code から実際に利用するスキル配置先（このリポジトリ内サンプル）
- `docs/gh-issues/`: Issue 編集用 Markdown の配置先
- `docs/plans/`: plan ファイル配置先
- `docs/refs/`: 補助資料

## 主要成果物

- Issue 編集ファイル: `docs/gh-issues/{issue_number}/{slug}.md`
- plan 親ファイル: `docs/plans/{name}.md`
- plan 子ファイル: `docs/plans/{name}/issues/{issue_number}-{slug}.md`
- tidy-up ログ: `gh-pr-log/{pr_number}/comments.md`

## セットアップ

### 1. スキルを導入

```bash
npx skills add iueda123/agent-skills-for-impl -y
```

実行すると、対象リポジトリの `.claude/skills/` 配下へインストールされます。

### 2. 必須ツール

- Claude Code
- GitHub CLI (`gh`)（インストール済み・認証済み）
- Python 3（`refine-issue*` の `scripts/issue_refine.py` で使用）
- Git（`pull-request` / `impl-multi` / `tidy-up` で使用）
- `git gtr`（`impl-multi` を使う場合）

## 補足

- `refine-issue` / `refine-issue-with-research` では `skills/*/scripts/issue_refine.py` を利用します。
- `create-plan` と `refine-plan` は計画作成専用で、実装は行いません。
- `tidy-up` は PR 作成後に実行し、PR コメントへ整合性レポートを投稿します。
