---
allowed-tools: Bash(git *), Bash(gh *), Bash(rm *), Read, Glob, Grep
---

# /ship — Commit, push, PR, auto-merge, wait, and clean up

You are shipping a completed feature. Follow these steps precisely.

## Step 1: Validate

Run `git branch --show-current` to get the current branch.

- **Must** be on a `feature/*` branch. If on `main`, stop and tell the user this command only works from a feature branch.
- Extract the feature name from the branch (e.g., `feature/new-post` -> `new-post`).

Run `git status` and `git log origin/main..HEAD --oneline` to verify there are either:
- Uncommitted changes to stage, OR
- Commits ahead of `origin/main` to push

If there's nothing to ship (no changes, no new commits), stop and tell the user.

## Step 2: Stage and Commit

If there are uncommitted changes:

1. Run `git diff` and `git diff --cached` and `git status` to review all changes
2. Stage relevant files with `git add <specific-files>` (avoid `git add -A` to prevent accidentally staging sensitive files)
3. Create a descriptive commit message summarizing all changes. Use this format:

```bash
git commit -m "$(cat <<'EOF'
Description of the change

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

If all changes are already committed, skip this step.

## Step 3: Push

Push the branch to the remote:

```bash
git push -u origin feature/{name}
```

## Step 4: Create PR

Look for a spec file in `.specs/` that matches the branch name. Read it to extract:
1. **Summary section** — use as the PR summary (convert to bullet points if not already)
2. **Test Plan section** — copy directly into the PR body, preserving the checked/unchecked state from the spec

The test plan items should already be checked off (`[x]`) from the implementation step. Do not re-write or paraphrase them — use the spec's exact test plan items.

Create the PR using content pulled from the spec:

```bash
gh pr create --title "Short descriptive title" --body "$(cat <<'EOF'
## Summary
{Bullet points derived from the spec's Summary section}

## Test plan
{Exact test plan checkboxes from the spec, preserving [x] / [ ] state}

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Keep the title under 70 characters. Use the body for details.

## Step 5: Auto-merge

Try to enable auto-merge (without `--delete-branch` — the worktree holds the local branch):

```bash
gh pr merge --squash --auto
```

If auto-merge is not enabled on the repo, this will fail — that's fine, proceed to step 6.

## Step 6: Wait for Merge

Tell the user the PR is created and you're waiting for CI, then watch for checks to complete:

```bash
gh pr checks --watch
```

Once checks finish, check if the PR was already merged (by auto-merge). If not, merge it manually (without `--delete-branch`):

```bash
state=$(gh pr view --json state --jq '.state')
if [ "$state" != "MERGED" ]; then
  gh pr merge --squash
fi
```

If auto-merge was enabled, poll until merged:

```bash
for i in $(seq 1 12); do
  state=$(gh pr view --json state --jq '.state')
  if [ "$state" = "MERGED" ]; then break; fi
  sleep 10
done
```

If the PR doesn't merge after polling, inform the user and provide the PR URL.

## Step 7: Clean Up

After the PR is merged, clean up in this order (worktree first, then pull):

1. Stop any running Hugo dev servers for the worktree
2. Remove the worktree directory and prune
3. Remove any untracked spec files for this feature from the main repo (they'll come in with the pull)
4. Switch to the main repo directory and pull latest main

```bash
rm -rf ../mrmatt-{name}
cd C:\dev\MrMatt.io
git worktree prune
rm -f .specs/NNN-{branch-name}.md
git pull origin main
```

If the worktree removal fails (e.g., locked files), inform the user.

## Step 8: Report

Print a clear summary:

```
Shipped and merged!

  PR:     {PR URL}
  Branch: feature/{name} (merged and deleted)
  Worktree: cleaned up
```

If the PR hasn't merged yet (timeout), instead print:

```
PR created and auto-merge enabled:

  PR:     {PR URL}
  Branch: feature/{name}
  Status: Waiting for CI — will auto-merge when checks pass

Worktree still exists at ../mrmatt-{name} (clean up manually after merge)
```
