# Issue 14 Summary

## What Was Implemented

Added cpan_install recipes for four popular Perl CLI tools: ack, perltidy, perlcritic, and carton. Each recipe follows the established pattern for ecosystem-specific installation actions.

## Changes Made

- `recipes/a/ack.toml`: grep-like source code search tool
- `recipes/p/perltidy.toml`: Perl code formatter
- `recipes/p/perlcritic.toml`: Perl code linter
- `recipes/c/carton.toml`: Perl dependency manager

## Key Decisions

- **Distribution naming**: Used CPAN distribution names (e.g., "Perl-Tidy") per documented cpan_install interface, not module names (e.g., "Perl::Tidy")
- **Version format**: Used "calver" for perltidy (uses YYYYMMDD versioning), "semver" for others

## Known Limitations

- **Blocked by tsuku-dev/tsuku#161**: The cpan_install action doesn't convert distribution names to module names before calling cpanm. Recipes use correct interface but installation fails until CLI is fixed.

## Future Improvements

- Add more Perl tools as cpan_install matures (App::Yath, Dist::Zilla, etc.)
- Consider XS module support for tools with native dependencies
