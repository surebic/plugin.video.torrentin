# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para EstrenosDTL
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# EstrenosDTL   Autor:  ciberus  (06-2015/01-2016)
# Ultima modificación 02-2017
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
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
    itemlist.append( Item(channel=item.channel, action="estrenos" , title="[B][COLOR lime]Estrenos   (Todas las calidades)[/COLOR][/B]" , url="http://www.estrenosdtl.com/peliculas-screener.html?pagina=" , extra="1",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="estrenos" , title="[B][COLOR yellow]Estrenos   (DVD-Screener)[/COLOR][/B]" , url="http://www.estrenosdtl.com/peliculas-screener.html?pagina=" , extra="1",show="&calidad=105",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="estrenos" , title="[B][COLOR yellow]Estrenos   (Telecine)[/COLOR][/B]" , url="http://www.estrenosdtl.com/peliculas-screener.html?pagina=" , extra="1",show="&calidad=106",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="estrenos" , title="[B][COLOR yellow]Estrenos   (TS-Screener)[/COLOR][/B]" , url="http://www.estrenosdtl.com/peliculas-screener.html?pagina=" , extra="1",show="&calidad=107",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="estrenos" , title="[B][COLOR yellow]Estrenos   (VHS-Screener)[/COLOR][/B]" , url="http://www.estrenosdtl.com/peliculas-screener.html?pagina=" , extra="1",show="&calidad=108",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="estrenos" , title="[B][COLOR yellow]Estrenos   (V.O. Subtituladas)[/COLOR][/B]" , url="http://www.estrenosdtl.com/peliculas-screener.html?pagina=" , extra="1",show="&calidad=110",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="search" , title="[B][COLOR magenta]Buscar Estrenos...[/COLOR][/B]",thumbnail= THUMBNAILIMAGE, fanart=FANARTIMAGE ))
    itemlist.append( Item(channel=item.channel, action="configuracion", title="[B][COLOR dodgerblue]Configuración del canal[/COLOR][/B]", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=False))
    return itemlist
    
def configuracion(item):
    from platformcode import platformtools
    ret = platformtools.show_channel_settings()
    platformtools.itemlist_refresh()
    return ret

def estrenos(item):
    logger.info("pelisalacarta.channels.EstrenosDTL estrenos")
    itemlist=[]
    if not item.show=="":
        data = scrapertools.cache_page(item.url + item.extra + item.show)
    else:
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
        if MODO_EXTENDIDO: fanart,plot,puntuacion,votos,fecha,genero = TMDb(StripTags(scrapedtitle))
        else:
            fanart = FANARTIMAGE
            plot = ""
            puntuacion = ""
            votos = ""
            fecha = ""
            genero = ""
        if puntuacion !="": puntuaciontitle = " [COLOR magenta](" + puntuacion + ")"
        else: puntuaciontitle = ""
        contentTitle=StripTags((unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")))
        contentType="movie"
        if not MODO_PLANO: titulo = "[B][COLOR yellow]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/B] [COLOR dodgerblue]("+scrapedcalidad + ")" + puntuaciontitle + " [COLOR limegreen]("+scrapedfecha+")[/COLOR]"
        else: titulo = contentTitle
        numero = scrapertools.find_single_match(scrapedurl,'-(\d+).')
        thumbnail = "http://www.estrenosdtl.com/imagenes/"+numero+".jpg"
        url= "http://www.estrenosdtl.com/"+scrapedurl
        itemlist.append( Item(channel=item.channel, action="play", title=titulo , fulltitle=titulo, contentType=contentType , contentTitle=contentTitle , context=["buscar_trailer"] , url=url , thumbnail=thumbnail , fanart=fanart, extra="", plot=plot,folder=False, infoLabels={"rating":puntuacion,"votes":votos,"year":fecha,"genre":genero }) )
    if haymas:
         itemlist.append( Item(channel=item.channel, action="estrenos", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , url=item.url , extra=pag_sig , fanart=FANARTIMAGE, thumbnail=NEXTPAGEIMAGE, show=item.show , folder=True) )
    return itemlist
    
def TMDb(title):
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/movie?api_key=cc4b67c52acb514bdf4931f7cedfd12b&query=" + title.replace(" ","%20").replace("'","").replace(":","") + "&language=es&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	sinopsis =  scrapertools.find_single_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	puntuacion = scrapertools.find_single_match(data,'"page":1,.*?"vote_average":(.*?)}')
	votos = scrapertools.find_single_match(data,'"page":1,.*?"vote_count":(.*?),')
	fecha = scrapertools.find_single_match(data,'"page":1,.*?"release_date":"(.*?)","').split("-")[0]
	listageneros = scrapertools.find_single_match(data,'"page":1,.*?"genre_ids":\[(.*?)\],"')
	genero = ""
	if listageneros != "":
		listageneros2 = listageneros.split(",")
		for g in listageneros2:
			try: genero += Generos.get(g) + " - "
			except: pass
	return fanart,sinopsis,puntuacion,votos,fecha,genero.strip(" - ")
	
def play(item):
    logger.info("pelisalacarta.channels.EstrenosDTL play")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    patron = 'XViD: <a href="(.*?)">Descargar TORRENT'  #link
    patron += '.*?cuadro_sinopsis">(.*?)</p>'    #plot
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedlink,scrapedplot in matches:
        plot= (unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")).replace("<br />","")
        itemlist.append( Item(channel=item.channel, action="play", server="torrent", title=item.title , fulltitle=item.title, url=scrapedlink , thumbnail=item.thumbnail , fanart=FANARTIMAGE , plot=plot , folder=False) )
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.EstrenosDTL search")
    if item.url=="":
        item.url="http://www.estrenosdtl.com/buscar.php"
    item.extra = urllib.urlencode({'busqueda':texto})
    try:
        return lista(item)
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
        if MODO_EXTENDIDO_B: fanart,plot,puntuacion,votos,fecha,genero = TMDb(StripTags(scrapedtitle))
        else:
            fanart = FANARTIMAGE
            plot = ""
            puntuacion = ""
            votos = ""
            fecha = ""
            genero = ""
        contentTitle=StripTags((unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")))
        contentType="movie"
        if not MODO_PLANO: titulo = "[COLOR yellow]" + (unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")).strip() + "[/COLOR] [COLOR dodgerblue]("+scrapedcalidad+")[/COLOR] [COLOR green]("+scrapedfecha+")[/COLOR]"
        else: titulo = contentTitle
        numero = scrapertools.find_single_match(scrapedurl,'-(\d+).')
        thumbnail = "http://www.estrenosdtl.com/imagenes/"+numero+".jpg"
        url= "http://www.estrenosdtl.com/"+scrapedurl
        itemlist.append( Item(channel=item.channel, action="play", title=titulo , fulltitle=titulo, contentType=contentType , contentTitle=contentTitle , context=["buscar_trailer"] , url=url , thumbnail=thumbnail , fanart=fanart, extra="", plot=plot,folder=False, infoLabels={"rating":puntuacion,"votes":votos,"year":fecha,"genre":genero }) )
    return itemlist
    #Solo da una pagina en las busquedas...

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



# Fin
