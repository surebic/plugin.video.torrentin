# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para EstrenosYa o estrenosGo (es la misma web) SOLO se extraen los enlaces torrent !!!
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# EstrenosYa   Autor: ciberus  (06-2015/01-2016/01-2017)
#------------------------------------------------------------

import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item

__channel__ = "estrenosya"
BASE_URL = "http://estrenosli.org"
FANARTIMAGE = "http://i.imgur.com/EmmVJPc.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/CPqv4rz.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"
MODO_EXTENDIDO = config.get_setting('modo_grafico', "estrenosya")
DEBUG = config.get_setting("debug")

def mainlist(item):
    logger.info("pelisalacarta.channels.EstrenosYa mainlist")
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR yellow]Cartelera  (Últimas)[/COLOR]", url="http://estrenosli.org/descarga-0-58126-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR yellow]Cartelera  (Por Géneros)[/COLOR]", url="http://estrenosli.org/descarga-0-58126-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR orange]Películas DVD Rip  (Últimas)[/COLOR]", url="http://estrenosli.org/descarga-0-581210-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR orange]Películas DVD Rip  (Por Géneros)[/COLOR]", url="http://estrenosli.org/descarga-0-581210-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR yellow]Películas HD Rip  (Últimas)[/COLOR]" ,  url="http://estrenosli.org/descarga-0-58128-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR yellow]Películas HD Rip  (Por Géneros)[/COLOR]" ,  url="http://estrenosli.org/descarga-0-58128-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR orange]Películas subtituladas  (Últimas)[/COLOR]" ,  url="http://estrenosli.org/descarga-0-58127-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR orange]Películas subtituladas  (Por Géneros)[/COLOR]" ,  url="http://estrenosli.org/descarga-0-58127-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR yellow]Películas V.O.  (Últimas)[/COLOR]" ,  url="http://estrenosli.org/descarga-0-5812255-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR yellow]Películas V.O.  (Por Géneros)[/COLOR]" ,  url="http://estrenosli.org/descarga-0-5812255-0-0-fx-1-" , extra="1",show="movie",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=__channel__, action="estrenos" , title="[COLOR orange]Series  (Últimos Capítulos)[/COLOR]" ,  url="http://estrenosli.org/descarga-0-58122-0-0-fx-1-" , extra="1",show="tv",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="categoriasaz" , title="[COLOR orange]Series  (Últimos Capítulos Por Letra)[/COLOR]" ,  url="http://estrenosli.org/descarga-0-58122-0-0-fx-1-" , extra="1",show="tv",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="categorias" , title="[COLOR orange]Series  (Por Nombre de la Serie)[/COLOR]" , url="http://estrenosli.org/descarga-0-58122-0-0-fx-1-" , extra="1",show="tv",plot="Opcion muy lenta >1.100 Series",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=__channel__, action="search" , title="[COLOR lime]Buscar...[/COLOR]",thumbnail= SEARCHIMAGE, fanart=FANARTIMAGE ))
    itemlist.append( Item(channel=__channel__, action="configuracion", title="[B][COLOR dodgerblue]Configuración del canal[/COLOR][/B]", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=False))
    return itemlist
    
def configuracion(item):
    from platformcode import platformtools
    platformtools.show_channel_settings()
    if config.is_xbmc():
        import xbmc
        xbmc.executebuiltin("Container.Refresh")

def categorias(item):
    logger.info("pelisalacarta.channels.EstrenosYa categorias")
    itemlist=[]
    data = scrapertools.cache_page(item.url + item.extra + "-.fx")
    logger.info("data="+data)
    data = scrapertools.find_single_match(data,'<div class="sublist">(.*?)<div class="item">')
    patron =    '<a href="(.*?)1-.fx.*?>(.*?)<' #  url  cat
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedcat in matches:
        itemlist.append( Item(channel=__channel__, action="estrenos", title="[COLOR lime]"+scrapedcat+"[/COLOR]"  , url=scrapedurl , thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, extra=item.extra, show=item.show, folder=True) )
    return itemlist
    
