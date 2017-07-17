import pdb


def download(url, headers=None, proxy=None, num_retries=2, data=None):
    import urlparse
    import urllib2
    print 'Downloading:', url
    request = urllib2.Request(url, data, headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read()
        code = response.code
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                return download(url, headers, proxy, num_retries - 1, data)
        else:
            code = None
    return html


def parsersitemap(url):
    import re
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in links:
        html = download(link)
        print html


def link_crawler(seed_url, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=1):
    """Crawl from the given seed URL following links matched by link_regex
    """
    import Queue
    # the queue of URL's that still need to be crawled
    crawl_queue = Queue.deque([seed_url])
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = 0
    rp = robotparser(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent
    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            depth = seen[url]
            if depth != max_depth:
                # can still crawl further
                for link in get_links(html):
                    if getUrlabsolute(link, seed_url):
                        link = getUrlabsolute(link, seed_url)
                    if link not in seen:
                        seen[link] = depth + 1
                        # check link is within same domain
                        if isSameDomain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)
            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt:', url


def getUrlabsolute(url, seed_url):
    import urlparse
    if urlparse.urlparse(url).netloc is "" and urlparse.urlparse(url).path:
        return urlparse.urljoin(seed_url, url)
    elif urlparse.urlparse(url).scheme == "http":
        return url
    else:
        return None


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    import urlparse
    link, _ = urlparse.urldefrag(link)
    # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)


def get_links(html):
    import re
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    print webpage_regex.findall(html)
    return webpage_regex.findall(html)


def writeTXT(text, filename="save.txt"):
    with open(filename, 'a') as f:
        for i in text:
            f.write(i)


def robotparser(url):
    import robotparser
    import urlparse
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


class Throttle(object):
    """add a delay between downloads to the same domain"""
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        import urlparse
        import datetime
        import time
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()


def isSameDomain(url1, url2):
    import urlparse
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc
