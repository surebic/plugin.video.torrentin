# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para divxtotal
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# DivxTotal,  My first channel,   Autor:  ciberus  (06-2015/01-2016)
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
#from servers import servertools

__channel__ = "divxtotal"
__category__ = "F,S"
__type__ = "generic"
__title__ = "DivX Total"
__language__ = "ES"

DEBUG = config.get_setting("debug")
BASE_URL = "http://www.divxtotal.com"
FANARTIMAGE = "http://i.imgur.com/6ETdWOY.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/F6qurea.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.divxtotal mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="menupelis" , title="[COLOR yellow]Películas   (Por Fecha)[/COLOR]" , url="http://www.divxtotal.com/peliculas/" , extra="http://www.divxtotal.com/peliculas/pagina/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="menupelisazgen" , title="[COLOR yellow]Películas   (Por Género)[/COLOR]" , url="http://www.divxtotal.com/peliculas/",extra="gen",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE,  folder=True))
    itemlist.append( Item(channel=__channel__, action="menupelisazgen" , title="[COLOR yellow]Películas   (Por Letra A-Z)[/COLOR]" , url="http://www.divxtotal.com/peliculas/",extra="az", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="menuseries" , title="[COLOR orange]Series   (Últimos capítulos - Por Fecha)[/COLOR]" , url="http://www.divxtotal.com/series/",extra="http://www.divxtotal.com/series/pagina/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="menuseriesaz" , title="[COLOR orange]Series   (Últimos capítulos - Por Letra A-Z)[/COLOR]" , url="http://www.divxtotal.com/series/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="menuserieslistado" , title="[COLOR orange]Series   (Listado completo)[/COLOR]" , url="http://www.divxtotal.com/series/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="search" , title="[COLOR yellow]Buscar Peliculas...[/COLOR]",thumbnail= SEARCHIMAGE,fanart= FANARTIMAGE ))
    itemlist.append( Item(channel=__channel__, action="search" , title="[COLOR orange]Buscar Series...[/COLOR]", plot="series",thumbnail= SEARCHIMAGE,fanart= FANARTIMAGE ))
    return itemlist

# Begin Peliculas

def menupelisazgen(item):
    logger.info("pelisalacarta.channels.divxtotal menupelis AZ y GENERO")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    if item.extra == "gen":
        data = scrapertools.find_single_match(data,'select name="generos"(.*?)</select>')
        logger.info("data="+data)
        patron =  '<option value="(.*?)" ?>([^<]+)<' # dir letra
    elif item.extra == "az":
        data = scrapertools.find_single_match(data,'div class="orden_alfa">(.*?)</div>')
        logger.info("data="+data)
        patron =  '<li><a href="(.*?)">(.*?)</a' # dir letra
    else: return itemlist
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle in matches:
        if scrapedtitle == "Todos": scrapedurl="/"+scrapedurl
        url = BASE_URL + scrapedurl
        if item.extra == "az":
            titulo = "[COLOR yellow]Letra:  [/COLOR][COLOR lime]" + scrapedtitle.upper() + "[/COLOR]"
        elif item.extra == "gen":
            titulo = "[COLOR yellow]Género:  [/COLOR][COLOR lime]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/COLOR]"
        else: titulo = "Titulo"
        extra = url + "pagina/"
        itemlist.append( Item(channel=__channel__, action="menupelis", title=titulo , fulltitle=titulo, url=url , thumbnail="" , plot="" , extra=extra, folder=True) )
    return itemlist

def menupelis(item):
    logger.info("pelisalacarta.channels.divxtotal menupelis")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    current_page = scrapertools.find_single_match(data,'span class="current">(.*?)<')
    if "Siguiente >>" in data: haymas=True
    else: haymas=False
    data = scrapertools.find_single_match(data,'<ul class="section_list">(.*?)</ul>')
    logger.info("data="+data)
    patron =  'seccontnom"><a href="(.*?)" title' # dir
    patron += '.*?>(.*?)</a' # titulo
    patron += '.*?seccontfetam">([^ ]+)</p' # fecha
    patron += '.*?seccontfetam">(.*?)</p' # tamaño
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,scrapedfecha,scrapedtam in matches:
        scrapedfecha=scrapedfecha.replace("\n","")
        titulo = "[COLOR yellow]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/COLOR] [COLOR blue]("+scrapedfecha+")[/COLOR] [COLOR green]("+scrapedtam+")[/COLOR]"
        numero = scrapedurl.split("/")[3]
        thumbnail = "http://www.divxtotal.com/torrents_img/t"+numero+"."+scrapedurl.split("/")[4]+".jpg"
        url= "http://www.divxtotal.com/download.php?id="+numero
        itemlist.append( Item(channel=__channel__, action="entraenpeli", title=titulo , fulltitle=titulo, url=url , thumbnail=thumbnail , plot="" , fanart= FANARTIMAGE, extra=scrapedurl, folder=True) )
    if haymas:
        next_page_url = item.extra + str(int(current_page)+1) + "/"
        itemlist.append( Item(channel=__channel__, action="menupelis", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , url=next_page_url , extra=item.extra , thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist

def entraenpeli(item):
    logger.info("pelisalacarta.channels.divxtotal entraenpeli")
    itemlist=[]
    pagina = BASE_URL+item.extra
    data = scrapertools.cache_page(pagina)
    patron = '"ficha_img".*?src="(.*?)" alt'
    patron += '.*?"fichatxt".*?</script(.*?)</div>'
    #patron += '.*?"fichatxt".*?</h3><br />(.*?)</div>'
    #patron += '.*?"fichatxt".*?</h3><br />(.*?)<[script|/div]'
    plot = scrapertools.find_single_match(data,'(.*?)<')
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedthumb,scrapedplot in matches:
        thumbnail=BASE_URL+scrapedthumb
        title = item.title + " - [COLOR pink](Torrent)[/COLOR]"
        # Añadido por modificacion en la web
        scrapedplotnew =  scrapedplot[1:scrapedplot.rfind("<script")] + scrapedplot[scrapedplot.rfind("</script")+9:scrapedplot.rfind("/div")]

        plot= (unicode( scrapedplotnew, "iso-8859-1" , errors="replace" ).encode("utf-8")).replace("<br />","")
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=title , fulltitle=title, url=item.url , thumbnail=thumbnail , plot=plot , viewmode="movie_with_plot", fanart=item.fanart , folder=False) )
    return itemlist

def information(item):
    import xbmc
    info(item)

def getthumbnail(dir):
    url = BASE_URL+dir
    data = scrapertools.cache_page(url)
    thumb = scrapertools.find_single_match(data,'"ficha_img".*?src="(.*?)" alt')
    return BASE_URL+thumb

# Begin series

def menuserieslistado(item):
    logger.info("pelisalacarta.channels.divxtotal menuseries AZ")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    data = scrapertools.find_single_match(data,'LISTADO DE TODAS LAS SERIES(.*?)BEGIN STANDARD TAG')
    logger.info("data="+data)
    patron =  "<a href='([^']+)' ?title=([^>]+)>" # dir title
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle in matches:
        url = BASE_URL + scrapedurl
        titulo = "[COLOR orange]" + scrapedtitle.capitalize().replace("-"," ") + "[/COLOR]"
        itemlist.append( Item(channel=__channel__, action="entraenserie", title=titulo , fulltitle=titulo, url=url , thumbnail="" , plot="" , folder=True) )
    return itemlist

def menuseriesaz(item):
    logger.info("pelisalacarta.channels.divxtotal menuseries AZ")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    data = scrapertools.find_single_match(data,'Alfabeticamente(.*?)</div>')
    logger.info("data="+data)
    patron =  '<li><a href="(.*?)">(.*?)</a' # dir letra
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle in matches:
        url = BASE_URL + scrapedurl
        titulo = "[COLOR orange]Letra:  [/COLOR][COLOR lime]" + scrapedtitle.upper() + "[/COLOR]"
        extra = url + "pagina/"
        itemlist.append( Item(channel=__channel__, action="menuseries", title=titulo , fulltitle=titulo, url=url , thumbnail="" , extra=extra, plot="" , folder=True) )
    return itemlist

def menuseries(item):
    logger.info("pelisalacarta.channels.divxtotal menu series")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    current_page = scrapertools.find_single_match(data,'span class="current">(.*?)<')
    if "Siguiente >>" in data: haymas=True
    else: haymas=False
    data = scrapertools.find_single_match(data,'letra-0(.*?)LISTADO DE')
    logger.info("data="+data)
    patron =  'secconimagen"><a href="(.*?)" title.*?img src="(.*?)" alt' # dir - thumb
    patron += '.*?seccontnom.*?title=.*?>(.*?)</a.*?seccontfetam">(.*?)</p>' # titulo fecha
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapeddir,scrapedthumb,scrapedtitle,scrapedfecha in matches:
        title = "[COLOR orange]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/COLOR] [COLOR blue]("+scrapedfecha+")[/COLOR]"
        thumbnail = BASE_URL+scrapedthumb
        fanart = FANARTIMAGE
        url= BASE_URL+scrapeddir
        itemlist.append( Item(channel=__channel__, action="entraenserie", title=title , fulltitle = title, url=url , thumbnail=thumbnail , fanart=fanart, plot=
"" , folder=True) )
    if haymas:
        next_page_url = item.extra + str(int(current_page)+1) + "/"
        itemlist.append( Item(channel=__channel__, action="menuseries", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , url=next_page_url , extra=item.extra , thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist

def entraenserie(item):
    logger.info("pelisalacarta.channels.divxtotal listado serie")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    scrapedthumb  = scrapertools.find_single_match(data,'"secciones".*?img src="(.*?)" +alt=') 
    scrapedplot  = scrapertools.find_single_match(data,'<h3>Descripcion</h3> <br /> (.*?)</div>') 
    data = scrapertools.find_single_match(data,'<h3>CAPITULOS(.*?)BEGIN STANDARD TAG')
    logger.info("data="+data)
    patron =  'fichserietabla.*?<a href="(.*?)" title="">(.*?)</a></td>' # link - title
    patron += '.*?capitulofecha">([^ ]+)</td' # fecha
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedtitle , scrapedfecha in matches:
        scrapedfecha=scrapedfecha.replace("\n","")
        title = "[COLOR orange]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/COLOR] [COLOR blue]("+scrapedfecha + ")[/COLOR]"
        numero = scrapertools.find_single_match(item.url,'-(\d+)/')
        thumbnail = "http://www.divxtotal.com/imagenes/series/thumbnails/"+numero+".jpg"
        fanart = BASE_URL+scrapedthumb
        #fanart = "http://www.divxtotal.com/imagenes/series/carteles/"+numero+".jpg" #mejor le sacamos de la pagina en vez de imaginarlo
        url= BASE_URL + scrapedurl
        plot= (unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")).replace("<br />","")
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=title , fulltitle = title, url=url , thumbnail=thumbnail , fanart=fanart, plot=plot , folder=False) )
    return itemlist

# Buscadores (standard solo pelis)

def search(item,texto):
    logger.info("pelisalacarta.channels.divxtotal search")
    if item.url=="":
        item.url="http://www.divxtotal.com/buscar.php?"
    #item.extra = urllib.urlencode({'busqueda':texto})
    item.extra = 'busqueda=' + texto
    try:
        if item.plot=="series": return listaseries(item)
        else: return lista(item)
    # Se captura la excepcion, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def lista(item):
    logger.info("pelisalacarta.channels.divxtotal lista")
    itemlist = []
    data = scrapertools.cachePage(item.url+item.extra)
    logger.info("data="+data)
    current_page = scrapertools.find_single_match(data,'<span class="current">(.*?)</span')
    patron =  'seccontnom">.*?peliculas.gif.*?<a href="(.*?)" title' # dir
    patron += '.*?>(.*?)</a'# tit
    patron += '.*?seccontfetam">(.*?)</p' # fecha
    patron += '.*?seccontfetam">(.*?)</p' # tam
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,scrapedfecha,scrapedtam in matches:
        titulo = "[COLOR yellow]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/COLOR] [COLOR blue]("+scrapedfecha+")[/COLOR] [COLOR green]("+scrapedtam+")[/COLOR]"
        numero = scrapedurl.split("/")[2]
        #thumbnail = "http://www.divxtotal.com/torrents_img/t"+numero+"."+scrapedurl.split("/")[3]+".jpg"
        thumbnail = getthumbnail("/"+scrapedurl)
        url= "http://www.divxtotal.com/download.php?id="+numero
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=titulo , fulltitle=titulo, url=url , thumbnail=thumbnail , plot="" , folder=False) )
    if "Siguiente >>" in data:
        next_page_url2 = item.extra + "&pagina=" + str(int(current_page)+1)
        itemlist.append( Item(channel=__channel__, action="lista", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , url=item.url , extra=next_page_url2  , thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist

def listaseries(item):
    logger.info("pelisalacarta.channels.divxtotal listaseries")
    itemlist = []
    data = scrapertools.cachePage(item.url+item.extra)
    logger.info("data="+data)
    current_page = scrapertools.find_single_match(data,'<span class="current">(.*?)</span')
    patron =  'seccontnom">.*?series.gif.*?<a href="(.*?)" title' # dir
    patron += '.*?>(.*?)</a'# tit
    patron += '.*?seccontfetam">(.*?)</p' # fecha
    patron += '.*?seccontfetam">(.*?)</p' # tam
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapeddir,scrapedtitle,scrapedfecha,scrapedtam in matches:
        titulo = "[COLOR orange]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/COLOR] [COLOR blue]("+scrapedfecha+")[/COLOR] [COLOR green]("+scrapedtam+")[/COLOR]"
        numero = scrapertools.find_single_match(scrapeddir,'-(\d+)/')
        thumbnail = "http://www.divxtotal.com/imagenes/series/thumbnails/"+numero+".jpg"
        #fanart = "http://www.divxtotal.com/imagenes/series/carteles/"+numero+".jpg"
        fanart = FANARTIMAGE
        url= BASE_URL+scrapeddir
        itemlist.append( Item(channel=__channel__, action="entraenserie", title=titulo , fulltitle = titulo, url=url , thumbnail=thumbnail , fanart=fanart, plot=item.plot , folder=True) )
    if "Siguiente >>" in data:
        next_page_url2 = item.extra + "&pagina=" + str(int(current_page)+1)
        itemlist.append( Item(channel=__channel__, action="listaseries", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , url=item.url , extra=next_page_url2  , thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist
