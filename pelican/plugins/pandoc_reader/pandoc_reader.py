"""Reader that processes Pandoc Markdown and returns HTML5."""
import json
import math
import os
import shutil
import subprocess

import bs4
from ruamel.yaml import YAML, constructor

from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open

DEFAULT_READING_SPEED = 200  # Words per minute
DEFAULT_PANDOC_EXECUTABLE = "pandoc"
DIR_PATH = os.path.dirname(__file__)
ENCODED_LINKS_TO_RAW_LINKS_MAP = {
    "%7Bstatic%7D": "{static}",
    "%7Battach%7D": "{attach}",
    "%7Bfilename%7D": "{filename}",
}
FILE_EXTENSIONS = ["md", "mkd", "mkdn", "mdwn", "mdown", "markdown", "Rmd"]
FILTERS_PATH = os.path.abspath(os.path.join(DIR_PATH, "filters"))
PANDOC_READER_HTML_TEMPLATE = "pandoc-reader-default.html"
PANDOC_SUPPORTED_MAJOR_VERSION = 2
PANDOC_SUPPORTED_MINOR_VERSION = 11

TEMPLATES_PATH = os.path.abspath(os.path.join(DIR_PATH, "templates"))
UNSUPPORTED_ARGUMENTS = ("--standalone", "--self-contained")
VALID_BIB_EXTENSIONS = ["json", "yaml", "bibtex", "bib"]

# Markdown variants supported in defaults files
# Update as Pandoc adds or removes support for formats
VALID_INPUT_FORMATS = (
    "commonmark",
    "commonmark_x",
    "gfm",
    "markdown",
    "markdown_mmd",
    "markdown_phpextra",
    "markdown_strict",
)
VALID_OUTPUT_FORMATS = ("html", "html5")


