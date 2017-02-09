# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Yify torrents (YTS)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# YTS Channel - Autor: ciberus  (06-2015/01-2016)
# He preferido poner los textos en ingles ya que es una web de peliculas en este idioma. para subtitulos usar opensubtitles de Kodi
#Lamentablemente yify (yts.to) cerro por denuncia de la MPAA, adaptado para el nuevo dominio yts.ag (01-2016)
# Arreglado y mejorado (Dec 2016)
# Incluida busqueda en TMDb y mejoras (Enero 2017)
# Ajustes en las busquedas para el buscador general (09-02-2017)
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

import xbmcgui

from core import logger
from core import config
from core import scrapertools
from core.item import Item
#from servers import servertools

__channel__ = "yify"
__category__ = "F,S"
__type__ = "generic"
__title__ = "YifiTorrents"
__language__ = "EN"

DEBUG = config.get_setting("debug")
FANARTIMAGE = "http://i.imgur.com/UKFZyfQ.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/9LWPgxZ.png"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"
MODO_EXTENDIDO = config.get_setting('modo_grafico', "yify")
MODO_NATIVO = config.get_setting('english_sinopsis', "yify")
MODO_PLANO = config.get_setting('only_filmname', "yify")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.YTS mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Latest Movies (All Qualities)[/COLOR][/B]",show="all" , url="https://yts.ag/browse-movies" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Latest Movies (720p)[/COLOR][/B]",show="720p" , url="https://yts.ag/browse-movies" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Latest Movies (1080p)[/COLOR][/B]",show="1080p" , url="https://yts.ag/browse-movies" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Latest Movies (3D)[/COLOR][/B]",show="3D" , url="https://yts.ag/browse-movies" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Most Downloaded Movies (720p)[/COLOR][/B]",show="720p" , url="https://yts.ag/browse-movies/0/all/all/0/downloads" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Most Downloaded Movies (1080p)[/COLOR][/B]",show="1080p" , url="https://yts.ag/browse-movies/0/all/all/0/downloads" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Most Downloaded Movies (3D)[/COLOR][/B]" , show="3D", url="https://yts.ag/browse-movies/0/all/all/0/downloads" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Most Rated Movies (720p)[/COLOR][/B]",show="720p" , url="https://yts.ag/browse-movies/0/all/all/0/rating" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Most Rated Movies (1080p)[/COLOR][/B]",show="1080p" , url="https://yts.ag/browse-movies/0/all/all/0/rating" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Most Rated Movies (3D)[/COLOR][/B]" , show="3D", url="https://yts.ag/browse-movies/0/all/all/0/rating" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="search" , title="[B][COLOR lime]Search (720p)[/COLOR][/B]",show="720p",thumbnail= SEARCHIMAGE, fanart=FANARTIMAGE ))
    itemlist.append( Item(channel=__channel__, action="search" , title="[B][COLOR lime]Search (1080p)[/COLOR][/B]",show="1080p",thumbnail= SEARCHIMAGE, fanart=FANARTIMAGE ))
    itemlist.append( Item(channel=__channel__, action="search" , title="[B][COLOR lime]Search (3D)[/COLOR][/B]",show="3D",thumbnail= SEARCHIMAGE, fanart=FANARTIMAGE ))

    itemlist.append( Item(channel=__channel__, action="advsearch" , title="[B][COLOR cyan]Advanced Search[/COLOR][/B]",thumbnail= SEARCHIMAGE, fanart=FANARTIMAGE ))
    
    itemlist.append( Item(channel=__channel__, action="configuracion", title="[B][COLOR dodgerblue]Configure Channel[/COLOR][/B]", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=False))
    return itemlist
    
def configuracion(item):
    from platformcode import platformtools
    platformtools.show_channel_settings()
    if config.is_xbmc():
        import xbmc
        xbmc.executebuiltin("Container.Refresh")

