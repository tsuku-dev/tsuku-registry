# Issue 3 Implementation Plan

## Summary

Create a Python script using only standard library modules (tomllib, pathlib, json) that parses all recipe TOML files, validates metadata, and outputs a sorted JSON file.

## Approach

Single-file Python script with clear separation between:
1. File discovery (pathlib glob)
2. Parsing and validation (tomllib + custom validation)
3. JSON generation (json.dumps)

The script is intentionally simple (~100 lines) with no external dependencies, making it easy to maintain and audit.

### Alternatives Considered
- **Multiple modules**: Not needed for this scope; single file is simpler
- **External validation library (jsonschema)**: Would add pip dependency; custom validation is sufficient for 5 rules

## Files to Create
- `scripts/generate.py` - Main generation script

## Files to Modify
- None (new feature)

## Implementation Steps
- [ ] Create scripts directory and generate.py skeleton
- [ ] Implement file discovery (glob recipes/*/*.toml)
- [ ] Implement TOML parsing with tomllib
- [ ] Implement validation rules (name, description, homepage, path, size)
- [ ] Implement JSON output generation
- [ ] Implement error aggregation and exit codes
- [ ] Test with existing 171 recipes

## Testing Strategy
- **Manual verification**: Run against all 171 recipes, verify output format
- **Edge case testing**: Test with invalid recipes (create temp test files)
- **Validation**: Verify error messages are descriptive

## Risks and Mitigations
- **Existing recipes may fail validation**: Run early to identify issues; may need to fix recipes
- **Performance with 171 files**: Should be fast (~1 second); verify

## Success Criteria
- [ ] Script parses all 171 existing recipes without error
- [ ] Output JSON matches schema (schema_version, generated_at, recipes array)
- [ ] Validation catches: missing fields, invalid homepage, long description, invalid name
- [ ] Exit code is non-zero on validation failures
- [ ] Recipes sorted alphabetically

## Open Questions
None - requirements are clear from design document.
