# -*- coding: utf-8 -*-
from lxml import etree
import sys
import urllib
import os
import shutil

class ParseRssNews ():
    imagenes=0
    titulos=0
    contenido=[]
    boolean=False
    links_imagenes=[]
    busqueda="afadsfasdf"
    noticias=[]
    linksnoticias=[]
    boolnoticias=-1
    contador=0
    def __init__ (self):
        if not os.path.exists("Imagenes"):
            os.makedirs("Imagenes")
        print ('---- Principio del archivo')


    def start (self, tag, attrib):
        lista=attrib.keys()
	if(tag == "title"):
		self.contador=self.contador+1 # Los dos primeros titulos no son noticias.
		self.boolnoticias=0
	if(tag == "link"):
		self.boolnoticias=1
        if(tag == "guid"):
            self.titulos=self.titulos+1

        if("type" in lista and attrib["type"]=="image/jpeg"):
            self.imagenes=self.imagenes+1
            self.links_imagenes.append(attrib["url"])

    def data (self, data):
            texto= str(data.encode('utf-8'))

	    if(self.boolnoticias==0 and self.contador>2):
		self.noticias.append(str(data.encode('utf-8')))
		self.boolnoticias=-1;
	    if(self.boolnoticias==1 and self.contador>2):
		self.linksnoticias.append(str(data.encode('utf-8')))
		self.boolnoticias=-1;
            if(texto.find(self.busqueda)>=0):
                self.contenido.append(texto)
            #print ('Toloco datos  %s' % data)

    def download_pictures(self):
        for i in self.links_imagenes:
            filename, request=urllib.urlretrieve(i)
            shutil.move(filename,"Imagenes/")
    def get_noticias(self):
        return self.noticias
    def get_links_noticias(self):
        return self.linksnoticias

    def close (self):
        print('El archivo contiene %i noticias' % (self.titulos))
        print('El archivo contiene %i imagenes' % (self.imagenes))
        #self.download_pictures()
        print('Elemento %s ha sido encontrado en los siguientes textos' % (self.busqueda))


        print ('---- Fin del archivo')
