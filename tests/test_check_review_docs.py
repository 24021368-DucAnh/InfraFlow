"""Regression tests for the local documentation review checker."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReviewDocsCheckTests(unittest.TestCase):
    def test_primary_recipe_must_cover_its_mapped_acceptance_case(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            shutil.copytree(ROOT / "docs", checkout / "docs")
            (checkout / "scripts").mkdir()
            shutil.copy2(ROOT / "scripts/check_review_docs.py", checkout / "scripts")

            sheet = checkout / "docs/planning/DUC-25-27-P3-P5-evidence-test-sheets.md"
            original = sheet.read_text(encoding="utf-8")
            old_row = "| BP-01 | P3-01 | URL-01 | P5-01 |"
            self.assertEqual(original.count(old_row), 1)
            sheet.write_text(original.replace(old_row, "| BP-01 | P3-08 | URL-01 | P5-01 |"), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(checkout / "scripts/check_review_docs.py")],
                cwd=checkout,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("P3-08 does not cover BP-01", result.stdout)


if __name__ == "__main__":
    unittest.main()
