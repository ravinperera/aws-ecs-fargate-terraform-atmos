from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "check_markdown_links.py"
SPEC = importlib.util.spec_from_file_location("check_markdown_links", MODULE_PATH)
assert SPEC and SPEC.loader
check_markdown_links = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_markdown_links)


class MarkdownLinkValidatorTests(unittest.TestCase):
    def test_accepts_existing_local_external_and_anchor_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (root / "README.md").write_text(
                "[Guide](docs/guide.md)\n"
                "[Section](#local-section)\n"
                "[Website](https://example.com)\n",
                encoding="utf-8",
            )

            self.assertEqual(check_markdown_links.validate(root), [])

    def test_reports_missing_local_link_with_source_line(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "README.md").write_text(
                "# Example\n\n[Missing](docs/missing.md)\n",
                encoding="utf-8",
            )

            self.assertEqual(
                check_markdown_links.validate(root),
                ["README.md:3: missing local target 'docs/missing.md'"],
            )

    def test_ignores_links_inside_fenced_code_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "README.md").write_text(
                "```markdown\n[Example](not-a-real-file.md)\n```\n",
                encoding="utf-8",
            )

            self.assertEqual(check_markdown_links.validate(root), [])

    def test_validates_reference_style_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (root / "README.md").write_text(
                "[Guide][guide]\n\n[guide]: docs/guide.md\n",
                encoding="utf-8",
            )

            self.assertEqual(check_markdown_links.validate(root), [])


if __name__ == "__main__":
    unittest.main()
