# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para newpct1
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# mod by ciberus (07-03-2017)
#------------------------------------------------------------

import re
import sys
import xbmc

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item

DEBUG = config.get_setting("debug")
MODO_EXTENDIDO = config.get_setting('modo_grafico', "newpct_1")
MODO_MANUAL = config.get_setting('modo_preguntar', "newpct_1")
MODO_CARATULA = config.get_setting('modo_caratula', "newpct_1")
MODO_STREAMING = config.get_setting('modo_streaming', "newpct_1")
MODO_DESCARGA = config.get_setting('modo_descarga', "newpct_1")

Generos = {"28":"Acción","12":"Aventura","16":"Animación","35":"Comedia","80":"Crimen","99":"Documental","18":"Drama","10751":"Familia","14":"Fantasía","36":"Historia","27":"Terror","10402":"Música","9648":"Misterio","10749":"Romance","878":"Ciencia ficción","10770":"película de la televisión","53":"Suspense","10752":"Guerra","37":"Western"}
	
def configuracion(item):
    from platformcode import platformtools
    ret = platformtools.show_channel_settings()
    #platformtools.itemlist_refresh()
    return ret

def mainlist(item):
    logger.info("[newpct1.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=item.channel, action="submenu", title="[COLOR yellow]Películas[/COLOR]", url="http://www.newpct1.com/", extra="peliculas") )
    itemlist.append( Item(channel=item.channel, action="submenu", title="[COLOR orange]Series[/COLOR]", url="http://www.newpct1.com/", extra="series") )
    itemlist.append( Item(channel=item.channel, action="search", title="[COLOR lime]Buscar[/COLOR]") )
    itemlist.append( Item(channel=item.channel, action="configuracion", title="[COLOR dodgerblue]Configuración del canal[/COLOR]"))
    return itemlist

def search(item,texto):
    logger.info("[newpct1.py] search:" + texto)
    texto = texto.replace(" ","+")
    item.url = "http://www.newpct1.com/index.php?page=buscar&q=%27" + texto +"%27&ordenar=Fecha&inon=Descendente"
    item.extra="buscar-list"
    try:
        itemlist = completo(item)

        # Esta pagina coloca a veces contenido duplicado, intentamos descartarlo
        dict_aux = {}
        for i in itemlist:
            if not i.url in dict_aux:
                dict_aux[i.url] = i
            else:
                itemlist.remove(i)

        return itemlist

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def submenu(item):
    logger.info("[newpct1.py] submenu")
    itemlist=[]

    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<li><a href="http://www.newpct1.com/'+item.extra+'/">.*?<ul>(.*?)</ul>'
    data = scrapertools.get_match(data,patron)

    patron = '<a href="([^"]+)".*?>([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = scrapedurl
        if item.extra=="peliculas":
            title = '[COLOR yellow]' + title + '[/COLOR]'
            az = '[COLOR lime] [A-Z][/COLOR]'
        else:
            title = '[COLOR orange]' + title + '[/COLOR]'
            az = '[COLOR cyan] [A-Z][/COLOR]'

        itemlist.append( Item(channel=item.channel, action="listado" ,title=title, url=url, extra="pelilist") )
        itemlist.append( Item(channel=item.channel, action="alfabeto" ,title=title+az, url=url, extra="pelilist") )
    
    return itemlist

def alfabeto(item):
    logger.info("[newpct1.py] alfabeto")
    itemlist = []

    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")

    patron = '<ul class="alfabeto">(.*?)</ul>'
    data = scrapertools.get_match(data,patron)

    patron = '<a href="([^"]+)"[^>]+>([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = '[COLOR limegreen]Letra:  [COLOR lime][B]' + scrapedtitle.upper() + '[/COLOR][/B]'
        url = scrapedurl

        itemlist.append( Item(channel=item.channel, action="completo" ,title=title, url=url, extra=item.extra) )

    return itemlist

def listado(item):
    logger.info("[newpct1.py] listado")
    #logger.info("[newpct1.py] listado url=" + item.url)
    itemlist = []
    
    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")    
        
    patron = '<ul class="'+item.extra+'">(.*?)</ul>'
    logger.info("[newpct1.py] patron="+patron)
    fichas = scrapertools.get_match(data,patron)

    #<li><a href="http://www.newpct1.com/pelicula/x-men-dias-del-futuro-pasado/ts-screener/" title="Descargar XMen Dias Del Futuro gratis"><img src="http://www.newpct1.com/pictures/f/58066_x-men-dias-del-futuro--blurayrip-ac3-5.1.jpg" width="130" height="180" alt="Descargar XMen Dias Del Futuro gratis"><h2>XMen Dias Del Futuro </h2><span>BluRayRip AC3 5.1</span></a></li>
    patron  = '<li><a href="([^"]+).*?' #url
    patron += 'title="([^"]+).*?' #titulo
    patron += '<img src="([^"]+)"[^>]+>.*?' #thumbnail
    patron += '<span>([^<]*)</span>' #calidad

    matches = re.compile(patron,re.DOTALL).findall(fichas)
       
    for scrapedurl,scrapedtitle,scrapedthumbnail,calidad in matches:
        url = scrapedurl
        title = scrapedtitle
        thumbnail = scrapedthumbnail
        action = "findvideos"
        extra = ""
       
        if "1.com/series" in url: 
            action = "completo"
            extra="serie"
            tipo="tvshow"
            title=scrapertools.find_single_match(title,'([^-]+)')
            title= title.replace("Ver online","",1).replace("Descarga Serie HD","",1).replace("Ver en linea","",1).strip() 
            color = 'orange]'
        else:    
            title= title.replace("Descargar","",1).strip()
            if title.endswith("gratis"): title= title[:-7]
            tipo="movie"
            color = 'yellow]'

            # Formateamos titulo para peliculas
            context_title = title.strip()
            context_title=context_title.replace('HDR',"").replace('V.Extendida','').replace('Version Extendida','').replace('Montaje del Director','').replace('3D','').replace('HOU','').replace('AA','').replace('A.A','').replace('SBS','').replace('IMAX','')
            context_title=context_title.replace('_Castellano_BDrip_720p_X26',"").replace('_',' ')
            year=""
            try:
                if re.search( '\d{4}', context_title[-4:]):
                    year=context_title[-4:]
                    context_title = context_title[:-4]
                elif re.search( '\(\d{4}\)', context_title[-6:]):
                    year=context_title[-5:].replace(')','')
                    context_title = context_title[:-6]
            except:
                pass
            context_title=context_title.strip()

        show = title.strip()
        if item.extra!="buscar-list":
            if calidad == "":
                title = '[COLOR ' + color + title + '[/COLOR]'
            else:
                title = '[COLOR ' + color + title + ' ' + '[COLOR dodgerblue](' + calidad + ')[/COLOR]'

        if tipo=="movie":itemlist.append( Item(channel=item.channel, action=action, title=title, url=url, thumbnail=thumbnail, extra=extra, contentTitle=context_title, contentType=tipo, context=["buscar_trailer"] , infoLabels={"year":year} ) )
        else: itemlist.append( Item(channel=item.channel, action=action, title=title, url=url, thumbnail=thumbnail, extra=extra, show=show, contentType=tipo , contentTitle=show, contentSerieName=show,context=["buscar_trailer"]) )

    if "pagination" in data:
        patron = '<ul class="pagination">(.*?)</ul>'
        paginacion = scrapertools.get_match(data,patron)
        
        if "Next" in paginacion:
            url_next_page  = scrapertools.get_match(paginacion,'<a href="([^>]+)>Next</a>')[:-1].replace(" ","%20")
            itemlist.append( Item(channel=item.channel, action="listado" , title="[COLOR magenta]>> Página siguiente[/COLOR]" , url=url_next_page, extra=item.extra))            
    #logger.info("[newpct1.py] listado items:" + str(len(itemlist)))
    return itemlist

def completo(item):
    logger.info("[newpct1.py] completo")
    itemlist = []
    categoryID=""
    
    # Guarda el valor por si son etiquetas para que lo vea 'listadofichas'
    item_extra = item.extra
    item_show= item.show
    item_title= item.title
       
    # Lee las entradas
    if item_extra.startswith("serie"):
        ultimo_action="get_episodios"
        
        if item.extra !="serie_add" and MODO_EXTENDIDO:
            tituserie= item.show
            item.fanart,thumb,item.plot,puntuacion,votos,fecha,genero = TMDb(item.show,item.contentType,"")
            item.infoLabels={"rating":puntuacion,"votes":votos, "genre":genero, "year":fecha, "plot":item.plot}
            if MODO_CARATULA: item.thumbnail=thumb
            item.show=tituserie
        else:
            item_title= item.show

        items_programas = get_episodios(item)        
    else:
        ultimo_action="listado"
        items_programas = listado(item)
        
    if len(items_programas) ==0:
            return itemlist # devolver lista vacia
            
    salir = False
    while not salir:

        # Saca la URL de la siguiente página    
        ultimo_item = items_programas[ len(items_programas)-1 ]
       
        # Páginas intermedias
        if ultimo_item.action==ultimo_action:
            # Quita el elemento de "Página siguiente" 
            ultimo_item = items_programas.pop()

            # Añade las entradas de la página a la lista completa
            itemlist.extend( items_programas )
    
            # Carga la siguiente página
            ultimo_item.extra = item_extra
            ultimo_item.show = item_show
            ultimo_item.title = item_title

            logger.info("[newpct1.py] completo url=" + ultimo_item.url)
            if item_extra.startswith("serie"):
                items_programas = get_episodios(ultimo_item)
            else:
                items_programas = listado(ultimo_item)
                
        # Última página
        else:
            # Añade a la lista completa y sale
            itemlist.extend( items_programas )
            salir = True          
      
    if (config.get_library_support() and len(itemlist)>0 and item.extra.startswith("serie")) :
        itemlist.append( Item(channel=item.channel, title="[COLOR cyan]Añadir esta serie a la biblioteca[/COLOR]", url=item.url, action="add_serie_to_library", extra="completo###serie_add" , show = item.show, thumbnail=item.thumbnail))
    logger.info("[newpct1.py] completo items="+ str(len(itemlist)))
    return itemlist
   
def get_episodios(item):
    logger.info("[newpct1.py] get_episodios")
    itemlist=[]
    logger.info("[newpct1.py] get_episodios url=" +item.url)   
    data = re.sub(r'\n|\r|\t|\s{2}|<!--.*?-->|<i class="icon[^>]+"></i>',"",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")
    
    logger.info("[newpct1.py] data=" +data)
      
    patron = '<ul class="buscar-list">(.*?)</ul>'
    #logger.info("[newpct1.py] patron=" + patron)
    
    fichas = scrapertools.get_match(data,patron)
    #logger.info("[newpct1.py] matches=" + str(len(fichas)))
    
    #<li><a href="http://www.newpct1.com/serie/forever/capitulo-101/" title="Serie Forever 1x01"><img src="http://www.newpct1.com/pictures/c/minis/1880_forever.jpg" alt="Serie Forever 1x01"></a> <div class="info"> <a href="http://www.newpct1.com/serie/forever/capitulo-101/" title="Serie Forever 1x01"><h2 style="padding:0;">Serie <strong style="color:red;background:none;">Forever - Temporada 1 </strong> - Temporada<span style="color:red;background:none;">[ 1 ]</span>Capitulo<span style="color:red;background:none;">[ 01 ]</span><span style="color:red;background:none;padding:0px;">Espa�ol Castellano</span> Calidad <span style="color:red;background:none;">[ HDTV ]</span></h2></a> <span>27-10-2014</span> <span>450 MB</span> <span class="color"><ahref="http://www.newpct1.com/serie/forever/capitulo-101/" title="Serie Forever 1x01"> Descargar</a> </div></li>
    #logger.info("[newpct1.py] get_episodios: " + fichas)
    patron  = '<li><a href="([^"]+).*?' #url
    patron += '<img src="([^"]+)".*?' #thumbnail
    patron += '<h2 style="padding(.*?)/h2>' #titulo, idioma y calidad
    
    matches = re.compile(patron,re.DOTALL).findall(fichas)
    #logger.info("[newpct1.py] get_episodios matches: " + str(len(matches)))
    for scrapedurl,scrapedthumbnail,scrapedinfo in matches:
        try:
            url = scrapedurl
            if '</span>' in scrapedinfo:
                #logger.info("[newpct1.py] get_episodios: scrapedinfo="+scrapedinfo)
                try:
                    #<h2 style="padding:0;">Serie <strong style="color:red;background:none;">The Big Bang Theory - Temporada 6 </strong> - Temporada<span style="color:red;background:none;">[ 6 ]</span>Capitulo<span style="color:red;background:none;">[ 03 ]</span><span style="color:red;background:none;padding:0px;">Español Castellano</span> Calidad <span style="color:red;background:none;">[ HDTV ]</span></h2>
                    patron = '<span style=".*?">\[\s*(.*?)\]</span>.*?' #temporada
                    patron += '<span style=".*?">\[\s*(.*?)\].*?' #capitulo
                    patron += ';([^/]+)' #idioma
                    info_extra = re.compile(patron, re.DOTALL).findall(scrapedinfo)
                    (temporada, capitulo, idioma) = info_extra[0]

                except:
                    # <h2 style="padding:0;">Serie <strong style="color:red;background:none;">The Affair  Temporada 3 Capitulo 5</strong> - <span style="color:red;background:none;padding:0px;">Español Castellano</span> Calidad <span style="color:red;background:none;">[ HDTV ]</span></h2>
                    patron = '<strong style=".*?">([^<]+).*?'  # temporada y capitulo
                    patron += '<span style=".*?">([^<]+)'

                    info_extra = re.compile(patron,re.DOTALL).findall(scrapedinfo)
                    (temporada_capitulo,idioma)=info_extra[0]
                    temporada, capitulo = scrapertools.get_season_and_episode(temporada_capitulo).split('x')
                
                #logger.info("[newpct1.py] get_episodios: temporada=" + temporada)
                #logger.info("[newpct1.py] get_episodios: capitulo=" + capitulo)
                logger.info("[newpct1.py] get_episodios: idioma=" + idioma)
                if '">' in idioma: 
                    idioma= " [" + scrapertools.find_single_match(idioma,'">([^<]+)').strip() +"]"
                elif '&nbsp' in idioma:
                    idioma= " [" + scrapertools.find_single_match(idioma,'&nbsp;([^<]+)').strip() +"]"
                '''else:
                    idioma=""'''
                title =  item.title + " [COLOR lime](" + temporada.strip() + "x" + capitulo.strip()  + ")[/COLOR] " + idioma
                
            else:
                #<h2 style="padding:0;">The Big Bang Theory - Temporada 6 [HDTV][Cap.602][Español Castellano]</h2>
                #<h2 style="padding:0;">The Beast - Temporada 1 [HDTV] [Capítulo 13] [Español]</h2
                #<h2 style="padding:0;">The Beast - Temp.1 [DVD-DVB][Cap.103][Spanish]</h2>             
                try:
                    temp ,cap = scrapertools.get_season_and_episode(scrapedinfo).split('x')
                except:
                    #Formatear temporadaXepisodio
                    patron= re.compile('Cap.*?\s*([\d]+)',re.IGNORECASE)
                    info_extra=patron.search(scrapedinfo)
                                       
                    if len(str(info_extra.group(1)))>=3:
                        cap=info_extra.group(1)[-2:]
                        temp=info_extra.group(1)[:-2]
                    else:
                        cap=info_extra.group(1)
                        patron='Temp.*?\s*([\d]+)'            
                        temp= re.compile(patron,re.IGNORECASE).search(scrapedinfo).group(1)

                title = item.title + " [COLOR lime]("+ temp + 'x' + cap + ")[/COLOR]"
            
            #logger.info("[newpct1.py] get_episodios: fanart= " +item.fanart)
            itemlist.append( Item(channel=item.channel, action="findvideos", title=title, url=url, thumbnail=item.thumbnail, show=item.show, fanart=item.fanart , infoLabels=item.infoLabels , contentTitle=item.show) )
        except:
            logger.info("[newpct1.py] ERROR al añadir un episodio")
    if "pagination" in data:
        patron = '<ul class="pagination">(.*?)</ul>'
        paginacion = scrapertools.get_match(data,patron)
        #logger.info("[newpct1.py] get_episodios: paginacion= " + paginacion)
        if "Next" in paginacion:
            url_next_page  = scrapertools.get_match(paginacion,'<a href="([^>]+)>Next</a>')[:-1]
            url_next_page= url_next_page.replace(" ","%20")
            #logger.info("[newpct1.py] get_episodios: url_next_page= " + url_next_page)
            itemlist.append( Item(channel=item.channel, action="get_episodios" , title="[COLOR magenta]>> Página siguiente[/COLOR]" , url=url_next_page   ,   infoLabels=item.infoLabels , thumbnail=item.thumbnail))

    return itemlist

def buscar_en_subcategoria(titulo, categoria):
    data= scrapertools.cache_page("http://www.newpct1.com/pct1/library/include/ajax/get_subcategory.php", post="categoryIDR=" + categoria)
    data=data.replace("</option>"," </option>")
    patron = '<option value="(\d+)">(' + titulo.replace(" ","\s").replace("(","/(").replace(")","/)") + '\s[^<]*)</option>'
    logger.info("[newpct1.py] buscar_en_subcategoria: data=" + data)
    logger.info("[newpct1.py] buscar_en_subcategoria: patron=" + patron)
    matches = re.compile(patron,re.DOTALL | re.IGNORECASE).findall(data)
    
    if len(matches)==0: matches=[('','')]
    logger.info("[newpct1.py] buscar_en_subcategoria: resultado=" + matches [0][0])
    return matches [0][0]

def findvideos(item):
    logger.info("[newpct1.py] findvideos")
    itemlist=[]   
          
    ## Cualquiera de las tres opciones son válidas
    #item.url = item.url.replace("1.com/","1.com/ver-online/")
    #item.url = item.url.replace("1.com/","1.com/descarga-directa/")
    item.url = item.url.replace("1.com/","1.com/descarga-torrent/")

    # Descarga la página
    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    data = unicode( data, "iso-8859-1" , errors="replace" ).encode("utf-8")
    
    title = scrapertools.find_single_match(data,"<h1><strong>([^<]+)</strong>[^<]+</h1>")
    title+= scrapertools.find_single_match(data,"<h1><strong>[^<]+</strong>([^<]+)</h1>")
    caratula = scrapertools.find_single_match(data,'<div class="entry-left">.*?src="([^"]+)"')

    #<a href="http://tumejorjuego.com/download/index.php?link=descargar-torrent/058310_yo-frankenstein-blurayrip-ac3-51.html" title="Descargar torrent de Yo Frankenstein " class="btn-torrent" target="_blank">Descarga tu Archivo torrent!</a>

    if MODO_EXTENDIDO and item.contentType=="movie":
        #titu=item.contentTitle.replace('HDR',"").replace('V.Extendida','').replace('Version Extendida','').replace('Montaje del Director','').replace('3D','').replace('HOU','').replace('AA','').replace('A.A','').replace('SBS','').replace('IMAX','').replace('_',' ')
        titu=item.contentTitle
        fanart,thumbnail,plot,puntuacion,votos,fecha,genero = TMDb(titu,item.contentType,item.infoLabels["year"])
        
        if thumbnail == "" and MODO_MANUAL:
            keyboard = xbmc.Keyboard(titu,'[COLOR yellow]"'+item.contentTitle+'"[/COLOR]' + " [COLOR magenta]No encontrada en TMDb,[COLOR cyan] modificar titulo...[/COLOR]")
            keyboard.doModal()
            if (keyboard.isConfirmed()):
                titu = keyboard.getText()
                fanart,thumbnail,plot,puntuacion,votos,fecha,genero = TMDb(titu,item.contentType,"")

        infoLabels={"rating":puntuacion,"votes":votos, "genre":genero, "year":fecha}
        item.plot=plot
        if MODO_CARATULA and thumbnail != "": caratula=thumbnail
    else:
        fanart=item.fanart
        infoLabels=item.infoLabels

    #if title=='': title=item.title

    patron = '<a href="([^"]+)" title="[^"]+" class="btn-torrent" target="_blank">'
    # escraped torrent
    url = scrapertools.find_single_match(data,patron)
    if url!="":
        itemlist.append( Item(channel=item.channel, action="play", server="torrent", title='[COLOR lime]' + title+" [COLOR cyan][torrent][/COLOR]", fulltitle=title, contentTitle=item.contentTitle, url=url , thumbnail=caratula, plot=item.plot, fanart=fanart, infoLabels=infoLabels , context=item.context , folder=False) )

    if MODO_STREAMING:
        # escraped ver vídeos, descargar vídeos un link, múltiples liks
        data = data.replace("'",'"')
        data = data.replace('javascript:;" onClick="popup("http://www.newpct1.com/pct1/library/include/ajax/get_modallinks.php?links=',"")
        data = data.replace("http://tumejorserie.com/descargar/url_encript.php?link=","")
        data = data.replace("$!","#!")

        patron_descargar = '<div id="tab2"[^>]+>.*?</ul>'
        patron_ver = '<div id="tab3"[^>]+>.*?</ul>'

        match_ver = scrapertools.find_single_match(data,patron_ver)
        match_descargar = scrapertools.find_single_match(data,patron_descargar)

        patron = '<div class="box1"><img src="([^"]+)".*?' # logo
        patron+= '<div class="box2">([^<]+)</div>'         # servidor
        patron+= '<div class="box3">([^<]+)</div>'         # idioma
        patron+= '<div class="box4">([^<]+)</div>'         # calidad
        patron+= '<div class="box5"><a href="([^"]+)".*?'  # enlace
        patron+= '<div class="box6">([^<]+)</div>'         # titulo

        enlaces_ver = re.compile(patron,re.DOTALL).findall(match_ver)
        enlaces_descargar = re.compile(patron,re.DOTALL).findall(match_descargar)

        for logo, servidor, idioma, calidad, enlace, titulo in enlaces_ver:
            servidor = servidor.replace("streamin","streaminto")
            titulo = titulo+" ["+servidor+"]"
            mostrar_server= True
            if config.get_setting("hidepremium")=="true":
                mostrar_server= servertools.is_server_enabled (servidor)
            if mostrar_server:
                try:
                    servers_module = __import__("servers."+servidor)
                    server_module = getattr(servers_module,servidor)
                    devuelve= server_module.find_videos(enlace)
                    if devuelve:
                        enlace=devuelve[0][1]
                        itemlist.append( Item(fanart=fanart, channel=item.channel, action="play", server=servidor, title='[COLOR yellow]' + titulo + '[/COLOR]', fulltitle = item.title, contentTitle=item.contentTitle,url=enlace , thumbnail=logo , plot=item.plot, infoLabels=infoLabels , context=item.context , folder=False) )
                except:
                    pass
        
    if MODO_STREAMING and MODO_DESCARGA:
        for logo, servidor, idioma, calidad, enlace, titulo in enlaces_descargar:
            servidor = servidor.replace("uploaded","uploadedto")
            partes = enlace.split(" ")
            p = 1
            for enlace in partes:
                parte_titulo = titulo+" (%s/%s)" % (p,len(partes)) + " ["+servidor+"]"
                p+= 1
                mostrar_server= True
                if config.get_setting("hidepremium")=="true":
                    mostrar_server= servertools.is_server_enabled (servidor)
                if mostrar_server:
                    try:
                        servers_module = __import__("servers."+servidor)
                        server_module = getattr(servers_module,servidor)
                        devuelve= server_module.find_videos(enlace)
                        if devuelve:
                            enlace=devuelve[0][1]
                            itemlist.append( Item(fanart=fanart, channel=item.channel, action="play", server=servidor, title='[COLOR orange]' + parte_titulo + '[/COLOR]' , fulltitle = item.title, contentTitle=item.contentTitle,url=enlace , thumbnail=logo , plot=item.plot, infoLabels=infoLabels , context=item.context , folder=False) )
                    except:
                        pass
    return itemlist

def TMDb(title,tipo,year):
	if tipo=="tvshow": tipo="tv"
	data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;',"",scrapertools.cachePage("http://api.themoviedb.org/3/search/" + tipo + "?api_key=cc4b67c52acb514bdf4931f7cedfd12b&query=" + title.replace(" ","%20") + "&year=" + year + "&language=es&include_adult=false"))
	try: fanart = "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"backdrop_path":"\\\(.*?)"')
	except: fanart = ""
	try: caratula =  "https://image.tmdb.org/t/p/original" + scrapertools.get_match(data,'"page":1,.*?"poster_path":"\\\(.*?)"')
	except: caratula =""
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
  
def episodios(item):
    # Necesario para las actualizaciones automaticas
    return completo(Item(channel=item.channel, url=item.url, show=item.show, extra= "serie_add"))
