# Design: Recipe Metadata Export for tsuku.dev

**Status**: Proposed

## Context and Problem Statement

The tsuku.dev website needs to display a browsable list of available recipes, enabling users to discover tools before installing tsuku. The high-level architecture has been decided: a GitHub Action in tsuku-registry generates JSON metadata that tsuku.dev consumes as a static file.

This design addresses the specific implementation: how the GitHub Action workflow extracts metadata from 170+ recipe TOML files and publishes it for tsuku.dev consumption.

### Current Situation

- Recipe TOML files live in `recipes/{first-letter}/{name}.toml`
- Each recipe has a `[metadata]` section with `name`, `description`, and `homepage` fields
- No automated process exports this metadata
- tsuku.dev has no data source to render a recipe browser

### Why This Matters

Without an automated export mechanism:
- Recipe browser implementation is blocked
- Manual maintenance would become a burden as recipes grow
- Data would drift out of sync with the canonical recipe definitions

### Scope

**In scope:**
- JSON schema for exported recipe metadata
- GitHub Action workflow definition
- Trigger conditions (push to main, scheduled)
- Cross-repo publish mechanism
- Validation of recipe metadata during export

**Out of scope:**
- tsuku.dev HTML/CSS/JS implementation (separate repo)
- Individual recipe detail pages (Phase 2)
- Version information in export (only metadata for now)

### Requirements

1. **Completeness**: Export all recipes from `recipes/{first-letter}/{name}.toml`
2. **Data fields**: Include `name`, `description`, `homepage`
3. **Performance**: Complete within 2 minutes for 200 recipes
4. **Validation**: Reject recipes with missing required metadata fields (fail-fast)
5. **Format**: Output valid JSON with schema version and generation timestamp
6. **Freshness**: Updates propagate to tsuku.dev within 5 minutes of merge to main

### Assumptions and Constraints

1. **Schema evolution**: New metadata fields will be additive; the JSON schema includes a version field for backward compatibility
2. **Failure mode**: Export fails entirely if any recipe has invalid metadata
3. **Update frequency**:
   - Trigger on every push to main (immediate freshness)
   - Scheduled daily run at 00:00 UTC (catch any missed updates)
   - Validation-only run on PRs (no publish, just verify recipes parse)
4. **JSON structure**:
   ```json
   {
     "schema_version": "1.0.0",
     "generated_at": "2025-11-29T12:00:00Z",
     "recipes": [
       {
         "name": "actionlint",
         "description": "GitHub Actions linter",
         "homepage": "https://github.com/rhysd/actionlint"
       }
     ]
   }
   ```
5. **GitHub Actions limits**: Workflow must complete within GitHub's 10-minute timeout

## Decision Drivers

- **Simplicity**: Minimal dependencies and moving parts
- **Reliability**: Export must not fail silently; errors should block merge
- **Freshness**: Data should update within minutes of recipe changes
- **Cross-repo coordination**: Must work with tsuku.dev without tight coupling
- **Validation**: Catch malformed recipes before they break the website

## External Research

### Homebrew (formulae.brew.sh)

**Approach**: A periodic GitHub Action pulls formula data from homebrew-core and homebrew-cask taps, then generates JSON via custom `brew generate-*-api` commands. Jekyll consumes the JSON to build the static site.

**Trade-offs**:
- Pro: Comprehensive API with per-formula endpoints and analytics
- Pro: Mature, battle-tested at scale (6000+ formulas)
- Con: Complex multi-repo architecture
- Con: Requires Ruby runtime and Homebrew-specific tooling

**Relevance to tsuku**: The pattern of generating JSON as a build artifact consumed by the static site is directly applicable. However, tsuku's simpler metadata (name/description/homepage only) doesn't require Homebrew's complexity.

