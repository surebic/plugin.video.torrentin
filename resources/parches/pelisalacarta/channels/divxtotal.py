# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para divxtotal
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# DivxTotal,  My first channel,   Autor:  ciberus  (06-2015/01-2016)
# Modificado, arreglado y mejorado 31-12-2016
# Arreglado buscador y añadido Generos en los listados (15-1-2017)
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item

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
MODO_EXTENDIDO = config.get_setting('modo_grafico', "divxtotal")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.divxtotal mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="menupelis" , title="[COLOR yellow][B]Películas   (Por Fecha)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas/" , extra="http://www.divxtotal.com/peliculas/page/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="menupelisazgen" , title="[COLOR yellow][B]Películas   (Por Género)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas/",extra="gen",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE,  folder=True))
    itemlist.append( Item(channel=__channel__, action="menupelisazgen" , title="[COLOR yellow][B]Películas   (Por Letra A-Z)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas/",extra="az", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="menuseries" , title="[COLOR orange][B]Series   (Últimos capítulos - Por Fecha)[/B][/COLOR]" , url="http://www.divxtotal.com/series/",extra="http://www.divxtotal.com/series/page/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="menuseriesaz" , title="[COLOR orange][B]Series   (Últimos capítulos - Por Letra A-Z)[/B][/COLOR]" , url="http://www.divxtotal.com/series/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="menuserieslistado" , title="[COLOR orange][B]Series   (Listado completo)[/B][/COLOR]" , url="http://www.divxtotal.com/series/",plot="[B] ¡¡¡ATENCION!!! Opción muy lenta, tarda bastante en obtener el listado completo de todas las series.[/B]",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="search" , title="[COLOR yellow][B]Buscador (General)...[/B][/COLOR]",plot="[B]Busca en todo...[/B]",thumbnail= SEARCHIMAGE,fanart= FANARTIMAGE ))
    itemlist.append( Item(channel=__channel__, action="search" , title="[COLOR orange][B]Buscador (Sólo Series)...[/B][/COLOR]", plot="[B]Busca solamente las Series TV (Se filtran los resultados para mostrar solo las series, por lo que si aparece [COLOR magenta]>>>Página siguiente[/COLOR] picar ahi porque puede haber mas resultados en las siguientes páginas).[/B]",thumbnail= SEARCHIMAGE,fanart= FANARTIMAGE ))
    itemlist.append( Item(channel=__channel__, action="configuracion", title="[B][COLOR dodgerblue]Configuración del canal[/COLOR][/B]", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=False))
    return itemlist

def configuracion(item):
    from platformcode import platformtools
    platformtools.show_channel_settings()
    if config.is_xbmc():
        import xbmc
        xbmc.executebuiltin("Container.Refresh")

# Begin Peliculas

def menupelisazgen(item):
    logger.info("pelisalacarta.channels.divxtotal menupelis AZ y GENERO")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    if item.extra == "gen":
        data = scrapertools.find_single_match(data,'select name="generos"(.*?)</select>')
        logger.info("data="+data)
        patron = "<option value='(.*?)'>(.*?)<" # dir letra
    elif item.extra == "az":
        data = scrapertools.find_single_match(data,'div class="orden_alfa">(.*?)</div>')
        logger.info("data="+data)
        patron =  '<li><a href="(.*?)">(.*?)</a' # dir letra
    else: return itemlist
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle in matches:
        if item.extra == "az":
            url = urlparse.urljoin(BASE_URL, scrapedurl)
            titulo = "[B][COLOR yellow]Letra:  [/COLOR][COLOR lime]" + scrapedtitle.upper() + "[/COLOR][/B]"
        elif item.extra == "gen":
            if "Espa" in scrapedtitle : scrapedtitle = "Espanolas"
            url= BASE_URL+"/category/" + scrapedtitle
            titulo = "[B][COLOR yellow]Género:  [/COLOR][COLOR lime]" + scrapedtitle + "[/COLOR][/B]"
        else: titulo = "Titulo"
        itemlist.append( Item(channel=__channel__, action="menupelis", title=titulo , fulltitle=titulo, url=url , thumbnail=SEARCHIMAGE , plot="" , folder=True) )
    return itemlist

def menupelis(item):
    logger.info("pelisalacarta.channels.divxtotal menupelis")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    listado = scrapertools.find_single_match(data,'<ul class="section_list">(.*?)</ul>')
    logger.info("data="+data)
    patron =  'seccontnom.*?<a href="(.*?)"' # dir
    patron += '.*?title.*?>(.*?)</a'# tit
    patron += '.*?a href=.*?>(.*?)</a'# gen
    patron += '.*?seccontfetam">(.*?)</p' # fecha
    patron += '.*?seccontfetam">(.*?)</p' # tam
    matches = re.compile(patron,re.DOTALL).findall(listado)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,scrapedgen,scrapedfecha,scrapedtam in matches:
        '''no nos vale, es la fecha en la que pusieron la peli en la web no la del estreno...
        # 
        anyo = scrapedfecha.split("-")[2]
        #if scrapedfecha == "29-10-2016" : scrapedfecha = ""
        #else: scrapedfecha = "[COLOR blue](" + scrapedfecha + ")[/COLOR]"
        '''
        if MODO_EXTENDIDO:
            fanart,thumbnail,plot,puntuacion,fecha = TMDb(scrapedtitle)
        else: 
            fanart = FANARTIMAGE
            thumbnail =THUMBNAILIMAGE
            plot = ""
            puntuacion = ""
            fecha = ""
        if "imgur" in thumbnail and MODO_EXTENDIDO: thumbnail = getthumbnail(scrapedurl)
        if puntuacion != "": puntuaciontitle = " [COLOR deeppink](" + puntuacion + ")[/COLOR]"
        else: puntuaciontitle = ""
        titulo = "[B][COLOR yellow]" + scrapedtitle.strip()+ "[/COLOR][/B] [COLOR cyan]("+scrapedgen+")" + "[/COLOR]" + puntuaciontitle + " [COLOR limegreen]("+scrapedtam+")[/COLOR]"
        itemlist.append( Item(channel=__channel__, action="entraenpeli", title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail=thumbnail , plot=plot , fanart= fanart, extra=scrapedurl, infoLabels={"rating":puntuacion, "genre":scrapedgen, "year":fecha}, folder=True) )
    patronvideos  = "pagination.*?class='current'.*?<a href='(.*?)'.*?</div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=__channel__, action="menupelis", title="[B][COLOR magenta]>>> Página siguiente[/COLOR][/B]" , url=next_page_url , extra=item.extra , thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist

def TMDb(title):
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/movie?api_key=cc4b67c52acb514bdf4931f7cedfd12b&query=" + title.replace(" ","%20") + "&language=es&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	try: caratula =  "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"poster_path":"\\\(.*?)"')
	except: caratula =THUMBNAILIMAGE
	sinopsis =  scrapertools.find_single_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	puntuacion = scrapertools.find_single_match(data,'"page":1,.*?"vote_average":(.*?)}')
	fecha = scrapertools.find_single_match(data,'"page":1,.*?"release_date":"(.*?)","').split("-")[0]
	return fanart,caratula,sinopsis,puntuacion,fecha
	
def entraenpeli(item):
    logger.info("pelisalacarta.channels.divxtotal entraenpeli")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    patron = '"ficha_img".*?src="(.*?)" alt' #Thumb
    patron += '.*?ficha_link_det.*?href="(.*?)"' #link_torrent
    patron += '.*?"fichatxt">(.*?)</div>' #Desc
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedthumb,scrapedurl,scrapedplot in matches:
        title = item.title + " [B][COLOR pink][Torrent][/COLOR][/B]"
        # Añadido por modificacion en la web
        #scrapedplotnew =  scrapedplot[1:scrapedplot.rfind("<script")] + scrapedplot[scrapedplot.rfind("</script")+9:scrapedplot.rfind("/div")]
        plot = re.sub('<[^<]+?>', '', scrapedplot)
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=title , fulltitle=title, url=scrapedurl , thumbnail=scrapedthumb , plot=plot , viewmode="movie_with_plot", fanart=item.fanart , folder=False) )
    return itemlist

