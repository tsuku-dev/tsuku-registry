# tsuku-registry

Recipe repository for tsuku. Contains TOML recipe files that define how to install tools.

## Structure

```
tsuku-registry/
├── recipes/
│   ├── a/              # Recipes starting with 'a'
│   │   ├── actionlint.toml
│   │   ├── age.toml
│   │   └── aws-cli.toml
│   ├── b/
│   │   ├── bat.toml
│   │   └── bottom.toml
│   └── ...
├── schema/
│   └── recipe.json     # JSON schema for validation
└── .github/
    └── workflows/
        └── validate.yml
```

## Recipe Format

```toml
[metadata]
name = "tool-name"
description = "Tool description"
homepage = "https://tool-homepage.com"

[version]
source = "github"
github_repo = "owner/repo"

[[steps]]
action = "github_archive"
[steps.params]
repo = "owner/repo"
asset_pattern = "tool-{version}-{os}-{arch}.tar.gz"

[steps.params.os_map]
darwin = "darwin"
linux = "linux"

[steps.params.arch_map]
amd64 = "amd64"
arm64 = "arm64"

[[steps]]
action = "install_binaries"
[steps.params]
binaries = ["tool-name"]

[verify]
command = "tool-name --version"
pattern = "{version}"
```

## Adding a Recipe

1. Create `recipes/{first-letter}/{tool-name}.toml`
2. Follow the recipe format above
3. Test locally: `tsuku install --recipe-file path/to/recipe.toml`
4. Submit PR

## Validation

CI automatically validates all recipes on PR:
- Valid TOML syntax
- Required fields present
- Schema compliance

## Actions Reference

| Action | Use Case |
|--------|----------|
| `github_archive` | GitHub release tar.gz/zip |
| `github_file` | Single binary from GitHub |
| `download_archive` | Any URL archive |
| `hashicorp_release` | HashiCorp tools |
| `homebrew_bottle` | Homebrew bottles |
| `npm_install` | npm packages |
| `pipx_install` | Python packages |
| `cargo_install` | Rust crates |
| `gem_install` | Ruby gems |
| `nix_install` | Nix packages |
