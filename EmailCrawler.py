"""   

    This file is part of seo_utils (https://github.com/sperea/seo_utils)

     written by Sergio Perea (https://www.sergioperea.net)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# -*- coding: utf-8 -*- 
import requests
import re
import urlparse

#Emails recolector grammar
email_re = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')

# HTML <a> regexp
# Matches href="" attribute. Seeks the following link to explore
link_re = re.compile(r'href="(.*?)"')
listaUrls = [""]

def crawl(url, maxlevel):
    # It is a recursive process . If not limit the depth of the crawl , we could explore the whole Internet!
    listaUrls.insert(-1,url)
    if(maxlevel == 0):
        return []

    # Get the url and download
    req = requests.get(url)
    result = []

    # Check if successful
    if(req.status_code != 200):
        return []

    # Find and follow all the links
    links = link_re.findall(req.text)
    for link in links:
        if not (link in listaUrls) and (link.find("wp-content")==-1) and (link.find(".css")==-1) and (link.find(".js")==-1) and (link.find(".ico")==-1) and (link.find("#")==-1)  and (link.find(".jpg")==-1) :
            print "explorando : " + link + " nivel : " + str(maxlevel)
            # Get an absolute URL for a link
            link = urlparse.urljoin(url, link)
            result += crawl(link, maxlevel - 1)

    # Find all emails on current page
    result += email_re.findall(req.text)
    result_sin_duplicado = list(set(result))
    return result_sin_duplicado 


def crawl_Url(url):
    emails = crawl(url, 2)

    print "Scrapped e-mail addresses:"
    for e in emails:
        print e + ";" + url
    return  

crawl_Url('http://www.jlaasociados.es')