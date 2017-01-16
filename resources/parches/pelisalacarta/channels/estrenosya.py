# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para EstrenosYa o estrenosGo (es la misma web) SOLO se extraen los enlaces torrent !!!
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# EstrenosYa   Autor: ciberus  (06-2015/01-2016)
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
#from servers import servertools

__channel__ = "estrenosya"
__category__ = "F,S,VOS"
__type__ = "generic"
__title__ = "EstrenosYa"
__language__ = "ES"

BASE_URL = "http://www.estrenosya.net"
FANARTIMAGE = "http://i.imgur.com/EmmVJPc.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/CPqv4rz.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"

#CANALTHUMB = os.path.join( config.get_runtime_path(), 'resources' , 'images' ,"estrenosgo.jpg")
#CANALFANART = os.path.join( config.get_runtime_path(), 'resources' , 'images' ,"estrenosyafanart.jpg")

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.EstrenosYa mainlist")
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR yellow]Cartelera  (Últimas)[/COLOR]", url="http://estrenosya.net/descarga-0-58126-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR yellow]Cartelera  (Por Géneros)[/COLOR]", url="http://estrenosya.net/descarga-0-58126-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR orange]Películas DVD Rip  (Últimas)[/COLOR]", url="http://estrenosya.net/descarga-0-581210-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR orange]Películas DVD Rip  (Por Géneros)[/COLOR]", url="http://estrenosya.net/descarga-0-581210-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR yellow]Películas HD Rip  (Últimas)[/COLOR]" ,  url="http://estrenosya.net/descarga-0-58128-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR yellow]Películas HD Rip  (Por Géneros)[/COLOR]" ,  url="http://estrenosya.net/descarga-0-58128-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR orange]Películas subtituladas  (Últimas)[/COLOR]" ,  url="http://estrenosya.net/descarga-0-58127-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR orange]Películas subtituladas  (Por Géneros)[/COLOR]" ,  url="http://estrenosya.net/descarga-0-58127-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR yellow]Películas V.O.  (Últimas)[/COLOR]" ,  url="http://estrenosya.net/descarga-0-5812255-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR yellow]Películas V.O.  (Por Géneros)[/COLOR]" ,  url="http://estrenosya.net/descarga-0-5812255-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR orange]Series  (Últimos Capítulos)[/COLOR]" ,  url="http://estrenosya.net/descarga-0-58122-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR orange]Series  (Por Nombre de la serie)[/COLOR]" , url="http://estrenosya.net/descarga-0-58122-0-0-fx-1-" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="search" , title="[COLOR lime]Buscar...[/COLOR]",thumbnail= SEARCHIMAGE, fanart=FANARTIMAGE ))

    return itemlist

def categorias(item):
    logger.info("pelisalacarta.channels.EstrenosYa estrenos")
    itemlist=[]
    data = scrapertools.cache_page(item.url + item.extra + "-.fx")
    logger.info("data="+data)
    data = scrapertools.find_single_match(data,'<div class="sublist">(.*?)<div class="item">')
    patron =    '<a href="(.*?)1-.fx.*?>(.*?)<' #  url  cat
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedcat in matches:
        itemlist.append( Item(channel=__channel__, action="estrenos", title="[COLOR lime]"+scrapedcat+"[/COLOR]"  , url=scrapedurl , thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, extra=item.extra, folder=True) )
    return itemlist

def estrenos(item):
    logger.info("pelisalacarta.channels.EstrenosYa estrenos")
    itemlist=[]
    data = scrapertools.cache_page(item.url + item.extra + "-.fx")
    logger.info("data="+data)
    pag_sig=str(int(item.extra)+1)
    patron =    '"MiniFicha".*?a href="(.*?)" .*?img src="(.*?)"' #  url  thumb
    patron += '.*?title=".*?>(.*?)</a>' # titulo
    patron += '.*?OpcionesDescargasMini">(.*?)</div>' # urls
    patron += '.*?display:none;">([^<]+)</div>' # plot
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl, scrapedthumb, scrapedtitle, scrapedurl2,scrapedplot in matches:
        titulo = "[COLOR yellow]" + acentos2(scrapedtitle)+ "[/COLOR]"
        thumb = urlparse.urljoin(BASE_URL,scrapedthumb)
        torrurl = scrapertools.find_single_match(scrapedurl2,'(/descargar-torrent-.*?)"')
        url = urlparse.urljoin(BASE_URL,torrurl)
        itemlist.append( Item(channel=__channel__, action="entraenpeli", title=titulo , fulltitle=titulo, url=url , thumbnail=thumb , plot=acentos(scrapedplot) , fanart=FANARTIMAGE, extra="", folder=True) )
    if ">Siguiente &raquo;</a>" in data: itemlist.append( Item(channel=__channel__, action="estrenos", title="[COLOR magenta]>>> Página Siguiente[/COLOR]" , url=item.url , extra=pag_sig , thumbnail= NEXTPAGEIMAGE , fanart=FANARTIMAGE, folder=True) )
    return itemlist

