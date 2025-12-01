# Issue 25 Implementation Plan

## Summary

Add a new CI workflow that runs `tsuku validate --strict` on all recipes, triggered on PRs and nightly schedule.

## Approach

Create a new workflow file that:
1. Builds tsuku from source (same pattern as test-installations.yml)
2. Runs `tsuku validate --strict recipes/**/*.toml`
3. Triggers on pull_request and schedule (nightly at 00:00 UTC)

### Why New Workflow vs Modifying Existing

- Keep validation separate from Python-based generation scripts
- Validation can run independently of recipe generation
- Clearer separation of concerns

## Files to Create

- `.github/workflows/validate-strict.yml` - New workflow for tsuku validate

## Implementation Steps

- [ ] Create validate-strict.yml workflow
- [ ] Configure PR trigger
- [ ] Configure nightly schedule trigger
- [ ] Pin actions to commit SHAs (matching existing patterns)
- [ ] Test workflow runs successfully

## Testing Strategy

- Push branch and verify workflow runs on PR
- Check that validation passes for existing recipes
- Manually trigger to test workflow_dispatch

## Success Criteria

- [ ] Workflow runs on pull_request events
- [ ] Workflow runs on scheduled nightly cron
- [ ] tsuku validate --strict runs on all recipe files
- [ ] CI fails if any validation errors or warnings
- [ ] Actions pinned to commit SHAs
