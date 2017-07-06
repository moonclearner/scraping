import re
import download


url = "https://www.zhihu.com/question/28207685"
html = download.download(url, headers={})
print html
download.writeTXT(html, "html.txt")
content = re.findall('<br><br>(.*?)<br><br>', html)
download.writeTXT(content, "content.txt")
