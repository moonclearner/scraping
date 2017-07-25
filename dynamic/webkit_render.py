# -*- coding: utf-8 -*-

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtWebKit import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    from PyQt4.QtWebKit import *
import lxml.html
from scraping.cache import Downloader
import pdb


def direct_download(url):
    download = Downloader.Downloader()
    return download(url)


def webkit_download(url):
    app = QApplication([])
    webview = QWebView()
    webview.loadFinished.connect(app.quit)
    webview.load(url)
    app.exec_()
    # delay here until download finished
    return webview.page().mainFrame().toHtml()


def parse(html):
    tree = lxml.html.fromstring(html)
    pdb.set_trace()
    print tree.cssselect('#result')[0].text_content()


def main():
    url = 'http://example.webscraping.com/dynamic'
    parse(direct_download(url))
    parse(webkit_download(url))


if __name__ == '__main__':
    main()
