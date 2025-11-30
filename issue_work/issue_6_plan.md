# Issue 6 Implementation Plan

## Summary

Create a GitHub Actions workflow that generates recipes.json and deploys to GitHub Pages on push to main and daily schedule.

## Approach

Use the standard GitHub Pages deployment pattern with actions pinned to commit SHAs for security and reproducibility.

### Alternatives Considered

- **Version tags (v4, v5)**: Less secure - tags can be moved. SHA pinning ensures exact code runs.
- **Self-hosted deployment**: Unnecessary complexity for static JSON file.

## Files to Create

- `.github/workflows/deploy.yml` - Deploy workflow for GitHub Pages

## Action SHAs (pinned for security)

- `actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3` (v6.0.0)
- `actions/setup-python@83679a892e2d95755f2dac6acb0bfd1e9ac5d548` (v6.1.0)
- `actions/configure-pages@983d7736d9b0ae728b81ab479565c72886d7745b` (v5.0.0)
- `actions/upload-pages-artifact@7b1f4a764d45c48632c6b24a0339c27f5614fb0b` (v4.0.0)
- `actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e` (v4.0.5)

## Implementation Steps

- [x] Create `.github/workflows/deploy.yml` with build and deploy jobs
- [ ] Verify workflow syntax with `gh workflow view`

## Workflow Structure

```yaml
name: Deploy Recipes
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily at 00:00 UTC
  workflow_dispatch:  # Manual trigger

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - setup-python 3.11
      - run generate.py
      - copy CNAME to _site/
      - upload-pages-artifact

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - configure-pages
      - deploy-pages
```

## Testing Strategy

- Push to branch triggers validate.yml (existing CI)
- After merge, deploy.yml runs and deploys
- Verify: `curl -I https://registry.tsuku.dev/recipes.json`

## Risks and Mitigations

- **Deploy failure**: workflow_dispatch allows manual re-trigger
- **Concurrent deploys**: concurrency group prevents race conditions

## Success Criteria

- [ ] Workflow file created with correct permissions
- [ ] Actions pinned to commit SHAs
- [ ] Triggers on push to main and daily schedule
- [ ] Deploys _site/ including CNAME

## Open Questions

None
