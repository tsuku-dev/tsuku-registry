# Issue 13 Summary

## What Was Implemented

Added a Perl runtime recipe that enables `tsuku install perl` to download relocatable-perl with bundled cpanm.

## Changes Made
- `recipes/p/perl.toml`: New recipe for Perl runtime

## Key Decisions
- Used `download_archive` action with tar.xz format (smaller than tar.gz)
- `github_repo = "skaji/relocatable-perl"` for version detection
- `strip_dirs = 1` to remove the top-level directory from the archive
- `install_mode = "directory"` to preserve Perl's full directory structure

## Trade-offs Accepted
- Uses skaji/relocatable-perl rather than official perl.org builds (relocatable-perl is actively maintained and includes cpanm)

## Test Coverage
- Recipe validation: passes (173 recipes now, was 172)
- Local installation test: Perl 5.42.0 installed successfully

## Known Limitations
- Windows not supported (relocatable-perl only supports linux/darwin)
- Requires network access to GitHub

## Future Improvements
- Will be used as hidden dependency for cpan_install action (tsuku-dev/tsuku#130)