def getthumbnail(url):
    data = scrapertools.cache_page(url)
    thumb = scrapertools.find_single_match(data,'"ficha_img".*?src="(.*?)" alt')
    return thumb

# Begin series

def menuserieslistado(item):
    logger.info("pelisalacarta.channels.divxtotal menuseries AZ")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    data = scrapertools.find_single_match(data,'"/series/">Todos(.*?)class="orden_alfa')
    logger.info("data="+data)
    #patron =  "<a href='([^']+)' ?title=([^>]+)>" # dir title
    patron= '<option value="(.*?)">(.*?)<.*?'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle in matches:
        titulo = "[COLOR orange]" + scrapedtitle.capitalize().replace("-"," ") + "[/COLOR]"
        itemlist.append( Item(channel=__channel__, action="entraenserie", title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail="" , plot="" , folder=True) )
    return itemlist

def menuseriesaz(item):
    logger.info("pelisalacarta.channels.divxtotal menuseries AZ")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'Alfabeticamente(.*?)</div>')
    logger.info("data="+data)
    patron =  '<li><a href="(.*?)">(.*?)</a' # dir letra
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle in matches:
        url = BASE_URL + scrapedurl
        titulo = "[B][COLOR orange]Letra:  [/COLOR][COLOR lime]" + scrapedtitle.upper() + "[/COLOR][/B]"
        extra = url + "page/"
        itemlist.append( Item(channel=__channel__, action="menuseries", title=titulo , fulltitle=titulo, url=url , thumbnail="" , extra=extra, plot="" , folder=True) )
    return itemlist

