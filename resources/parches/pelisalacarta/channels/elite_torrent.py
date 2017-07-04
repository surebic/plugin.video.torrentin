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
# Añadida informacion de TMDb (25-1-2017)
# Ampliado con numero de votos, eliminado codigo innecesario, etc. (09-02-2017)
# Incluida busqueda en TMDb para series y busquedas (14-02-2017)
#--------------------------------------------------------------
import urlparse,re,time,xbmc
from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = config.get_setting("debug")
BASE_URL = 'http://www.elitetorrent.net'
FANARTIMAGE = "http://i.imgur.com/O2AmwUX.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/2MM3O7z.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"
MODO_EXTENDIDO = config.get_setting('modo_grafico', "elite_torrent")
MODO_EXTENDIDO_B = config.get_setting('modo_grafico_b', "elite_torrent")
MODO_RAPIDO = config.get_setting('modo_rapido', "elite_torrent")
MODO_ENTRA_EN_SERIE = config.get_setting('modo_serie_completa', "elite_torrent")
MODO_PLANO = config.get_setting('only_filmname', "elite_torrent")
Generos = {"28":"Acción","12":"Aventura","16":"Animación","35":"Comedia","80":"Crimen","99":"Documental","18":"Drama","10751":"Familia","14":"Fantasía","36":"Historia","27":"Terror","10402":"Música","9648":"Misterio","10749":"Romance","878":"Ciencia ficción","10770":"película de la televisión","53":"Suspense","10752":"Guerra","37":"Western"}
	
