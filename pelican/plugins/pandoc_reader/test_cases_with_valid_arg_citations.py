"""Tests using valid arguments and citations for pandoc-reader plugin."""
import os
import unittest

from pelican.tests.support import get_settings

from pandoc_reader import PandocReader

DIR_PATH = os.path.dirname(__file__)
TEST_CONTENT_PATH = os.path.abspath(os.path.join(DIR_PATH, "test_content"))

# Test settings that will be set in pelicanconf.py by plugin users
PANDOC_ARGS = ["--mathjax"]
PANDOC_EXTENSIONS = ["+smart"]


class TestValidCaseWithArgumentsAndCitations(unittest.TestCase):
    """Test cases with valid arguments and citations."""

    def test_citations_1(self):
        """Check if output and citations through -C argument is valid."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS
            + [
                "-C",
                "--csl=https://www.zotero.org/styles/ieee-with-url",
                "--metadata=link-citations:false",
                "--metadata=reference-section-title:References",
            ],
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        output, metadata = pandoc_reader.read(source_path)

        # Setting this so that assert is able to execute the difference
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

    def test_citations_2(self):
        """Check if output and citations through --citeproc argument is valid."""
        settings = get_settings(
            PANDOC_EXTENSIONS=PANDOC_EXTENSIONS,
            PANDOC_ARGS=PANDOC_ARGS
            + [
                "--citeproc",
                "--csl=https://www.zotero.org/styles/ieee-with-url",
                "--metadata=link-citations:false",
                "--metadata=reference-section-title:References",
            ],
        )

        pandoc_reader = PandocReader(settings)
        source_path = os.path.join(TEST_CONTENT_PATH, "valid_content_with_citation.md")
        output, metadata = pandoc_reader.read(source_path)

        # Setting this so that assert is able to execute the difference
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
