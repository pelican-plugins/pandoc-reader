CHANGELOG
=========

2.1.0 - 2023-11-23
------------------

* Using [wordcount Lua Filter](https://github.com/pandoc/lua-filters/tree/master/wordcount) instead of the [markdown-word-count](https://github.com/gandreadis/markdown-word-count) Python package to calculate word count

Contributed by [nandac](https://github.com/nandac) via [PR #35](https://github.com/pelican-plugins/pandoc-reader/pull/35/)


2.0.0 - 2023-08-12
------------------

* Dropping support for Python 3.7
* Removed `PANDOC_DEFAULT_FILES` in favour of `PANDOC_DEFAULTS_FILES`
* Upgrade PyYAML and ruamel.yaml to the latest version available

1.2.0 - 2022-10-29
------------------

* Deprecating `PANDOC_DEFAULT_FILES` setting in favour of `PANDOC_DEFAULTS_FILES`
* Handle defaults files in a manner consistent with Pandoc's handling of these files

Contributed by [nandac](https://github.com/nandac) via [PR #25](https://github.com/pelican-plugins/pandoc-reader/pull/25/)


1.1.0 - 2021-02-16
------------------

Add PANDOC_EXECUTABLE_PATH setting to customize `pandoc` executable location

[nandac](https://github.com/nandac) [PR #19](https://github.com/pelican-plugins/pandoc-reader/pull/19/)

1.0.1 - 2021-02-05
------------------

* Raise exception for metadata with leading or trailing whitespace
* Remove citations extension check since Pandoc now enables it by default

1.0.0 - 2020-12-04
------------------

* Convert to namespace plugin
* Add support for citations, table of contents generation, and reading time calculation
* Add support for Pandoc default files
* Add support for specifying `citeproc` as a filter
