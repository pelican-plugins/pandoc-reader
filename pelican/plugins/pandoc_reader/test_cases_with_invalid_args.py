"""Tests using invalid arguments and extensions for pandoc-reader plugin."""
import os
import unittest

from pelican.tests.support import get_settings

from pandoc_reader import PandocReader

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_content"))

# Test settings that will be set in pelicanconf.py by plugin users
PANDOC_ARGS = ["--mathjax"]
PANDOC_EXTENSIONS = ["+smart"]


class TestInvalidCasesWithArguments(unittest.TestCase):
    """Invalid test cases using Pandoc arguments and extensions."""

    def test_invalid_standalone_argument(self):
        """Check that specifying --standalone raises an exception."""
        pandoc_arguments = ["--standalone"]
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=pandoc_arguments
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Argument --standalone is not supported.", message)

    def test_invalid_self_contained_argument(self):
        """Check that specifying --self-contained raises an exception."""
        pandoc_arguments = ["--self-contained"]
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=pandoc_arguments
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")

        with self.assertRaises(ValueError) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Argument --self-contained is not supported.", message)


if __name__ == "__main__":
    unittest.main()