def estrenos(item):
    logger.info("pelisalacarta.channels.YTS peliculas")
    itemlist=[]
    if item.extra =="1":  data = scrapertools.cache_page(item.url)
    else: data = scrapertools.cache_page(item.url + "?page=" + item.extra)
    logger.info("data="+data)
    pag_sig=str(int(item.extra)+1)
    patron =    'browse-movie-wrap.*?src="(.*?)" alt=' #  thumb
    patron += '.*?rating">(.*?)</h4>.*?<h4>(.*?)</h4>' # rating  genero (mod yts.ag)
    patron += '.*?title">([^<]+)<.*?year">([^<]+)<' # titulo año
    patron += '.*?movie-tags">(.*?)</div>' # pelis
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedthumb, scrapedrating, scrapedgenero, scrapedtitulo, scrapedfecha, scrapedlinks, in matches:
        scrapedrating = scrapedrating.replace(" / 10","")
        if MODO_EXTENDIDO:
            fanart,sinopsis,puntuacion,votos,genero = TMDb(scrapedtitulo,scrapedfecha)
        else:
            fanart = FANARTIMAGE
            sinopsis =""
            puntuacion = ""
            votos = ""
            genero  = ""
        if MODO_NATIVO: genero = scrapedgenero
        if scrapedlinks.count("download") >=1:
            patron2 = '.*?<a href="(.*?)".*?>(.*?)</a>' #urls de los torrents
            matches2 = re.compile(patron2,re.DOTALL).findall(scrapedlinks)
            scrapertools.printMatches(matches2)
            for scrapedurl, scrapedcalidad in matches2:
                if item.show == "all": pass
                elif scrapedcalidad == item.show: pass
                else: continue
                if MODO_PLANO: titulo = scrapertools.htmlclean(scrapedtitulo)
                else: titulo = "[B][COLOR yellow]" + scrapertools.htmlclean(scrapedtitulo) + "[/COLOR][/B] [COLOR lime]("+scrapedcalidad+")[/COLOR] [COLOR cyan]("+scrapedfecha+")[/COLOR] [COLOR orange]("+scrapedgenero+")[/COLOR] [COLOR magenta]("+scrapedrating+")[/COLOR]"
                itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail=scrapedthumb , fanart=fanart, plot=sinopsis, infoLabels={"rating":puntuacion,"votes":votos, "year":scrapedfecha,"genre":genero }, extra="", folder=False) )
    if ">Next &raquo;</a>" in data: itemlist.append( Item(channel=__channel__, action="estrenos", title="[B][COLOR brown]>>> Next page[/COLOR][/B]" , show=item.show , url=item.url , extra=pag_sig , thumbnail= NEXTPAGEIMAGE , fanart=FANARTIMAGE, folder=True) )
    return itemlist

def TMDb(title,year):
	if MODO_NATIVO: args = "en"
	else:
		Generos = {"28":"Acción","12":"Aventura","16":"Animación","35":"Comedia","80":"Crimen","99":"Documental","18":"Drama","10751":"Familia","14":"Fantasía","36":"Historia","27":"Terror","10402":"Música","9648":"Misterio","10749":"Romance","878":"Ciencia ficción","10770":"película de la televisión","53":"Suspense","10752":"Guerra","37":"Western"}
		args = "es"
	data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",scrapertools.cachePage("http://api.themoviedb.org/3/search/movie?api_key=cc4b67c52acb514bdf4931f7cedfd12b&query=" + title.replace(" ","%20") + "&year=" + year + "&language=" + args + "&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	try: sinopsis =  scrapertools.get_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	except: sinopsis = "Not found."
	puntuacion = scrapertools.find_single_match(data,'"page":1,.*?"vote_average":(.*?)}')
	votos = scrapertools.find_single_match(data,'"page":1,.*?"vote_count":(.*?),')
	#return fanart,sinopsis + "\n[B][COLOR purple]TMDb Rating: [COLOR magenta]" + puntuacion + "[/COLOR][/B]"
	genero = ""
	if not MODO_NATIVO:
		listageneros = scrapertools.find_single_match(data,'"page":1,.*?"genre_ids":\[(.*?)\],"')
		if listageneros != "":
			listageneros2 = listageneros.split(",")
			for g in listageneros2:
				try: genero += Generos.get(g) + " - "
				except: pass
	return fanart,sinopsis,puntuacion,votos,genero.strip(" - ")

