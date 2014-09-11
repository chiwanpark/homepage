# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime
from types import GeneratorType

from jinja2 import Environment, PackageLoader
from markdown import Markdown
from pytz import timezone


DEST_DIR = os.environ.get('OUTPUT_DIR', './_build')
DEFAULT_TIMEZONE = timezone('Asia/Seoul')
MARKDOWN = Markdown(extensions=['meta', 'footnotes', 'codehilite(linenums=True)'])
DATE_FORMAT = '%b %d, %Y'


def create_jinja2_env() -> Environment:
    def url(*args):
        return '/' + '/'.join(list(args))

    def assets(name):
        return url('assets', name)

    env = Environment(loader=PackageLoader('build'))
    env.globals.update(url=url, assets=assets)
    return env


JINJA_ENV = create_jinja2_env()
TEMPLATES = {
    'index': JINJA_ENV.get_template('index.html'),
    'article': JINJA_ENV.get_template('article.html'),
    'article-index': JINJA_ENV.get_template('article-index.html')
}


class Page(object):
    def __init__(self, path: str=None, file_content: str=None):
        self.path = path
        self.file_content = file_content

    def save_to_file(self):
        current_path = os.path.join(get_current_dir(), 'pages')
        dest_path = self.path.replace(current_path, DEST_DIR).replace('.md', '.html')
        dest_dir = os.path.dirname(dest_path)
        make_output_dir(dest_dir)

        with open(dest_path, 'wb') as f:
            f.write(self.file_content.encode('utf-8'))


class ArticlePage(Page):
    def __init__(self, path: str=None, title: str=None, date: datetime=datetime.now(tz=DEFAULT_TIMEZONE),
                 content: str=None, summary: str=None):
        self.title = title
        self.date = date
        self.content = content
        self.summary = summary

        rendered = TEMPLATES['article'].render(article=self)
        super().__init__(path, rendered)

    @property
    def url(self) -> str:
        current_path = os.path.join(get_current_dir(), 'pages')
        return self.path.replace(current_path, '').replace('.md', '.html')


class ArticleIndexPage(Page):
    def __init__(self, path: str=None, articles: list=None):
        articles = list(articles)
        articles.sort(key=lambda article: article.date, reverse=True)

        rendered = TEMPLATES['article-index'].render(articles=articles)
        super().__init__(path, rendered)


class IndexPage(Page):
    def __init__(self, path: str=None, content: str=None):
        self.content = content

        rendered = TEMPLATES['index'].render(page=self)
        super().__init__(path, rendered)


def get_current_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def create_page(path: str=None, content: str=None):
    assert path
    assert content

    converted = MARKDOWN.reset().convert(content)
    meta = MARKDOWN.Meta

    page_type = meta['type'][0]
    if page_type == 'index':
        return IndexPage(path, converted)
    elif page_type == 'article':
        title = meta['title'][0]
        date = datetime.strptime(meta['date'][0], DATE_FORMAT)
        summary = meta['summary'][0]

        return ArticlePage(path, title, date, converted, summary)
    else:
        return None


def iter_pages(path: str=None) -> GeneratorType:
    if not path:
        path = os.path.join(get_current_dir(), 'pages')

    for name in os.listdir(path):
        abspath = os.path.join(path, name)
        if os.path.isdir(abspath):
            for subpage in iter_pages(abspath):
                yield subpage
        else:
            with open(abspath, 'rb') as f:
                content = f.read().decode('utf-8')

            page = create_page(abspath, content)
            if page:
                yield page


def make_output_dir(path: str=None):
    if not path:
        path = DEST_DIR
    if not os.path.exists(path):
        os.mkdir(path)


def clear_output_dir():
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    make_output_dir()


def copy_assets():
    shutil.copytree(os.path.join('.', 'assets'), os.path.join(DEST_DIR, 'assets'))


def build():
    clear_output_dir()
    copy_assets()

    current_path = os.path.join(get_current_dir(), 'pages')
    article_pages = []
    for page in iter_pages():
        if isinstance(page, ArticlePage):
            article_pages.append(page)

        page.save_to_file()

    page = ArticleIndexPage(os.path.join(current_path, 'articles', 'index.md'), article_pages)
    page.save_to_file()


def run_http_server():
    import http.server
    import socketserver

    httpd = socketserver.TCPServer(('', 8000), http.server.SimpleHTTPRequestHandler, bind_and_activate=False)
    httpd.allow_reuse_address = True
    httpd.server_bind()
    httpd.server_activate()
    httpd.serve_forever()


if __name__ == '__main__':
    build()
    if os.environ.get('local', 'False') == 'True':
        os.chdir(DEST_DIR)
        run_http_server()