**Source**: [Homebrew/formulae.brew.sh](https://github.com/Homebrew/formulae.brew.sh)

### mise (registry.toml)

**Approach**: Single TOML file in the main repo defines all tools with backends, descriptions, and test commands. The registry.html page is generated at build time.

**Trade-offs**:
- Pro: Single-file simplicity (one registry.toml)
- Pro: No cross-repo coordination needed
- Con: Doesn't scale as well for detailed per-tool metadata

**Relevance to tsuku**: tsuku already has per-tool TOML files (more flexible than single-file), so the generation approach differs, but the "build-time static generation" pattern applies.

**Source**: [jdx/mise registry.toml](https://github.com/jdx/mise/blob/main/registry.toml)

### Research Summary

**Common patterns:**
- Build-time JSON generation from canonical source files
- Static output consumed by frontend (no runtime API)
- GitHub Actions as the automation mechanism

**Key differences:**
- Homebrew uses complex multi-repo with Ruby tooling
- mise uses single-file registry
- tsuku needs per-file TOML parsing with simpler output

**Implications for tsuku:**
- A simple shell/Python script to parse TOML and emit JSON is sufficient
- Cross-repo publishing requires either `repository_dispatch` or committing to the target repo
- Validation should happen in CI before merge, not just during export

## Considered Options

This design addresses two orthogonal decisions:
1. **Generation script**: How to parse TOML and emit JSON
2. **Publishing mechanism**: How to get JSON to tsuku.dev

### Option 1a: Shell Script with yq/jq

Use a shell script with `yq` (TOML parser) and `jq` (JSON processor) to extract metadata and build the JSON file.

**Pros:**
- No additional runtime dependencies beyond common CLI tools
- Easy to understand and debug
- Runs quickly for small datasets

**Cons:**
- yq TOML support is less mature than dedicated parsers
- Multiple `yq` implementations exist (mikefarah vs python-yq) with different syntax
- Shell scripting is fragile for complex parsing logic
- Error handling is verbose
- Hard to unit test

### Option 1b: Python Script with tomllib

Use Python (3.11+) with the standard library `tomllib` module to parse TOML and emit JSON.

**Pros:**
- `tomllib` is in the Python standard library (3.11+)
- Robust error handling
- Easy to extend with validation logic
- GitHub Actions runners have Python 3.11+ pre-installed
- JSON schema validation libraries readily available
- Easy to unit test
- Rich standard library for file operations

**Cons:**
- Requires Python 3.11+ (reasonable for CI)
- Slightly more verbose than shell for simple tasks

### Option 1c: Go Script Using tsuku's TOML Parser

Write a Go tool that reuses tsuku's existing TOML parsing logic.

**Pros:**
- Single binary, no runtime dependencies
- Could share code with tsuku CLI
- Type-safe parsing
- Could validate recipes using same logic as tsuku CLI
- Could enable future recipe linting tools

**Cons:**
- Requires Go toolchain in CI (setup-go action needed)
- More setup overhead for a simple metadata extraction task
- Adds complexity to the registry repo (Go module setup)
- Registry repo is currently code-free (TOML only)

---

### Option 2a: Commit JSON to tsuku.dev Repository

The GitHub Action in tsuku-registry commits the generated JSON directly to tsuku.dev repo using a deploy key.

**Pros:**
- JSON is versioned in tsuku.dev repo
- Cloudflare Pages auto-deploys on commit
- Simple, single workflow to maintain
- Clear audit trail in tsuku.dev commit history

**Cons:**
- Requires deploy key setup with write access to tsuku.dev
- Commit history in tsuku.dev shows automated commits (Git history pollution)
- Tight coupling between repos
- Commit message convention needs to be established

### Option 2b: Trigger tsuku.dev Build via repository_dispatch

tsuku-registry sends a `repository_dispatch` event to tsuku.dev, which fetches the JSON during its build.

**Pros:**
- tsuku.dev owns its data fetching logic
- No automated commits to tsuku.dev
- Looser coupling
- tsuku.dev can implement rate limiting/caching independently
- Easier to add multiple consumers later (docs site, CLI search index)

**Cons:**
- Requires PAT with repo scope
- Two workflows to maintain (one here, one in tsuku.dev)
- Slightly more complex debugging
- tsuku.dev build must fetch JSON (adds external dependency)

### Option 2c: Publish JSON to GitHub Pages from tsuku-registry

Generate and publish `recipes.json` to GitHub Pages served from tsuku-registry itself (e.g., `https://registry.tsuku.dev/recipes.json`). tsuku.dev fetches from this stable URL at build time.

**Pros:**
- No cross-repo coordination needed at build time
- Stable URL for any consumer
- GitHub-native hosting with CDN
- No PAT or deploy key required
- Enables other consumers (CLI, third-party integrations)

**Cons:**
- Requires GitHub Pages setup in tsuku-registry
- Requires custom domain DNS configuration
- tsuku.dev build depends on external URL availability
- Slight delay between push and Pages deployment

### Decision Driver Evaluation

| Option | Simplicity | Reliability | Freshness | Cross-repo | Validation |
|--------|------------|-------------|-----------|------------|------------|
| 1a: Shell/yq | Fair | Poor | N/A | N/A | Poor |
| 1b: Python | Good | Good | N/A | N/A | Good |
| 1c: Go | Fair | Good | N/A | N/A | Good |
| 2a: Commit | Good | Good | Good | Fair | N/A |
| 2b: Dispatch | Fair | Fair | Good | Good | N/A |
| 2c: GitHub Pages | Good | Good | Good | Good | N/A |

### Recommended Combinations

Based on the decision drivers, the most viable combinations are:

1. **Python (1b) + Commit (2a)**: Best for simplicity. Single workflow, immediate updates, but creates commit noise in tsuku.dev.

2. **Python (1b) + GitHub Pages (2c)**: Best for decoupling. tsuku-registry owns its data endpoint, no cross-repo credentials needed, enables future consumers.

### Uncertainties

- Python 3.11+ availability on GitHub Actions runners (believed available on ubuntu-latest)
- Cloudflare Pages build trigger behavior with `repository_dispatch` (untested)
- Whether automated commits to tsuku.dev will cause notification noise
- GitHub Pages CDN cache invalidation timing

## Decision Outcome

**Chosen option: Python (1b) + GitHub Pages (2c)**

A Python script using `tomllib` generates the JSON, which is published to GitHub Pages from tsuku-registry. This combination provides the best balance of simplicity, decoupling, and extensibility.

### Rationale

This option was chosen because:
- **Simplicity**: Python's `tomllib` is in the standard library (no dependencies), and GitHub Pages requires minimal setup
- **Validation**: Python makes it easy to add schema validation and fail-fast error handling
- **Cross-repo decoupling**: No credentials needed between tsuku-registry and tsuku.dev
- **Extensibility**: A stable URL (`registry.tsuku.dev/recipes.json`) enables future consumers (CLI search, third-party tools)

Alternatives were rejected because:
- **Shell/yq (1a)**: Fragile parsing and multiple yq implementations make it unreliable
- **Go (1c)**: Adds Go module complexity to a currently code-free repository
- **Commit to tsuku.dev (2a)**: Creates commit noise and requires deploy key management
- **repository_dispatch (2b)**: Two workflows to maintain, more complex debugging

### Trade-offs Accepted

By choosing this option, we accept:
- **DNS configuration**: Requires setting up `registry.tsuku.dev` subdomain pointing to GitHub Pages
- **GitHub Pages setup**: Need to configure Pages deployment in this repository
- **Cache timing**: GitHub Pages CDN may have brief delays (typically under 1 minute)
- **Python dependency**: Script requires Python 3.11+ (available on GitHub Actions ubuntu-latest)

These are acceptable because:
- DNS setup is a one-time task
- GitHub Pages is free and low-maintenance
- Sub-minute cache delays don't impact the "within 5 minutes" freshness requirement
- Python 3.11+ is readily available in GitHub Actions

## Solution Architecture

### Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      tsuku-registry                          │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐  │
│  │ recipes/     │ ──▶  │ scripts/     │ ──▶  │ _site/    │  │
│  │ *.toml       │      │ generate.py  │      │ recipes.  │  │
│  │              │      │              │      │ json      │  │
│  └──────────────┘      └──────────────┘      └───────────┘  │
│                              │                     │         │
│                    GitHub Actions            GitHub Pages    │
│                    (on push/schedule)        (auto-deploy)   │
└─────────────────────────────────────────────────────────────┘
                                                     │
                                                     ▼
                                    https://registry.tsuku.dev/recipes.json
                                                     │
                                                     ▼
                                    ┌─────────────────────────┐
                                    │       tsuku.dev         │
                                    │   (Cloudflare Pages)    │
                                    │   fetches at build      │
                                    └─────────────────────────┘
```

### Components

1. **Recipe TOML files** (`recipes/{letter}/{name}.toml`)
   - Source of truth for tool metadata
   - Contains `[metadata]` section with name, description, homepage

2. **Generation script** (`scripts/generate.py`)
   - Parses all recipe TOML files
   - Validates required fields
   - Outputs `_site/recipes.json`

3. **GitHub Actions workflow** (`.github/workflows/generate-recipes.yml`)
   - Triggers on push to main and daily schedule
   - Runs generation script
   - Deploys to GitHub Pages

4. **GitHub Pages** (`_site/` directory)
   - Serves `recipes.json` at stable URL
   - Custom domain: `registry.tsuku.dev`

### Key Interfaces

**Output JSON Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "schema_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "generated_at": { "type": "string", "format": "date-time" },
    "recipes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "description", "homepage"],
        "properties": {
          "name": { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "description": { "type": "string", "maxLength": 200 },
          "homepage": { "type": "string", "format": "uri" }
        }
      }
    }
  },
  "required": ["schema_version", "generated_at", "recipes"]
}
```

**Validation Rules**:
- `name`: Must match filename stem (without `.toml`), lowercase alphanumeric and hyphens only
- `description`: Required, max 200 characters, no control characters (U+0000-U+001F)
- `homepage`: Required, must start with `https://` (reject `http://`, `javascript:`, `data:`)
- File path: Must match pattern `recipes/[a-z]/[a-z0-9-]+\.toml`
- File size: Maximum 100KB per recipe file

### Data Flow

1. **On push to main** or **daily at 00:00 UTC**:
   - GitHub Actions triggers `generate-recipes.yml`
   - Checkout repository
   - Run `python scripts/generate.py`
   - Script finds all `recipes/*/*.toml` files
   - For each file: parse TOML, extract metadata, validate
   - If any validation fails: exit with error (fail CI)
   - If all valid: write `_site/recipes.json`
   - Deploy `_site/` to GitHub Pages

2. **On tsuku.dev build** (Cloudflare Pages):
   - Fetch `https://registry.tsuku.dev/recipes.json`
   - Render recipe browser page

## Implementation Approach

### Phase 1: Generation Script

Create `scripts/generate.py`:
- Use `tomllib` to parse TOML
- Use `pathlib` to find recipe files
- Create `_site/` directory if it doesn't exist
- Validate required fields (fail-fast with descriptive errors)
- Validate file paths stay within `recipes/` directory (path traversal check)
- Validate file size under 100KB limit
- Validate filename matches `metadata.name` (case-sensitive)
- Output sorted JSON (alphabetically by name, case-insensitive)
- Exit non-zero on validation errors (print all errors, not just first)

Deliverable: Script that can be run locally to generate JSON.

### Phase 2: DNS and Pages Configuration

Configure GitHub Pages (before workflow, so deployment has a target):
- Enable Pages in repository settings
- Set source to GitHub Actions
- Configure custom domain `registry.tsuku.dev` (CNAME record pointing to `tsuku-dev.github.io`)
- Commit `_site/CNAME` file containing `registry.tsuku.dev`

Deliverable: GitHub Pages configured and ready for deployments.

### Phase 3: GitHub Actions Workflow

Create `.github/workflows/generate-recipes.yml`:
- Trigger on `push` to `main` and `schedule` (daily at 00:00 UTC)
- Run generation script
- Deploy to GitHub Pages using `actions/deploy-pages`
- Pin actions to commit SHAs (not tags)

Deliverable: Automated generation on every push.

### Phase 4: PR Validation Workflow

Create `.github/workflows/validate-recipes.yml`:
- Trigger on `pull_request`
- Run generation script (validates all recipes)
- Do NOT deploy (validation only)

Deliverable: PRs with invalid recipes fail CI.

## Consequences

### Positive

- **Discovery**: Users can browse recipes before installing tsuku
- **Automation**: Recipe list stays in sync with registry automatically
- **Extensibility**: Stable URL enables future consumers (CLI, third parties)
- **Simplicity**: Single repository owns generation and hosting

### Negative

- **DNS dependency**: Requires `registry.tsuku.dev` subdomain setup
- **GitHub Pages limits**: 100GB/month bandwidth (more than sufficient)
- **Build latency**: ~1 minute delay between push and URL update
- **Script maintenance**: Python script needs to evolve with schema changes

### Mitigations

- DNS setup is a one-time task with clear documentation
- Bandwidth limits are unlikely to be hit for a JSON file
- 1-minute latency is acceptable for the "within 5 minutes" requirement
- Script is simple (~50 lines) and easy to maintain

## Security Considerations

### Download Verification

**Not applicable** - This feature does not download external artifacts. The generation script only reads local TOML files already in the repository. The only "download" is tsuku.dev fetching the generated JSON from GitHub Pages, which is served over HTTPS with TLS verification.

### Execution Isolation

The generation script runs in GitHub Actions with minimal permissions:

- **File system access**: Read-only access to `recipes/` directory, write access to `_site/` output directory
- **Network access**: None required during generation; GitHub Pages deployment uses GitHub's built-in actions
- **Privilege escalation**: None. Script runs as unprivileged GitHub Actions user

**GitHub Actions permissions** should be scoped to:
```yaml
permissions:
  contents: read
  pages: write
  id-token: write  # Required for Pages deployment
```

### Supply Chain Risks

**Input source**: Recipe TOML files are contributed via pull requests. The trust model is:

1. **PR review**: All changes require human review before merge
2. **Malicious metadata**: A malicious contributor could add XSS payloads in `description` or `homepage` fields
3. **Upstream compromise**: If tsuku-registry is compromised, the attacker could inject malicious JSON
4. **GitHub Actions compromise**: A compromised action version could inject malicious code

**Mitigations**:

| Risk | Mitigation | Residual Risk |
|------|------------|---------------|
| XSS in description | Validate no control characters; consumer must use `textContent` (not `innerHTML`) or escape HTML entities | Consumer implementation bug |
| Malicious homepage URL | Validate HTTPS-only; reject `javascript:`, `data:` schemes; consumer uses `rel="noopener noreferrer"` | User clicks link to phishing site |
| Repository compromise | Branch protection (require PR + review + status checks); 2FA for maintainers | Sophisticated attacker with stolen maintainer credentials |
| GitHub Actions compromise | Pin actions to commit SHAs; enable Dependabot alerts | Compromised action version before security advisory |

**Repository Security Configuration** (required before going live):
- Branch protection on `main`:
  - Require pull request before merging
  - Require at least 1 approval
  - Require status checks (validate-recipes workflow)
- Require 2FA for all maintainers
- Enable Dependabot for GitHub Actions version monitoring

### User Data Exposure

**Data accessed**: Only recipe TOML files in the public repository. No user data is accessed.

**Data transmitted**: The generated JSON is published to GitHub Pages. This JSON contains:
- Recipe names (public, from TOML filenames)
- Descriptions (public, from TOML files)
- Homepage URLs (public, from TOML files)
- Generation timestamp (not sensitive)
- Schema version (not sensitive)

**Privacy implications**: None. All data is already public in the repository. The JSON export does not expose any private or user-specific information.

### Additional Security Measures

1. **Input validation**: The generation script validates:
   - Recipe names match `^[a-z0-9-]+$` pattern (no special characters)
   - Homepage URLs use HTTPS scheme only (reject `http://`, `javascript:`, `data:`)
   - Description length is bounded (max 200 chars)
   - No control characters in description (U+0000-U+001F)
   - File size under 100KB per recipe

2. **Path validation**: Ensure recipe file paths resolve within `recipes/` directory (prevents path traversal attacks).

3. **Fail-fast**: Any invalid recipe fails the entire CI run, preventing partial or corrupted output.

4. **No secrets**: The workflow requires no secrets or tokens beyond GitHub's built-in `GITHUB_TOKEN` for Pages deployment.

5. **Actions pinning**: Pin GitHub Actions to commit SHAs instead of version tags.

6. **Dependency management**: Use Python 3.11+ standard library only (`tomllib`, `pathlib`, `json`). No external pip dependencies.

