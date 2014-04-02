pandoc_reader
=============

A pandoc markdown reader plugin for pelican


Requirements
------------

  - [pypandoc]
  - [pandoc] in $PATH


Installation
------------

Instructions for installation of pelican plugins can be obtained from the [pelican plugin manual](https://github.com/getpelican/pelican-plugins/blob/master/Readme.rst).


Configuration
-------------

Additional command line parameters can be passed to pandoc via the PANDOC_ARGS parameter.

    PANDOC_ARGS = [
      '--mathjax',
      '--smart',
      '--toc',
      '--toc-depth=2',
      '--number-sections',
    ]



[pandoc]: http://johnmacfarlane.net/pandoc/
[pypandoc]: https://github.com/bebraw/pypandoc

