# -*- coding: utf-8 -*-
import os
import re
import shutil
import http.server
import socketserver
import subprocess
from threading import Thread
from datetime import datetime
from types import GeneratorType

import click
from pytz import timezone
from markdown import Markdown
from jinja2 import Environment, PackageLoader


def get_current_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


DEST_DIR = os.path.join(get_current_dir(), '_build')
DEFAULT_TIMEZONE = timezone('Asia/Seoul')
MARKDOWN = Markdown(extensions=['meta', 'footnotes', 'codehilite(linenums=True)', 'fenced_code'])
DATE_FORMAT = '%b %d, %Y'
GIT_REPOSITORY_URL = 'https://github.com/chiwanpark/chiwanpark.github.io'


def create_jinja2_env() -> Environment:
    def url(*args):
        return '/' + '/'.join(list(args))

    def assets(name):
        return url('assets', name)

    def git_hash_link(path):
        cmds = ['/usr/bin/git', 'log', '--pretty=format:"%H,%h"', '-1', '--', path]
        git_log = subprocess.Popen(cmds, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
        if not git_log:
            return 'UNCOMMITED'
        full_hash, short_hash = git_log.replace('"', '').split(',')
        path = path.replace(get_current_dir() + '/', '')

        return '<a href="%s/blob/%s/%s">%s</a>' % (GIT_REPOSITORY_URL, full_hash, path, short_hash)

    env = Environment(loader=PackageLoader('cli'))
    env.globals.update(url=url, assets=assets, git_hash_link=git_hash_link)
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

        rendered = TEMPLATES['article'].render(article=self, path=path)
        super().__init__(path, rendered)

    @property
    def url(self) -> str:
        current_path = os.path.join(get_current_dir(), 'pages')
        return self.path.replace(current_path, '').replace('.md', '.html')


class ArticleIndexPage(Page):
    def __init__(self, path: str=None, articles: list=None):
        articles = list(articles)
        articles.sort(key=lambda article: article.date, reverse=True)

        rendered = TEMPLATES['article-index'].render(articles=articles, path=path)
        super().__init__(path, rendered)


class IndexPage(Page):
    def __init__(self, path: str=None, content: str=None):
        self.content = content

        rendered = TEMPLATES['index'].render(page=self, path=path)
        super().__init__(path, rendered)


def create_page(path: str=None, content: str=None):
    assert path
    assert content

    converted = MARKDOWN.reset().convert(content)
    meta = MARKDOWN.Meta

    page_type = meta['type'][0]
    if page_type == 'index':
        click.echo('[BUILD] Index page detected (%s)' % path)
        return IndexPage(path, converted)
    elif page_type == 'article':
        title = meta['title'][0]
        date = datetime.strptime(meta['date'][0], DATE_FORMAT)
        summary = meta['summary'][0]

        click.echo('[BUILD] Article page detected (%s)' % path)
        return ArticlePage(path, title, date, converted, summary)
    else:
        return None


def iter_pages(path: str=None) -> GeneratorType:
    if not path:
        path = os.path.join(get_current_dir(), 'pages')

    for name in os.listdir(path):
        if name.startswith('.'):
            continue
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


def build_assets(path: str=None):
    current_dir = get_current_dir()
    base_path = os.path.join(current_dir, 'assets')
    dest_base_path = os.path.join(DEST_DIR, 'assets')

    if not path:
        path = base_path

    make_output_dir(dest_base_path)

    for name in os.listdir(path):
        abspath = os.path.join(path, name)
        if os.path.isdir(abspath):
            build_assets(abspath)
        else:
            dest_path = abspath.replace(base_path, dest_base_path)
            if abspath.split('.')[-1] == 'less':
                click.echo('[BUILD] Asset file detected (%s) -> LESS' % abspath)
                dest_path = re.sub(r'less$', 'css', dest_path)
                cmds = ['lessc', '-x', abspath, dest_path]
                subprocess.call(cmds)
            else:
                click.echo('[BUILD] Asset file detected (%s)' % abspath)
                shutil.copy(abspath, dest_path)


def make_output_dir(path: str=None):
    if not path:
        path = DEST_DIR
    if not os.path.exists(path):
        os.mkdir(path)


@click.group(chain=True)
def cli():
    pass


@cli.command()
def build():
    click.echo('[BUILD] Build whole pages of site.')
    if not os.path.exists(DEST_DIR):
        click.echo('[BUILD] There is no destination directory, so we create destination directory.')
        make_output_dir()

    build_assets()

    current_path = os.path.join(get_current_dir(), 'pages')
    article_pages = []
    for page in iter_pages():
        if isinstance(page, ArticlePage):
            article_pages.append(page)

        page.save_to_file()

    page = ArticleIndexPage(os.path.join(current_path, 'articles', 'index.md'), article_pages)
    page.save_to_file()


class HttpdThread(Thread):
    def __init__(self):
        super().__init__()
        self.httpd = socketserver.TCPServer(('', 8000), http.server.SimpleHTTPRequestHandler, bind_and_activate=False)

    def run(self):
        os.chdir(DEST_DIR)

        self.httpd.allow_reuse_address = True

        self.httpd.server_bind()
        self.httpd.server_activate()

        click.echo('[HTTPD] Running on http://0.0.0.0:8000')

        self.httpd.serve_forever()

    def shutdown(self):
        click.echo('[HTTPD] Stopping daemon...')
        self.httpd.shutdown()


@cli.command()
def clean():
    os.chdir(get_current_dir())
    if os.path.exists(DEST_DIR):
        click.echo('[BUILD] Clean destination directory.')
        shutil.rmtree(DEST_DIR)


@cli.command()
@click.pass_context
def watch(ctx):
    from time import sleep
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    ctx.invoke(clean)
    ctx.invoke(build)

    current_dir = get_current_dir()
    click.echo('[WATCH] Watching %s' % current_dir)

    httpd_thread = HttpdThread()

    class RecompileAllEventHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            nonlocal httpd_thread

            if event.is_directory:
                return

            click.echo('[WATCH] Event detected (%s), try rebuilding site.' % event)

            httpd_thread.shutdown()

            os.chdir(current_dir)

            ctx.invoke(clean)
            ctx.invoke(build)

            httpd_thread = HttpdThread()
            httpd_thread.start()

    observer = Observer()
    all_event_handler = RecompileAllEventHandler()

    observer.schedule(all_event_handler, os.path.join(current_dir, 'templates'), recursive=True)
    observer.schedule(all_event_handler, os.path.join(current_dir, 'pages'), recursive=True)
    observer.schedule(all_event_handler, os.path.join(current_dir, 'assets'), recursive=True)

    httpd_thread.start()
    observer.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        click.echo('[BUILD] Keyboard Interrupt detected, shutdown.')
        if observer.is_alive():
            observer.stop()
        if httpd_thread.is_alive():
            httpd_thread.shutdown()

    observer.join()

    ctx.invoke(clean)


if __name__ == '__main__':
    cli()