def mainlist(item):
    logger.info("[elitetorrent.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=item.channel, title="[B][COLOR red]www.EliteTorrent.net  ha cerrado la web...[/COLOR][/B]" , action="mainlist", extra="movie",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=item.channel, title="[B][COLOR red]No se pueden sacar enlaces de donde no los hay[/COLOR][/B]" , action="mainlist", extra="movie",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=item.channel, title="[B][COLOR red]Si se vuelve a abrir se actualizará el canal[/COLOR][/B]" , action="mainlist", extra="movie",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    '''
    itemlist.append( Item(channel=item.channel, title="[B][COLOR yellow]Películas[/COLOR][/B]" , action="menu", extra="movie",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=item.channel, title="[B][COLOR orange]Series[/COLOR][/B]" , action="menu", extra="tv",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Documentales y TV[/COLOR][/B]" , action="menu", extra="docu",thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=item.channel, action="search" , title="[B][COLOR yellow]Buscar...[/COLOR][/B]", thumbnail= SEARCHIMAGE, fanart= FANARTIMAGE))
    itemlist.append( Item(channel=item.channel, action="configuracion", title="[B][COLOR dodgerblue]Configuración del canal[/COLOR][/B]", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=False))
    '''
    return itemlist

def menu(item):
    itemlist =[]
    if item.extra =="movie":
        itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Estrenos  (Por fecha)[/COLOR][/B]"       , extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Estrenos  (Por valoración)[/COLOR][/B]"       ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Estrenos  (Por popularidad)[/COLOR][/B]"       ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR yellow]Películas  (Por fecha)[/COLOR][/B]"      ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR yellow]Películas  (Por valoración)[/COLOR][/B]"      ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR yellow]Películas  (Por popularidad)[/COLOR][/B]"      ,extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Peliculas HDRip  (Por fecha)[/COLOR][/B]",extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Peliculas HDRip  (Por valoración)[/COLOR][/B]",extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Peliculas HDRip  (Por popularidad)[/COLOR][/B]",extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR yellow]Peliculas MicroHD  (Por fecha)[/COLOR][/B]",extra=item.extra, action="peliculas", url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR yellow]Peliculas MicroHD  (Por valoración)[/COLOR][/B]", action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR yellow]Peliculas MicroHD  (Por popularidad)[/COLOR][/B]", action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR cyan]Peliculas V.O.S.E.[/COLOR][/B]" , action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/14/peliculas-vose/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    elif item.extra=="docu":
        itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Docus y TV  (Por fecha)[/COLOR][/B]" , action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Docus y TV  (Por valoración)[/COLOR][/B]" , action="peliculas", extra=item.extra, url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR lime]Docus y TV  (Por popularidad)[/COLOR][/B]" , action="peliculas",extra=item.extra, url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    elif item.extra=="tv":
        itemlist.append( Item(channel=item.channel, title="[B][COLOR orange]Series  (Por fecha)[/COLOR][/B]" , action="peliculas",extra=item.extra, show="2",url="http://www.elitetorrent.net/categoria/4/series/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR orange]Series  (Por valoración)[/COLOR][/B]" , action="peliculas",extra=item.extra, show="2", url="http://www.elitetorrent.net/categoria/4/series/modo:mini/orden:valoracion", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR orange]Series  (Por popularidad)[/COLOR][/B]" , action="peliculas", extra=item.extra, show="2", url="http://www.elitetorrent.net/categoria/4/series/modo:mini/orden:popularidad", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
        itemlist.append( Item(channel=item.channel, title="[B][COLOR cyan]Series V.O.S.E.[/COLOR][/B]" , action="peliculas",extra=item.extra, show="2", url="http://www.elitetorrent.net/categoria/16/series-vose/modo:mini", thumbnail= THUMBNAILIMAGE, fanart= FANARTIMAGE))
    return itemlist

def configuracion(item):
    from platformcode import platformtools
    ret = platformtools.show_channel_settings()
    platformtools.itemlist_refresh()
    return ret
    
def peliculas(item):
    logger.info("[elite_torrent.py] peliculas")
    itemlist = []
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.torrentin")'): data = scrapertools.cache_page(item.url)
    else: data =''
    if data.startswith('<meta http-equiv="Refresh"'):
        data = scrapertools.cache_page(item.url)
    patron =  '<a href="(/torrent/[^"]+)">'
    patron += '<img src="(thumb_fichas/[^"]+)" border="0" title="([^"]+)"[^>]+></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    yaesta=False
    buscado=""
    result=0
    estv = re.compile(r'\d{1,2}[x]\d{2}')
    start = time.time()
    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        title = "[B][COLOR yellow]"+scrapedtitle.strip()+"[/COLOR][/B]"
        url = urlparse.urljoin(BASE_URL, scrapedurl)
        if (item.show=="1" or item.show=="3") and MODO_EXTENDIDO_B:
            if estv.search(scrapedtitle): item.extra="tv"
            else: item.extra="movie"
            
        if item.extra=="tv":
            contentSerieName=StripTags(scrapedtitle.split("-")[0].strip())
            contentTitle=contentSerieName
            contentType="tvshow"
            if contentSerieName != buscado:
                buscado = contentSerieName
                yaesta=False
            else: 
                yaesta=True
        else:
            contentTitle=StripTags(scrapedtitle)
            contentType="movie"
            buscado=""
            yaesta=False
            if MODO_PLANO:  title = contentTitle
            
        if (item.extra == "movie" or item.extra == "tv") and MODO_EXTENDIDO and MODO_RAPIDO and not yaesta:
            result = result +1
            if result == 40:
                while time.time()-start < 10:
                    time.sleep(1)
            fanart,thumbnail,sinopsis,puntuacion,votos,year,genero = TMDb(StripTags(scrapedtitle),item.extra)
            if thumbnail == "": thumbnail = urlparse.urljoin(BASE_URL, scrapedthumbnail)
            #if puntuacion !="":
                #sinopsis = sinopsis + "\n[COLOR purple]Puntuación TMDb: [COLOR magenta]" + puntuacion + "[/COLOR]"
        elif not yaesta:
            fanart = FANARTIMAGE
            thumbnail = urlparse.urljoin(BASE_URL, scrapedthumbnail)
            sinopsis = ""
            puntuacion = ""
            votos = ""
            year = "0"
            genero = ""
        if MODO_RAPIDO:
            if item.extra=="tv":
                if item.show=="1" or item.show=="2" and MODO_ENTRA_EN_SERIE:
                    if not yaesta:itemlist.append( Item(channel=item.channel, action="peliculas",contentType=contentType, contentSerieName=contentSerieName  , contentTitle=contentSerieName ,context=["buscar_trailer"] , server="torrent", title="[COLOR cyan][Serie]  [B][COLOR orange]" +scrapedtitle.split("-")[0] +"[/B][COLOR midnightblue] (" +  scrapedtitle.split("-")[1].strip() + ")[/COLOR]" , viewmode="movie_with_plot" , plot =sinopsis, url="http://www.elitetorrent.net/resultados/"+scrapedtitle.split("-")[0].strip().replace(" ","%20")+"/modo:mini" , thumbnail=thumbnail , extra="tv",show="3" ,fanart=fanart, folder=True, infoLabels={"rating":puntuacion,"votes":votos,"year":year,"genre":genero } ) )
                else: itemlist.append( Item(channel=item.channel, action="play",contentType=contentType,  contentSerieName=contentSerieName ,contentTitle=contentSerieName ,context=["buscar_trailer"] , title=title , url=url , thumbnail=thumbnail , folder=True, viewmode="movie_with_plot" , plot =sinopsis, fanart= fanart, show=scrapedtitle, extra=item.extra, infoLabels={"rating":puntuacion,"votes":votos,"year":year,"genre":genero } ) )
            else:
                itemlist.append( Item(channel=item.channel, action="play", title=title ,contentType=contentType , contentTitle=contentTitle, context=["buscar_trailer"] , url=url , thumbnail=thumbnail , folder=True, viewmode="movie_with_plot" , plot =sinopsis, fanart= fanart, show=scrapedtitle, extra=item.extra, infoLabels={"rating":puntuacion,"votes":votos,"year":year,"genre":genero } ) )
        else:
            
            if item.extra=="tv":
                itemlist.append( Item(channel=item.channel, action="preplay", title=title , contentType=contentType  , contentSerieName=contentSerieName ,contentTitle=contentSerieName ,context=["buscar_trailer"] , url=url , thumbnail=thumbnail  , folder=True, viewmode="movie_with_plot" , plot =sinopsis, fanart= fanart, show=scrapedtitle, extra=item.extra, ya=item.ya ) )
            else:
                itemlist.append( Item(channel=item.channel, action="preplay", title=title , contentType=contentType  ,contentTitle=contentTitle , context=["buscar_trailer"] , url=url , thumbnail=thumbnail  , folder=True, viewmode="movie_with_plot" , plot =sinopsis, fanart= fanart, show=scrapedtitle, extra=item.extra, ya=item.ya  ) )

    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">Siguiente \&raquo\;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=item.channel, action="peliculas", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , thumbnail= NEXTPAGEIMAGE , fanart= FANARTIMAGE , show=item.show , url=scrapedurl, extra=item.extra , folder=True) )
    return itemlist

def preplay(item):
    logger.info("[elite_torrent.py] preplay")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    if data.startswith('<meta http-equiv="Refresh"'):
        data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    if (item.extra == "movie" or item.extra == "tv") and MODO_EXTENDIDO:
        fanart,thumbnail,sinopsis,puntuacion,votos,year,genero = TMDb(StripTags(item.show),item.extra)
        if thumbnail =="": thumbnail = item.thumbnail
    else:
        fanart = item.fanart
        thumbnail = item.thumbnail
        sinopsis = ""
        puntuacion = ""
        votos = ""
        year= ""
        genero = ""
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
    #if puntuacion !="":
        #sip = sip + "\n[COLOR purple]Puntuación TMDb: [COLOR magenta]" + puntuacion + "[/COLOR]"
        #plot = plot + "\n[COLOR purple]Puntuación TMDb: [COLOR magenta]" + puntuacion + "[/COLOR]"
    itemlist.append( Item(channel=item.channel, action="play", server="torrent", title=item.title + valoracion + " [COLOR lime][torrent][/COLOR]" , contentTitle=item.contentTitle , contentType=item.contentType , context=item.context , viewmode="movie_with_plot" , url=linkt , thumbnail=thumbnail , plot=sip , fanart=fanart, folder=True , show=item.show , infoLabels={"rating":puntuacion,"votes":votos,"year":year,"genre":genero }) )
    itemlist.append( Item(channel=item.channel, action="play", server="torrent", title=item.title + valoracion + " [COLOR limegreen][magnet][/COLOR]" , contentTitle=item.contentTitle , contentType=item.contentType  , context=item.context , viewmode="movie_with_plot" , url=linkm , thumbnail=thumbnail , plot=plot ,fanart=fanart, folder=True, show=item.show, infoLabels={"rating":puntuacion,"votes":votos,"year":year,"genre":genero }) )
    if item.extra=="tv":
        #info
        if not item.ya=="1": itemlist.append( Item(channel=item.channel, action="peliculas", server="torrent", title="[B][COLOR cyan]Entrar en la serie completa[/COLOR][/B]" , contentType=item.contentType , contentSerieName=item.contentSerieName , contentTitle=item.contentTitle , context=item.context , url="http://www.elitetorrent.net/resultados/"+item.show.split("-")[0].strip().replace(" ","%20")+"/modo:mini" , thumbnail=thumbnail , extra="tv",show="1",ya="1",fanart=fanart, folder=True) )
    return itemlist

def play(item):
    logger.info("[elite_torrent.py] play")
    itemlist = []
    if MODO_RAPIDO:
        data = scrapertools.cache_page(item.url)
        if data.startswith('<meta http-equiv="Refresh"'):
            data = scrapertools.cache_page(item.url)
        linkt = scrapertools.get_match(data,'<a href="(/get-torrent[^"]+)" class="enlace_torrent[^>]+>Descargar el .torrent</a>')
        item.url = urlparse.urljoin(item.url,linkt)
    itemlist.append( Item(channel=item.channel, action="play", server="torrent", title=item.title , url=item.url , thumbnail=item.thumbnail , folder=False) )
    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.elite_torrent search")
    if item.url=="":
        texto = texto.replace("+","%20").replace(" ","%20")
        item.url="http://www.elitetorrent.net/resultados/"+texto+"/modo:mini"
    item.show = "1"
    try:
        return peliculas(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
        
def TMDb(title,tipo):
	if tipo == "tv": title = title.split("-")[0].strip()
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/" + tipo + "?api_key=cc4b67c52acb514bdf4931f7cedfd12b&query=" + title.replace(" ","%20").replace("'","").replace(":","") + "&language=es&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	try: caratula =  "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"poster_path":"\\\(.*?)"')
	except: caratula =""
	sinopsis =  scrapertools.find_single_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	puntuacion = scrapertools.find_single_match(data,'"page":1,.*?"vote_average":(.*?),|}')
	if tipo=="tv": puntuacion = puntuacion.split(",")[0]
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
     