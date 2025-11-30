# Issue 4 Implementation Plan

## Summary

Configure GitHub Pages to serve recipes.json at registry.tsuku.dev by creating the CNAME file and documenting manual configuration steps.

## Approach

This issue involves mostly manual configuration (GitHub Settings, DNS) with one code artifact (CNAME file). The approach is to commit the CNAME file and document the manual steps in the PR for the maintainer to complete.

### Alternatives Considered

- **Terraform/Infrastructure as Code**: Overkill for a single CNAME record and GitHub Pages setting - adds unnecessary complexity.
- **GitHub API automation**: GitHub Pages settings can be configured via API but requires admin token and adds no practical value for one-time setup.

## Files to Create

- `CNAME` - Custom domain configuration file at repo root containing `registry.tsuku.dev` (deploy workflow copies to _site/)

## Implementation Steps

- [x] Create `_site/CNAME` with domain `registry.tsuku.dev`
- [x] Verify CI still passes with CNAME file present

## Manual Steps (for maintainer)

1. **Enable GitHub Pages in repository settings**
   - Go to Settings > Pages
   - Source: "GitHub Actions"

2. **Configure DNS CNAME record**
   - Provider: wherever tsuku.dev DNS is managed
   - Record: `registry` CNAME pointing to `tsuku-dev.github.io`

3. **Verify HTTPS** (auto-provisioned by GitHub after DNS propagates)

4. **Verify CORS**
   ```bash
   curl -I https://registry.tsuku.dev/recipes.json
   # Should include: Access-Control-Allow-Origin: *
   ```

## Testing Strategy

- CI validation: ensure generate.py still works with CNAME file present
- Manual verification: after DNS setup, verify CORS headers are present

## Risks and Mitigations

- **DNS propagation delay**: May take up to 48 hours. Mitigation: document expected behavior, no code changes needed.
- **Certificate provisioning**: GitHub auto-provisions but may take time. Mitigation: HTTPS is not blocking for initial PR merge.

## Success Criteria

- [ ] CNAME file committed at `_site/CNAME`
- [ ] CI passes
- [ ] Manual steps documented in PR description

## Open Questions

None - manual steps are straightforward GitHub/DNS configuration.
