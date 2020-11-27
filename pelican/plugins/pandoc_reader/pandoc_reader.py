"""Reader that processes Pandoc Markdown and returns HTML 5."""
import math
import os
import shutil
import subprocess

from mwc.counter import count_words_in_markdown
from yaml import safe_load

from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open

DIR_PATH = os.path.dirname(__file__)
TEMPLATES_PATH = os.path.abspath(os.path.join(DIR_PATH, "templates"))
TOC_TEMPLATE = "toc-template.html"
DEFAULT_READING_SPEED = 200  # Words per minute

ENCODED_LINKS_TO_RAW_LINKS_MAP = {
    "%7Bstatic%7D": "{static}",
    "%7Battach%7D": "{attach}",
    "%7Bfilename%7D": "{filename}",
}

VALID_INPUT_FORMATS = ("markdown", "commonmark", "gfm")
VALID_OUTPUT_FORMATS = ("html", "html5")
UNSUPPORTED_ARGUMENTS = ("--standalone", "--self-contained")
VALID_BIB_EXTENSIONS = ["json", "yaml", "bibtex", "bib"]
FILE_EXTENSIONS = ["md", "markdown", "mkd", "mdown"]


class PandocReader(BaseReader):
    """Convert files written in Pandoc Markdown to HTML 5."""

    enabled = True
    file_extensions = FILE_EXTENSIONS

    def read(self, source_path):
        """Parse Pandoc Markdown and return HTML5 markup and metadata."""
        # Check if pandoc is installed and is executable
        if not shutil.which("pandoc"):
            raise Exception("Could not find Pandoc. Please install.")

        # Open markdown file and read content
        content = ""
        with pelican_open(source_path) as file_content:
            content = file_content

        # Retrieve HTML content and metadata
        output, metadata = self._create_html(source_path, content)

        return output, metadata

    def _create_html(self, source_path, content):
        """Create HTML5 content."""
        # Get settings set in pelicanconf.py
        default_files = self.settings.get("PANDOC_DEFAULT_FILES", [])
        arguments = self.settings.get("PANDOC_ARGS", [])
        extensions = self.settings.get("PANDOC_EXTENSIONS", [])

        if isinstance(extensions, list):
            extensions = "".join(extensions)

        # Check validity of arguments or default files
        table_of_contents, citations = self._validate_fields(
            default_files, arguments, extensions
        )

        # Construct preliminary pandoc command
        pandoc_cmd = self._construct_pandoc_command(
            default_files, arguments, extensions
        )

        # Find and add bibliography if citations are specified
        if citations:
            for bib_file in self._find_bibs(source_path):
                pandoc_cmd.append("--bibliography={0}".format(bib_file))

        # Create HTML content
        output = self._run_pandoc(pandoc_cmd, content)

        # Replace all occurrences of %7Bstatic%7D to {static},
        # %7Battach%7D to {attach} and %7Bfilename%7D to {filename}
        # so that static links are resolvable by pelican
        for encoded_str, raw_str in ENCODED_LINKS_TO_RAW_LINKS_MAP.items():
            output = output.replace(encoded_str, raw_str)

        metadata = {}
        if table_of_contents:
            # Create table of contents and add to metadata
            metadata["toc"] = self.process_metadata(
                "toc", self._create_toc(pandoc_cmd, content)
            )

        if self.settings.get("CALCULATE_READING_TIME", []):
            # Calculate reading time and add to metadata
            metadata["reading_time"] = self.process_metadata(
                "reading_time", self._calculate_reading_time(content)
            )

        # Parse YAML metadata placed in the document's header
        metadata = self._process_header_metadata(
            list(content.splitlines()), metadata, pandoc_cmd
        )

        return output, metadata

    def _validate_fields(self, default_files, arguments, extensions):
        """Validate fields and return citations and ToC request values."""
        # If default_files is empty then validate the argument and extensions
        if not default_files:
            # Validate the arguments to see that they are supported
            # by the plugin
            self._check_arguments(arguments)

            # Check if citations have been requested
            citations = self._check_if_citations(arguments, extensions)

            # Check if table of contents has been requested
            table_of_contents = self._check_if_toc(arguments)
        else:
            # Validate default files and get the citations
            # abd table of contents request value
            citations, table_of_contents = self._check_defaults(default_files)
        return table_of_contents, citations

    def _check_defaults(self, default_files):
        """Check if the given Pandoc defaults file has valid values."""
        citations = False
        table_of_contents = False
        for default_file in default_files:
            defaults = {}

            # Convert YAML data to a Python dictionary
            with open(default_file) as file_handle:
                defaults = safe_load(file_handle)

            self._check_if_unsupported_settings(defaults)
            reader = self._check_input_format(defaults)
            self._check_output_format(defaults)

            if not citations:
                if defaults.get("citeproc", "") and "+citations" in reader:
                    citations = True

            if not table_of_contents:
                if defaults.get("table-of-contents", ""):
                    table_of_contents = True

        return citations, table_of_contents

    def _create_toc(self, pandoc_cmd, content):
        """Generate table of contents."""
        toc_args = [
            "--standalone",
            "--template",
            os.path.join(TEMPLATES_PATH, TOC_TEMPLATE),
        ]

        pandoc_cmd = pandoc_cmd + toc_args
        table_of_contents = self._run_pandoc(pandoc_cmd, content)
        return table_of_contents

    def _calculate_reading_time(self, content):
        """Calculate time taken to read content."""
        reading_speed = self.settings.get("READING_SPEED", DEFAULT_READING_SPEED)
        wordcount = count_words_in_markdown(content)

        time_unit = "minutes"
        try:
            reading_time = math.ceil(float(wordcount) / float(reading_speed))
            if reading_time == 1:
                time_unit = "minute"
            reading_time = "{} {}".format(str(reading_time), time_unit)
        except ValueError as words_per_minute_nan:
            raise ValueError(
                "READING_SPEED setting must be a number."
            ) from words_per_minute_nan

        return reading_time

    def _process_header_metadata(self, content, metadata, pandoc_cmd):
        """Process YAML metadata and export."""
        # Check that the given text is not empty
        if not content:
            raise Exception("Could not find metadata. File is empty.")

        # Check that the first line of the file starts with a YAML header
        if content[0].strip() not in ["---", "..."]:
            raise Exception("Could not find metadata header '...' or '---'.")

        # Find the end of the YAML block
        lines = content[1:]
        yaml_end = ""
        for line_num, line in enumerate(lines):
            if line.strip() in ["---", "..."]:
                yaml_end = line_num
                break

        # Check if the end of the YAML block was found
        if not yaml_end:
            raise Exception("Could not find end of metadata block.")

        # Process the YAML block
        for line in lines[:yaml_end]:
            metalist = line.split(":", 1)
            if len(metalist) == 2:
                key, value = (
                    metalist[0].lower(),
                    metalist[1].strip().strip('"'),
                )
                # Takes care of metadata that should be converted to HTML
                if key in self.settings["FORMATTED_FIELDS"]:
                    value = self._run_pandoc(pandoc_cmd, value)
                metadata[key] = self.process_metadata(key, value)
        return metadata

    @staticmethod
    def _construct_pandoc_command(default_files, arguments, extensions):
        """Construct Pandoc command for content."""
        pandoc_cmd = []
        if not default_files:
            pandoc_cmd = [
                "pandoc",
                "--from",
                "markdown" + extensions,
                "--to",
                "html5",
            ]
            pandoc_cmd.extend(arguments)
        else:
            pandoc_cmd = ["pandoc"]
            for default_file in default_files:
                pandoc_cmd.append("--defaults={0}".format(default_file))
        return pandoc_cmd

    @staticmethod
    def _run_pandoc(pandoc_cmd, content):
        """Execute the given pandoc command and return output."""
        output = subprocess.run(
            pandoc_cmd,
            input=content,
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
        return output.stdout

    @staticmethod
    def _check_if_citations(arguments, extensions):
        """Check if citations are specified."""
        citations = False
        if arguments and extensions:
            if (
                "--citeproc" in arguments or "-C" in arguments
            ) and "+citations" in extensions:
                citations = True
        return citations

    @staticmethod
    def _check_if_toc(arguments):
        """Check if a table of contents should be generated."""
        table_of_contents = False
        if arguments:
            if "--toc" in arguments or "--table-of-contents" in arguments:
                table_of_contents = True
        return table_of_contents

    @staticmethod
    def _find_bibs(source_path):
        """Find bibliographies recursively in the sourcepath given."""
        bib_files = []
        filename = os.path.splitext(os.path.basename(source_path))[0]
        directory_path = os.path.dirname(os.path.abspath(source_path))
        for root, _, files in os.walk(directory_path):
            for extension in VALID_BIB_EXTENSIONS:
                bib_name = ".".join([filename, extension])
                if bib_name in files:
                    bib_files.append(os.path.join(root, bib_name))
        return bib_files

    @staticmethod
    def _check_arguments(arguments):
        """Check to see that only supported arguments have been passed."""
        for arg in arguments:
            if arg in UNSUPPORTED_ARGUMENTS:
                raise ValueError("Argument {0} is not supported.".format(arg))

    @staticmethod
    def _check_if_unsupported_settings(defaults):
        """Check if unsupported settings are specified in the defaults."""
        for arg in UNSUPPORTED_ARGUMENTS:
            arg = arg[2:]
            if defaults.get(arg, ""):
                raise ValueError("The default {} should be set to false.".format(arg))

    @staticmethod
    def _check_input_format(defaults):
        """Check if the input format given is a Markdown variant."""
        reader = ""
        reader_input = defaults.get("reader", "")
        from_input = defaults.get("from", "")

        # Case where no input format is specified
        if not reader_input and not from_input:
            raise ValueError("No input format specified.")

        # Case where both reader and from are specified which is not supported
        if reader_input and from_input:
            raise ValueError(
                (
                    "Specifying both from and reader is not supported."
                    " Please specify just one."
                )
            )

        if reader_input or from_input:
            if reader_input:
                reader = reader_input
            elif from_input:
                reader = from_input

            reader_prefix = reader.replace("+", "-").split("-")[0]

            # Check to see if the reader_prefix matches a valid input
            if not reader_prefix.startswith(VALID_INPUT_FORMATS):
                raise ValueError("Input type has to be a markdown variant.")
        return reader

    @staticmethod
    def _check_output_format(defaults):
        """Check if the output format is HTML or HTML5."""
        writer_output = defaults.get("writer", "")
        to_output = defaults.get("to", "")

        # Case where both writer and to are specified which is not supported
        if writer_output and to_output:
            raise ValueError(
                (
                    "Specifying both to and writer is not supported."
                    " Please specify just one."
                )
            )

        # Case where neither writer nor to value is set to html
        if (
            writer_output not in VALID_OUTPUT_FORMATS
            and to_output not in VALID_OUTPUT_FORMATS
        ):
            output_formats = " or ".join(VALID_OUTPUT_FORMATS)
            raise ValueError(
                "Output format type must be either {}.".format(output_formats)
            )


def add_reader(readers):
    """Add the PandocReader as the reader for all Pandoc Markdown files."""
    for ext in PandocReader.file_extensions:
        readers.reader_classes[ext] = PandocReader


def register():
    """Register the PandocReader."""
    signals.readers_init.connect(add_reader)
