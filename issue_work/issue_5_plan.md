# Issue 5 Implementation Plan

## Summary

Rename validate.yml to validate-recipes.yml and pin all actions to commit SHAs for security.

## Approach

The existing validate.yml already meets most requirements. Only changes needed:
1. Rename file to match issue acceptance criteria
2. Pin actions to commit SHAs (currently uses version tags)

### Alternatives Considered

- **Create new file, keep old**: Would cause duplicate CI runs. Better to rename.
- **Keep version tags**: Less secure - tags can be moved. SHA pinning required by issue.

## Files to Modify

- `.github/workflows/validate.yml` → `.github/workflows/validate-recipes.yml`
  - Rename file
  - Pin actions to SHAs

## Implementation Steps

- [ ] Rename validate.yml to validate-recipes.yml
- [ ] Pin actions/checkout to SHA (v4 → 1af3b93b6815bc44a9784bd300feb67ff0d1eeb3)
- [ ] Pin actions/setup-python to SHA (v5 → 83679a892e2d95755f2dac6acb0bfd1e9ac5d548)

## Action SHAs (from issue #6 research)

- `actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3` (v6.0.0)
- `actions/setup-python@83679a892e2d95755f2dac6acb0bfd1e9ac5d548` (v6.1.0)

## Testing Strategy

- Push to branch triggers renamed workflow
- Verify CI passes

## Success Criteria

- [ ] Workflow file renamed to validate-recipes.yml
- [ ] Actions pinned to commit SHAs
- [ ] Triggers on pull_request events
- [ ] Does NOT deploy (validation only)
- [ ] CI passes on PR

## Open Questions

None
