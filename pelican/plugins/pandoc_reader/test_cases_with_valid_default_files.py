"""Tests using valid default files for pandoc-reader plugin."""
import os
import unittest

from pelican.tests.support import get_settings

from pandoc_reader import PandocReader

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_content"))
TEST_DEFAULT_FILES_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_default_files"))


class TestValidCasesWithDefaultFiles(unittest.TestCase):
    """Valid test cases using default files."""

    def test_valid_file_with_valid_defaults(self):
        """Check if we get the appropriate output specifying defaults."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "valid_defaults.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(
            (
                "<p>This is some valid content that should pass."
                " If it does not pass we will know something is wrong.</p>"
            ),
            output,
        )

        self.assertEqual("Valid Content", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_mathjax_with_valid_defaults(self):
        """Check if mathematics is rendered correctly with defaults."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "valid_defaults.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "mathjax_content.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(
            (
                '<p><span class="math display">\\[\n'
                "e^{i\\theta} = \\cos\\theta + i \\sin\\theta.\n"
                "\\]</span></p>"
            ),
            output,
        )

        self.assertEqual("MathJax Content", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_toc_with_valid_defaults(self):
        """Check if output and table of contents are valid with defaults."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "valid_defaults_with_toc.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)
        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_toc.md")
        output, metadata = pandoc_reader.read(source_path)
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(
            (
                "<p>This is some valid content that should pass."
                " If it does not pass we will know something is wrong.</p>\n"
                '<h2 id="first-heading">First Heading</h2>\n'
                "<p>This should be the first heading in my"
                " table of contents.</p>\n"
                '<h2 id="second-heading">Second Heading</h2>\n'
                "<p>This should be the second heading in my"
                " table of contents.</p>\n"
                '<h3 id="first-subheading">First Subheading</h3>\n'
                "<p>This is a subsection that should be shown as such"
                " in the table of contents.</p>\n"
                '<h3 id="second-subheading">Second Subheading</h3>\n'
                "<p>This is another subsection that should be shown as"
                " such in the table of contents.</p>"
            ),
            output,
        )

        self.assertEqual("Valid Content with Table of Contents", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))
        self.assertEqual(
            '<nav class="toc" role="doc-toc">\n'
            "<ul>\n"
            '<li><a href="#first-heading">First Heading</a></li>\n'
            '<li><a href="#second-heading">Second Heading</a>\n'
            "<ul>\n"
            '<li><a href="#first-subheading">First Subheading</a></li>\n'
            '<li><a href="#second-subheading">Second Subheading</a></li>\n'
            "</ul></li>\n"
            "</ul>\n"
            "</nav>",
            str(metadata["toc"]),
        )


if __name__ == "__main__":
    unittest.main()
