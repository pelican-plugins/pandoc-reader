CHANGELOG
=========

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
