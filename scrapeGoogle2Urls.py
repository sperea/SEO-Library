# -*- coding: utf-8 -*-
__author__ = 'Sergio Perea'

from bs4 import BeautifulSoup
from urlparse import urlparse
import requests



maxPages = 20
counter = 0

import os
ficheros = os.listdir(os.getcwd()+'/tmp')
print ficheros

for fichero in ficheros:
    ecj_data = open("tmp/"+fichero,'r').read()
    html = BeautifulSoup(ecj_data)
    # Obtenemos todos los divs donde estan las entradas
    entradas = html.find_all('li',{'class':'g'})
    #print entradas
    # Recorremos todas las entradas para extraer el título, autor y fecha
    for entrada in entradas:
        counter += 1
        #titulo = entrada.find('div', {'class' : 'f kv _SWb'}).getText()
        url = entrada.find('cite', {}).getText()

        
        parsed_uri = urlparse( "http://" + url.encode("utf-8") )
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        print domain

        # Imprimo el Título, Autor y Fecha de las entradas
        #print "%s" %(url)

