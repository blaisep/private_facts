# -*- coding: utf-8 -*-

extensions = ['sphinx.ext.autodoc',
              'furo',
#              'pydata_sphinx_theme',
              ]

templates_path = ['_templates']
source_suffix = {'.rst': 'restructuredtext', '.md': 'restructuredtext'}
master_doc = 'index'
project = u'Tahoe-LAFS'
copyright = u'2025, The Tahoe-LAFS Developers'
author = u'The Tahoe-LAFS Developers'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'1.x'
# The full version, including alpha/beta/rc tags.
release = u'1.x'
language = "en"
exclude_patterns = ['_build']
pygments_style = 'sphinx'
# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "content_footer_items": ["last-updated"],
    "inherit" : "basic",
    "stylesheet" : "styles/pydata-sphinx-theme.css",
    "pygments_style" : "tango",
    "sidebars" : "sidebar-nav-bs.html",
}
# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "The Private Facts Project"

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "Private Facts"
html_static_path = ['_static']
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True
htmlhelp_basename = 'Tahoe-LAFSdoc'
# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',

# Latex figure (float) alignment
#'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Tahoe-LAFS.tex', u'Tahoe-LAFS Documentation',
     u'The Tahoe-LAFS Developers', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'tahoe-lafs', u'Tahoe-LAFS Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Tahoe-LAFS', u'Tahoe-LAFS Documentation',
     author, 'Tahoe-LAFS', 'One line description of project.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False
