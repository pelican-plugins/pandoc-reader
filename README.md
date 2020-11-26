Pandoc Reader: A Plugin for Pelican
===================================

[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/pandoc-reader/build)](https://github.com/pelican-plugins/pandoc-reader/actions) [![PyPI Version](https://img.shields.io/pypi/v/pelican-pandoc-reader)](https://pypi.org/project/pelican-pandoc-reader/) ![License](https://img.shields.io/pypi/l/pelican-pandoc-reader?color=blue)

Pandoc Reader is a Pelican plugin for processing [Markdown][] content with [Pandoc][].

Requirements
------------

  - `pandoc` executable in $PATH

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-pandoc-reader

Configuration
-------------

Additional command-line parameters can be passed to `pandoc` via the `PANDOC_ARGS` parameter:

    PANDOC_ARGS = [
      "--mathjax",
      "--smart",
      "--toc",
      "--toc-depth=2",
      "--number-sections",
    ]

Pandoc's Markdown extensions can be enabled or disabled via the `PANDOC_EXTENSIONS` parameter:

    PANDOC_EXTENSIONS = [
      "+hard_line_breaks",
      "-citations"
    ]

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/pandoc-reader/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the AGPL-3.0 license.


[Markdown]: https://daringfireball.net/projects/markdown/
[Pandoc]: https://pandoc.org/
