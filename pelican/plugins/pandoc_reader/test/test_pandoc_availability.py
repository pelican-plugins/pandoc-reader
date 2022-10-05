"""Test if a supported version of the pandoc executable is available."""
import os
import shutil
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


class TestPandocAvailability(unittest.TestCase):
    """Test if a support version of the pandoc executable is available."""

    def test_pandoc_availability_one(self):
        """Check if pandoc executable is available."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "empty.md")

        if not shutil.which("pandoc"):
            # Case where pandoc is not available
            with self.assertRaises(Exception) as context_manager:
                pandoc_reader.read(source_path)

            message = str(context_manager.exception)
            self.assertEqual("Could not find Pandoc. Please install.", message)
        else:
            self.assertTrue(True)

    def test_pandoc_availability_two(self):
        """Check if pandoc executable is available at the given path."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
            PANDOC_EXECUTABLE_PATH="2.11/bin/pandoc",
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "empty.md")

        with self.assertRaises(Exception) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Could not find Pandoc. Please install.", message)

    def test_pandoc_unsupported_major_version(self):
        """Check if the installed pandoc has a supported major version."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
            PANDOC_EXECUTABLE_PATH="1.19/bin/pandoc",
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "empty.md")

        with self.assertRaises(Exception) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Pandoc version must be 2.11 or higher.", message)

    def test_pandoc_unsupported_minor_version(self):
        """Check if the installed pandoc has a supported minor version."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS,
            PANDOC_EXECUTABLE_PATH="2.10/bin/pandoc",
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "empty.md")

        with self.assertRaises(Exception) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Pandoc version must be 2.11 or higher.", message)


if __name__ == "__main__":
    unittest.main()
