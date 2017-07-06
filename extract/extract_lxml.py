"""
pip install lxml
pip install cssselect
"""
import lxml.html

broken_html = "<ul class=country><li>Area <li>Population</ul>"
tree = lxml.html.fromstring(broken_html)
fixed_html = lxml.html.tostring(tree, pretty_print=True)
print fixed_html
# fixed_html
"""
  <ul class="country">
   <li>Area</li>
   <li>Population</li>
  </ul>
"""
# css select
tree = lxml.html.fromstring(fixed_html)
li = tree.cssselect('ul.country > li:nth-child(1)')
for i in li:
    print i.text_content()
