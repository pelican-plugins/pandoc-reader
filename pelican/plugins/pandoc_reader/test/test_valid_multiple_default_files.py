"""Test using multiple valid defaults files with the pandoc-reader plugin."""
import os
import unittest

from pelican.plugins.pandoc_reader import PandocReader
from pelican.plugins.pandoc_reader.test.html.expected_html import (
    HTML_TOC,
    HTML_WITH_HEADINGS,
)
from pelican.tests.support import get_settings

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "markdown"))
TEST_DEFAULTS_FILES_PATH = os.path.abspath(os.path.join(DIR_PATH, "defaults_files"))


class TestValidCasesWithMultipleDefaultsFiles(unittest.TestCase):
    def test_multiple_defaults_files_valid_case(self):
        """Check that we get the expected output with multiple valid default files."""
        pandoc_defaults_files = [
            os.path.join(TEST_DEFAULTS_FILES_PATH, "valid_defaults_file_1.yaml"),
            os.path.join(TEST_DEFAULTS_FILES_PATH, "valid_defaults_file_2.yaml"),
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
