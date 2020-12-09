"""Tests using invalid metadata for pandoc-reader plugin."""
import os
import unittest

from pelican.tests.support import get_settings

from pandoc_reader import PandocReader

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_content"))

# Test settings that will be set in pelicanconf.py by plugin users
PANDOC_ARGS = ["--mathjax"]
PANDOC_EXTENSIONS = ["+smart"]


class TestInvalidMetadata(unittest.TestCase):
    """Invalid Metadata test cases."""

    def test_empty_file(self):
        """Check if a file is empty."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "empty.md")

        # If the file is empty retrieval of metadata should fail
        with self.assertRaises(Exception) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Could not find metadata. File is empty.", message)

    def test_non_empty_file_no_metadata(self):
        """Check if a file has no metadata."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "no_metadata.md")

        # If the file is not empty but has no metadata it should fail
        with self.assertRaises(Exception) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Could not find metadata header '---'.", message)

    def test_metadata_start_with_leading_spaces(self):
        """Check if metadata block starting with leading spaces throws an exception."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(
            TEST_CONTENT_PATH, "metadata_start_with_leading_spaces.md"
        )

        # Metadata staring --- should not have leading spaces
        with self.assertRaises(Exception) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Could not find metadata header '---'.", message)

    def test_metadata_block_end_with_leading_spaces(self):
        """Check if metadata block ending with leading spaces throws an exception."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(
            TEST_CONTENT_PATH, "metadata_end_with_leading_spaces.md"
        )

        # Metadata end --- or ... should not have leading spaces
        with self.assertRaises(Exception) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Could not find end of metadata block.", message)

    def test_no_metadata_block_end(self):
        """Check if the metadata block ends."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "no_metadata_end.md")

        # Metadata blocks should end with '___' or '...' if not it should fail
        with self.assertRaises(Exception) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Could not find end of metadata block.", message)

    def test_invalid_metadata_block_end(self):
        """Check if the metadata block end is wrong."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS, PANDOC_ARGS=PANDOC_ARGS
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "no_metadata_end.md")

        # Metadata blocks should end with '___' or '...' if not it should fail
        with self.assertRaises(Exception) as context_manager:
            pandoc_reader.read(source_path)

        message = str(context_manager.exception)
        self.assertEqual("Could not find end of metadata block.", message)
