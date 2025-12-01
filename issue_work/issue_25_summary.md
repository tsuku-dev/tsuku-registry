# Issue 25 Summary

## What Was Implemented

Added a new CI workflow (`validate-strict.yml`) that runs `tsuku validate --strict` on all recipes for comprehensive validation.

## Changes Made

- `.github/workflows/validate-strict.yml`: New workflow that:
  - Triggers on PRs changing recipes
  - Triggers nightly at 00:00 UTC
  - Builds tsuku from source
  - Runs `tsuku validate --strict recipes/**/*.toml`

## Key Decisions

- **Separate workflow**: Created new workflow instead of modifying existing validate-recipes.yml to keep Python-based generation separate from tsuku-based validation
- **Build from source**: Uses same pattern as test-installations.yml to get latest validation features
- **Strict mode**: Uses `--strict` flag to treat warnings as errors for high recipe quality

## Trade-offs Accepted

- **Two validation workflows**: validate-recipes.yml (Python) and validate-strict.yml (tsuku) both run, providing defense in depth but some redundancy