def entraenpeli(item):
    logger.info("pelisalacarta.channels.EstrenosYa entraenpeli")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    patron =    'div class="fila".*?a href="(.*?)" title="(.*?)"' #  url title
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0 :
        itemlist.append( Item(channel=__channel__, title="[COLOR orange]No hay enlaces torrent para este vídeo...[/COLOR]", thumbnail =item.thumbnail, fanart=item.fanart,folder=False) )
        return itemlist
    for scrapedurl, scrapedtitle in matches:
        title = "[COLOR lime]Ver: [/COLOR]" + "[COLOR yellow]" + scrapedtitle+ "[/COLOR]" + "[COLOR pink] (Torrent)[/COLOR]"
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=item.title, url=scrapedurl , thumbnail=item.thumbnail , plot=item.plot , fanart=item.fanart, folder=False) )
    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.EstrenosYa Play")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    patron =    'Descargar Torrent:.*?a href="(.*?)"' #  url
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl in matches:
        url = urlparse.urljoin(BASE_URL+"/",scrapedurl)
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title , fulltitle=item.title, url=url , thumbnail=item.thumbnail , plot=item.plot , fanart=item.fanart, extra="", folder=False) )
    return itemlist


def search(item,texto):
    logger.info("pelisalacarta.channels.EstrenosYa search")
    if item.url=="":
        texto = texto.replace("+","%20").replace(" ","%20")
        item.url = "http://estrenosya.net/descarga-0-0-0-0-fx-1-1-sch-titulo-"+texto+"-sch.fx"
    item.extra = "0"
    try:
        return lista(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def lista(item):
    #No se maneja paginacion, solo sale una pagina de resultados
    logger.info("pelisalacarta.channels.EstrenosYa lista")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    patron =    '"MiniFicha".*?a href="(.*?)" .*?img src="(.*?)"' #  url  thumb
    patron += '.*?title=".*?>(.*?)</a>' # titulo
    patron += '.*?OpcionesDescargasMini">(.*?)</div>' # urls
    patron += '.*?display:none;">([^<]+)</div>' # plot
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl, scrapedthumb, scrapedtitle, scrapedurl2,scrapedplot in matches:
        titulo = "[COLOR yellow]" + acentos2(scrapedtitle)+ "[/COLOR]"
        thumb = urlparse.urljoin(BASE_URL,scrapedthumb)
        torrurl = scrapertools.find_single_match(scrapedurl2,'(/descargar-torrent-.*?)"')
        url = urlparse.urljoin(BASE_URL,torrurl)
        itemlist.append( Item(channel=__channel__, action="entraenpeli", title=titulo , fulltitle=titulo, url=url , thumbnail=thumb , plot=acentos(scrapedplot) , fanart=FANARTIMAGE, extra="", folder=True) )
    return itemlist

def acentos(texto):
    return texto.replace("&amp;aacute;","á").replace("&amp;iacute;","í").replace("&amp;eacute;","é").replace("&amp;oacute;","ó").replace("&amp;uacute;","ú").replace("&amp;ntilde;","ñ").replace("&amp;Aacute;","Á").replace("&amp;Iacute;","Í").replace("&amp;Eacute;","É").replace("&amp;Oacute;","Ó").replace("&amp;Uacute;","Ú").replace("&amp;Ntilde;","Ñ")

def acentos2(texto):
    return texto.replace("&aacute;","á").replace("&iacute;","í").replace("&eacute;","é").replace("&oacute;","ó").replace("&uacute;","ú").replace("&ntilde;","ñ").replace("&Aacute;","Á").replace("&Iacute;","Í").replace("&Eacute;","É").replace("&Oacute;","Ó").replace("&Uacute;","Ú").replace("&Ntilde;","Ñ").replace("&amp;","&")

# END