class PandocReader(BaseReader):
    """Convert files written in Pandoc Markdown to HTML 5."""

    enabled = True
    file_extensions = FILE_EXTENSIONS

    def read(self, source_path):
        """Parse Pandoc Markdown and return HTML5 markup and metadata."""
        # Get the user-defined path to the Pandoc executable or fall back to default
        pandoc_executable = self.settings.get(
            "PANDOC_EXECUTABLE_PATH", DEFAULT_PANDOC_EXECUTABLE
        )

        # If user-defined path, expand and make it absolute in case the path is relative
        if pandoc_executable != DEFAULT_PANDOC_EXECUTABLE:
            pandoc_executable = os.path.abspath(os.path.expanduser(pandoc_executable))

        # Check if pandoc is installed and is executable
        if not shutil.which(pandoc_executable):
            raise Exception("Could not find Pandoc. Please install.")

        # Check if the version of pandoc installed is 2.11 or higher
        self._check_pandoc_version(pandoc_executable)

        # Open Markdown file and read content
        content = ""
        with pelican_open(source_path) as file_content:
            content = file_content

        # Retrieve HTML content and metadata
        output, metadata = self._create_html(source_path, content, pandoc_executable)

        return output, metadata

    def _create_html(self, source_path, content, pandoc_executable):
        """Create HTML5 content."""
        # Get settings set in pelicanconf.py
        defaults_files = self.settings.get("PANDOC_DEFAULTS_FILES", [])
        arguments = self.settings.get("PANDOC_ARGS", [])
        extensions = self.settings.get("PANDOC_EXTENSIONS", [])

        if isinstance(extensions, list):
            extensions = "".join(extensions)

        # Check if source content has a YAML metadata block
        self._check_yaml_metadata_block(content)

        # Check validity of arguments or defaults files
        table_of_contents, citations = self._validate_fields(
            defaults_files, arguments, extensions
        )

        # Construct preliminary pandoc command
        pandoc_cmd = self._construct_pandoc_command(
            pandoc_executable, defaults_files, arguments, extensions
        )

        # Find and add bibliography if citations are specified
        if citations:
            for bib_file in self._find_bibs(source_path):
                pandoc_cmd.append(f"--bibliography={bib_file}")

        # Create HTML content using pandoc-reader-default.html template
        output = self._run_pandoc(pandoc_cmd, content)

        # Extract table of contents, text and metadata from HTML output
        output, toc, pandoc_metadata = self._extract_contents(output, table_of_contents)

        # Replace all occurrences of %7Bstatic%7D to {static},
        # %7Battach%7D to {attach} and %7Bfilename%7D to {filename}
        # so that static links are resolvable by pelican
        for encoded_str, raw_str in ENCODED_LINKS_TO_RAW_LINKS_MAP.items():
            output = output.replace(encoded_str, raw_str)

        # Parse Pandoc metadata and add it to Pelican
        metadata = self._process_metadata(pandoc_metadata)

        if table_of_contents:
            # Create table of contents and add to metadata
            metadata["toc"] = self.process_metadata("toc", toc)

        if self.settings.get("CALCULATE_READING_TIME", []):
            # Calculate reading time and add to metadata
            metadata["reading_time"] = self.process_metadata(
                "reading_time",
                self._calculate_reading_time(pandoc_executable, source_path),
            )

        return output, metadata

    def _validate_fields(self, defaults_files, arguments, extensions):
        """Validate fields and return citations and ToC request values."""
        # If defaults_files is empty then validate the argument and extensions
        if not defaults_files:
            # Validate the arguments to see that they are supported
            # by the plugin
            self._check_arguments(arguments)

            # Check if citations have been requested
            citations = self._check_if_citations(arguments, extensions)

            # Check if table of contents has been requested
            table_of_contents = self._check_if_toc(arguments)
        else:
            # Validate defaults files and get the citations
            # abd table of contents request value
            citations, table_of_contents = self._check_defaults(defaults_files)
        return table_of_contents, citations

    def _check_defaults(self, defaults_files):
        """Check if the given Pandoc defaults file has valid values."""
        citations = False
        table_of_contents = False

        # Get the data in all defaults files as a string
        defaults_data = ""
        for defaults_file in defaults_files:
            with open(defaults_file) as file_handle:
                for line in file_handle.readlines():
                    defaults_data += line

        # Convert YAML data to a Python dictionary
        defaults = {}
        try:
            yaml = YAML()
            defaults = yaml.load(defaults_data)
        except constructor.DuplicateKeyError as duplicate_key_error:
            raise ValueError(
                "Duplicate keys defined in multiple defaults files."
            ) from duplicate_key_error

        self._check_if_unsupported_settings(defaults)
        reader = self._check_input_format(defaults)
        self._check_output_format(defaults)

        if not citations:
            citeproc_specified = False

            # Cases where citeproc is specified as citeproc: true
            if defaults.get("citeproc", ""):
                citeproc_specified = True

            # Cases where citeproc is specified in filters
            elif "citeproc" in defaults.get("filters", ""):
                citeproc_specified = True

            # The extension +citations is enabled by default in Pandoc 2.11
            # we are checking that the extension is not disabled using -citations
            if citeproc_specified and "-citations" not in reader:
                citations = True

        if not table_of_contents:
            if defaults.get("table-of-contents", ""):
                table_of_contents = True

        return citations, table_of_contents

    def _calculate_reading_time(self, pandoc_executable, source_path):
        """Calculate time taken to read content."""
        reading_speed = self.settings.get("READING_SPEED", DEFAULT_READING_SPEED)

        # Use the workcount.lua filter to calulcate the reading time
        output = subprocess.run(
            [
                pandoc_executable,
                "--lua-filter",
                os.path.join(FILTERS_PATH, "wordcount.lua"),
                source_path,
            ],
            capture_output=True,
            encoding="utf-8",
            check=True,
        )

        # We have to extract the word count from stdout which looks like
        # 102 words in body
        # 536 characters in body
        # 636 characters in body (including spaces)
        wordcount = output.stdout.split()[0]

        time_unit = "minutes"
        try:
            reading_time = math.ceil(float(wordcount) / float(reading_speed))
            if reading_time == 1:
                time_unit = "minute"
            reading_time = f"{str(reading_time)} {time_unit}"
        except ValueError as words_per_minute_nan:
            raise ValueError(
                "READING_SPEED setting must be a number."
            ) from words_per_minute_nan

        return reading_time

    def _process_metadata(self, pandoc_metadata):
        """Process Pandoc metadata and add it to Pelican."""
        # Cycle through the metadata and process them
        metadata = {}
        for key, value in pandoc_metadata.items():
            key = key.lower()
            if value and isinstance(value, str):
                value = value.strip().strip('"')

            # Process the metadata
            metadata[key] = self.process_metadata(key, value)
        return metadata

    @staticmethod
    def _check_pandoc_version(pandoc_executable):
        """Check that the specified version of Pandoc is 2.11 or higher."""
        output = subprocess.run(
            [pandoc_executable, "--version"],
            capture_output=True,
            encoding="utf-8",
            check=True,
        )

        # Returns a string of the form pandoc <version>
        pandoc_version = output.stdout.split("\n")[0]

        # Get the major and minor version from the above version string
        major_version = pandoc_version.split()[1].split(".")[0]
        minor_version = pandoc_version.split()[1].split(".")[1]

        # Pandoc major version less than 2 are not supported
        if int(major_version) < PANDOC_SUPPORTED_MAJOR_VERSION:
            raise Exception("Pandoc version must be 2.11 or higher.")

        # Pandoc major version 2 minor version less than 11 are not supported
        if (
            int(major_version) == PANDOC_SUPPORTED_MAJOR_VERSION
            and int(minor_version) < PANDOC_SUPPORTED_MINOR_VERSION
        ):
            raise Exception("Pandoc version must be 2.11 or higher.")

    @staticmethod
    def _check_yaml_metadata_block(content):
        """Check if the source content has a YAML metadata block."""
        # Check that the given content is not empty
        if not content:
            raise Exception("Could not find metadata. File is empty.")

        # Split content into a list of lines
        content_lines = content.splitlines()

        # Check that the first line of the file starts with a YAML block
        if content_lines[0].rstrip() not in ["---"]:
            raise Exception("Could not find metadata header '---'.")

        # Find the end of the YAML block
        yaml_block_end = ""
        for line_num, line in enumerate(content_lines[1:]):
            if line.rstrip() in ["---", "..."]:
                yaml_block_end = line_num
                break

        # Check if the end of the YAML block was found
        if not yaml_block_end:
            raise Exception("Could not find end of metadata block.")

    @staticmethod
    def _construct_pandoc_command(
        pandoc_executable, defaults_files, arguments, extensions
    ):
        """Construct Pandoc command for content."""
        pandoc_cmd = [
            pandoc_executable,
            "--standalone",
            "--template={}".format(
                os.path.join(TEMPLATES_PATH, PANDOC_READER_HTML_TEMPLATE)
            ),
        ]
        if not defaults_files:
            pandoc_cmd.extend(["--from", "markdown" + extensions, "--to", "html5"])
            pandoc_cmd.extend(arguments)
        else:
            for defaults_file in defaults_files:
                pandoc_cmd.append(f"--defaults={defaults_file}")
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
    def _extract_contents(html_output, table_of_contents):
        """Extract body html, table of contents and metadata from output."""
        # Extract pandoc metadata from html output
        pandoc_json_metadata, _, html_output = html_output.partition("\n")

        # Convert JSON string to dict
        pandoc_metadata = json.loads(pandoc_json_metadata)

        # Parse HTML output
        soup = bs4.BeautifulSoup(html_output, "html.parser")

        # Extract the table of contents if one was requested
        toc = ""
        if table_of_contents:
            # Find the table of contents
            toc = soup.body.find("nav", id="TOC")

            if toc:
                # Convert it to a string
                toc = str(toc)

                # Replace id=TOC with class="toc"
                toc = toc.replace('id="TOC"', 'class="toc"')

                # Remove the table of contents from the HTML output
                soup.body.find("nav", id="TOC").decompose()

        # Remove body tag around html output
        soup.body.unwrap()

        # Strip leading and trailing spaces
        html_output = str(soup).strip()

        return html_output, toc, pandoc_metadata

    @staticmethod
    def _check_if_citations(arguments, extensions):
        """Check if citations are specified."""
        citations = False
        if arguments and extensions:
            # The +citations extension is enabled by default in Pandoc 2.11
            # therefore we do a check to see that it is not disabled in extensions
            if (
                "--citeproc" in arguments or "-C" in arguments
            ) and "-citations" not in extensions:
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
                raise ValueError(f"Argument {arg} is not supported.")

    @staticmethod
    def _check_if_unsupported_settings(defaults):
        """Check if unsupported settings are specified in the defaults."""
        for arg in UNSUPPORTED_ARGUMENTS:
            arg = arg[2:]
            if defaults.get(arg, ""):
                raise ValueError(f"The default {arg} should be set to false.")

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
                "Specifying both from and reader is not supported."
                " Please specify just one."
            )

        if reader_input or from_input:
            if reader_input:
                reader = reader_input
            elif from_input:
                reader = from_input

            reader_prefix = reader.replace("+", "-").split("-")[0]

            # Check to see if the reader_prefix matches a valid input format
            if reader_prefix not in VALID_INPUT_FORMATS:
                raise ValueError("Input type has to be a Markdown variant.")
        return reader

    @staticmethod
    def _check_output_format(defaults):
        """Check if the output format is HTML or HTML5."""
        writer_output = defaults.get("writer", "")
        to_output = defaults.get("to", "")

        # Case where both writer and to are specified which is not supported
        if writer_output and to_output:
            raise ValueError(
                "Specifying both to and writer is not supported."
                " Please specify just one."
            )

        # Case where neither writer nor to value is set to html
        if (
            writer_output not in VALID_OUTPUT_FORMATS
            and to_output not in VALID_OUTPUT_FORMATS
        ):
            output_formats = " or ".join(VALID_OUTPUT_FORMATS)
            raise ValueError(f"Output format type must be either {output_formats}.")


def add_reader(readers):
    """Add the PandocReader as the reader for all Pandoc Markdown files."""
    for ext in PandocReader.file_extensions:
        readers.reader_classes[ext] = PandocReader


def register():
    """Register the PandocReader."""
    signals.readers_init.connect(add_reader)
