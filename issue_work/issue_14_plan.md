# Issue 14 Implementation Plan

## Summary

Create cpan_install recipes for popular Perl CLI tools (ack, perltidy, perlcritic, carton) using the established recipe pattern.

## Approach

Following the pattern established by gem_install (bundler.toml) and pipx_install (httpie.toml):
- Use `cpan_install` action with `distribution` and `executables` parameters
- Declare `dependencies = ["perl"]` in metadata
- Use `source = "metacpan"` for version resolution
- Add verification commands matching executable output patterns

### Alternatives Considered

- **Use tsuku create command**: Not ready yet; manual recipe creation is needed
- **Generate recipes from MetaCPAN API**: Overkill for 4 recipes; manual is faster and more reliable

## Files to Create

- `recipes/a/ack.toml` - grep-like text finder
- `recipes/p/perltidy.toml` - Perl code formatter
- `recipes/p/perlcritic.toml` - Perl code linter
- `recipes/c/carton.toml` - Perl dependency manager

## Implementation Steps

- [x] Create ack.toml recipe (ack distribution)
- [x] Create perltidy.toml recipe (Perl-Tidy distribution)
- [x] Create perlcritic.toml recipe (Perl-Critic distribution)
- [x] Create carton.toml recipe (Carton distribution)
- [ ] Test all recipes locally (blocked by tsuku-dev/tsuku#161)

## Testing Strategy

- Local verification: `tsuku install --recipe-file <path> --force`
- Verify each tool executes correctly after installation
- Confirm wrapper scripts set PERL5LIB correctly
- CI will test on PR via test-installations.yml workflow

## Risks and Mitigations

- **XS module dependencies**: All target tools are pure Perl; verified via MetaCPAN
- **Version verification patterns**: May need adjustment based on actual output format

## Success Criteria

- [ ] All recipes validate with action-validator
- [ ] All recipes install successfully on Linux
- [ ] Installed tools execute without errors
- [ ] PR passes CI checks

## Open Questions

None - all tools are well-known pure Perl distributions.

## Blockers

- **tsuku-dev/tsuku#161**: cpan_install action doesn't convert distribution names to module names before calling cpanm. Recipes use correct distribution names per documented interface, but installation fails until CLI is fixed.
