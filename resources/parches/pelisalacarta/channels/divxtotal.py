# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para divxtotal
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# DivxTotal,  My first channel,   Autor:  ciberus  (06-2015/01-2016)
# Modificado, arreglado y mejorado 31-12-2016
# Arreglado buscador y añadido Generos en los listados (15-1-2017)
# Añadido TMDb para pelisculas desde las busquedas. (09-02-2017)
# Añadido TMDb para las series. (11-02-2017)
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item

__channel__ = "divxtotal"

DEBUG = config.get_setting("debug")
BASE_URL = "http://www.divxtotal.com"
FANARTIMAGE = "http://i.imgur.com/6ETdWOY.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/F6qurea.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"
MODO_EXTENDIDO = config.get_setting('modo_grafico', "divxtotal")

def mainlist(item):
    logger.info("pelisalacarta.channels.divxtotal mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="menupelis" , title="[COLOR yellow][B]Películas   (Por Fecha)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas/" , extra="http://www.divxtotal.com/peliculas/page/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="menupelisazgen" , title="[COLOR yellow][B]Películas   (Por Género)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas/",extra="gen",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE,  folder=True))
    itemlist.append( Item(channel=__channel__, action="menupelisazgen" , title="[COLOR yellow][B]Películas   (Por Letra A-Z)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas/",extra="az", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="menuseries" , title="[COLOR orange][B]Series   (Últimos capítulos - Por Fecha)[/B][/COLOR]" , url="http://www.divxtotal.com/series/",extra="http://www.divxtotal.com/series/page/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="menuseriesaz" , title="[COLOR orange][B]Series   (Últimos capítulos - Por Letra A-Z)[/B][/COLOR]" , url="http://www.divxtotal.com/series/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="menuserieslistado" , title="[COLOR orange][B]Series   (Listado completo)[/B][/COLOR]" , url="http://www.divxtotal.com/series/",plot="[B] ¡¡¡ATENCION!!! Opción muy lenta, tarda bastante en obtener el listado completo de todas las series ( > 1.000 series).[/B]",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="search" , title="[COLOR yellow][B]Buscador (General)...[/B][/COLOR]",plot="[B]Busca en todo... (Peliculas, Series, Musica, Programas, Otros).[/B]",thumbnail= SEARCHIMAGE,fanart= FANARTIMAGE ))
    itemlist.append( Item(channel=__channel__, action="listaseries" , title="[COLOR orange][B]Buscador (Sólo Series)...[/B][/COLOR]", plot="[B]Busca solamente las Series TV (Se filtran los resultados para mostrar solo las series, por lo que si aparece [COLOR magenta]>>>Página siguiente[/COLOR] picar ahi porque puede haber mas resultados en las siguientes páginas).[/B]",thumbnail= SEARCHIMAGE,fanart= FANARTIMAGE ))
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
        if MODO_EXTENDIDO:
            fanart,thumbnail,plot,puntuacion,votos,fecha,genero = TMDb(scrapedtitle,"movie")
        else: 
            fanart = FANARTIMAGE
            thumbnail =THUMBNAILIMAGE
            plot = ""
            puntuacion = ""
            votos=""
            fecha = ""
            genero=""
        if "imgur" in thumbnail and MODO_EXTENDIDO: thumbnail = getthumbnail(scrapedurl)
        if puntuacion != "": puntuaciontitle = " [COLOR deeppink](" + puntuacion + ")[/COLOR]"
        else: puntuaciontitle = ""
        titulo = "[B][COLOR yellow]" + scrapedtitle.strip()+ "[/COLOR][/B] [COLOR cyan]("+scrapedgen+")" + "[/COLOR]" + puntuaciontitle + " [COLOR limegreen]("+scrapedtam+")[/COLOR]"
        itemlist.append( Item(channel=__channel__, action="entraenpeli", title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail=thumbnail , plot=plot , fanart= fanart, extra=scrapedurl, infoLabels={"rating":puntuacion,"votes":votos, "genre":genero, "year":fecha}, folder=True) )
    patronvideos  = "pagination.*?class='current'.*?<a href='(.*?)'.*?</div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=__channel__, action="menupelis", title="[B][COLOR magenta]>>> Página siguiente[/COLOR][/B]" , url=next_page_url , extra=item.extra , thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist

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
        plot = re.sub('<[^<]+?>', '', scrapedplot)
        if not item.show == "" and MODO_EXTENDIDO: #venimos de la busqueda
            fanart,thumbnail,sip,puntuacion,votos,fecha,genero = TMDb(item.show,"movie")
            #plot= sip + "\n\n" + plot
            item.fanart = fanart
            item.infoLabels={"rating":puntuacion,"votes":votos, "genre":genero, "year":fecha}
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=title , fulltitle=title, url=scrapedurl , thumbnail=scrapedthumb , plot=plot , viewmode="movie_with_plot", fanart=item.fanart , infoLabels=item.infoLabels, folder=False) )
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
        title = "[B][COLOR orange]" + scrapedtitle + "[/COLOR][/B] [COLOR dodgerblue]("+scrapedfecha+")[/COLOR]"
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
    if MODO_EXTENDIDO:
        scrapedtituloserie = scrapertools.find_single_match(data,'"secciones".*?title="(.*?)"') 
        fanart,thumbnail,sip,puntuacion,votos,fecha,genero = TMDb(scrapedtituloserie,"tv")
        if not "imgur" in fanart: scrapedthumb = fanart
        if not "imgur" in thumbnail: item.thumbnail = thumbnail
        puntuacion = puntuacion.split(",")[0]
        infoLabels={"rating":puntuacion,"votes":votos, "genre":genero, "year":fecha}
    else: infoLabels={}
    plot = re.sub('<[^<]+?>', '', scrapedplot)
    data = scrapertools.find_single_match(data,'CAPITULOS(.*?)id="footer"')
    logger.info("data="+data)
    patron =  'fichserietabla.*?<a href="(.*?)" title="">(.*?)</a>' # link - title
    patron += '.*?capitulodescarga.*?<td>(.*?)</td>' # fecha
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedtitle , scrapedfecha in matches:
        scrapedfecha=scrapedfecha.replace("\n","")
        if scrapedfecha != "" : scrapedfecha = " [COLOR dodgerblue](" + scrapedfecha + ")[/COLOR]"
        title = "[B][COLOR orange]" + scrapedtitle + "[/COLOR][/B]" +scrapedfecha
        itemlist.append( Item(channel=__channel__, action="play", server="torrent", title=title , fulltitle = title, url=scrapedurl , thumbnail=item.thumbnail , fanart=scrapedthumb, plot=plot , folder=False , infoLabels=infoLabels) )
    return itemlist

# Buscadores

def search(item,texto):
    logger.info("pelisalacarta.channels.divxtotal search")
    if item.url=="":
        item.url="http://www.divxtotal.com/?s="
        texto = texto.replace("+","%20").replace(" ","%20")
    item.extra = texto
    if texto=="": return []
    try:
        return lista(item)
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
    #patron += '.*?seccontgen">(.*?)</p'# genero (la cagaron)
    patron += '.*?seccontfetam">(.*?)</p' # fecha
    patron += '.*?seccontfetam">(.*?)</p' # tam
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,scrapedfecha,scrapedtam in matches:
        if scrapedfecha == "29-10-2016" : scrapedfecha = ""
        else: scrapedfecha = " [COLOR dodgerblue](" + scrapedfecha + ")[/COLOR]"
        if scrapedtam == "N/A":
            accion = "entraenserie"
            scrapedtam = "Serie"
            show = ""
        else:
            accion = "entraenpeli"
            if "peliculas" in scrapedurl:
                show= scrapedtitle
            else: show = ""
        titulo = "[B][COLOR yellow]" + scrapedtitle + "[/COLOR][/B] "+scrapedfecha+" [COLOR limegreen]("+scrapedtam+")[/COLOR]"
        itemlist.append( Item(channel=__channel__, action=accion, title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail="" , plot="" , show=show , folder=True) )
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
    if item.url == "":
        import xbmc
        texto = ""
        keyboard = xbmc.Keyboard(texto)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            texto = keyboard.getText().replace(" ","+")
            item.extra = texto
        else: return itemlist
        item.url="http://www.divxtotal.com/?s="
    
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
            titulo = "[B][COLOR yellow]" + scrapedtitle + "[/COLOR][/B] [COLOR dodgerblue]("+scrapedfecha+")[/COLOR]"
            itemlist.append( Item(channel=__channel__, action="entraenserie", title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail="" , plot="" , folder=True) )
    patronvideos  = "pagination.*?class='current'.*?<a href='(.*?)'.*?</div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=__channel__, action="listaseries", title="[COLOR magenta]>>> Página siguiente  [COLOR dodgerblue](Puede haber más)[/COLOR]" , url=next_page_url , extra= "", thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist

def TMDb(title,tipo):
	Generos = {"28":"Acción","12":"Aventura","16":"Animación","35":"Comedia","80":"Crimen","99":"Documental","18":"Drama","10751":"Familia","14":"Fantasía","36":"Historia","27":"Terror","10402":"Música","9648":"Misterio","10749":"Romance","878":"Ciencia ficción","10770":"película de la televisión","53":"Suspense","10752":"Guerra","37":"Western"}
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/" + tipo + "?api_key=cc4b67c52acb514bdf4931f7cedfd12b&query=" + title.replace(" ","%20") + "&language=es&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	try: caratula =  "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"poster_path":"\\\(.*?)"')
	except: caratula =THUMBNAILIMAGE
	sinopsis =  scrapertools.find_single_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	puntuacion = scrapertools.find_single_match(data,'"page":1,.*?"vote_average":(.*?)}')
	votos = scrapertools.find_single_match(data,'"page":1,.*?"vote_count":(.*?),')
	if tipo == "movie":fecha = scrapertools.find_single_match(data,'"page":1,.*?"release_date":"(.*?)","').split("-")[0]
	else: fecha = scrapertools.find_single_match(data,'"page":1,.*?"first_air_date":"(.*?)","').split("-")[0]
	listageneros = scrapertools.find_single_match(data,'"page":1,.*?"genre_ids":\[(.*?)\],"')
	genero = ""
	if listageneros != "":
		listageneros2 = listageneros.split(",")
		for g in listageneros2:
			try: genero += Generos.get(g) + " - "
			except: pass
	return fanart,caratula,sinopsis,puntuacion,votos,fecha,genero.strip(" - ")

