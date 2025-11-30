# Issue 3 Summary

## What Was Implemented

A Python script that parses all recipe TOML files, validates metadata against the schema, and outputs a sorted JSON file for the tsuku.dev recipe browser.

## Changes Made

- `scripts/generate.py`: New script (~200 lines) implementing:
  - File discovery using pathlib glob
  - TOML parsing with tomllib (Python 3.11+ stdlib)
  - Comprehensive validation (5 rules)
  - JSON output with schema_version and generated_at
  - Error aggregation with descriptive messages

## Key Decisions

- **Single file**: Kept implementation in one file for simplicity; script is small enough (~200 lines) that splitting would add unnecessary complexity
- **No external deps**: Used only stdlib (tomllib, pathlib, json, re) to avoid dependency management in CI
- **Fail-fast with aggregation**: Collect all errors before failing, so users see all issues at once

## Trade-offs Accepted

- **No unit tests**: Script is straightforward; validation was tested manually against all 171 recipes and edge cases
- **Static paths**: RECIPES_DIR and OUTPUT_DIR are hardcoded; acceptable for single-purpose script

## Test Coverage

- Manual testing: All 171 existing recipes parse successfully
- Edge case testing: Verified validation catches invalid homepage, name mismatch, long description, etc.
- No automated tests (acceptable for simple script)

## Known Limitations

- Script must be run from repository root (uses relative paths)
- No support for incremental generation (always regenerates full JSON)

## Future Improvements

- Could add --dry-run flag for validation without output
- Could add --verbose flag for debugging
