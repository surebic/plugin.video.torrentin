# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para elitetorrent
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# modificado por ciberus (06-2015/01-2016), Añadido listado por categorias fecha, valoracion y popularidad, añadido buscador (no tenia), modificado para obtener el torrent en vez del magnet, menus con colores para diferenciar, peliculas, Docus, series, etc. Añadido fanart y thumbnails
# modificado el 12-12-16 
# Arreglado buscador y aviso, arreglado spam repitiendo [quitado aviso 19-12-16]
# Mejorado con descripcion y valoracion de la pelicula (Descipcion completa sale con peli en  torrent y solo la sinopsis con el magnet [26-12-2016].
# Cambiado el nombre del canal para no interferir con el original de pelisalacarta (19-1-2017)
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
#from servers import servertools

__channel__ = "elite_torrent"
__category__ = "F,S,D,T"
__type__ = "generic"
__title__ = "EliteTorrent.net"
__language__ = "ES"

DEBUG = config.get_setting("debug")
BASE_URL = 'http://www.elitetorrent.net'

FANARTIMAGE = "http://i.imgur.com/O2AmwUX.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/2MM3O7z.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[elitetorrent.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="[B][COLOR yellow]Películas[/COLOR][/B]" , action="menu", extra="pelis",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=__channel__, title="[B][COLOR orange]Series[/COLOR][/B]" , action="menu", extra="series",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Documentales y TV[/COLOR][/B]" , action="menu", extra="tv",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=__channel__, action="search" , title="[B][COLOR yellow]Buscar...[/COLOR][/B]", thumbnail= SEARCHIMAGE, fanart= FANARTIMAGE))
    return itemlist

def menu(item):
    itemlist =[]

    if item.extra =="pelis":
        itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Estrenos  (Por fecha)[/COLOR][/B]"       , extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Estrenos  (Por valoración)[/COLOR][/B]"       ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Estrenos  (Por popularidad)[/COLOR][/B]"       ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR yellow]Películas  (Por fecha)[/COLOR][/B]"      ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR yellow]Películas  (Por valoración)[/COLOR][/B]"      ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR yellow]Películas  (Por popularidad)[/COLOR][/B]"      ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Peliculas HDRip  (Por fecha)[/COLOR][/B]",extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Peliculas HDRip  (Por valoración)[/COLOR][/B]",extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Peliculas HDRip  (Por popularidad)[/COLOR][/B]",extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR yellow]Peliculas MicroHD  (Por fecha)[/COLOR][/B]",extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR yellow]Peliculas MicroHD  (Por valoración)[/COLOR][/B]", action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR yellow]Peliculas MicroHD  (Por popularidad)[/COLOR][/B]", action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR cyan]Peliculas V.O.S.E.[/COLOR][/B]" , action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/14/peliculas-vose/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    elif item.extra=="tv":
        itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Docus y TV  (Por fecha)[/COLOR][/B]" , action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Docus y TV  (Por valoración)[/COLOR][/B]" , action="peliculas", extra=item.extra, url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR lime]Docus y TV  (Por popularidad)[/COLOR][/B]" , action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    elif item.extra=="series":
        itemlist.append( Item(channel=__channel__, title="[B][COLOR orange]Series  (Por fecha)[/COLOR][/B]" , action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/4/series/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR orange]Series  (Por valoración)[/COLOR][/B]" , action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/4/series/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR orange]Series  (Por popularidad)[/COLOR][/B]" , action="peliculas", extra=item.extra, url="http://www.elitetorrent.net/categoria/4/series/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=__channel__, title="[B][COLOR cyan]Series V.O.S.E.[/COLOR][/B]" , action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/16/series-vose/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
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
    #patron += '.*?<span class="descrip">(.*?)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        title = "[B][COLOR yellow]"+scrapedtitle.strip()+"[/COLOR][/B]"
        url = urlparse.urljoin(BASE_URL, scrapedurl)
        thumbnail = urlparse.urljoin(BASE_URL, scrapedthumbnail)
        #plot = re.sub('<[^<]+?>', '', scrapedplot)
        #if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="preplay", title=title , url=url , thumbnail=thumbnail , folder=True, viewmode="movie_with_plot" , fanart= FANARTIMAGE, show=scrapedtitle, extra=item.extra ) )
    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">Siguiente \&raquo\;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , thumbnail= NEXTPAGEIMAGE , fanart= FANARTIMAGE , url=scrapedurl, extra=item.extra , folder=True) )
    return itemlist

def preplay(item):
    logger.info("[elitetorrent.py] play")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    if data.startswith('<meta http-equiv="Refresh"'):
        data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    if item.extra == "pelis" and config.get_setting('modo_grafico', "elite_torrent"):
    #if config.get_setting('modo_grafico', "elite_torrent"):
        fanart,thumbnail,sinopsis,puntuacion = TMDb(StripTags(item.show))
        if "imgur" in thumbnail: thumbnail = item.thumbnail
    else:
        fanart = item.fanart
        thumbnail = item.thumbnail
        sinopsis = ""
        puntuacion = ""
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
    if "No hay detalles" in plot and sinopsis != "": 
        plot = sinopsis
        sip = sinopsis
    if puntuacion !="":
        sip = sip + "\n[B][COLOR purple]Puntuación TMDb: [COLOR magenta]" + puntuacion + "[/COLOR][/B]"
        plot = plot + "\n[B][COLOR purple]Puntuación TMDb: [COLOR magenta]" + puntuacion + "[/COLOR][/B]"
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title + valoracion + " [COLOR lime][torrent][/COLOR]" , viewmode="movie_with_plot" , url=linkt , thumbnail=thumbnail , plot=sip , fanart=fanart, folder=True) )
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title + valoracion + " [COLOR limegreen][magnet][/COLOR]" , viewmode="movie_with_plot" , url=linkm , thumbnail=thumbnail , plot=plot ,fanart=fanart, folder=True) )
    return itemlist

