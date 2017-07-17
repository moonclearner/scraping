# -*- coding: utf-8 -*-
import csv
from zipfile import ZipFile
from StringIO import StringIO
from scraping.cache import Downloader


def alexa():
    D = Downloader.Downloader()
    zipped_data = D('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
    urls = []
    # top 1 million URL's will be stored in this list
    with ZipFile(StringIO(zipped_data)) as zf:
        # 因为现在的是zip数据流 需要一个对应的接口
        csv_filename = zf.namelist()[0]
        for _, website in csv.reader(zf.open(csv_filename)):
            urls.append('http://' + website)
    return urls


if __name__ == '__main__':
    print len(alexa())
