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
# Corregido por nuevo formato de la web (22-06-2017) se suprime fecha y tamaño en listado pelis y se añade nueva seccion Peliculas HD
#------------------------------------------------------------
import urlparse,urllib2,urllib,re,xbmc

from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = config.get_setting("debug")
BASE_URL = "http://www.divxtotal.com"
FANARTIMAGE = "http://i.imgur.com/6ETdWOY.jpg"
THUMBNAILIMAGE = "http://i.imgur.com/F6qurea.jpg"
SEARCHIMAGE = "http://i.imgur.com/STE2K8O.png"
NEXTPAGEIMAGE = "http://i.imgur.com/lqt8JcD.png"
MODO_EXTENDIDO = config.get_setting('modo_grafico', "divxtotal")
MODO_PLANO = config.get_setting('only_filmname', "divxtotal")
Generos = {"28":"Acción","12":"Aventura","16":"Animación","35":"Comedia","80":"Crimen","99":"Documental","18":"Drama","10751":"Familia","14":"Fantasía","36":"Historia","27":"Terror","10402":"Música","9648":"Misterio","10749":"Romance","878":"Ciencia ficción","10770":"película de la televisión","53":"Suspense","10752":"Guerra","37":"Western"}
	
def mainlist(item):
    logger.info("pelisalacarta.channels.divxtotal mainlist")
    itemlist = []
    itemlist.append( Item(channel=item.channel, action="menupelis" , title="[COLOR yellow][B]Películas   (Por Fecha)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas/" , extra="http://www.divxtotal.com/peliculas/page/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="menupelisazgen" , title="[COLOR yellow][B]Películas   (Por Género)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas/",extra="gen",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE,  folder=True))
    itemlist.append( Item(channel=item.channel, action="menupelisazgen" , title="[COLOR yellow][B]Películas   (Por Letra A-Z)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas/",extra="az", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=item.channel, action="menupelis" , title="[COLOR yellow][B]Películas HD  (Por Fecha)[/B][/COLOR]" , url="http://www.divxtotal.com/peliculas-hd/" , extra="http://www.divxtotal.com/peliculas-hd/page/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=item.channel, action="menuseries" , title="[COLOR orange][B]Series   (Últimos capítulos - Por Fecha)[/B][/COLOR]" , url="http://www.divxtotal.com/series/",extra="http://www.divxtotal.com/series/page/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="menuseriesaz" , title="[COLOR orange][B]Series   (Últimos capítulos - Por Letra A-Z)[/B][/COLOR]" , url="http://www.divxtotal.com/series/",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))
    itemlist.append( Item(channel=item.channel, action="menuserieslistado" , title="[COLOR orange][B]Series   (Listado completo)[/B][/COLOR]" , url="http://www.divxtotal.com/series/",plot="[B] ¡¡¡ATENCION!!! Opción muy lenta, tarda bastante en obtener el listado completo de todas las series ( > 1.000 series).[/B]",thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=True))

    itemlist.append( Item(channel=item.channel, action="search" , title="[COLOR yellow][B]Buscador...[/B][/COLOR]",plot="[B]Busca en todo... (Peliculas, Series, Musica, Programas, Otros).[/B]",thumbnail= SEARCHIMAGE,fanart= FANARTIMAGE ))
    #itemlist.append( Item(channel=item.channel, action="listaseries" , title="[COLOR orange][B]Buscador (Sólo Series)...[/B][/COLOR]", plot="[B]Busca solamente las Series TV (Se filtran los resultados para mostrar solo las series, por lo que si aparece [COLOR magenta]>>>Página siguiente[/COLOR] picar ahi porque puede haber mas resultados en las siguientes páginas).[/B]",thumbnail= SEARCHIMAGE,fanart= FANARTIMAGE ))
    itemlist.append( Item(channel=item.channel, action="configuracion", title="[B][COLOR dodgerblue]Configuración del canal[/COLOR][/B]", thumbnail= THUMBNAILIMAGE,fanart= FANARTIMAGE, folder=False))
    return itemlist

def configuracion(item):
    from platformcode import platformtools
    ret = platformtools.show_channel_settings()
    platformtools.itemlist_refresh()
    return ret

# Begin Peliculas

def menupelisazgen(item):
    logger.info("pelisalacarta.channels.divxtotal menupelisazgen")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    if item.extra == "gen":
        data = scrapertools.find_single_match(data,'select name="generos"(.*?)</select>')
        logger.info("data="+data)
        patron = "value='(.*?)'>(.*?)<" # dir gen
    elif item.extra == "az":
        data = scrapertools.find_single_match(data,'<div class="row orden_alfa"(.*?)</div>')
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
            #if "Espa" in scrapedtitle : scrapedtitle = "Espanolas"
            url= BASE_URL+"/category/" + scrapedtitle
            url=scrapedurl
            titulo = "[B][COLOR yellow]Género:  [/COLOR][COLOR lime]" + scrapedtitle + "[/COLOR][/B]"
        else: titulo = "Titulo"
        itemlist.append( Item(channel=item.channel, action="menupelis", title=titulo , fulltitle=titulo, url=url , thumbnail=SEARCHIMAGE , plot="" , folder=True) )
    return itemlist

def menupelis(item):
    logger.info("pelisalacarta.channels.divxtotal menupelis")
    itemlist=[]
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.torrentin")'): data = scrapertools.cache_page(item.url)
    else: data =''
    logger.info("##### data="+data)
    listado = scrapertools.find_single_match(data,'<tbody>(.*?)</tbody>')
    logger.info("##### Listado="+listado)
    patron =  '<a href="(.*?)"' # dir
    patron += '.*?title.*?>(.*?)</a'# tit
    #patron += '.*?<a href=.*?>(.*?)</a>'# gen
    patron += '.*?<td>(.*?)</td>'# gen
    matches = re.compile(patron,re.DOTALL).findall(listado)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,scrapedgen in matches:
        if not "N/A" in scrapedgen: scrapedgen = scrapertools.find_single_match(scrapedgen,'">(.*?)</a')
        else: scrapedgen = "No definido"
        year=''
        scrapedtitlesearch = scrapedtitle
        if 'peliculas-hd' in item.url: scrapedtitlesearch = re.sub(' (HD)| HD| mp4| Castellano','',scrapedtitlesearch)
        try:
            if re.search( '\d{4}', scrapedtitlesearch[-4:]):
                year=scrapedtitlesearch[-4:]
                scrapedtitlesearch = scrapedtitlesearch[:-4]
            elif re.search( '\(\d{4}\)', scrapedtitlesearch[-6:]):
                year=scrapedtitlesearch[-5:].replace(')','')
                scrapedtitlesearch = scrapedtitlesearch[:-6]
        except:
            pass
        if MODO_EXTENDIDO:
            fanart,thumbnail,plot,puntuacion,votos,fecha,genero = TMDb(scrapedtitlesearch,"movie",year)
        else: 
            fanart = FANARTIMAGE
            thumbnail =THUMBNAILIMAGE
            plot = ""
            puntuacion = ""
            votos=""
            fecha = ""
            genero=""
        if "imgur" in thumbnail and MODO_EXTENDIDO: thumbnail = getthumbnail(scrapedurl)
        if not MODO_PLANO:
            if puntuacion != "": puntuaciontitle = " [COLOR deeppink](" + puntuacion + ")[/COLOR]"
            else: puntuaciontitle = ""
            titulo = "[B][COLOR yellow]" + scrapedtitle.strip()+ "[/COLOR][/B] [COLOR cyan]("+scrapedgen+")" + "[/COLOR]" + puntuaciontitle
        else: titulo = scrapedtitle.strip()
        itemlist.append( Item(channel=item.channel, action="entraenpeli", title=titulo , fulltitle=titulo, contentType="movie" , contentTitle=scrapedtitle.strip() , context=["buscar_trailer"] , url=scrapedurl , thumbnail=thumbnail , plot=plot , fanart= fanart, extra=scrapedurl, infoLabels={"rating":puntuacion,"votes":votos, "genre":genero, "year":fecha}, folder=True) )
    patronvideos  = "pagination.*?current.*?<a href='(.*?)'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=item.channel, action="menupelis", title="[B][COLOR magenta]>>> Página siguiente[/COLOR][/B]" , url=next_page_url , extra=item.extra , thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist

def entraenpeli(item):
    logger.info("pelisalacarta.channels.divxtotal entraenpeli")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    patron = 'HOTWordsTxt.*?src="(.*?)" alt' #Thumb
    patron += '.*?Fecha.*?href="(.*?)"' #link_torrent
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedthumb,scrapedurl in matches:
        if not MODO_PLANO: title = item.title + " [COLOR navajowhite][Torrent][/COLOR]"
        else: title = item.title
        #plot = re.sub('<[^<]+?>', '', scrapedplot)
        if not item.show == "" and MODO_EXTENDIDO: #venimos de la busqueda
            fanart,thumbnail,sip,puntuacion,votos,fecha,genero = TMDb(item.show,"movie")
            item.contentTitle=item.show
            item.fanart = fanart
            item.infoLabels={"rating":puntuacion,"votes":votos, "genre":genero, "year":fecha, "plot":sip}
        itemlist.append( Item(channel=item.channel, action="play", server="torrent", title=title , fulltitle=title, contentTitle=item.contentTitle , context=item.context , contentType="movie" , url=scrapedurl , thumbnail=scrapedthumb , plot=item.plot , viewmode="movie_with_plot", fanart=item.fanart , infoLabels=item.infoLabels, folder=False) )
    return itemlist

def getthumbnail(url):
    data = scrapertools.cache_page(url)
    thumb = scrapertools.find_single_match(data,'"HOTWordsTxt".*?src="(.*?)" alt')
    return thumb

# Begin series

def menuserieslistado(item):
    logger.info("pelisalacarta.channels.divxtotal menuserieslistado")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    data = scrapertools.find_single_match(data,'/series/">Todos(.*?)class="row orden_alfa')
    logger.info("###########data="+data)
    #patron =  "<a href='([^']+)' ?title=([^>]+)>" # dir title
    patron= 'value="(.*?)">(.*?)<.*?'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle in matches:
        titulo = "[COLOR orange]" + scrapedtitle.capitalize().replace("-"," ") + "[/COLOR]"
        itemlist.append( Item(channel=item.channel, action="entraenserie", title=titulo , fulltitle=titulo, contentSerieName=scrapedtitle, contenType="tvshow" , context=["buscar_trailer"] , url=scrapedurl , thumbnail="" , plot="" , folder=True) )
    return itemlist

def menuseriesaz(item):
    logger.info("pelisalacarta.channels.divxtotal menuseriesaz")
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
        itemlist.append( Item(channel=item.channel, action="menuseries", title=titulo , fulltitle=titulo, url=url , thumbnail="" , extra=extra, plot="" , folder=True) )
    return itemlist

def menuseries(item):
    logger.info("pelisalacarta.channels.divxtotal menuseries")
    itemlist=[]
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.torrentin")'): data = scrapertools.cache_page(item.url)
    else: data =''
    logger.info("data="+data)
    listado = scrapertools.find_single_match(data,'letra-0(.*?)id="footer"')
    logger.info("data="+listado)
    patron =  'secconimagen"><a href="(.*?)" title.*?img src="(.*?)" alt' # dir - thumb
    patron += '.*?seccontnom.*?title=.*?>(.*?)</a.*?seccontfetam">(.*?)</p>' # titulo fecha
    matches = re.compile(patron,re.DOTALL).findall(listado)
    scrapertools.printMatches(matches)
    for scrapeddir,scrapedthumb,scrapedtitle,scrapedfecha in matches:
        title = "[B][COLOR orange]" + scrapedtitle + "[/COLOR][/B] [COLOR dodgerblue]("+scrapedfecha+")[/COLOR]"
        contentSerieName=re.sub(r"\d{1,2}[x]\d{2}|[-]","",scrapedtitle).strip()
        itemlist.append( Item(channel=item.channel, action="entraenserie",contentSerieName=contentSerieName, contentType="tvshow",contentTitle=contentSerieName , context=["buscar_trailer"],title=title , fulltitle = title, url=scrapeddir , thumbnail=scrapedthumb , fanart=FANARTIMAGE, plot=
"" , folder=True) )
    patronvideos  = "pagination.*?current.*?<a href='(.*?)'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=item.channel, action="menuseries", title="[B][COLOR magenta]>>> Página siguiente[/COLOR][/B]" , url=next_page_url , extra=item.extra , thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist
    
def entraenserie(item):
    logger.info("pelisalacarta.channels.divxtotal entraenserie")
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    scrapedthumb  = scrapertools.find_single_match(data,'"panel panel-default peliculas-bloque bloque-home".*?img.*?src="(.*?)"') 
    scrapedplot  = scrapertools.find_single_match(data,'Descripcion.*?<p>(.*?)</div>') 
    scrapedtituloserie = scrapertools.find_single_match(data,'"panel panel-default peliculas-bloque bloque-home".*?title="(.*?)"') 
    if MODO_EXTENDIDO:
        #scrapedtituloserie = scrapertools.find_single_match(data,'"secciones".*?title="(.*?)"') 
        fanart,thumbnail,sip,puntuacion,votos,fecha,genero = TMDb(scrapedtituloserie,"tv")
        if not "imgur" in fanart: scrapedthumb = fanart
        if not "imgur" in thumbnail: item.thumbnail = thumbnail
        puntuacion = puntuacion.split(",")[0]
        infoLabels={"rating":puntuacion,"votes":votos, "genre":genero, "year":fecha, "plot":sip}
    else: infoLabels={}
    plot = re.sub('<[^<]+?>', '', scrapedplot)
    #plot=sip
    data = scrapertools.find_single_match(data,'CAPITULOS DE LA SERIE(.*?)RECOMMENDED CONFIGURATION VARIABLES')
    logger.info("data="+data)
    patron =  'img src=.*?<a href="(.*?)" title="">(.*?)</a>' # link - title
    patron += '.*?</a>.*?<td>(.*?)</td>' # fecha
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl , scrapedtitle , scrapedfecha in matches:
        scrapedfecha=scrapedfecha.replace("\n","")
        if scrapedfecha != "" : scrapedfecha = " [COLOR dodgerblue](" + scrapedfecha + ")[/COLOR]"
        title = "[B][COLOR orange]" + scrapedtitle + "[/COLOR][/B]" +scrapedfecha
        itemlist.append( Item(channel=item.channel, action="play", server="torrent", title=title , fulltitle = title, contentSerieName=scrapedtituloserie , contentTitle=scrapedtituloserie , context=item.context , contentType="tvshow" , url=scrapedurl , thumbnail=item.thumbnail , fanart=scrapedthumb , plot=plot , folder=False , infoLabels=infoLabels) )
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
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.torrentin")'): data = scrapertools.cache_page(item.url+item.extra)
    else: data =''
    logger.info("data="+data)
    
    listado = scrapertools.find_single_match(data,'<tbody>(.*?)</tbody>')
    logger.info("##### Listado="+listado)

    patron =  '<tr>.*?<a href="(.*?)"' # dir
    patron += '.*?title.*?>(.*?)</a'# tit
    patron += '.*?<td class="text-left">(.*?)</td'#  gen/tam
    patron += '.*?<td class="text-left">(.*?)</td' # fecha

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,scrapedtam,scrapedfecha in matches:
        #if scrapedfecha == "29-10-2016" : scrapedfecha = ""
        #else: scrapedfecha = " [COLOR dodgerblue](" + scrapedfecha + ")[/COLOR]"
        scrapedfecha = " [COLOR dodgerblue](" + scrapedfecha + ")[/COLOR]"
        if "N/A" in scrapedtam:
            if "/programas/" in scrapedurl:
                accion = "entraenpeli"
                scrapedtam = "Programa"
                show=""
                contentType=""
            elif "/otros/" in scrapedurl:
                accion = "entraenpeli"
                scrapedtam = "Otros"
                show=""
                contentType=""
            elif "/series/" in scrapedurl:
                accion = "entraenserie"
                scrapedtam = "Serie"
                show = scrapedtitle
                contentType="tvshow"
        else:
            accion = "entraenpeli"
            if "/peliculas/" in scrapedurl:
                scrapedtam = scrapertools.find_single_match(scrapedtam,'">(.*?)</a>') 
                show= scrapedtitle
                contentType="movie"
            else:
                show = ""
                contentType="movie"
        titulo = "[B][COLOR yellow]" + scrapedtitle + "[/COLOR][/B] "+scrapedfecha+" [COLOR limegreen]("+scrapedtam+")[/COLOR]"
        itemlist.append( Item(channel=item.channel, action=accion, title=titulo , fulltitle=titulo, contentType=contentType , contentSerieName=show , contentTitle=show , context=["buscar_trailer"] , url=scrapedurl , thumbnail="" , plot="" , show=show , folder=True) )
    patronvideos  = "pagination.*?current.*?<a href='(.*?)'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=item.channel, action="lista", title="[COLOR magenta]>>> Página siguiente[/COLOR]" , url=next_page_url , extra= "", thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist
    
def listaseries(item):
    logger.info("pelisalacarta.channels.divxtotal listaseries")
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
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.torrentin")'): data = scrapertools.cache_page(item.url+item.extra)
    else: data =''
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
            itemlist.append( Item(channel=item.channel, action="entraenserie", show=re.sub(r"\d{1,2}[x]\d{2}|[-]","",scrapedtitle).strip(), context=["buscar_trailer"] , title=titulo , fulltitle=titulo, url=scrapedurl , thumbnail="" , plot="" , folder=True) )
    patronvideos  = "pagination.*?class='current'.*?<a href='(.*?)'.*?</div>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)>0:
        next_page_url = matches[0]
        itemlist.append( Item(channel=item.channel, action="listaseries", title="[COLOR magenta]>>> Página siguiente  [COLOR dodgerblue](Puede haber más)[/COLOR]" , url=next_page_url , extra= "", thumbnail= NEXTPAGEIMAGE,fanart= FANARTIMAGE , folder=True) )
    return itemlist

def TMDb(title,tipo,year=''):
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/" + tipo + "?api_key=cc4b67c52acb514bdf4931f7cedfd12b&query=" + title.replace(" ","%20") + "&language=es" + "&year=" + year + "&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = FANARTIMAGE
	try: caratula =  "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"poster_path":"\\\(.*?)"')
	except: caratula =THUMBNAILIMAGE
	sinopsis =  scrapertools.find_single_match(data,'"page":1,.*?"overview":"(.*?)","').replace('\\"','"')
	puntuacion = scrapertools.find_single_match(data,'"page":1,.*?"vote_average":(.*?),|}')
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

#EOF ciberus (2015-2017)


