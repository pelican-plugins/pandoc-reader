"""Test if pandoc executable is available."""
import os
import shutil
import unittest

from pelican.tests.support import get_settings

from pandoc_reader import PandocReader

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_content"))

# Test settings that will be set in pelicanconf.py by plugin users
PANDOC_ARGS = ["--mathjax"]
PANDOC_EXTENSIONS = ["+smart", "+implicit_figures"]


class TestPandocAvailability(unittest.TestCase):
    """Test Pandoc availability."""

    def test_pandoc_availability(self):
        """Check if Pandoc executable is available."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
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
            # Case where pandoc is available
            message = "Pandoc is installed."
            self.assertEqual("Pandoc is installed.", message)


if __name__ == "__main__":
    unittest.main()
