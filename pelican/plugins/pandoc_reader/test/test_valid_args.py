"""Test using valid arguments and extensions with the pandoc-reader plugin."""
import os
import unittest

from pelican.plugins.pandoc_reader import PandocReader
from pelican.plugins.pandoc_reader.test.html.expected_html import (
    HTML_MATHJAX,
    HTML_RAW_CONVERSION,
    HTML_TOC,
    HTML_VALID_TEXT,
    HTML_WITH_HEADINGS,
)
from pelican.tests.support import get_settings

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "markdown"))

# These settings will be set in pelicanconf.py by plugin users.
# Appending --wrap=None so that rendered HTML5 does not have new lines (\n)
# which causes tests to fail.
# See https://pandoc.org/MANUAL.html#general-writer-options
PANDOC_ARGS = ["--mathjax", "--wrap=none"]
PANDOC_EXTENSIONS = ["+smart"]


class TestValidCasesWithArguments(unittest.TestCase):
    """Valid test cases using Pandoc arguments and extensions."""

    def test_valid_file(self):
        """Check if we get the expected output for valid input."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(HTML_VALID_TEXT, output)
        self.assertEqual("Valid Content", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_mathjax_content(self):
        """Check if mathematics is rendered correctly."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "mathjax_content.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(HTML_MATHJAX, output)
        self.assertEqual("MathJax Content", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_encoded_to_raw_conversion(self):
        """Check if raw paths are left untouched in output returned."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_raw_paths.md")
        output, metadata = pandoc_reader.read(source_path)

        # Setting this so that assert is able to execute the difference
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(HTML_RAW_CONVERSION, output)
        self.assertEqual(
            "Valid Content with Fictitious Raw Paths", str(metadata["title"])
        )
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_valid_content_with_toc_1(self):
        """Check if expected output is returned with --toc argument."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS + ["--toc"],
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_toc.md")
        output, metadata = pandoc_reader.read(source_path)

        # Setting this so that assert is able to execute the difference
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(HTML_WITH_HEADINGS, output)
        self.assertEqual("Valid Content with Table of Contents", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))
        self.assertEqual(HTML_TOC, str(metadata["toc"]))

    def test_valid_content_with_toc_2(self):
        """Check if expected output is returned with --table-of-contents argument."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS + ["--table-of-contents"],
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_toc.md")
        output, metadata = pandoc_reader.read(source_path)

        # Setting this so that assert is able to execute the difference
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(HTML_WITH_HEADINGS, output)
        self.assertEqual("Valid Content with Table of Contents", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))
        self.assertEqual(HTML_TOC, str(metadata["toc"]))


if __name__ == "__main__":
    unittest.main()
