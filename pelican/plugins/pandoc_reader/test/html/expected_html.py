"""Expected HTML output for various types of text."""

HTML_WITH_CITATIONS = "\n".join(
    [
        '<h2 id="string-theory">String Theory</h2>',
        (
            "<p>But this foundational principle of science has now "
            "been called into question by "
            '<a href="https://www.britannica.com/science/string-theory">'
            "String Theory</a>, "
            "which is a relative newcomer to theoretical physics, but one that has "
            "captured the common imagination, judging by the popular explanations "
            "that abound on the Web "
            '<span class="citation" data-cites="mann2019 wood2019 jones2020">[1]–[3]'
            "</span>. And whether string theory is or is not science, Popper "
            "notwithstanding, is an issue that is still up for debate "
            '<span class="citation" '
            'data-cites="siegel2015 castelvecchi2016 alves2017 francis2019">'
            "[4]–[7]</span>.</p>"
        ),
        '<h1 class="unnumbered" id="bibliography">References</h1>',
        '<div class="references csl-bib-body" id="refs" role="list">',
        '<div class="csl-entry" id="ref-mann2019" role="listitem">',
        (
            '<div class="csl-left-margin">[1] </div><div class="csl-right-inline">'
            "A. Mann, "
            "<span>“<span>What Is String Theory?</span>”</span> Mar. 20, 2019. "
            "Available: "
            '<a href="https://www.livescience.com/65033-what-is-string-theory.html">'
            "https://www.livescience.com/65033-what-is-string-theory.html</a>. "
            "[Accessed: Nov. 12, 2020]</div>"
        ),
        "</div>",
        '<div class="csl-entry" id="ref-wood2019" role="listitem">',
        (
            '<div class="csl-left-margin">[2] </div><div class="csl-right-inline">'
            "C. Wood, <span>“<span>What Is String Theory?</span>. Reference article: "
            "A simplified explanation and brief history of string theory,”</span> "
            'Jul. 11, 2019. Available: <a href="https://www.space.com/'
            "17594-string-theory"
            '.html">https://www.space.com/17594-string-theory.html</a>. '
            "[Accessed: Nov. 12, 2020]</div>"
        ),
        "</div>",
        '<div class="csl-entry" id="ref-jones2020" role="listitem">',
        (
            '<div class="csl-left-margin">[3] </div><div class="csl-right-inline">'
            'A. Z. Jones, <span>“<span class="nocase">The Basics of String Theory'
            "</span>,"
            '”</span> Mar. 02, 2019. Available: <a href="https://www.thoughtco.com/'
            'what-is-string-theory-2699363">https://www.thoughtco.com/'
            "what-is-string-theory-2699363</a>. [Accessed: Nov. 12, 2020]</div>"
        ),
        "</div>",
        '<div class="csl-entry" id="ref-siegel2015" role="listitem">',
        (
            '<div class="csl-left-margin">[4] </div><div class="csl-right-inline">'
            "E. Siegel, "
            "<span>“<span>Why String Theory Is Not A Scientific Theory</span>,”</span> "
            "Dec. "
            '23, 2015. Available: <a href="https://www.forbes.com/sites/startswithabang'
            '/2015/12/23/why-string-theory-is-not-science/">https://www.forbes.com'
            "/sites/"
            "startswithabang/2015/12/23/why-string-theory-is-not-science/</a>. "
            "[Accessed: "
            "Nov. 12, 2020]</div>"
        ),
        "</div>",
        '<div class="csl-entry" id="ref-castelvecchi2016" role="listitem">',
        (
            '<div class="csl-left-margin">[5] </div><div class="csl-right-inline">D. '
            'Castelvecchi, <span>“<span class="nocase">Feuding physicists turn to '
            "philosophy "
            "for help</span>. String theory is at the heart of a debate over the "
            "integrity of "
            "the scientific method itself,”</span> Jan. 05, 2016. Available: "
            '<a href="https://www.nature.com/news/feuding-physicists-turn-to-philosophy'
            "-for-"
            'help-1.19076">https://www.nature.com/news/feuding-physicists-turn-to-'
            "philosophy-"
            "for-help-1.19076</a>. [Accessed: Nov. 12, 2020]</div>"
        ),
        "</div>",
        '<div class="csl-entry" id="ref-alves2017" role="listitem">',
        (
            '<div class="csl-left-margin">[6] </div><div class="csl-right-inline">R. '
            'A. Batista and J. Primack, <span>“<span class="nocase">Is String theory '
            "falsifiable?</span>. Can a theory that isn’t completely testable still be "
            "useful "
            'to physics?”</span> Available: <a href="https://metafact.io/factchecks/'
            "30-is-"
            'string-theory-falsifiable">https://metafact.io/factchecks/30-is-string-'
            "theory-"
            "falsifiable</a>. [Accessed: Nov. 12, 2020]</div>"
        ),
        "</div>",
        '<div class="csl-entry" id="ref-francis2019" role="listitem">',
        (
            '<div class="csl-left-margin">[7] </div><div class="csl-right-inline">'
            "M. R. "
            'Francis, <span>“<span class="nocase">Falsifiability and physics</span>. '
            "Can a theory that isn’t completely testable still be useful to physics?”"
            "</span> "
            'Apr. 23, 2019. Available: <a href="https://www.scientificamerican.com/'
            "article/"
            'is-string-theory-science/">https://www.scientificamerican.com/article/'
            "is-string-"
            "theory-science/</a>. [Accessed: Nov. 12, 2020]</div>"
        ),
        "</div>",
        "</div>",
    ]
)

