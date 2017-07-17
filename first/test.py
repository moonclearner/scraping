import download
seed_url = "http://example.webscraping.com/index"
user_agent1 = "BadCrawler"
#  print download.download("http://www.baidu.com")
#  print download.parsersitemap("http://example.webscraping.com/sitemap.html")

# test get_links
#  content = download.download("http://www.baidu.com/")
#  download.writeTXT(content)
#  print download.get_links(content)


# test link crawl

download.link_crawler(seed_url, max_depth=2)
