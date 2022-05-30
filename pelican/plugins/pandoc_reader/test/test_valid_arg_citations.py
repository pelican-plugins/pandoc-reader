"""Test using valid arguments and citations with the pandoc-reader plugin."""
import os
import unittest

from pelican.plugins.pandoc_reader import PandocReader
from pelican.plugins.pandoc_reader.test.html.expected_html import (
    HTML_CITATION_TOC,
    HTML_WITH_CITATIONS,
)
from pelican.tests.support import get_settings

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "markdown"))
TEST_DEFAULTS_FILES_PATH = os.path.abspath(os.path.join(DIR_PATH, "defaults_files"))

# These settings will be set in pelicanconf.py by plugin users.
# Appending --wrap=None so that rendered HTML5 does not have new lines (\n)
# which causes tests to fail.
# See https://pandoc.org/MANUAL.html#general-writer-options
PANDOC_ARGS = ["--mathjax", "--wrap=none"]
PANDOC_EXTENSIONS = ["+smart"]


class TestValidCaseWithArgumentsAndCitations(unittest.TestCase):
    """Test cases with valid arguments and citations."""

    def test_citations_1(self):
        """Check if expected output and citations is returned with -C argument."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS
            + [
                "-C",
                "--csl=https://www.zotero.org/styles/ieee-with-url",
                "--metadata=link-citations:false",
                "--metadata=reference-section-title:References",
            ],
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        output, metadata = pandoc_reader.read(source_path)

        # Setting this so that assert is able to execute the difference
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(HTML_WITH_CITATIONS, output)
        self.assertEqual("Valid Content With Citation", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_citations_2(self):
        """Check if expected output and citations is returned with --citeproc."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS
            + [
                "--citeproc",
                "--csl=https://www.zotero.org/styles/ieee-with-url",
                "--metadata=link-citations:false",
                "--metadata=reference-section-title:References",
            ],
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        output, metadata = pandoc_reader.read(source_path)

        # Setting this so that assert is able to execute the difference
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(HTML_WITH_CITATIONS, output)
        self.assertEqual("Valid Content With Citation", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_citations_and_toc_with_valid_defaults(self):
        """Check if expected output, citations and table of contents is returned."""
        pandoc_defaults_files = [
            os.path.join(
                TEST_DEFAULTS_FILES_PATH,
                "valid_defaults_with_toc_and_citations.yaml",
            )
        ]

        settings = get_settings(
            PANDOC_DEFAULTS_FILES=pandoc_defaults_files,
        )
        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        output, metadata = pandoc_reader.read(source_path)
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(HTML_WITH_CITATIONS, output)
        self.assertEqual("Valid Content With Citation", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))
        self.assertEqual(HTML_CITATION_TOC, str(metadata["toc"]))

    def test_citations_and_with_citeproc_filter(self):
        """Check if expected output, citations are returned using citeproc filter."""
        pandoc_defaults_files = [
            os.path.join(
                TEST_DEFAULTS_FILES_PATH,
                "valid_defaults_with_citeproc_filter.yaml",
            )
        ]

        settings = get_settings(
            PANDOC_DEFAULTS_FILES=pandoc_defaults_files,
        )
        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        output, metadata = pandoc_reader.read(source_path)
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(HTML_WITH_CITATIONS, output)
        self.assertEqual("Valid Content With Citation", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))


if __name__ == "__main__":
    unittest.main()
