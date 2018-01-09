# -*- coding: utf-8 -*-

import alagitpull
alagitpull.projects = [
    {
        'name': 'LumberJack',
        'url': 'https://github.com/clarkzjw/LumberJack',
    },
    {
        'name': 'nginx-proxy-google',
        'url': 'https://github.com/clarkzjw/nginx-proxy-google',
    },
    {
        'name': 'GuidedFilter',
        'url': 'https://github.com/clarkzjw/GuidedFilter',
    },
    {
        'name': 'one-two-three...infinity',
        'url': 'https://github.com/clarkzjw/one-two-three...infinity'
    },
    {
        'name': 'Dehaze',
        'url': 'https://github.com/clarkzjw/Dehaze'
    },
    {
        'name': 'brainfuck',
        'url': 'https://github.com/clarkzjw/brainfuck'
    }
]

extensions = [
  'sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx',
  'sphinx.ext.todo', 'sphinx.ext.viewcode', 'alagitpull'
]

html_title = 'Hello World'

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'ring0.xyz 🍵'
copyright = u'2013 - 2018, clarkzjw'  # NOQA

version = '0.0'
release = '0.0'

exclude_patterns = ['_build', '.venv']

pygments_style = 'sphinx'

html_theme_path = [alagitpull.get_path()]
html_theme = 'alagitpull'
html_favicon = 'favicon.ico'
html_theme_options = {
    'logo': 'img/bagua.png',
    'projects': alagitpull.projects,
}
html_sidebars = {
    '**': [
        'about.html',
        'relations.html',
        'more.html',
    ]
}

html_static_path = ['_static']

htmlhelp_basename = 'confuciangentlemansclubdoc'


latex_elements = {
}

latex_documents = [
  ('index', 'confuciangentlemansclub.tex', u'confucian gentleman\'s',
   u'Tony Narlock', 'manual'),
]

man_pages = [
    ('index', 'confuciangentlemansclub', u'confucian gentleman\'s club',
     [u'Tony Narlock'], 1)
]

texinfo_documents = [
  ('index', 'confuciangentlemansclub', u'confucian gentleman\'s club',
   u'Tony Narlock', 'confuciangentlemansclub', 'Scribe.',
   'Miscellaneous'),
]

intersphinx_mapping = {
    'https://docs.python.org/2/': None,
    'sphinx': ('https://sphinx.readthedocs.io/en/latest/', None),
    'django': (
        'https://docs.djangoproject.com/en/1.11/',
        'https://docs.djangoproject.com/en/1.11/_objects/'
    ),
    'flask': ('http://flask.pocoo.org/docs/', None),
    'flask-sqlalchemy': ('http://flask-sqlalchemy.pocoo.org/2.2/', None),
    'werkzeug': ('http://werkzeug.pocoo.org/docs/0.12/', None),
    'jinja': ('http://jinja.pocoo.org/docs/dev', None),
    'sqlalchemy': ('http://docs.sqlalchemy.org/en/latest/', None),
    'uwsgi': ('https://uwsgi-docs.readthedocs.io/en/latest/', None),
}
