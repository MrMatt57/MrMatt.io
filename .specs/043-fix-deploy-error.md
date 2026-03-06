# 043: Remove Obsolete Cloudflare Project Creation Step

**Branch**: `feature/fix-deploy-error`
**Created**: 2026-03-05

## Summary

The deploy workflow has a "Create Cloudflare Pages project" step that always fails because the project already exists. Although `continue-on-error: true` prevents it from blocking the deploy, it logs a noisy error on every run. Remove the step since the project was created long ago and will never need to be recreated.

## Requirements

- Remove the "Create Cloudflare Pages project (if needed)" step from `.github/workflows/deploy.yml`
- Do not change any other workflow steps

## Design

Delete lines 37-44 of `deploy.yml` (the `Create Cloudflare Pages project` step). No other changes needed.

## Files to Modify

| File | Change |
|------|--------|
| `.github/workflows/deploy.yml` | Remove the "Create Cloudflare Pages project (if needed)" step |

## Test Plan

- [x] Deploy workflow YAML is valid
- [x] No other steps are affected
