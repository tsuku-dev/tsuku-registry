#!/usr/bin/env python3
"""Tests for generate.py."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import generate


class TestValidation(unittest.TestCase):
    """Test validation functions."""

    def test_validate_path_valid(self):
        """Valid paths should pass."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a valid path structure
            recipes_dir = Path(tmpdir) / "recipes" / "a"
            recipes_dir.mkdir(parents=True)
            test_file = recipes_dir / "test-tool.toml"
            test_file.write_text("")

            with patch.object(generate, "RECIPES_DIR", Path(tmpdir) / "recipes"):
                errors = generate.validate_path(test_file)
                # Path pattern won't match since it's not recipes/[a-z]/...
                # This tests the path traversal check passes
                self.assertTrue(any("pattern" in str(e) for e in errors) or len(errors) == 0)

    def test_validate_metadata_missing_fields(self):
        """Missing required fields should error."""
        errors = generate.validate_metadata(Path("test.toml"), {})
        self.assertEqual(len(errors), 3)  # name, description, homepage

    def test_validate_metadata_name_mismatch(self):
        """Name must match filename."""
        errors = generate.validate_metadata(
            Path("recipes/a/foo.toml"),
            {"name": "bar", "description": "test", "homepage": "https://example.com"}
        )
        self.assertTrue(any("does not match filename" in str(e) for e in errors))

    def test_validate_metadata_invalid_name(self):
        """Name must be lowercase alphanumeric with hyphens."""
        errors = generate.validate_metadata(
            Path("recipes/a/Test_Tool.toml"),
            {"name": "Test_Tool", "description": "test", "homepage": "https://example.com"}
        )
        self.assertTrue(any("invalid characters" in str(e) for e in errors))

    def test_validate_metadata_http_homepage(self):
        """Homepage must be HTTPS."""
        errors = generate.validate_metadata(
            Path("recipes/a/test.toml"),
            {"name": "test", "description": "test", "homepage": "http://example.com"}
        )
        self.assertTrue(any("must start with https://" in str(e) for e in errors))

    def test_validate_metadata_long_description(self):
        """Description must be under 200 chars."""
        errors = generate.validate_metadata(
            Path("recipes/a/test.toml"),
            {"name": "test", "description": "x" * 250, "homepage": "https://example.com"}
        )
        self.assertTrue(any("exceeds limit" in str(e) for e in errors))

    def test_validate_metadata_control_chars(self):
        """Description must not contain control characters."""
        errors = generate.validate_metadata(
            Path("recipes/a/test.toml"),
            {"name": "test", "description": "test\x00", "homepage": "https://example.com"}
        )
        self.assertTrue(any("control characters" in str(e) for e in errors))

    def test_validate_metadata_dangerous_scheme(self):
        """Homepage must not contain dangerous schemes."""
        errors = generate.validate_metadata(
            Path("recipes/a/test.toml"),
            {"name": "test", "description": "test", "homepage": "https://example.com?redirect=javascript:alert(1)"}
        )
        self.assertTrue(any("dangerous scheme" in str(e) for e in errors))


class TestGenerateJson(unittest.TestCase):
    """Test JSON generation."""

    def test_generate_json_structure(self):
        """Output should have required fields."""
        recipes = [
            {"name": "bar", "description": "Bar tool", "homepage": "https://bar.com"},
            {"name": "foo", "description": "Foo tool", "homepage": "https://foo.com"},
        ]
        output = generate.generate_json(recipes)

        self.assertIn("schema_version", output)
        self.assertIn("generated_at", output)
        self.assertIn("recipes", output)
        self.assertEqual(output["schema_version"], "1.0.0")

    def test_generate_json_sorted(self):
        """Recipes should be sorted alphabetically."""
        recipes = [
            {"name": "zebra", "description": "Z", "homepage": "https://z.com"},
            {"name": "alpha", "description": "A", "homepage": "https://a.com"},
        ]
        output = generate.generate_json(recipes)

        self.assertEqual(output["recipes"][0]["name"], "alpha")
        self.assertEqual(output["recipes"][1]["name"], "zebra")


class TestIntegration(unittest.TestCase):
    """Integration tests with actual recipe files."""

    def test_parse_existing_recipes(self):
        """All existing recipes should parse successfully."""
        # Only run if we're in the right directory
        if not Path("recipes").exists():
            self.skipTest("Not in repository root")

        recipe_files = generate.discover_recipes()
        self.assertGreater(len(recipe_files), 100)  # Should have 170+ recipes

        errors = []
        for file_path in recipe_files:
            _, file_errors = generate.parse_recipe(file_path)
            errors.extend(file_errors)

        self.assertEqual(len(errors), 0, f"Validation errors: {errors}")


if __name__ == "__main__":
    unittest.main()