def play(item):
    logger.info("[elitetorrent.py] play")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title , url=item.url , thumbnail=item.thumbnail , folder=False) )
    return itemlist

'''
    {"page":1,"results":[{"poster_path":"\/qgeWwxhEFbuGNXwta7xMNK2l8xJ.jpg","adult":false,"overview":"Inspirada en los hechos que tuvieron lugar durante un intento por alcanzar el pico más alto del mundo, narra las peripecias de dos expediciones que se enfrentan a la peor tormenta de nieve conocida. En un desesperado esfuerzo por sobrevivir, el temple de los alpinistas se ve puesto a prueba al tener que enfrentarse a la furia desatada de los elementos y a obstáculos casi insuperables.","release_date":"2015-09-10","genre_ids":[12,18],"id":253412,"original_title":"Everest","original_language":"en","title":"Everest","backdrop_path":"\/uoEGDW5hgEjV14XVIaB0ImqSHgx.jpg","popularity":2.672036,"vote_count":1208,"video":false,"vote_average":6.7},{"poster_path":"\/4qpRLxlRzgm8UOQ1n9DxeWycLLY.jpg","adult":false,"overview":"Documental que narra la historia real de un equipo internacional de escaladores que en la primavera de 1996 se propusieron escalar el monte Everest. Su exitosa ascensión al monte, pocos días después de que otros compañeros murieran allí atrapados por una tormenta de nieve cerca de la cumbre, demuestra la fuerza del espíritu humano y el respeto, amor y temor que suscita (y suscitará siempre) la montaña más alta del mundo. El filme describe los largos preparativos para la ascensión, su viaje a la cumbre y su exitoso regreso al Campo Base. También muestra muchos de los retos a los que se enfrentó el grupo, incluyendo avalanchas, falta de oxígeno, traicioneras paredes de hielo y una tormenta mortal.","release_date":"1998-03-06","genre_ids":
'''
def TMDb(title):
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/movie?api_key=f7f51775877e0bb6703520952b3c7840&query=" + title.replace(" ","%20").replace("'","").replace(":","") + "&language=es&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	try: caratula =  "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"poster_path":"\\\(.*?)"')
	except: caratula =THUMBNAILIMAGE
	try: sinopsis =  scrapertools.get_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	except: sinopsis = ""
	try: puntuacion = scrapertools.get_match(data,'"page":1,.*?"vote_average":(.*?)}')
	except: puntuacion = ""
	return fanart,caratula,sinopsis,puntuacion


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
        
def StripTags(text):
     finished = 0
     while not finished:
         finished = 1
         start = text.find("[")
         if start >= 0:
             stop = text[start:].find("]")
             if stop >= 0:
                 text = text[:start] + text[start+stop+1:]
                 finished = 0
     text = StripTags2(text)
     return text.strip()

def StripTags2(text):
     finished = 0
     while not finished:
         finished = 1
         start = text.find("(")
         if start >= 0:
             stop = text[start:].find(")")
             if stop >= 0:
                 text = text[:start] + text[start+stop+1:]
                 finished = 0
     return text