def categoriasaz(item):
    logger.info("pelisalacarta.channels.EstrenosYa categoriasaz")
    itemlist=[]
    data = scrapertools.cache_page(item.url + item.extra + "-.fx")
    logger.info("data="+data)
    data = scrapertools.find_single_match(data,'Letra: (.*?)</p>')
    patron =    '<a href="(.*?)1-.fx.*?>(.*?)<' #  url  cat
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedcat in matches:
        url = urlparse.urljoin(BASE_URL,scrapedurl)
        itemlist.append( Item(channel=__channel__, action="estrenos", title="[COLOR lime]Letra: "+scrapedcat+"[/COLOR]"  , url=url , thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, extra=item.extra, show=item.show, folder=True) )
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
    completa=False
    for scrapedurl, scrapedthumb, scrapedtitle, scrapedurl2,scrapedplot in matches:
        titulo = "[COLOR yellow]" + acentos2(scrapedtitle)+ "[/COLOR]"
        tituloproc = acentos2(scrapedtitle).replace("LINE","").replace("line","").replace("Line","")
        thumb = urlparse.urljoin(BASE_URL,scrapedthumb)
        torrurl = scrapertools.find_single_match(scrapedurl2,'(/descargar-torrent-.*?)"')
        url = urlparse.urljoin(BASE_URL,torrurl)
        if not completa:
            if (item.show == "movie" or item.show=="tv") and MODO_EXTENDIDO:
                if item.show=="movie":
                    fanart,thumbnail,plot,puntuacion,votos,genero = TMDb(tituloproc.split(" - ")[0].strip(),scrapedtitle.split(" - ")[-1].strip(),item.show)
                elif item.show=="tv":
                    fanart,thumbnail,plot,puntuacion,votos,genero = TMDb(re.sub(r"\d+[x]\d{2}|[-]|\d{4}","",scrapedtitle).strip(),"",item.show)
                if "imgur" in thumbnail: thumbnail = thumb
                if plot == "": plot = acentos(scrapedplot)
                if puntuacion !="":
                    titulo = titulo + " [COLOR magenta](" + puntuacion + ")[/COLOR]"
                if item.seriecompleta=="1": completa=True
            else:
                fanart= FANARTIMAGE
                thumbnail = thumb
                puntuacion = ""
                votos = ""
                plot = acentos(scrapedplot)
                genero = ""
        itemlist.append( Item(channel=__channel__, action="entraenpeli", title= titulo , fulltitle=titulo, url=url , thumbnail=thumbnail , plot=plot , fanart=fanart, extra="",show=item.show, seriecompleta=item.seriecompleta, folder=True , infoLabels={'year': scrapedtitle.split(" - ")[-1].strip() , "rating":puntuacion, "votes":votos, "genre":genero } ) )
    if ">Siguiente &raquo;</a>" in data: itemlist.append( Item(channel=__channel__, action="estrenos", title="[COLOR cyan]>>> Página Siguiente[/COLOR]" , url=item.url , extra=pag_sig ,seriecompleta=item.seriecompleta, show=item.show, thumbnail= NEXTPAGEIMAGE , fanart=FANARTIMAGE, folder=True) )
    return itemlist
    
def TMDb(title,year,tipo):
	Generos = {"28":"Acción","12":"Aventura","16":"Animación","35":"Comedia","80":"Crimen","99":"Documental","18":"Drama","10751":"Familia","14":"Fantasía","36":"Historia","27":"Terror","10402":"Música","9648":"Misterio","10749":"Romance","878":"Ciencia ficción","10770":"película de la televisión","53":"Suspense","10752":"Guerra","37":"Western"}
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/"+tipo+"?api_key=cc4b67c52acb514bdf4931f7cedfd12b&query=" + title.replace(" ","%20").replace("'","").replace(":","").strip() + "&year=" + year + "&language=es&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	try: caratula =  "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"poster_path":"\\\(.*?)"')
	except: caratula =THUMBNAILIMAGE
	sinopsis =  scrapertools.find_single_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	puntuacion = scrapertools.find_single_match(data,'"page":1,.*?"vote_average":(.*?)}')
	if tipo=="tv": puntuacion = puntuacion.split(",")[0]
	votos = scrapertools.find_single_match(data,'"page":1,.*?"vote_count":(.*?),')
	listageneros = scrapertools.find_single_match(data,'"page":1,.*?"genre_ids":\[(.*?)\],"')
	genero = ""
	if listageneros != "":
		listageneros2 = listageneros.split(",")
		for g in listageneros2:
			try: genero += Generos.get(g) + " - "
			except: pass
	return fanart,caratula,sinopsis,puntuacion,votos,genero.strip(" - ")
	
def entraenpeli(item):
    logger.info("pelisalacarta.channels.EstrenosYa entraenpeli")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    patron =    'div class="fila".*?a href="(.*?)" title="(.*?)"' #  url title
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0 :
        itemlist.append( Item(channel=__channel__, title="[COLOR orange]No hay enlaces torrent para este vídeo...[/COLOR]", thumbnail =item.thumbnail, fanart=item.fanart,folder=False, infoLabels=item.infoLabels) )
        return itemlist
    for scrapedurl, scrapedtitle in matches:
        title = "[COLOR yellow]" + scrapedtitle+ "[/COLOR]" + "[COLOR pink] [Torrent][/COLOR]"
        itemlist.append( Item(channel=__channel__, action="play", title=title , fulltitle=title, url=scrapedurl , thumbnail=item.thumbnail , plot=item.plot , fanart=item.fanart, folder=False, infoLabels=item.infoLabels) )
        if item.show=="tv" and not item.seriecompleta == "1":
            patron2 = 'linkMoreMovies.*?a href="(.*?)1-.fx".*? peliculas de (.*?)</a>'
            matches2 = re.compile(patron2,re.DOTALL).findall(data)
            for serie,seriename in matches2:
                serie = serie.replace("descargar-torrent","descarga").replace("-0-0-0-0-","-0-0-")
                itemlist.append( Item(channel=__channel__, action="estrenos", title="[COLOR cyan][Ir a Serie][COLOR orange] "+seriename + "[/COLOR]" , url=serie , extra="1", show=item.show , seriecompleta="1", thumbnail=item.thumbnail  , fanart=item.fanart, folder=True) )
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
        item.url = "http://estrenosli.org/descarga-0-0-0-0-fx-1-1-sch-titulo-"+texto+"-sch.fx"
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
        patron = re.compile(r'\d{1,2}[x]\d{2}')
        if patron.search(scrapedtitle): show="tv"
        else: show="movie"
        titulo = "[COLOR yellow]" + acentos2(scrapedtitle)+ "[/COLOR]"
        thumb = urlparse.urljoin(BASE_URL,scrapedthumb)
        torrurl = scrapertools.find_single_match(scrapedurl2,'(/descargar-torrent-.*?)"')
        url = urlparse.urljoin(BASE_URL,torrurl)
        itemlist.append( Item(channel=__channel__, action="entraenpeli", title=titulo , fulltitle=titulo, url=url , thumbnail=thumb , plot=acentos(scrapedplot) , show=show , fanart=FANARTIMAGE, extra="", folder=True) )
    return itemlist

def acentos(texto):
    return texto.replace("&amp;aacute;","á").replace("&amp;iacute;","í").replace("&amp;eacute;","é").replace("&amp;oacute;","ó").replace("&amp;uacute;","ú").replace("&amp;ntilde;","ñ").replace("&amp;Aacute;","Á").replace("&amp;Iacute;","Í").replace("&amp;Eacute;","É").replace("&amp;Oacute;","Ó").replace("&amp;Uacute;","Ú").replace("&amp;Ntilde;","Ñ")

def acentos2(texto):
    return texto.replace("&aacute;","á").replace("&iacute;","í").replace("&eacute;","é").replace("&oacute;","ó").replace("&uacute;","ú").replace("&ntilde;","ñ").replace("&Aacute;","Á").replace("&Iacute;","Í").replace("&Eacute;","É").replace("&Oacute;","Ó").replace("&Uacute;","Ú").replace("&Ntilde;","Ñ").replace("&amp;","&")

# END
