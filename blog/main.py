#!/usr/bin/env python
#-*-coding=utf-8-*-
from flask import Flask, render_template, request
from flask_flatpages import FlatPages,pygments_style_defs
from flask_frozen import Freezer
import sys

BOLG_URL = 'http://blog.zeromake.com'

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_MARKDOWN_EXTENSIONS = ['markdown.extensions.extra','markdown.extensions.codehilite','pymdownx.github', 'markdown.extensions.toc', 'markdown.extensions.tables']
app = Flask(__name__)
app.config.from_object(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    pages = [p for p in flatpages if 'date' in p.meta]
    # print(pages[0].meta)
    pages = sorted(pages, key=lambda page: page.meta['date'], reverse = True)
    return render_template('index.html', pages=pages)

@app.route('/pages/<path:path>/')
def page(path):
    page = flatpages.get_or_404(path)
    # print(dir(page))
    return render_template('page.html', page=page, root_url=BOLG_URL)

@app.template_filter('md5')
def str_to_md5(s):
    import hashlib
    m = hashlib.md5()
    s = str(s)
    m.update(s.encode('utf8'))
    return m.hexdigest()

@app.route('/css/pygments.css')
def pygments_css():
    return pygments_style_defs('xcode'), 200, {'Content-Type': 'text/css'}
    # ['colorful', 'fruity', 'emacs', 'pastie', 'default', 'rrt', 'igor',
    # 'bw', 'perldoc', 'paraiso-light', 'tango', 'monokai', 'vs', 'xcode', 'trac',
    # 'borland', 'algol_nu', 'paraiso-dark', 'algol', 'autumn', 'manni', 'lovelace',
    # 'native', 'murphy', 'vim', 'friendly']

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "make":
        freezer.freeze()
    else:
        app.run('0.0.0.0',port=8000)
