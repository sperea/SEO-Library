"""from BeautifulSoup import BeautifulSoup
import urllib
import re

site = urllib.urlopen('http://duckduckgo.com/html/?q=opticas+madrid')
data = site.read()
parsed = BeautifulSoup(data)

first_link = parsed.findAll('div', {'class': re.compile('links_main*')})[0].a['href']

for i in parsed.findAll('div', {'class': re.compile('links_main*')}):
    print i.a['href']

"""
import urllib
try:
    import json
except ImportError:
    import simplejson as json

end_point='http://api.duckduckgo.com/?q='
#query_string = urllib.quote_plus(query)
final_url = end_point + urllib.quote_plus("opticas+madrid") +'&format=json&pretty=1'
response = urllib.urlopen(final_url)
data = json.load(response)
#params = dict(form.fields)
print data
