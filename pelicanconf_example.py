# Example Pelican configuration file with global bibliography support
# Copy this to your pelicanconf.py and customize as needed

# Enable citations
PANDOC_ARGS = [
    "--citeproc",
    "--csl=https://www.zotero.org/styles/ieee-with-url",
    "--metadata=link-citations:false",
    "--metadata=reference-section-title:References",
]

PANDOC_EXTENSIONS = ["+smart"]

# Global bibliography files to search for
# Default names are: ["_bibliography", "bibliography", "references"]
PANDOC_GLOBAL_BIB_FILES = ["_bibliography", "bibliography", "references"]

# Alternative custom global bibliography names
# PANDOC_GLOBAL_BIB_FILES = ["my_bib", "global_refs", "shared_bibliography"]

# Other common Pelican settings
AUTHOR = "Your Name"
SITENAME = "Your Site Name"
SITEURL = ""

# Path to your content directory
PATH = "content"

# Output directory
OUTPUT_PATH = "output"

# Theme settings (if using a theme)
THEME = "theme"

# URL settings
ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"

PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"

# Feed settings
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

# Social widget
SOCIAL = (
    ("GitHub", "https://github.com/yourusername"),
    ("Twitter", "https://twitter.com/yourusername"),
)

# Pagination
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True 