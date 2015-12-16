#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PyQt4 import QtCore, QtGui, uic
import requests
import re
import urlparse
import threading
from tld import get_tld
import validators
 
# Cargar nuestro archivo .ui
form_class = uic.loadUiType("ui/crawler.ui")[0]
 
class MyWindowClass(QtGui.QMainWindow, form_class):

 listaUrls = [""]
 #Emails recolector
 email_re = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')
 email_mailto = re.compile(r'mailto:.+?@.+.')

 # HTML <a> regexp
 # Matches href="" attribute. Seeks the following link to explore
 link_re = re.compile(r'href="(.*?)"')

 def __init__(self, parent=None):
  QtGui.QMainWindow.__init__(self, parent)
  self.setupUi(self)
  self.btnStart.clicked.connect(self.Start)



 
 def CrawlUrl(self, url, maxlevel):
    # It is a recursive process . If not limit the depth of the crawl , we could explore the whole Internet!
    
    self.listaUrls.insert(-1,url)
    if(maxlevel == 0):
        return []

    # Get the webpage
    req = requests.get(url)
    result = []

    # Check if successful
    if(req.status_code != 200):
        return []

    # Find and follow all the links
    links = self.link_re.findall(req.text)
    for link in links:
        print "enlace encontrado : " + link + " nivel : " + str(maxlevel) + " url: " + url
        if validators.url(link):
          actualDomain = get_tld(link)
          if (not link.lower().startswith("http")):
            print "Enlace reconstruido: " + link + " ----> " + url + link
            link = url + link

          enlaceCorrecto = (str(actualDomain).lower().strip() == str(self.globalDomain).lower().strip())
          if not (enlaceCorrecto):
            print "ESTE ENLACE NO ES CORRECTO: " + link 
            print actualDomain
            print self.globalDomain
          if (enlaceCorrecto) and not (link in self.listaUrls) and (link.find("wp-content")==-1) and (link.find(".css")==-1) and (link.find(".js")==-1) and (link.find(".ico")==-1) and (link.find("#")==-1) and (link.find(".jpg")==-1) :
              print "-------EXPLORANDO : " + link + " nivel : " + str(maxlevel) + " url: " + url
              #self.LogText("explorando : " + link + " nivel : " + str(maxlevel) + " url: " + url)
              # Get an absolute URL for a link
              url = str(url)
              link = urlparse.urljoin(url, link)
              result += self.CrawlUrl(link, maxlevel - 1)
        else:
          print "Enlace " + str(link) + " no válido"

    # Find all emails on current page
    if self.email_re.findall(req.text):
      result += self.email_re.findall(req.text)
      print "-------------EMAILS CAPTURADOS: " + ''.join(self.email_re.findall(req.text))

    result_sin_duplicado = list(set(result))
    
    return result_sin_duplicado 

 # Evento del boton btn_CtoF
 def Start(self):

  listOfUrls = str(self.lstUrls.toPlainText()).split("\n")
  for lineUrl in listOfUrls:
    linkurl = lineUrl 
    print "LINEA: " + linkurl
    self.globalDomain = get_tld(linkurl, as_object=True)
    resultado = self.CrawlUrl(linkurl, 4)
    print "---FIN---"
    
    for item in resultado:
      self.lstEmails.setPlainText(self.lstEmails.toPlainText() + item + ";" + linkurl + "\n")

 
app = QtGui.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()