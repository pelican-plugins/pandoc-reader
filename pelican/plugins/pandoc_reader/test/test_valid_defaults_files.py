"""Test using valid default files with the pandoc-reader plugin."""
import os
import unittest

from pelican.plugins.pandoc_reader import PandocReader
from pelican.plugins.pandoc_reader.test.html.expected_html import (
    HTML_MATHJAX,
    HTML_TOC,
    HTML_VALID_TEXT,
    HTML_WITH_HEADINGS,
)
from pelican.tests.support import get_settings

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "markdown"))
TEST_DEFAULTS_FILES_PATH = os.path.abspath(os.path.join(DIR_PATH, "defaults_files"))


class TestValidCasesWithDefaultsFiles(unittest.TestCase):
    """Valid test cases using defaults files."""

    def test_valid_file_with_valid_defaults(self):
        """Check if we get the expected output specifying valid defaults."""
        pandoc_defaults_files = [
            os.path.join(TEST_DEFAULTS_FILES_PATH, "valid_defaults.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULTS_FILES=pandoc_defaults_files)

        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(HTML_VALID_TEXT, output)
        self.assertEqual("Valid Content", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_mathjax_with_valid_defaults(self):
        """Check if mathematics is rendered correctly with valid defaults."""
        pandoc_defaults_files = [
            os.path.join(TEST_DEFAULTS_FILES_PATH, "valid_defaults.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULTS_FILES=pandoc_defaults_files)

        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "mathjax_content.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(HTML_MATHJAX, output)
        self.assertEqual("MathJax Content", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_toc_with_valid_defaults(self):
        """Check if output and table of contents are as expected with valid defaults."""
        pandoc_defaults_files = [
            os.path.join(TEST_DEFAULTS_FILES_PATH, "valid_defaults_with_toc.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULTS_FILES=pandoc_defaults_files)
        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_toc.md")
        output, metadata = pandoc_reader.read(source_path)
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(HTML_WITH_HEADINGS, output)
        self.assertEqual("Valid Content with Table of Contents", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))
        self.assertEqual(HTML_TOC, str(metadata["toc"]))


if __name__ == "__main__":
    unittest.main()
