# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para elitetorrent
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# modificado por ciberus (06-2015/01-2016), Añadido listado por categorias fecha, valoracion y popularidad, añadido buscador (no tenia), modificado para obtener el torrent en vez del magnet, menus con colores para diferenciar, peliculas, Docus, series, etc. Añadido fanart y thumbnails
# modificado el 12-12-16 
# Arreglado buscador y aviso, arreglado spam repitiendo [quitado aviso 19-12-16]
# Mejorado con descripcion y valoracion de la pelicula (Descipcion completa sale con peli en  torrent y solo la sinopsis con el magnet [26-12-2016].
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
#from servers import servertools

__channel__ = "elitetorrent"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "Elite Torrent"
__language__ = "ES"

DEBUG = config.get_setting("debug")
BASE_URL = 'http://www.elitetorrent.net'

FANARTIMAGE = "http://i.imgur.com/O2AmwUX.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/y1hDx1t.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[elitetorrent.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Películas[/COLOR]" , action="menu", extra="pelis",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=__channel__, title="[COLOR orange]Series[/COLOR]" , action="menu", extra="series",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=__channel__, title="[COLOR lime]Documentales y TV[/COLOR]" , action="menu", extra="tv",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=__channel__, action="search" , title="[COLOR yellow]Buscar...[/COLOR]", thumbnail= SEARCHIMAGE, fanart= FANARTIMAGE))
    return itemlist

def menu(item):
    itemlist =[]

    if item.extra =="pelis":
        itemlist.append( Item(channel=__channel__, title="[COLOR lime]Estrenos  (Por fecha)[/COLOR]"       , action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR lime]Estrenos  (Por valoración)[/COLOR]"       , action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR lime]Estrenos  (Por popularidad)[/COLOR]"       , action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Películas  (Por fecha)[/COLOR]"      , action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Películas  (Por valoración)[/COLOR]"      , action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Películas  (Por popularidad)[/COLOR]"      , action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR lime]Peliculas HDRip  (Por fecha)[/COLOR]", action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR lime]Peliculas HDRip  (Por valoración)[/COLOR]", action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR lime]Peliculas HDRip  (Por popularidad)[/COLOR]", action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Peliculas MicroHD  (Por fecha)[/COLOR]", action="peliculas", url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Peliculas MicroHD  (Por valoración)[/COLOR]", action="peliculas", url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR yellow]Peliculas MicroHD  (Por popularidad)[/COLOR]", action="peliculas", url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR cyan]Peliculas VOSE[/COLOR]" , action="peliculas", url="http://www.elitetorrent.net/categoria/14/peliculas-vose/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

    elif item.extra=="tv":

        itemlist.append( Item(channel=__channel__, title="[COLOR lime]Docus y TV  (Por fecha)[/COLOR]" , action="peliculas", url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR lime]Docus y TV  (Por valoración)[/COLOR]" , action="peliculas", url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR lime]Docus y TV  (Por popularidad)[/COLOR]" , action="peliculas", url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

    elif item.extra=="series":

        itemlist.append( Item(channel=__channel__, title="[COLOR orange]Series  (Por fecha)[/COLOR]" , action="peliculas", url="http://www.elitetorrent.net/categoria/4/series/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR orange]Series  (Por valoración)[/COLOR]" , action="peliculas", url="http://www.elitetorrent.net/categoria/4/series/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR orange]Series  (Por popularidad)[/COLOR]" , action="peliculas", url="http://www.elitetorrent.net/categoria/4/series/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))

        itemlist.append( Item(channel=__channel__, title="[COLOR cyan]Series VOSE[/COLOR]" , action="peliculas", url="http://www.elitetorrent.net/categoria/16/series-vose/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    item.extra =""
    return itemlist

def peliculas(item):
    logger.info("[elitetorrent.py] peliculas")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    #data = scrapertools.cachePage(item.url)  #2º intento (repeticion, evita spam)
    #<meta http-equiv="Refresh" content="0;url=http://www.bajui.com/redi.php?url=/categoria/1/series/modo:mini"/>
    if data.startswith('<meta http-equiv="Refresh"'):
        data = scrapertools.cache_page(item.url)
    patron =  '<a href="(/torrent/[^"]+)">'
    patron += '<img src="(thumb_fichas/[^"]+)" border="0" title="([^"]+)"[^>]+></a>'
    patron += '.*?<span class="descrip">(.*?)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        title = "[COLOR yellow]"+scrapedtitle.strip()+"[/COLOR]"
        url = urlparse.urljoin(BASE_URL, scrapedurl)
        thumbnail = urlparse.urljoin(BASE_URL, scrapedthumbnail)
        plot = re.sub('<[^<]+?>', '', scrapedplot)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="preplay", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True, viewmode="movie_with_plot" , fanart= FANARTIMAGE ) )
    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">Siguiente \&raquo\;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , thumbnail= NEXTPAGEIMAGE , fanart= FANARTIMAGE , url=scrapedurl , folder=True) )

    return itemlist

def preplay(item):
    logger.info("[elitetorrent.py] play")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    #data = scrapertools.cache_page(item.url)  #2º intento (repeticion, evita spam)
    if data.startswith('<meta http-equiv="Refresh"'):
        data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    linkt = scrapertools.get_match(data,'<a href="(/get-torrent[^"]+)" class="enlace_torrent[^>]+>Descargar el .torrent</a>')
    linkm = scrapertools.get_match(data,'<a href="(magnet[^"]+)" class="enlace_torrent[^>]+>Descargar por magnet link</a>')
    linkt = urlparse.urljoin(item.url,linkt)
    linkm = urlparse.urljoin(item.url,linkm)
    patron = 'Detalles.*?="descrip">(.*?)</p>'
    patron +='.*?id="valor_media">(.*?)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedplot,scrapedval in matches:
        #plot = re.sub('<[^<]+?>', '', scrapedplot)
        plot = scrapedplot.replace("<br/>","")
        valoracion = "[COLOR pink] ("+scrapedval + ")[/COLOR]"
    try:
        sip = plot.split("Sinopsis:")[1]
    except:
        try:
            sip = plot.split("Sinopsis")[1]
        except:
            try:
                sip = plot.split("SINOPSIS")[1]
            except:
                sip = plot
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title + valoracion + " [COLOR lime][torrent][/COLOR]" , viewmode="movie_with_plot" , url=linkt , thumbnail=item.thumbnail , plot=sip , fanart=FANARTIMAGE, folder=True) )
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title + valoracion + " [COLOR green][magnet][/COLOR]" , viewmode="movie_with_plot" , url=linkm , thumbnail=item.thumbnail , plot=plot ,fanart=FANARTIMAGE, folder=True) )
    return itemlist

def play(item):
    logger.info("[elitetorrent.py] play")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title , url=item.url , thumbnail=item.thumbnail , folder=False) )
    return itemlist


def search(item,texto):
# http://www.elitetorrent.net/busqueda/en+la/modo:mini #han cambiado a resultados
    logger.info("pelisalacarta.channels.elitetorrent search")
    if item.url=="":
        texto = texto.replace("+","%20").replace(" ","%20")
        item.url="http://www.elitetorrent.net/resultados/"+texto+"/modo:mini"
    item.extra = "1"
    try:
        return peliculas(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

