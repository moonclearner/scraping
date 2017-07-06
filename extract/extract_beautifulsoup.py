from bs4 import BeautifulSoup


broken_html = "<ul class=country><li>Area <li>Population</ul>"
soup = BeautifulSoup(broken_html, "lxml")
fixed_html = soup.prettify()
# fixed_html
"""
<html>
 <body>
  <ul class="country">
   <li>
    Area
   </li>
   <li>
    Population
   </li>
  </ul>
 </body>
</html>
"""


ul = BeautifulSoup(fixed_html, "lxml").find('ul', attrs={'class': 'country'})
print ul
"""
<ul class="country">
 <li>
  Area
 </li>
 <li>
  Population
 </li>
</ul>
"""
print ul.find('li')
"""
   <li>
    Area
   </li>
"""
print ul.find('li').text
"""
Area
"""
print ul.find_all('li')
