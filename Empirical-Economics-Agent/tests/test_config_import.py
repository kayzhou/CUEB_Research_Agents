"""Smoke-test the public Python configuration import surface."""

from __future__ import annotations

import unittest
from pathlib import Path

from code.config import PATHS, PROJECT_SLUG, REPO_ROOT, TOOLS


class ConfigImportSmokeTest(unittest.TestCase):
    def test_public_exports_resolve_from_repository(self) -> None:
        expected_root = Path(__file__).resolve().parents[1]
        self.assertEqual(REPO_ROOT, expected_root)
        self.assertEqual(PATHS["raw"], expected_root / "data" / "raw")
        self.assertEqual(
            PATHS["analysis"],
            expected_root / "code" / "analysis" / PROJECT_SLUG,
        )
        self.assertIn("python", TOOLS)
        self.assertIn("rscript", TOOLS)


if __name__ == "__main__":
    unittest.main()
