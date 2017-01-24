# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para EstrenosDTL
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# EstrenosDTL   Autor:  ciberus  (06-2015/01-2016)
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
#from servers import servertools

__channel__ = "estrenosdtl"
__category__ = "F,S"
__type__ = "generic"
__title__ = "EstrenosDTL"
__language__ = "ES"

FANARTIMAGE = "http://imgur.com/fUaeSco.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/o08O5Ey.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.EstrenosDTL mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[B][COLOR yellow]Estrenos   (Todas las calidades)[/COLOR][/B]" , url="http://www.estrenosdtl.com/peliculas-screener.html?pagina=" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="search" , title="[B][COLOR yellow]Buscar Estrenos...[/COLOR][/B]",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE ))
    return itemlist

# Begin Peliculas

def estrenos(item):
    logger.info("pelisalacarta.channels.EstrenosDTL estrenos")
    itemlist=[]
    data = scrapertools.cache_page(item.url + item.extra)
    logger.info("data="+data)
    if ">Siguiente<" in data:
        haymas=True
        pag_sig=str(int(item.extra)+1)
    else: haymas=False
    data = scrapertools.find_single_match(data,'body_big_post1(.*?)<div class="body_big_bottom">')
    logger.info("data="+data)
    patron =  'div class=.*?<a href="(.*?)" title="(.*?)">' # dir title
    patron += '.*?Calidad: <b>(.*?)</b>.*?fecha">.*?<p>(.*?)</p>' # fecha
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedtitle , scrapedcalidad , scrapedfecha in matches:
        if config.get_setting('modo_grafico', "estrenosdtl"): fanart,plot,puntuacion = TMDb(StripTags2(scrapedtitle))
        else:
            fanart = FANARTIMAGE
            plot = ""
            puntuacion = ""
        if puntuacion !="": puntuacion = " [COLOR magenta] (" + puntuacion + ")"
        titulo = "[B][COLOR yellow]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/B] [COLOR blue]("+scrapedcalidad + ")" + puntuacion + " [COLOR limegreen]("+scrapedfecha+")[/COLOR]"
        numero = scrapertools.find_single_match(scrapedurl,'-(\d+).')
        thumbnail = "http://www.estrenosdtl.com/imagenes/"+numero+".jpg"
        url= "http://www.estrenosdtl.com/"+scrapedurl
        itemlist.append( Item(channel=__channel__, action="play", title=titulo , fulltitle=titulo, url=url , thumbnail=thumbnail , fanart=fanart, extra="", plot=plot,folder=False) )
    if haymas:
         itemlist.append( Item(channel=__channel__, action="estrenos", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , url=item.url , extra=pag_sig , fanart=FANARTIMAGE, thumbnail=NEXTPAGEIMAGE, folder=True) )
    return itemlist
    
def TMDb(title):
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/movie?api_key=f7f51775877e0bb6703520952b3c7840&query=" + title.replace(" ","%20").replace("'","").replace(":","") + "&language=es&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	try: sinopsis =  scrapertools.get_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	except: sinopsis = ""
	try:  puntuacion = scrapertools.get_match(data,'"page":1,.*?"vote_average":(.*?)}')
	except: puntuacion = ""
	return fanart,sinopsis,puntuacion

def play(item):
    logger.info("pelisalacarta.channels.EstrenosDTL entraenpeli")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    patron = 'XViD: <a href="(.*?)">Descargar TORRENT'  #link
    patron += '.*?cuadro_sinopsis">(.*?)</p>'    #plot
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedlink,scrapedplot in matches:
        plot= (unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")).replace("<br />","")
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=item.title , fulltitle=item.title, url=scrapedlink , thumbnail=item.thumbnail , fanart=os.path.join( config.get_runtime_path(), 'resources' , 'images' ,"estrenosdtlfanart.jpg") , plot=plot , folder=False) )
    return itemlist

# Buscador

def search(item,texto):
    logger.info("pelisalacarta.channels.EstrenosDTL search")
    if item.url=="":
        item.url="http://www.estrenosdtl.com/buscar.php"
    item.extra = urllib.urlencode({'busqueda':texto})
    try:
        return lista(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def lista(item):
    logger.info("pelisalacarta.channels.EstrenosDTL lista")
    itemlist = []
    if item.extra=="":
        data = scrapertools.cachePage(item.url)
    else:
        data = scrapertools.cachePage(item.url , post=item.extra)
    data = scrapertools.find_single_match(data,'Peliculas de estrenos(.*?)fin buscar peliculas')
    logger.info("data="+data)
    patron =  'div class=.*?<a href="(.*?)" title="(.*?)">' # dir title
    patron += '.*?Calidad: <b>(.*?)</b>.*?fecha">.*?<p>(.*?)</p>' # fecha
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedtitle , scrapedcalidad , scrapedfecha in matches:
        titulo = "[COLOR yellow]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/COLOR] [COLOR blue]("+scrapedcalidad+")[/COLOR] [COLOR green]("+scrapedfecha+")[/COLOR]"
        numero = scrapertools.find_single_match(scrapedurl,'-(\d+).')
        thumbnail = "http://www.estrenosdtl.com/imagenes/"+numero+".jpg"
        url= "http://www.estrenosdtl.com/"+scrapedurl
        itemlist.append( Item(channel=__channel__, action="entraenpeli", title=titulo , fulltitle=titulo, url=url , thumbnail=thumbnail , fanart=os.path.join( config.get_runtime_path(), 'resources' , 'images' ,"estrenosdtlfanart.jpg"), extra="", folder=True) )
    return itemlist
    #Solo da una pagina en las busquedas...

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
     return text.strip()

# Fin, este era facilito.
