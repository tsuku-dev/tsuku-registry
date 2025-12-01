# Issue 15 Summary

## What Was Implemented

Added a Go toolchain recipe that enables `tsuku install go` to download and install the official Go distribution from go.dev.

## Changes Made
- `recipes/g/go.toml`: New recipe for Go toolchain

## Key Decisions
- Used `download_archive` action: Go toolchain is a binary distribution, not a source package requiring compilation
- URL pattern `go.dev/dl/go{version}.{os}-{arch}.tar.gz`: Official distribution URL from go.dev
- `strip_dirs = 1`: Go archives contain a `go/` top-level directory that should be stripped
- `install_mode = "directory"`: Go needs its full directory structure (includes src/, pkg/ for stdlib)

## Trade-offs Accepted
- No checksum verification in recipe: The tsuku download_archive action handles this via go.dev metadata

## Test Coverage
- Recipe validation: passes (172 recipes now, was 171)
- Python tests: 11/11 passing

## Known Limitations
- Windows not supported (linux/darwin only per design)
- Requires network access to go.dev

## Future Improvements
- The go_install action (tsuku-dev/tsuku#117) will use this as a hidden dependency for installing Go tools
