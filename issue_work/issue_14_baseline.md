# Issue 14 Baseline

## Environment
- Date: 2025-11-30
- Branch: feature/14-perl-tool-recipes
- Base commit: 0667e1efbe3b356f073703c20620d11a1966104b

## Repository Type
This is a recipe registry (TOML files only). No build or test suite.

## Validation
Recipe validation is performed by CI via `.github/workflows/validate.yml`.

## Pre-existing State
- perl.toml recipe already exists (from issue #13)
- cpanm is bundled with the perl recipe
- Target tools: ack, perltidy, perlcritic, carton

## Dependencies
- Issue #13 (Perl runtime recipe): CLOSED
- tsuku-dev/tsuku#130 (cpan_install action): CLOSED
