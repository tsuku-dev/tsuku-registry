# tsuku-registry

Recipe definitions for [tsuku](https://github.com/tsuku-dev/tsuku), a self-contained package manager.

## Structure

Recipes are organized alphabetically:

```
recipes/
├── a/
│   ├── actionlint.toml
│   ├── age.toml
│   └── ...
├── b/
│   ├── bat.toml
│   └── ...
└── ...
```

## Adding a Recipe

1. Fork this repository
2. Create your recipe in the appropriate `recipes/[first-letter]/` directory
3. Test locally: `tsuku install --recipe-file path/to/recipe.toml`
4. Submit a pull request

## Recipe Format

Each recipe is a TOML file with the following structure:

```toml
[metadata]
name = "tool-name"
description = "Brief description of the tool"
homepage = "https://example.com"

[version]
github_repo = "owner/repo"  # For version detection

[[steps]]
action = "github_archive"   # Or other action type
repo = "owner/repo"
asset_pattern = "tool-{version}-{os}-{arch}.tar.gz"
binaries = ["tool"]

[verify]
command = "tool --version"
pattern = "{version}"
```

See the [tsuku documentation](https://github.com/tsuku-dev/tsuku) for the complete recipe format reference.

## Requirements

- Valid TOML syntax
- `[metadata]` section with name and description
- At least one `[[steps]]` section
- Supports both Linux and macOS (unless the tool is platform-specific)
- No hardcoded paths or secrets

## License

MIT