def search(item,texto):
# https://yts.ag/browse-movies/king/720p/comedy/4/seeds?page=1
# va (12/16) https://yts.ag/browse-movies/sea/all/all/0/latest
    logger.info("pelisalacarta.channels.yts search")
    
    if "720p" in item.title: item.show = "720p"
    elif "1080p" in item.title: item.show="1080p"
    elif "3D" in item.title: item.show="3D"
    else: item.show="all"
    
    #if item.show =="": item.show = "all"
    
    #if texto == "": texto = "0"
    if texto == "": return []
    if item.url=="":
        texto = texto.replace("+","%20").replace(" ","%20")
        #item.url="https://yts.ag/browse-movies/"+texto+"/"+item.show+"/all/0/latest"
        item.url="https://yts.ag/browse-movies/"+texto+"/all/all/0/latest"
    item.extra = "1"
    try:
        return estrenos(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def advsearch(item):
# https://yts.ag/browse-movies/0/all/all/0/latest
# texto calidad genero puntuacion orden
    logger.info("pelisalacarta.channels.yts advsearch")
    Quality = ["All" , "720p" , "1080p" , "3D"]
    Genre = ["All" , "Action" , "Adventure" , "Animation" , "Biography" , "Comedy" , "Crime" , "Documentary" , "Drama" , "Family" , "Fantasy" , "FilmNoir" , "History" , "Horror" , "Music" , "Musical" , "Mystery" , "News" , "Romance" , "SciFi" , "Short" , "Sport" , "Thriller" , "War" , "Western"]
    Rating = ["0+" , "9+" , "8+" , "7+" , "6+" , "5+" , "4+" , "3+" , "2+" , "1+"]
    OrderBy = ["Latest" , "Oldest" , "Seeds" , "Peers" , "Year" , "Rating" , "Likes" , "Alphabetical" , "Downloads"]

    import xbmc
    texto = ""
    keyboard = xbmc.Keyboard(texto)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        texto = keyboard.getText()
    else: return []

    selquality = xbmcgui.Dialog().select("Select Quality:  (esc = All)", Quality)
    if selquality != -1:
        qualityselected = Quality[selquality].lower()
    else: qualityselected = "all"
    item.show = qualityselected
    
    selgenre = xbmcgui.Dialog().select("Select Genre:  (esc = All)", Genre)
    if selgenre != -1:
        genreselected = Genre[selgenre].lower()
    else: genreselected = "all"

    selrating = xbmcgui.Dialog().select("Select Min. Rating:  (esc = All)", Rating)
    if selrating != -1:
        ratingselected = Rating[selrating].replace("+","")
    else: ratingselected = "0"

    selorderby = xbmcgui.Dialog().select("Select Order by:  (esc = Latest)", OrderBy)
    if selorderby != -1:
        orderbyselected = OrderBy[selorderby].lower()
    else: orderbyselected = "latest"

    if texto == "": texto= "0"
    texto = texto.replace("+","%20").replace(" ","%20")
    #item.url="https://yts.ag/browse-movies/"+texto+"/"+qualityselected+"/"+genreselected+"/"+ratingselected+"/"+orderbyselected
    # Modificado en Diciembre 2016, ya no admite busquedas por calidades, salen todas y se filtran
    item.url="https://yts.ag/browse-movies/"+texto+"/all/"+genreselected+"/"+ratingselected+"/"+orderbyselected
    item.extra = "1"
    try:
        return estrenos(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
