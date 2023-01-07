Pelican Academic Bibliographies Plugin
======================================

This plugin is a version of the [Pelican Pandoc Reader Plugin](https://github.com/pelican-plugins/pandoc-reader), modified with a view to extending the flexibility of citation functionality. In all other respects the plugin is unaltered from the original. 

The original plugin provides citation functionality in the following manner: when citations are turned on in the plugin's configuration, the plugin searches the path of each file to be processed looking for a bibliography file with the same name but a different extension. For example, to provide references for `blog_post.md`, one would need to provide a bibliography file names `blog_post.bib`. A csl file can be provided in the pandoc defaults file. 

This is satisfactory for occasional use, but for heavy users of citations and bibliographies, this is quite limited. For instance, one may need to refer to certain works frequently, but the references will need to be added in a new file for each new post in which they are cited.

On the other hand, while a single csl file may be sufficient for most blogging purposes, in some situations specific settings will be necessary and the original plugin had no way of providing them. A common use case is an academic blog that provides a listing of the author's publications in a format that differs from standard reference lists (this was the use case that prompted this extension).

Usage
-----

The plugin's usage has not changed from the original—-[original documentation](https://github.com/pelican-plugins/pandoc-reader)--**except for the following additional functionality**:

- Site wide settings for bibliographies and a csl file can be provided in the `pelicanconf.py` file with the following keys:
    - `DEFAULT_BIBLIOGRAPHIES` = […, 'absolute/or/relative/path/to/mybib.bib', …]
    - `DEFAULT_CSL` = 'path or url'
- A page/post-specific bibliography can be set in the metadata block of the page/post using one of the following keys: `biliography`, or `exclusive_bibliography`. If the latter is used then no other bibliography files will be loaded. The value is an absolute or relative path to a bibliography file. 
- A page/post csl file can be set in the metadata block of the page/post using the key: `csl`. This will always replace the `DEFAULT_CSL` setting should it have been set in `pelicanconf.py`.
- Metadata in the page/post will need to be well formed, e.g.:

```yaml
---
title: My post
anotherfield: Some value
bibliography: content/bib/mybib.bib
csl: https://zotero.com/somecslfile.csl
...
```

Changes to the original plugin
==============================

Changes by Jonathan Mair as of 7 Jan 2023 described for the benefit of anyone who wants to find the changes in the code:

- amended `_check_yaml_metadata_block()` so that in addition to validating the yaml block in the content it also returns the metadata contained as a dictionary. Renamed to: _check_and_get_yaml_metadata_block()
- added two new variables `defualt_bibliograhies` and `default_csl` that are fetched from the following keys in `pelicanconf.py`, if present: 
    - `DEFAULT_BIBLIOGRAPHIES` = […, 'absolute/or/relative/path/to/mybib.bib', …]
    - `DEFAULT_CSL` = 'path or url'
- altered construction of the pandoc command so that bibliographies are added in the following way:
    1. by specifying a bibliography file in the metadata block of a given file:
        - if, in the metadata block of any given file, `exclusive_bibliography`is set with a path to a bibliography file as the value, *only* the bibliography to which it points will be added to the pandoc command for that file
        - if, in the metadata block of any given file, `bibliography`is set with a path to a bibliography file as the value, that bibliography will be added to the pandoc command for that file along with any others that are added by other means
    2. by specifying a list of bibliographies as the site-wide defaults in `pelicanconf.py` with the key: `DEFAULT_BIBLIOGRAPHIES`
    3. by the plugin's original method, which is placing a bibliography file in the same path as the file to be processed with the same name but an appropriate bibliography extension (see original documentation below) 

