# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Yify torrents (YTS)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# YTS   Autor: ciberus  (06-2015/01-2016)
# He preferido poner los textos en ingles ya que es una web de peliculas en este idioma. para subtitulos usar opensubtitles de Kodi
#Lamentablemente yify (yts.to) cerro por denuncia de la MPAA, adaptado para el nuevo dominio yts.ag (01-2016)
# Arreglado y mejorado (Dec 2016)
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

    itemlist.append( Item(channel=__channel__, action="search" , title="[B][COLOR cyan]Advanced Search[/COLOR][/B]",show="adv",thumbnail= SEARCHIMAGE, fanart=FANARTIMAGE ))
    return itemlist

def estrenos(item):
    logger.info("pelisalacarta.channels.YTS peliculas")
    itemlist=[]
    if item.extra =="1":  data = scrapertools.cache_page(item.url)
    else: data = scrapertools.cache_page(item.url + "?page=" + item.extra)
    #print "CACHEADA: " + item.url + "?page=" + item.extra
    #print data
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
        fanart,sinopsis = TMDb(scrapedtitulo,scrapedfecha)
        if scrapedlinks.count("download") >=1:
            patron2 = '.*?<a href="(.*?)".*?>(.*?)</a>' #urls
            matches2 = re.compile(patron2,re.DOTALL).findall(scrapedlinks)
            scrapertools.printMatches(matches2)
            for scrapedurl, scrapedcalidad in matches2:
                if item.show == "all": pass
                elif scrapedcalidad == item.show: pass
                else: continue
                titulo = "[B][COLOR yellow]" + scrapertools.htmlclean(scrapedtitulo) + "[/COLOR][/B] [COLOR lime]("+scrapedcalidad+")[/COLOR] [COLOR cyan]("+scrapedfecha+")[/COLOR] [COLOR orange]("+scrapedgenero+")[/COLOR] [COLOR magenta]("+scrapedrating+")[/COLOR]"
                itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail=scrapedthumb , fanart=fanart, plot=sinopsis, extra="", folder=False) )
    if ">Next &raquo;</a>" in data: itemlist.append( Item(channel=__channel__, action="estrenos", title="[B][COLOR brown]>>> Next page[/COLOR][/B]" , show=item.show , url=item.url , extra=pag_sig , thumbnail= NEXTPAGEIMAGE , fanart=FANARTIMAGE, folder=True) )
    return itemlist

def TMDb(title,year):
	data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",scrapertools.cachePage("http://api.themoviedb.org/3/search/movie?api_key=f7f51775877e0bb6703520952b3c7840&query=" + title.replace(" ","%20").strip() + "&year=" + year + "&language=en&include_adult=false"))
	try:
		fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except:
		fanart = FANARTIMAGE
	try:
		sinopsis =  scrapertools.get_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	except:
		sinopsis = ""
	try:
		puntuacion = scrapertools.get_match(data,'"page":1,.*?"vote_average":(.*?)}')
	except:
		puntuacion = ""
	return fanart,sinopsis + "\n[B][COLOR purple]TMDb Rating: [COLOR magenta]" + puntuacion + "[/COLOR][/B]"

def search(item,texto):
# https://yts.ag/browse-movies/king/720p/comedy/4/seeds?page=1
# va (12/16) https://yts.ag/browse-movies/sea/all/all/0/latest
    logger.info("pelisalacarta.channels.yts search")
    
    if item.show == "adv":
        return advsearch(item,texto)
    if item.show =="": item.show = "all"
    
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

def advsearch(item,texto):
# https://yts.ag/browse-movies/0/all/all/0/latest
# texto calidad genero puntuacion orden
    logger.info("pelisalacarta.channels.yts advsearch")
    Quality = ["All" , "720p" , "1080p" , "3D"]
    Genre = ["All" , "Action" , "Adventure" , "Animation" , "Biography" , "Comedy" , "Crime" , "Documentary" , "Drama" , "Family" , "Fantasy" , "FilmNoir" , "History" , "Horror" , "Music" , "Musical" , "Mystery" , "News" , "Romance" , "SciFi" , "Short" , "Sport" , "Thriller" , "War" , "Western"]
    Rating = ["0+" , "9+" , "8+" , "7+" , "6+" , "5+" , "4+" , "3+" , "2+" , "1+"]
    OrderBy = ["Latest" , "Oldest" , "Seeds" , "Peers" , "Year" , "Rating" , "Likes" , "Alphabetical" , "Downloads"]

    
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
    item.url="https://yts.ag/browse-movies/"+texto+"/all/"+genreselected+"/"+ratingselected+"/"+orderbyselected
    item.extra = "1"
    try:
        return estrenos(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