def menuseries(item):
    logger.info("pelisalacarta.channels.divxtotal menu series")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    listado = scrapertools.find_single_match(data,'letra-0(.*?)id="footer"')
    logger.info("data="+data)
    patron =  'secconimagen"><a href="(.*?)" title.*?img src="(.*?)" alt' # dir - thumb
    patron += '.*?seccontnom.*?title=.*?>(.*?)</a.*?seccontfetam">(.*?)</p>' # titulo fecha
    matches = re.compile(patron,re.DOTALL).findall(listado)
    scrapertools.printMatches(matches)
    for scrapeddir,scrapedthumb,scrapedtitle,scrapedfecha in matches:
        title = "[B][COLOR orange]" + scrapedtitle + "[/COLOR][/B] [COLOR blue]("+scrapedfecha+")[/COLOR]"
        itemlist.append( Item(channel=__channel__, action="entraenserie", title=title , fulltitle = title, url=scrapeddir , thumbnail=scrapedthumb , fanart=FANARTIMAGE, plot=
"" , folder=True) )
    patronvideos  = "pagination.*?class='current'.*?<a href='(.*?)'.*?</div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=__channel__, action="menuseries", title="[B][COLOR magenta]>>> Página siguiente[/COLOR][/B]" , url=next_page_url , extra=item.extra , thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist
    
def entraenserie(item):
    logger.info("pelisalacarta.channels.divxtotal listado serie")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    scrapedthumb  = scrapertools.find_single_match(data,'"secciones".*?img src="(.*?)" +alt=') 
    scrapedplot  = scrapertools.find_single_match(data,'Descripcion.*?<p>(.*?)</div>') 
    plot = re.sub('<[^<]+?>', '', scrapedplot)
    data = scrapertools.find_single_match(data,'CAPITULOS(.*?)id="footer"')
    logger.info("data="+data)
    patron =  'fichserietabla.*?<a href="(.*?)" title="">(.*?)</a>' # link - title
    patron += '.*?capitulodescarga.*?<td>(.*?)</td>' # fecha
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedtitle , scrapedfecha in matches:
        scrapedfecha=scrapedfecha.replace("\n","")
        if scrapedfecha != "" : scrapedfecha = " [COLOR blue](" + scrapedfecha + ")[/COLOR]"
        title = "[B][COLOR orange]" + scrapedtitle + "[/COLOR][/B]" +scrapedfecha
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=title , fulltitle = title, url=scrapedurl , thumbnail=item.thumbnail , fanart=scrapedthumb, plot=plot , folder=False) )
    return itemlist

# Buscadores

def search(item,texto):
	#http://www.divxtotal.com/?s=avecina
    logger.info("pelisalacarta.channels.divxtotal search")
    if item.url=="":
        item.url="http://www.divxtotal.com/?s="
        texto = texto.replace("+","%20").replace(" ","%20")
    #item.extra = urllib.urlencode({'busqueda':texto})
    item.extra = texto
    if texto=="": return []
    try:
        if "Series" in item.plot: return listaseries(item)
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
    print item.url+item.extra
    logger.info("data="+data)
    patron =  'seccontnom.*?<a href="(.*?)"' # dir
    patron += '.*?title.*?>(.*?)</a'# tit
    patron += '.*?seccontgen.*?<a href=".*?>(.*?)</a'# genero
    patron += '.*?seccontfetam">(.*?)</p' # fecha
    patron += '.*?seccontfetam">(.*?)</p' # tam
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,scrapedgen,scrapedfecha,scrapedtam in matches:
        if scrapedfecha == "29-10-2016" : scrapedfecha = ""
        else: scrapedfecha = " [COLOR blue](" + scrapedfecha + ")[/COLOR]"
        if scrapedtam == "N/A":
            accion = "entraenserie"
            scrapedtam = "Serie"
        else: accion = "entraenpeli"
        titulo = "[B][COLOR yellow]" + scrapedtitle + "[/COLOR][/B] [COLOR cyan](" + scrapedgen + ")[/COLOR]"+scrapedfecha+" [COLOR limegreen]("+scrapedtam+")[/COLOR]"
        itemlist.append( Item(channel=__channel__, action=accion, title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail="" , plot="" , folder=True) )
    patronvideos  = "pagination.*?class='current'.*?<a href='(.*?)'.*?</div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=__channel__, action="lista", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , url=next_page_url , extra= "", thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist
    
def listaseries(item):
    logger.info("pelisalacarta.channels.divxtotal lista")
    itemlist = []
    data = scrapertools.cachePage(item.url+item.extra)
    logger.info("data="+data)
    patron =  'seccontnom.*?<a href="(.*?)"' # dir
    patron += '.*?title.*?>(.*?)</a'# tit
    patron += '.*?seccontfetam">(.*?)</p' # fecha
    patron += '.*?seccontfetam">(.*?)</p' # tam
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,scrapedfecha,scrapedtam in matches:
        if scrapedtam == "N/A":
            titulo = "[B][COLOR yellow]" + scrapedtitle + "[/COLOR][/B] [COLOR blue]("+scrapedfecha+")[/COLOR]"
            itemlist.append( Item(channel=__channel__, action="entraenserie", title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail="" , plot="" , folder=True) )
    patronvideos  = "pagination.*?class='current'.*?<a href='(.*?)'.*?</div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=__channel__, action="listaseries", title="[COLOR magenta]>>> Página siguiente  [COLOR blue](Puede haber más resultados)[/COLOR]" , url=next_page_url , extra= "", thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist

