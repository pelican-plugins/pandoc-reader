"""Test global bibliography support with the pandoc-reader plugin."""

import os
import unittest

from pelican.plugins.pandoc_reader import PandocReader
from pelican.tests.support import get_settings

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "markdown"))

PANDOC_ARGS = ["--mathjax", "--wrap=none", "--citeproc"]
PANDOC_EXTENSIONS = ["+smart"]


class TestGlobalBibliography(unittest.TestCase):
    """Test cases for global bibliography functionality."""

    def test_individual_bibliography_only(self):
        """Test that individual bibliography files still work."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual("Valid Content With Citation", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_global_bibliography_default_names(self):
        """Test that global bibliography files with default names are found."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "content_with_global_bib.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual("Content With Global Bibliography", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_custom_global_bibliography_names(self):
        """Test that custom global bibliography file names work."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
            PANDOC_GLOBAL_BIB_FILES=["my_bib", "global_refs"],
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(
            TEST_CONTENT_PATH, "content_with_custom_global_bib.md"
        )
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(
            "Content With Custom Global Bibliography", str(metadata["title"])
        )
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_both_individual_and_global_bibliography(self):
        """Test that both individual and global bibliography files are found."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "content_with_both_bibs.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual("Content With Both Bibliographies", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_no_bibliography_files(self):
        """Test behavior when no bibliography files exist."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "content_without_bib.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual("Content Without Bibliography", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_multiple_global_bibliography_files(self):
        """Test that multiple global bibliography files are found."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(
            TEST_CONTENT_PATH, "content_with_multiple_global_bibs.md"
        )
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(
            "Content With Multiple Global Bibliographies", str(metadata["title"])
        )
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))


if __name__ == "__main__":
    unittest.main()
