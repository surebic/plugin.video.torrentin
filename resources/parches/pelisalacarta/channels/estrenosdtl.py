# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para EstrenosDTL
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# EstrenosDTL   Autor:  ciberus  (06-2015/01-2016)
# Ultima modificación 02-2017
# Re-escrito por nueva web (20-7-2017)
#------------------------------------------------------------
import urlparse,urllib2,urllib,re,xbmc
from core import logger
from core import config
from core import scrapertools
from core.item import Item

FANARTIMAGE = "http://imgur.com/fUaeSco.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/o08O5Ey.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"
MODO_EXTENDIDO = config.get_setting('modo_grafico', "estrenosdtl")
MODO_EXTENDIDO_B = config.get_setting('modo_grafico_b', "estrenosdtl")
DEBUG = config.get_setting("debug")
MODO_PLANO = config.get_setting('only_filmname', "estrenosdtl")
Generos = {"28":"Acción","12":"Aventura","16":"Animación","35":"Comedia","80":"Crimen","99":"Documental","18":"Drama","10751":"Familia","14":"Fantasía","36":"Historia","27":"Terror","10402":"Música","9648":"Misterio","10749":"Romance","878":"Ciencia ficción","10770":"película de la televisión","53":"Suspense","10752":"Guerra","37":"Western"}
	
def mainlist(item):
    logger.info("pelisalacarta.channels.EstrenosDTL mainlist")
    itemlist = []
    itemlist.append( Item(channel=item.channel, action="newtop" , title="[B][COLOR lime]Novedades[/COLOR][/B]" , url="http://www.estrenosdtl.com" ,thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="newtop" , title="[B][COLOR lime]Top Descargas[/COLOR][/B]" , url="http://www.estrenosdtl.com", extra='top' ,thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="generos" , title="[B][COLOR yellow]Estrenos por Género[/COLOR][/B]" , url="http://www.estrenosdtl.com" ,thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="calidad" , title="[B][COLOR yellow]Estrenos por Calidad[/COLOR][/B]" , url="http://www.estrenosdtl.com" ,thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="search" , title="[B][COLOR magenta]Buscar Estrenos...[/COLOR][/B]",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE ))
    itemlist.append( Item(channel=item.channel, action="configuracion", title="[B][COLOR dodgerblue]Configuración del canal[/COLOR][/B]", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=False))
    return itemlist
    
def configuracion(item):
    from platformcode import platformtools
    ret = platformtools.show_channel_settings()
    platformtools.itemlist_refresh()
    return ret

def newtop(item):
    logger.info("pelisalacarta.channels.EstrenosDTL estrenos")
    itemlist=[]
    data=scrapertools.cache_page(item.url)
    logger.info("data="+data)
    if not xbmc.getCondVisibility('System.HasAddon("plugin.video.torrentin")'): data = ''
    if item.extra=='top':
        data = scrapertools.find_single_match(data,'cuadro_der(.*?)end of the loop')
    else:
        data = scrapertools.find_single_match(data,'cuadro_izq(.*?)cuadro_der')
    #logger.info("data="+data)
    patron =  'div class="new_item.*?<p>(.*?)</p.*?a href="(.*?)" title="(.*?)"' # FECHA dir title
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedfecha , scrapedurl , scrapedtitle  in matches:
        title,year = limpia(scrapedtitle)
        if MODO_EXTENDIDO: fanart,caratula,plot,puntuacion,votos,fecha,genero = TMDb(title,year)
        else:
            fanart = FANARTIMAGE
            caratula,plot = getthumbandplot(scrapedurl)
            puntuacion = ""
            votos = ""
            fecha = ""
            genero = ""
        if puntuacion !="": puntuaciontitle = " [COLOR magenta](" + puntuacion + ")"
        else: puntuaciontitle = ""
        #contentTitle=StripTags((unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")))
        contentTitle=title
        contentType="movie"
        if not MODO_PLANO: titulo = "[B][COLOR yellow]" + scrapedtitle + "[/B]" + puntuaciontitle + " [COLOR limegreen]("+scrapedfecha+")[/COLOR]"
        else: titulo = contentTitle
        url= scrapedurl
        itemlist.append( Item(channel=item.channel, action="play", title=titulo , fulltitle=titulo, contentType=contentType , contentTitle=contentTitle , context=["buscar_trailer"] , url=url , thumbnail=caratula , fanart=fanart, extra="", plot=plot,folder=False, infoLabels={"rating":puntuacion,"votes":votos,"year":fecha,"genre":genero }) )
    return itemlist
    
def limpia(titulo):
    titul = titulo.replace('HQ-TC','').replace('DVD-S','').replace('Subtitulada','').replace('Sub. Esp.','').replace('Sub. Esp','').strip()
    if re.search( '\(\d{4}\)', titul[-6:]): year=titul[-5:].replace(')','')
    else: year = ""
    return StripTags(titul),year

def getthumbandplot(url):
    data = scrapertools.cache_page(url)
    thumb = scrapertools.find_single_match(data,'contenedor_ficha.*?src="(.*?)"')
    plot = re.sub('<[^<]+?>', '', scrapertools.find_single_match(data,'<p class="cuadro_sinopsis">(.*?)</p>'))
    return thumb,plot

def generos(item):
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    fichas = scrapertools.find_single_match(data,'<h4>Generos</h4>(.*?)f_body_derecho')
    patron = 'a href="(.*?)" >(.*?)<' #url gen
    matches = re.compile(patron,re.DOTALL).findall(fichas)
    for url, gen in matches:
        itemlist.append( Item(channel=item.channel, action="findvideos", title="[B][COLOR cyan]" + gen + "[/COLOR][/B]" , url=url , fanart=FANARTIMAGE, thumbnail=NEXTPAGEIMAGE, folder=True) )
    return itemlist

