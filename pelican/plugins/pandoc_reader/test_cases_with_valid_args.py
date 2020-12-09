"""Tests using valid arguments and extensions for pandoc-reader plugin."""
import os
import unittest

from pelican.tests.support import get_settings

from pandoc_reader import PandocReader

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_content"))

# Test settings that will be set in pelicanconf.py by plugin users
PANDOC_ARGS = ["--mathjax"]
PANDOC_EXTENSIONS = ["+smart"]


class TestValidCasesWithArguments(unittest.TestCase):
    """Valid test cases using Pandoc arguments and extensions."""

    def test_valid_file(self):
        """Check if we get the appropriate output for valid input."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(
            (
                "<p>This is some valid content that should pass."
                " If it does not pass we"
                " will know something is wrong.</p>"
            ),
            output,
        )

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

        self.assertEqual(
            (
                "<p>This is some valid content that should pass."
                " If it does not pass we will know something is wrong.</p>\n"
                "<p>Our fictitious internal files are available"
                ' <a href="{filename}/path/to/file">at</a>:</p>\n'
                "<p>Our fictitious static files are available"
                ' <a href="{static}/path/to/file">at</a>:</p>\n'
                "<p>Our fictitious attachments are available"
                ' <a href="{attach}path/to/file">at</a>:</p>'
            ),
            output,
        )

        self.assertEqual(
            "Valid Content with Fictitious Raw Paths", str(metadata["title"])
        )
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_valid_content_with_toc_1(self):
        """Check if output returned is valid and table of contents is valid."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS + ["--toc"],
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_toc.md")
        output, metadata = pandoc_reader.read(source_path)

        # Setting this so that assert is able to execute the difference
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

    def test_valid_content_with_toc_2(self):
        """Check if output returned is valid and table of contents is valid."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS + ["--table-of-contents"],
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_toc.md")
        output, metadata = pandoc_reader.read(source_path)

        # Setting this so that assert is able to execute the difference
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
