---
allowed-tools: Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Read, Write, Glob, Grep, AskUserQuestion
---

# /setup — One-time GitHub repo best practices setup

You are setting up a GitHub repository with best practices for a solo developer. This command is designed to run once. Follow these steps precisely.

## Step 1: Detect Repo

Run `gh repo view --json nameWithOwner,defaultBranch --jq '{repo: .nameWithOwner, branch: .defaultBranch}'` to identify the repo.

If this fails, tell the user they need to be in a git repo with a GitHub remote.

## Step 2: Audit Current State

Run these commands to understand what's already configured:

```bash
# Repo settings
gh api repos/{owner}/{repo} --jq '{
  topics: .topics,
  has_issues: .has_issues,
  has_wiki: .has_wiki,
  has_discussions: .has_discussions,
  allow_merge_commit: .allow_merge_commit,
  allow_squash_merge: .allow_squash_merge,
  allow_rebase_merge: .allow_rebase_merge,
  delete_branch_on_merge: .delete_branch_on_merge,
  allow_auto_merge: .allow_auto_merge
}'

# Branch protection
gh api repos/{owner}/{repo}/branches/main/protection 2>&1

# Existing labels
gh label list --json name --jq '.[].name'

# Check for existing files
ls .github/dependabot.yml 2>/dev/null
ls .github/ISSUE_TEMPLATE/ 2>/dev/null
ls .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null
ls SECURITY.md 2>/dev/null
```

## Step 3: Present Summary

Based on the audit, present a clear summary to the user. Group changes into categories and mark items that are already configured:

```
Here's what I'll set up for {repo}:

**Branch Protection (main):**
  {✓ already | → will set} Required CI status checks (strict: up-to-date)
  {✓ already | → will set} Remove required PR reviews (solo dev — no reviewer needed)
  {✓ already | → will set} Require linear history (clean squash merges)
  {✓ already | → will set} Block force pushes
  {✓ already | → will set} Block branch deletion

**Repo Settings:**
  → Add topics: hugo, blog, personal-site, static-site, cloudflare-pages, papermod
  → Enable vulnerability alerts

**Files to Create:**
  {✓ exists | → create} .github/dependabot.yml
  {✓ exists | → create} .github/ISSUE_TEMPLATE/bug_report.yml
  {✓ exists | → create} .github/ISSUE_TEMPLATE/feature_request.yml
  {✓ exists | → create} .github/ISSUE_TEMPLATE/config.yml
  {✓ exists | → create} .github/PULL_REQUEST_TEMPLATE.md

**Labels to Add:**
  {list only labels that don't already exist}
  content, theme, infrastructure, ci-cd
```

Use AskUserQuestion to confirm:
> Ready to apply these changes?

If the user declines, stop.

## Step 4: Apply Branch Protection

Update the branch protection rule on `main`. This is a single PUT that replaces the full protection config — include ALL settings (both existing and new):

```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["build-and-deploy"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

**Important:** Setting `required_pull_request_reviews` to `null` removes the PR review requirement entirely. This is intentional for a solo dev workflow.

## Step 5: Apply Repo Settings

```bash
# Set topics
gh api repos/{owner}/{repo}/topics --method PUT --input - <<'EOF'
{"names":["hugo","blog","personal-site","static-site","cloudflare-pages","papermod"]}
EOF

# Enable vulnerability alerts
gh api repos/{owner}/{repo}/vulnerability-alerts --method PUT
```

## Step 6: Create Dependabot Config

Only create if `.github/dependabot.yml` doesn't exist.

Write `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "ci"
```

## Step 7: Create Issue Templates

Only create files that don't already exist.

Write `.github/ISSUE_TEMPLATE/bug_report.yml`:

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: Thanks for reporting a bug! Please fill out the details below.
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear description of the bug
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this?
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
    validations:
      required: true
  - type: dropdown
    id: component
    attributes:
      label: Component
      options:
        - Content
        - Theme / Styling
        - Deployment / CI
        - Infrastructure
        - Other
    validations:
      required: true
  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Screenshots, browser info, etc.
```

Write `.github/ISSUE_TEMPLATE/feature_request.yml`:

```yaml
name: Feature Request
description: Suggest a new feature or improvement
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem does this solve? Or what would be improved?
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should it work?
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Any other approaches you've thought about?
  - type: dropdown
    id: component
    attributes:
      label: Component
      options:
        - Content
        - Theme / Styling
        - Deployment / CI
        - Infrastructure
        - Other
    validations:
      required: true
```

Write `.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: false
```

## Step 8: Create PR Template

Only create if `.github/PULL_REQUEST_TEMPLATE.md` doesn't exist.

Write `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Summary

-

## Test plan

- [ ]
```

## Step 9: Add Project Labels

For each label below, only create it if it doesn't already exist:

```bash
gh label create "content" --color "0e8a16" --description "Blog posts and page content" --force
gh label create "theme" --color "5319e7" --description "PaperMod theme and styling" --force
gh label create "infrastructure" --color "1d76db" --description "Hosting, DNS, Cloudflare" --force
gh label create "ci-cd" --color "c5def5" --description "GitHub Actions and deployment" --force
```

The `--force` flag makes this idempotent — it updates the label if it already exists.

## Step 10: Report

Print a summary of everything that was configured:

```
Repo setup complete!

  Branch protection: CI required, linear history, no PR reviews needed
  Topics: hugo, blog, personal-site, static-site, cloudflare-pages, papermod
  Vulnerability alerts: enabled
  Dependabot: GitHub Actions (weekly)
  Issue templates: bug report + feature request
  PR template: Summary + Test plan format
  Labels: content, theme, infrastructure, ci-cd

Note: This command is designed to run once. Re-running is safe (idempotent)
but shouldn't be necessary.
```
