# Issue 18 Implementation Plan

## Summary

Add 6 new Go tool recipes using the `go_install` action pattern with `dependencies = ["go"]`. The dlv tool is excluded because it requires cgo.

## Approach

The issue requires recipes to use the `go_install` action, which builds tools from source using `go install`. This provides:
- Consistent builds across platforms
- No need to track release asset naming patterns
- Automatic version resolution from Go module proxy

### Alternatives Considered
- **github_archive (pre-built binaries)**: Faster install, but requires tracking asset patterns per tool and some tools don't publish binaries
- **Mixed approach**: Use binaries when available, go_install as fallback. Not chosen because the issue explicitly requires go_install.

### Tools Excluded
- **dlv (debugger)**: Requires cgo for platform-specific debugging features. The design doc specifies CGO_ENABLED=0 as a hard constraint.

## Files to Create

Based on the recipe format from the design doc:

- `recipes/g/gofumpt.toml` - Go code formatter (stricter than gofmt)
- `recipes/s/staticcheck.toml` - Go static analysis linter
- `recipes/g/gore.toml` - Go REPL
- `recipes/c/cobra-cli.toml` - CLI scaffolding generator
- `recipes/m/mockgen.toml` - Go mock generator
- `recipes/g/goimports.toml` - Go imports formatter

## Implementation Steps

- [ ] Create recipe for gofumpt
- [ ] Create recipe for staticcheck
- [ ] Create recipe for gore
- [ ] Create recipe for cobra-cli
- [ ] Create recipe for mockgen
- [ ] Create recipe for goimports

## Recipe Format

Each recipe follows this pattern:

```toml
[metadata]
name = "<tool-name>"
description = "<description>"
homepage = "<homepage-url>"
version_format = "semver"
dependencies = ["go"]

[version]
source = "goproxy"
module = "<module-path>"

[[steps]]
action = "go_install"
module = "<module-path>"
executables = ["<binary-name>"]

[verify]
command = "<verify-command>"
pattern = "<pattern>"
```

## Testing Strategy

- **Validation**: Run `python3 scripts/generate.py` to validate TOML syntax and metadata
- **CI**: The test-installations.yml workflow will test each changed recipe by building tsuku from source and installing the tool
- **Manual verification**: Optional local test with tsuku if available

## Risks and Mitigations

- **Build failures in CI**: Some tools may have complex dependencies or platform-specific issues
  - Mitigation: CI tests on both ubuntu-latest and macos-latest
- **Version verification**: Some tools don't have --version flags
  - Mitigation: Use alternative verification commands (help output, simple execution)

## Success Criteria

- [ ] 6 new recipes created (gofumpt, staticcheck, gore, cobra-cli, mockgen, goimports)
- [ ] All recipes pass `python3 scripts/generate.py` validation
- [ ] All recipes follow the go_install pattern with dependencies = ["go"]
- [ ] CI passes (both validate-recipes and test-installations workflows)

## Open Questions

None - all requirements are clear.
