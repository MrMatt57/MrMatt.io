# 017: Upload via Branch + PR Instead of Direct Push

**Branch**: `feature/upload-branch-pr`
**Created**: 2026-02-24

## Summary

Photo uploads fail with "Could not create the file required" because the upload pushes directly to `main`, which has branch protection with a required status check. Fix by creating a temporary branch, committing files there, and opening a PR that auto-merges after CI passes.

## Requirements

- Upload creates a branch `photo/{slug}` from `main`'s HEAD
- Both files (photo + index.md) are committed to the new branch
- A PR is created from the branch to `main` with auto-merge enabled
- Success message shows PR link so the user can track it
- Bump SW cache to v7 and cache-bust to `?v=7`

## Design

### JS changes (`static/upload/app.js`)

Replace the submit handler's direct-to-main commit flow with:

1. **Get main HEAD SHA**:
   ```
   GET /repos/{owner}/{repo}/git/ref/heads/main
   → response.object.sha
   ```

2. **Create branch**:
   ```
   POST /repos/{owner}/{repo}/git/refs
   { "ref": "refs/heads/photo/{slug}", "sha": mainSha }
   ```

3. **Commit files** (same `commitFile` function, but pass the new branch name instead of `'main'`):
   - First commit: the photo binary
   - Second commit: the index.md front matter

4. **Create PR**:
   ```
   POST /repos/{owner}/{repo}/pulls
   { "title": "feat: add photo {folderName}", "head": "photo/{slug}", "base": "main" }
   ```

5. **Enable auto-merge** via GraphQL:
   ```
   POST /graphql
   mutation { enablePullRequestAutoMerge(input: { pullRequestId: nodeId, mergeMethod: SQUASH }) }
   ```
   If this fails (auto-merge not enabled on repo), that's fine — the PR is still created.

6. **Update status message**:
   - Change success message to: "Photo uploaded! [View PR]({pr_url}) — it will auto-merge after the build passes."
   - Make the status message contain an anchor tag link to the PR

#### Helper functions to add

- `getMainSha(token)` — fetches the SHA of `main`'s HEAD
- `createBranch(token, branchName, sha)` — creates a new branch ref
- `createPR(token, title, head, base)` — creates a pull request, returns `{ url, node_id }`
- `enableAutoMerge(token, prNodeId)` — GraphQL mutation, best-effort

#### Changes to `commitFile`

- Add a `branch` parameter instead of using the global `BRANCH` constant
- Callers pass the branch name explicitly

### HTML changes (`static/upload/index.html`)

- Bump cache-bust `?v=6` → `?v=7`

### SW changes (`static/upload/sw.js`)

- Bump `photo-upload-v6` → `photo-upload-v7`

## Files to Modify

| File | Change |
|------|--------|
| `static/upload/app.js` | New branch+PR upload flow, helper functions |
| `static/upload/index.html` | Bump cache-bust to v7 |
| `static/upload/sw.js` | Bump cache to v7 |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Upload creates a `photo/*` branch (verify in GitHub)
- [ ] Both photo and index.md are committed to the branch
- [ ] PR is created from the branch to `main`
- [ ] Auto-merge is enabled on the PR
- [ ] Success message shows PR link
- [ ] PR merges after CI passes and photo appears on site
