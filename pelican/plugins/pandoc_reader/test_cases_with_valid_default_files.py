"""Tests using valid default files for pandoc-reader plugin."""
import os
import unittest

from pelican.tests.support import get_settings

from pandoc_reader import PandocReader

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_content"))
TEST_DEFAULT_FILES_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_default_files"))


class TestValidCasesWithDefaultFiles(unittest.TestCase):
    """Valid test cases using default files."""

    def test_valid_file_with_valid_defaults(self):
        """Check if we get the appropriate output specifying defaults."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "valid_defaults.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(
            (
                "<p>This is some valid content that should pass."
                " If it does not pass we will know something is wrong.</p>"
            ),
            output,
        )

        self.assertEqual("Valid Content", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_mathjax_with_valid_defaults(self):
        """Check if mathematics is rendered correctly with defaults."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "valid_defaults.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)

        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "mathjax_content.md")
        output, metadata = pandoc_reader.read(source_path)

        self.assertEqual(
            (
                '<p><span class="math display">\\[\n'
                "e^{i\\theta} = \\cos\\theta + i \\sin\\theta.\n"
                "\\]</span></p>"
            ),
            output,
        )

        self.assertEqual("MathJax Content", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))

    def test_toc_with_valid_defaults(self):
        """Check if output and table of contents are valid with defaults."""
        pandoc_default_files = [
            os.path.join(TEST_DEFAULT_FILES_PATH, "valid_defaults_with_toc.yaml")
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files)
        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_toc.md")
        output, metadata = pandoc_reader.read(source_path)
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(
            (
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
            ),
            output,
        )

        self.assertEqual("Valid Content with Table of Contents", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))
        self.assertEqual(
            '<nav class="toc" role="doc-toc">\n'
            "<ul>\n"
            '<li><a href="#first-heading">First Heading</a></li>\n'
            '<li><a href="#second-heading">Second Heading</a>\n'
            "<ul>\n"
            '<li><a href="#first-subheading">First Subheading</a></li>\n'
            '<li><a href="#second-subheading">Second Subheading</a></li>\n'
            "</ul></li>\n"
            "</ul>\n"
            "</nav>",
            str(metadata["toc"]),
        )

    def test_citations_and_toc_with_valid_defaults(self):
        """Check if output, citations and table of contents are valid."""
        pandoc_default_files = [
            os.path.join(
                TEST_DEFAULT_FILES_PATH, "valid_defaults_with_toc_and_citations.yaml",
            )
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files,)
        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        output, metadata = pandoc_reader.read(source_path)
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(
            (
                '<h2 id="string-theory">String Theory</h2>\n'
                "<p>But this foundational principle of science has"
                " now been called into question by"
                ' <a href="https://www.britannica.com/science/'
                'string-theory">String Theory</a>,'
                " which is a relative newcomer to theoretical physics, but one"
                " that has captured the common imagination, judging by"
                " the popular explanations that abound on the Web"
                ' <span class="citation" data-cites="mann2019 wood2019'
                ' jones2020">[1]–[3]</span>.'
                " And whether string theory is or is not science, Popper"
                " notwithstanding, is an issue that is still up for debate"
                " <span"
                ' class="citation" data-cites="siegel2015 castelvecchi2016'
                ' alves2017 francis2019">[4]–[7]</span>.</p>\n'
                '<h1 class="unnumbered" id="bibliography">References</h1>\n'
                '<div class="references csl-bib-body" id="refs"'
                ' role="doc-bibliography">\n'
                '<div class="csl-entry" id="ref-mann2019"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[1]'
                ' </div><div class="csl-right-inline">A. Mann,'
                " <span>“<span>What Is String Theory?</span>”</span>"
                " 20-Mar-2019. [Online]."
                ' Available: <a href="https://www.livescience.com/'
                '65033-what-is-string-theory.html">'
                "https://www.livescience.com/"
                "65033-what-is-string-theory.html</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-wood2019"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[2] </div>'
                '<div class="csl-right-inline">'
                "C. Wood, <span>“<span>What Is String Theory?</span>."
                " Reference article:"
                " A simplified explanation and brief history of string"
                " theory,”</span> 11-Jul-2019."
                ' [Online]. Available: <a href="https://www.space.com/'
                '17594-string-theory.html">'
                "https://www.space.com/17594-string-theory.html</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-jones2020"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[3]'
                ' </div><div class="csl-right-inline">'
                'A. Z. Jones, <span>“<span class="nocase">The Basics of String'
                " Theory</span>,”</span> 02-Mar-2019. [Online]. Available:"
                ' <a href="https://www.thoughtco.com/'
                'what-is-string-theory-2699363">'
                "https://www.thoughtco.com/what-is-string-theory-2699363</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-siegel2015"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[4]'
                ' </div><div class="csl-right-inline">'
                "E. Siegel, <span>“<span>Why String Theory Is Not A Scientific"
                " Theory</span>,”</span> 23-Dec-2015. [Online]. Available:"
                " <a"
                ' href="https://www.forbes.com/sites/'
                "startswithabang/2015/12/23/"
                'why-string-theory-is-not-science/">https://www.forbes.com/'
                "sites/startswithabang/2015/12/23/"
                "why-string-theory-is-not-science/</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-castelvecchi2016"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[5]'
                ' </div><div class="csl-right-inline">'
                'D. Castelvecchi, <span>“<span class="nocase">'
                "Feuding physicists turn"
                " to philosophy for help</span>. String theory is at the"
                " heart of a debate over the integrity of the scientific"
                " method itself,”</span> 05-Jan-2016. [Online]. Available:"
                ' <a href="https://www.nature.com/news/'
                'feuding-physicists-turn-to-philosophy-for-help-1.19076">'
                "https://www.nature.com/news/"
                "feuding-physicists-turn-to-philosophy-for-help-1.19076</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-alves2017"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[6] </div>'
                '<div class="csl-right-inline">'
                'R. A. Batista and J. Primack, <span>“<span class="nocase">'
                "Is String theory falsifiable?</span>. Can a theory that isn’t"
                " completely testable still be useful to physics?”</span>"
                " [Online]."
                ' Available: <a href="https://metafact.io/factchecks/'
                '30-is-string-theory-falsifiable">'
                "https://metafact.io/factchecks/"
                "30-is-string-theory-falsifiable</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-francis2019"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[7]'
                ' </div><div class="csl-right-inline">'
                'M. R. Francis, <span>“<span class="nocase">Falsifiability and'
                " physics</span>. Can a theory that isn’t completely testable"
                " still be useful to physics?”</span> 23-Apr-2019."
                " [Online]. Available:"
                ' <a href="https://www.scientificamerican.com/'
                'article/is-string-theory-science/">'
                "https://www.scientificamerican.com/article/is-"
                "string-theory-science/</a>. [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                "</div>"
            ),
            output,
        )

        self.assertEqual("Valid Content With Citation", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))
        self.assertEqual(
            (
                '<nav class="toc" role="doc-toc">\n'
                "<ul>\n"
                '<li><a href="#string-theory">String Theory</a></li>\n'
                '<li><a href="#bibliography">References</a></li>\n'
                "</ul>\n</nav>"
            ),
            str(metadata["toc"]),
        )

    def test_citations_and_with_citeproc_filter(self):
        """Check if output, citations are valid using citeproc filter."""
        pandoc_default_files = [
            os.path.join(
                TEST_DEFAULT_FILES_PATH, "valid_defaults_with_citeproc_filter.yaml",
            )
        ]

        settings = get_settings(PANDOC_DEFAULT_FILES=pandoc_default_files,)
        pandoc_reader = PandocReader(settings)

        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        output, metadata = pandoc_reader.read(source_path)
        self.maxDiff = None  # pylint: disable=invalid-name

        self.assertEqual(
            (
                '<h2 id="string-theory">String Theory</h2>\n'
                "<p>But this foundational principle of science has"
                " now been called into question by"
                ' <a href="https://www.britannica.com/science/'
                'string-theory">String Theory</a>,'
                " which is a relative newcomer to theoretical physics, but one"
                " that has captured the common imagination, judging by"
                " the popular explanations that abound on the Web"
                ' <span class="citation" data-cites="mann2019 wood2019'
                ' jones2020">[1]–[3]</span>.'
                " And whether string theory is or is not science, Popper"
                " notwithstanding, is an issue that is still up for debate"
                " <span"
                ' class="citation" data-cites="siegel2015 castelvecchi2016'
                ' alves2017 francis2019">[4]–[7]</span>.</p>\n'
                '<h1 class="unnumbered" id="bibliography">References</h1>\n'
                '<div class="references csl-bib-body" id="refs"'
                ' role="doc-bibliography">\n'
                '<div class="csl-entry" id="ref-mann2019"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[1]'
                ' </div><div class="csl-right-inline">A. Mann,'
                " <span>“<span>What Is String Theory?</span>”</span>"
                " 20-Mar-2019. [Online]."
                ' Available: <a href="https://www.livescience.com/'
                '65033-what-is-string-theory.html">'
                "https://www.livescience.com/"
                "65033-what-is-string-theory.html</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-wood2019"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[2] </div>'
                '<div class="csl-right-inline">'
                "C. Wood, <span>“<span>What Is String Theory?</span>."
                " Reference article:"
                " A simplified explanation and brief history of string"
                " theory,”</span> 11-Jul-2019."
                ' [Online]. Available: <a href="https://www.space.com/'
                '17594-string-theory.html">'
                "https://www.space.com/17594-string-theory.html</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-jones2020"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[3]'
                ' </div><div class="csl-right-inline">'
                'A. Z. Jones, <span>“<span class="nocase">The Basics of String'
                " Theory</span>,”</span> 02-Mar-2019. [Online]. Available:"
                ' <a href="https://www.thoughtco.com/'
                'what-is-string-theory-2699363">'
                "https://www.thoughtco.com/what-is-string-theory-2699363</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-siegel2015"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[4]'
                ' </div><div class="csl-right-inline">'
                "E. Siegel, <span>“<span>Why String Theory Is Not A Scientific"
                " Theory</span>,”</span> 23-Dec-2015. [Online]. Available:"
                " <a"
                ' href="https://www.forbes.com/sites/'
                "startswithabang/2015/12/23/"
                'why-string-theory-is-not-science/">https://www.forbes.com/'
                "sites/startswithabang/2015/12/23/"
                "why-string-theory-is-not-science/</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-castelvecchi2016"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[5]'
                ' </div><div class="csl-right-inline">'
                'D. Castelvecchi, <span>“<span class="nocase">'
                "Feuding physicists turn"
                " to philosophy for help</span>. String theory is at the"
                " heart of a debate over the integrity of the scientific"
                " method itself,”</span> 05-Jan-2016. [Online]. Available:"
                ' <a href="https://www.nature.com/news/'
                'feuding-physicists-turn-to-philosophy-for-help-1.19076">'
                "https://www.nature.com/news/"
                "feuding-physicists-turn-to-philosophy-for-help-1.19076</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-alves2017"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[6] </div>'
                '<div class="csl-right-inline">'
                'R. A. Batista and J. Primack, <span>“<span class="nocase">'
                "Is String theory falsifiable?</span>. Can a theory that isn’t"
                " completely testable still be useful to physics?”</span>"
                " [Online]."
                ' Available: <a href="https://metafact.io/factchecks/'
                '30-is-string-theory-falsifiable">'
                "https://metafact.io/factchecks/"
                "30-is-string-theory-falsifiable</a>."
                " [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                '<div class="csl-entry" id="ref-francis2019"'
                ' role="doc-biblioentry">\n'
                '<div class="csl-left-margin">[7]'
                ' </div><div class="csl-right-inline">'
                'M. R. Francis, <span>“<span class="nocase">Falsifiability and'
                " physics</span>. Can a theory that isn’t completely testable"
                " still be useful to physics?”</span> 23-Apr-2019."
                " [Online]. Available:"
                ' <a href="https://www.scientificamerican.com/'
                'article/is-string-theory-science/">'
                "https://www.scientificamerican.com/article/is-"
                "string-theory-science/</a>. [Accessed: 12-Nov-2020]</div>\n"
                "</div>\n"
                "</div>"
            ),
            output,
        )

        self.assertEqual("Valid Content With Citation", str(metadata["title"]))
        self.assertEqual("My Author", str(metadata["author"]))
        self.assertEqual("2020-10-16 00:00:00", str(metadata["date"]))


if __name__ == "__main__":
    unittest.main()
