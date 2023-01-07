"""Test reading time and summary output from the pandoc-reader plugin."""
import os
import unittest

from pelican.plugins.pandoc_reader import PandocReader
from pelican.tests.support import get_settings

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "markdown"))

# These settings will be set in pelicanconf.py by plugin users.
# Appending --wrap=None so that rendered HTML5 does not have new lines (\n)
# which causes tests to fail.
# See https://pandoc.org/MANUAL.html#general-writer-options
PANDOC_ARGS = ["--mathjax", "--wrap=none"]
PANDOC_EXTENSIONS = ["+smart"]
CALCULATE_READING_TIME = True
FORMATTED_FIELDS = ["summary"]


class TestReadingTimeAndSummary(unittest.TestCase):
    """Test reading time and summary formatted fields."""

    def test_default_wpm_reading_time(self):
        """Check if 200 words per minute gives us a reading time of 1 minute."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
            CALCULATE_READING_TIME=CALCULATE_READING_TIME,
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "reading_time_content.md")
        _, metadata = pandoc_reader.read(source_path)

        self.assertEqual("1 minute", str(metadata["reading_time"]))

    def test_user_defined_wpm_reading_time(self):
        """Check if a user defined 100 words per minute gives us 2 minutes."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
            CALCULATE_READING_TIME=CALCULATE_READING_TIME,
            READING_SPEED=100,
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "reading_time_content.md")
        _, metadata = pandoc_reader.read(source_path)

        self.assertEqual("2 minutes", str(metadata["reading_time"]))

    def test_invalid_user_defined_wpm(self):
        """Check if an exception is raised if words per minute is not a number."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
            CALCULATE_READING_TIME=CALCULATE_READING_TIME,
            READING_SPEED="my words per minute",
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "reading_time_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("READING_SPEED setting must be a number.", message)

    def test_summary(self):
        """Check if summary output is valid."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
            FORMATTED_FIELDS=FORMATTED_FIELDS,
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        _, metadata = pandoc_reader.read(source_path)

        self.assertEqual(
            (
                "But this foundational principle of science has now been"
                " called into question by"
                ' <a href="https://www.britannica.com/science/string-theory">'
                "String Theory</a>."
            ),
            str(metadata["summary"]),
        )


if __name__ == "__main__":
    unittest.main()
