# Issue 25 Baseline

## Environment
- Date: 2025-11-30
- Branch: ci/25-validate-strict
- Base commit: c8bac754031019360c03c0dae3d7b48800a294d9

## Repository Type
This is a recipe registry (TOML files + CI workflows). No build or test suite.

## Existing CI Workflows
- validate.yml - Basic recipe validation
- test-installations.yml - Test changed recipes by building tsuku from source
- deploy.yml - Deploy to GitHub Pages

## Task
Add tsuku validate --strict to CI for comprehensive recipe validation.