HTML_CITATION_TOC = (
    '<nav class="toc" role="doc-toc">\n'
    "<ul>\n"
    '<li><a href="#string-theory" id="toc-string-theory">String Theory</a></li>\n'
    '<li><a href="#bibliography" id="toc-bibliography">References</a></li>\n'
    "</ul>\n</nav>"
)

HTML_VALID_TEXT = (
    "<p>This is some valid content that should pass."
    " If it does not pass we"
    " will know something is wrong.</p>"
)

HTML_MATHJAX = (
    '<p><span class="math display">\\[\n'
    "e^{i\\theta} = \\cos\\theta + i \\sin\\theta.\n"
    "\\]</span></p>"
)

HTML_RAW_CONVERSION = (
    "<p>This is some valid content that should pass."
    " If it does not pass we will know something is wrong.</p>\n"
    "<p>Our fictitious internal files are available"
    ' <a href="{filename}/path/to/file">at</a>:</p>\n'
    "<p>Our fictitious static files are available"
    ' <a href="{static}/path/to/file">at</a>:</p>\n'
    "<p>Our fictitious attachments are available"
    ' <a href="{attach}path/to/file">at</a>:</p>'
)

HTML_WITH_HEADINGS = (
    "<p>This is some valid content that should pass."
    " If it does not pass we will know something is wrong.</p>\n"
    '<h2 id="first-heading">First Heading</h2>\n'
    "<p>This should be the first heading in my"
    " table of contents.</p>\n"
    '<h2 id="second-heading">Second Heading</h2>\n'
    "<p>This should be the second heading in my"
    " table of contents.</p>\n"
    '<h3 id="first-subheading">First Subheading</h3>\n'
    "<p>This is a subsection that should be shown as such"
    " in the table of contents.</p>\n"
    '<h3 id="second-subheading">Second Subheading</h3>\n'
    "<p>This is another subsection that should be shown as"
    " such in the table of contents.</p>"
)

HTML_TOC = (
    '<nav class="toc" role="doc-toc">\n'
    "<ul>\n"
    '<li><a href="#first-heading" id="toc-first-heading">'
    "First Heading</a></li>\n"
    '<li><a href="#second-heading" id="toc-second-heading">Second Heading</a>\n'
    "<ul>\n"
    '<li><a href="#first-subheading"'
    ' id="toc-first-subheading">First Subheading</a></li>\n'
    '<li><a href="#second-subheading"'
    ' id="toc-second-subheading">Second Subheading</a></li>\n'
    "</ul></li>\n"
    "</ul>\n"
    "</nav>"
)
