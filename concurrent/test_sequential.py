# -*- coding: utf-8 -*-

#  from crawler import crawler
from scraping.cache.mongo_cache import MongoCache
from alexa_dzip_call import AlexaCallback


def main():
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    # cache.clear()
    #  crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache, timeout=10, ignore_robots=True)


if __name__ == '__main__':
    main()