def calidad(item):
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    fichas = scrapertools.find_single_match(data,'<h4>Calidad</h4>(.*?)Generos')
    patron = 'a href="(.*?)" >(.*?)<' #url gen
    matches = re.compile(patron,re.DOTALL).findall(fichas)
    for url, gen in matches:
        itemlist.append( Item(channel=item.channel, action="findvideos", title="[B][COLOR cyan]" + gen + "[/COLOR][/B]" , url=url , fanart=FANARTIMAGE, thumbnail=NEXTPAGEIMAGE, folder=True) )
    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.EstrenosDTL findvideos")
    itemlist=[]
    data=scrapertools.cache_page(item.url+item.extra)
    logger.info("data="+data)
    if not xbmc.getCondVisibility('System.HasAddon("plugin.video.torrentin")'): data = ''
    if item.extra == '':
        fichas = scrapertools.find_single_match(data,'body_big_post1(.*?)body_big_bottom')
    else:
        fichas = scrapertools.find_single_match(data,'Resultados de buscar:(.*?)fin buscar peliculas')
    patron =  '<a href="(.*?)" title="(.*?)".*?Calidad: <b>(.*?)<.*?fecha.*?<p>(.*?)</p>' # dir title cali fecha
    matches = re.compile(patron,re.DOTALL).findall(fichas)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedtitle , scrapedcalidad , scrapedfecha in matches:
        title,year = limpia(scrapedtitle)
        if (item.extra == '' and MODO_EXTENDIDO) or (item.extra != '' and MODO_EXTENDIDO_B):
            fanart,caratula,plot,puntuacion,votos,fecha,genero = TMDb(title,year)
            if caratula == "": caratula,plot = getthumbandplot(scrapedurl)
        else:
            fanart = FANARTIMAGE
            caratula,plot = getthumbandplot(scrapedurl)
            puntuacion = ""
            votos = ""
            fecha = ""
            genero = ""
        if puntuacion !="": puntuaciontitle = " [COLOR magenta][" + puntuacion + "]"
        else: puntuaciontitle = ""
        contentTitle=title
        contentType="movie"
        if not MODO_PLANO: titulo = "[B][COLOR yellow]" + scrapedtitle + "[/B]" + puntuaciontitle + " [COLOR cyan](" + scrapedcalidad + ") [COLOR limegreen]("+scrapedfecha+")[/COLOR]"
        else: titulo = contentTitle
        url= scrapedurl
        itemlist.append( Item(channel=item.channel, action="play", title=titulo , fulltitle=titulo, contentType=contentType , contentTitle=contentTitle , context=["buscar_trailer"] , url=url , thumbnail=caratula , fanart=fanart, extra="", plot=plot,folder=False, infoLabels={"rating":puntuacion,"votes":votos,"year":fecha,"genre":genero }) )
    patronvideos  = "pagination.*?current.*?<a href='(.*?)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=item.channel, action="findvideos", title="[B][COLOR lime]>>> Página siguiente[/COLOR][/B]" , url=next_page_url , fanart=FANARTIMAGE, thumbnail=NEXTPAGEIMAGE, show=item.show , folder=True) )
    return itemlist
    
def TMDb(title,year):
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/movie?api_key=cc4b67c52acb514bdf4931f7cedfd12b&query=" + title.replace(" ","%20").replace("'","").replace(":","") + "&year=" + year + "&language=es&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	try: caratula =  "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"poster_path":"\\\(.*?)"')
	except: caratula = ""
	sinopsis =  scrapertools.find_single_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	puntuacion = scrapertools.find_single_match(data,'"page":1,.*?"vote_average":(.*?),|}')
	votos = scrapertools.find_single_match(data,'"page":1,.*?"vote_count":(.*?),')
	fecha = scrapertools.find_single_match(data,'"page":1,.*?"release_date":"(.*?)","').split("-")[0]
	listageneros = scrapertools.find_single_match(data,'"page":1,.*?"genre_ids":\[(.*?)\],"')
	genero = ""
	if listageneros != "":
		listageneros2 = listageneros.split(",")
		for g in listageneros2:
			try: genero += Generos.get(g) + " - "
			except: pass
	return fanart,caratula,sinopsis,puntuacion,votos,fecha,genero.strip(" - ")
	
def play(item):
    logger.info("pelisalacarta.channels.EstrenosDTL play")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
#<h2><br><b>Fichero:<a href="http://estrenosdtl.com/wp-content/uploads/2017/06/Mi-Villano-Favorito-3-2017-TS-HQ-estrenosdtl.com_.torrent">Descargar TORRENT</a></b></h2> 
    scrapedlink = scrapertools.find_single_match(data,'Fichero:<a href="(.*?)">Descargar TORRENT')
    itemlist.append( Item(channel=item.channel, action="play", server="torrent", title=item.title , fulltitle=item.title, url=scrapedlink , plot=item.plot ,  thumbnail=item.thumbnail , fanart=FANARTIMAGE , folder=False) )
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.EstrenosDTL search")
    if item.url=="":
        item.url="http://estrenosdtl.com/?s="
        texto = texto.replace(" ","+")
    item.extra = texto
    if texto=="": return []
    try:
        return findvideos(item)
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

# EOF (ciberus 07/17)
