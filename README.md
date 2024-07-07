Pandoc Reader: A Plugin for Pelican
===================================

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/pandoc-reader/main.yml?branch=main)](https://github.com/pelican-plugins/pandoc-reader/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-pandoc-reader)](https://pypi.org/project/pelican-pandoc-reader/)
![License](https://img.shields.io/pypi/l/pelican-pandoc-reader?color=blue)

Pandoc Reader is a [Pelican][] plugin that converts documents written in [Pandoc’s variant of Markdown][] into HTML.

Requirements
------------

This plugin requires:

* Python 3.8 or higher; and
* Pandoc 2.11 or higher [[Pandoc installation instructions](https://pandoc.org/installing.html)].

By default, the plugin looks for a `pandoc` executable on your `PATH`. If you wish, [you may specify an alternative location for your `pandoc` executable](#customizing-the-path-for-the-pandoc-executable).

Installation
------------

This plugin can be installed via:

```bash
python -m pip install pelican-pandoc-reader
```

Configuration
-------------

This plugin converts [Pandoc’s variant of Markdown][] into HTML. Conversion from other Markdown variants is supported but requires the use of a [Pandoc defaults file](https://pandoc.org/MANUAL.html#defaults-files).

Converting to output formats other than HTML is not supported.

### Specifying File Metadata

The plugin expects all Markdown files to start with a YAML-formatted content header, as shown below.

```yaml
---
title: "<post-title>"
author: "<author-name>"
data: "<date>"
---
```

… or …

```yaml
---
title: "<post-title>"
author: "<author-name>"
date: "<date>"
...
```

> ⚠️ **Note:** The YAML-formatted header shown above is syntax specific to Pandoc for specifying content metadata. This is different from Pelican’s front-matter format. If you ever decide to stop using this plugin and switch to Pelican’s default Markdown handling, you may need to switch your front-matter metadata to [Python-Markdown’s Meta-Data format](https://python-markdown.github.io/extensions/meta_data/).

If you have files that use Pelican's front matter format, there is a script written by [Joseph Reagle](https://github.com/reagle) available that [converts Pelican's front matter to Pandoc's YAML header format](https://gist.github.com/reagle/5bc44ba9e2f1b961d1aaca9179fb403b).

For more information on Pandoc's YAML metadata block or Pelican's default metadata format please visit the links below:

* [Pandoc’s YAML metadata blocks](https://pandoc.org/MANUAL.html#metadata-blocks)
* [Pelican’s default metadata format](https://docs.getpelican.com/en/stable/content.html#file-metadata)

### Specifying Pandoc Options

The plugin supports two **mutually exclusive** methods for passing options to Pandoc.

#### Method One: Via Pelican Settings

The first method involves configuring two settings in your Pelican settings file (e.g., `pelicanconf.py`):

* `PANDOC_ARGS`
* `PANDOC_EXTENSIONS`

In the `PANDOC_ARGS` setting, you may specify any arguments supported by Pandoc, as shown below:

```python
PANDOC_ARGS = [
    "--mathjax",
    "--citeproc",
]
```

In the `PANDOC_EXTENSIONS` setting, you may enable/disable any number of the supported [Pandoc extensions](https://pandoc.org/MANUAL.html#extensions):

```python
PANDOC_EXTENSIONS = [
    "+footnotes",   # Enabled extension
    "-pipe_tables", # Disabled extension
]
```

#### Method Two: Using Pandoc Defaults Files

The second method involves specifying the path(s) to one or more [Pandoc defaults files][], with all your preferences written in YAML format.

These paths should be set in your Pelican settings file by using the setting `PANDOC_DEFAULTS_FILES`. The paths may be absolute or relative, but relative paths are recommended as they are more portable.

```python
PANDOC_DEFAULTS_FILES = [
    "<path/to/defaults/file_one.yaml>",
    "<path/to/defaults/file_two.yaml>",
]
```

Here is a minimal example of content that should be available in a Pandoc defaults file:

```yaml
reader: markdown
writer: html5
```

Using defaults files has the added benefit of allowing you to use other Markdown variants supported by Pandoc, such as [CommonMark](https://commonmark.org/) and [GitHub-Flavored Markdown](https://docs.github.com/en/free-pro-team@latest/github/writing-on-github).

Please see [Pandoc defaults files][] for a more complete example.

> ⚠️ **Note:** Neither method supports the `--standalone` or `--self-contained` arguments, which will yield an error if invoked.

### Generating a Table of Contents

If you want to create a table of contents (ToC) for posts or pages, you may do so by specifying the `--toc` or `--table-of-contents` argument in the `PANDOC_ARGS` setting, as shown below:

```python
PANDOC_ARGS = [
    "--toc",
]
```

… or …

```python
PANDOC_ARGS = [
    "--table-of-contents",
]
```

To add a ToC via a Pandoc defaults file, use the syntax below:

```yaml
table-of-contents: true
```

The table of contents will be available for use in templates using the `{{ article.toc }}` or `{{ page.toc }}` Jinja template variables.

### Enabling Citations

You may enable citations by specifying the `-C` or `--citeproc` option.

Set the `PANDOC_ARGS` and `PANDOC_EXTENSIONS` in your Pelican settings file as shown below:

```python
PANDOC_ARGS = [
    "--citeproc",
]
```

… or …

```python
PANDOC_ARGS = [
    "-C",
]
```

If you are using a Pandoc defaults file, you need the following as a bare minimum to enable citations:

```yaml
reader: markdown
writer: html5

citeproc: true
```

Without these settings, citations will not be processed by the plugin.

It is not necessary to specify the `+citations` extension since it is enabled by default. However, if you were to disable citations by specifying `-citations` in `PANDOC_EXTENSIONS` or by setting `reader: markdown-citations` in your defaults file, citations will **not** work.

You may write your bibliography in any format supported by Pandoc with the appropriate extensions specified. However, you **must** name the bibliography file the same as your post.

For example, a post with the file name `my-post.md` should have a bibliography file called `my-post.bib`, `my-post.json`, `my-post.yaml` or `my-post.bibtex` in the same directory as your post, or in a subdirectory of the directory that your blog resides in. Failure to do so will prevent the references from being picked up.

#### Known Issues with Citations

If enabling citations with a specific style, you need to specify a CSL (Citation Style Language) file, available from the [Zotero Style Repository](https://www.zotero.org/styles). For example, if you are using `ieee-with-url` style file, it may be specified in your Pelican settings file, as shown below:

```python
PANDOC_ARGS = [
   "--csl=https://www.zotero.org/styles/ieee-with-url",
]
```

Or in a Pandoc defaults file:

```yaml
csl: "https://www.zotero.org/styles/ieee-with-url"
```

Specifying a *remote* (that is, not local) CSL file as shown above dramatically increases the time taken to process Markdown content. To improve processing speed, it is _highly_ recommended that you use a local copy of the CSL file downloaded from Zotero.

You may then reference it in your Pelican settings file as shown below:

```python
PANDOC_ARGS = [
   "--csl=path/to/file/ieee-with-url.csl",
]
```

Or in a Pandoc defaults file:

```yaml
csl: "path/to/file/ieee-with-url.csl"
```

### Calculating and Displaying Reading Times

This plugin may be used to calculate the estimated reading time of articles and pages by setting `CALCULATE_READING_TIME` to `True` in your Pelican settings file:

```python
CALCULATE_READING_TIME = True
```

You may display the estimated reading time using the `{{ article.reading_time }}` or `{{ page.reading_time }}` template variables. The unit of time will be displayed as “minute” for reading times less than or equal to one minute, or “minutes” for those greater than one minute.

The reading time is calculated by dividing the number of words by the reading speed, which is the average number of words read in a minute.

The default value for reading speed is set to 200 words per minute, but may be customized by setting `READING_SPEED` to the desired words per minute value in your Pelican settings file:

```python
READING_SPEED = <words-per-minute>
```

The number of words in a document is calculated using the [wordcount Lua Filter](https://github.com/pandoc/lua-filters/tree/master/wordcount).

### Customizing the Path for the `pandoc` Executable

If your `pandoc` executable does not reside on your `PATH`, set the `PANDOC_EXECUTABLE_PATH` in your Pelican settings file to the absolute path of where your `pandoc` resides as shown below:

```python
PANDOC_EXECUTABLE_PATH = /path/to/my/pandoc
```

This setting is useful in cases where the `pandoc` executable from your hosting provider is not recent enough, and you may need to install a version of Pandoc-compatible with this plugin—in a non-standard location.

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

Special thanks to [Justin Mayer](https://justinmayer.com), [Erwin Janssen](https://github.com/ErwinJanssen), [Joseph Reagle](https://github.com/reagle) and [Deniz Turgut](https://github.com/avaris) for their improvements and feedback on this plugin.

[existing issues]: https://github.com/pelican-plugins/pandoc-reader/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the AGPL-3.0 license.

[Pelican]: https://getpelican.com
[Pandoc’s variant of Markdown]: https://pandoc.org/MANUAL.html#pandocs-markdown
[Pandoc defaults files]: https://pandoc.org/MANUAL.html#default-files
