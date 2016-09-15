# -*- coding: utf-8 -*-
#------------------------------------------------------------
# latinototal - XBMC Add-on by 19hdz19 (latinototal19@gmail.com)
# Version 0.1.0 (03.12.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, nstream, ioncube

from framescrape import *
from resources.tools.resolvers import *
from resources.tools.update import *
from resources.tools.scrape import *
from resources.tools.torrentvru import *
from resources.tools.vaughnlive import *
from resources.tools.ninestream import *
from resources.tools.vercosas import *
from resources.tools.torrent1 import *
from resources.tools.directwatch import *
from resources.tools.freetvcast import *
from resources.tools.freebroadcast import *
from resources.tools.shidurlive import *
from resources.tools.latuerka import *
from resources.tools.laligatv import *
from resources.tools.updater import *
from resources.tools.castalba import *
from resources.tools.castdos import *
from resources.tools.new_regex import *
from resources.tools.sportseven import *
from resources.tools.streamingfreetv import *
from resources.tools.dailymotion import *
from resources.tools.getposter import *





home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.latinototal/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.latinototal/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.latinototal/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.latinototal/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'




# Entry point
def run():

    plugintools.log("---> latinototal.run <---")
    
    # Obteniendo parámetros...
    params = plugintools.get_params() 
    
    if params.get("action") is None:
        main_list(params)
    else:
       action = params.get("action")
       url = params.get("url")
       exec action+"(params)"
    
    if not os.path.exists(playlists) :
        os.makedirs(playlists)

   

    plugintools.close_item_list()


  
# Main menu

def main_list(params):
    plugintools.log("[latinototal-0.1.0].main_list "+repr(params))
  
    # Control del skin de latinototal
    mastermenu = xml_skin()
    plugintools.log("XML menu: "+mastermenu)
    try:
        data = plugintools.read(mastermenu)
    except:
        mastermenu = 'http://pastebin.com/raw.php?i=n9BF6Cwe'
        data = plugintools.read(mastermenu)
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('latinototal', "XML no reconocido...", 3 , art+'icon.png'))    

    matches = plugintools.find_multiple_matches(data,'<menu_info>(.*?)</menu_info>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        date = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        plugintools.add_item( action="" , title = title + date , fanart = fanart , thumbnail=thumbnail , folder = False , isPlayable = False )

    data = plugintools.read(mastermenu)        
    matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        action = plugintools.find_single_match(entry,'<action>(.*?)</action>')
        last_update = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')
        url = plugintools.find_single_match(entry,'<url>(.*?)</url>')
        date = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')

        # Control paternal
        pekes_no = plugintools.get_setting("pekes_no")
        if pekes_no == "true" :
            print "Control paternal en marcha"
            if title.find("Adultos") >= 0 :
                plugintools.log("Activando control paternal...")
            else:
                fixed = title
                plugintools.log("fixed= "+fixed)
                if fixed == "Actualizaciones":
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
                elif fixed == 'Agenda TV':
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )                
                else:
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
        else:
            fixed = title
            if fixed == "Actualizaciones":
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
            elif fixed == "Agenda TV":
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR red]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
            else:
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
            
               

def play(params):
    plugintools.log("[latinototal-0.1.0].play "+repr(params))
    # plugintools.direct_play(params.get("url"))
    # xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(params.get("url"))
    url = params.get("url")

    # Notificación de inicio de resolver en caso de enlace RTMP

    if url.startswith("http") == True:
        if url.find("allmyvideos") >= 0 :
            allmyvideos(params)
        elif url.find("streamcloud") >= 0 :
            streamcloud(params)
        elif url.find("vidspot") >= 0 :
            vidspot(params)
        elif url.find("played.to") >= 0 :
            playedto(params)
        elif url.find("vk.com") >= 0 :
            vk(params)
        elif url.find("nowvideo") >= 0 :
            nowvideo(params)
        elif url.find("tumi") >= 0 :
            tumi(params)
        elif url.find("streamin.to") >= 0 :
            streaminto(params)              
        else:
            url = params.get("url")
            plugintools.play_resolved_url(url)

    elif url.startswith("rtp") >= 0:  # Control para enlaces de Movistar TV
        plugintools.play_resolved_url(url)
       
    else:
        plugintools.play_resolved_url(url)
        while OnPlayBackStarted() == False:
            print "No se está reproduciendo..."
            time.sleep(3)
            if OnPlayBackStarted():
                print "En reproducción!"
            else:
                print "No ha empezado"
                
              
 
def runPlugin(url):
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')


def live_items_withlink(params):
    plugintools.log("[latinototal-0.1.0].live_items_withlink "+repr(params))
    data = plugintools.read(params.get("url"))

    # ToDo: Agregar función lectura de cabecera (fanart, thumbnail, título, últ. actualización)
    header_xml(params)

    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')  # Localizamos fanart de la lista
    if fanart == "":
        fanart = art + 'fanart.jpg'
        
    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')  # Localizamos autor de la lista (encabezado)
    
    matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        title = title.replace("<![CDATA[", "")
        title = title.replace("]]>", "")
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        url = plugintools.find_single_match(entry,'<link>(.*?)</link>')
        url = url.replace("<![CDATA[", "")
        url = url.replace("]]>", "")
        plugintools.add_item(action = "play" , title = title , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )
        

  
def xml_lists(params):
    plugintools.log("[latinototal-0.1.0].xml_lists "+repr(params))
    data = plugintools.read( params.get("url") )
    name_channel = params.get("title")
    name_channel = parser_title(name_channel)
    plugintools.log("name_channel= "+name_channel)
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)

    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR]' , thumbnail= art + 'special.png' , fanart = fanart , folder = False , isPlayable = False )
    
    # Control paternal
    pekes_no = plugintools.get_setting("pekes_no")
    
    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<fanart>([^<]+)</fanart>([^<]+)<action>([^<]+)</action>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    for biny, ciny, diny, winy, pixy, dixy, boxy, susy, lexy, muny, kiny in subchannel:
        if pekes_no == "true" :
            print "Control paternal en marcha"
            if ciny.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")
            else:             
                plugintools.add_item( action = susy , title = ciny , url= muny , thumbnail = winy , fanart = dixy , extra = dixy , page = dixy , folder = True , isPlayable = False )
                params["fanart"]=dixy
                # params["thumbnail"]=pixy
                
        else:        
            plugintools.add_item( action = susy , title = ciny , url= muny , thumbnail = winy , fanart = dixy , extra = dixy , page = dixy , folder = True , isPlayable = False )
            params["fanart"]=dixy
            # params["thumbnail"]=pixy       
                

            
def getstreams_now(params):
    plugintools.log("[latinototal-0.1.0].getstreams_now "+repr(params))
    
    data = plugintools.read( params.get("url") )
    poster = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    plugintools.add_item(action="" , title='[COLOR blue][B]'+poster+'[/B][/COLOR]', url="", folder =False, isPlayable=False)
    matches = plugintools.find_multiple_matches(data,'<title>(.*?)</link>')
    
    for entry in matches:
        title = plugintools.find_single_match(entry,'(.*?)</title>')
        url = plugintools.find_single_match(entry,'<link> ([^<]+)')
        plugintools.add_item( action="play" , title=title , url=url , folder = False , isPlayable = True )
        
     

# Soporte de listas de canales por categorías (Livestreams, XBMC México, Motor SportsTV, etc.). 

def livestreams_channels(params):
    plugintools.log("[latinototal-0.1.0].livestreams_channels "+repr(params))
    data = plugintools.read( params.get("url") )
       
    # Extract directory list
    thumbnail = params.get("thumbnail")
    
    if thumbnail == "":
        thumbnail = 'icon.jpg'
        plugintools.log(thumbnail)
    else:
        plugintools.log(thumbnail)
    
    if thumbnail == art + 'icon.png':
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</items>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_subchannels" , title=title , url=params.get("url") , thumbnail=thumbnail , fanart=fanart , folder = True , isPlayable = False )

    else:
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</items>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_items" , title=title , url=params.get("url") , fanart=fanart , thumbnail=thumbnail , folder = True , isPlayable = False )
   
        
def livestreams_subchannels(params):
    plugintools.log("[latinototal-0.1.0].livestreams_subchannels "+repr(params))

    data = plugintools.read( params.get("url") )
    # title_channel = params.get("title")
    title_channel = params.get("title")
    name_subchannel = '<name>'+title_channel+'</name>'
    data = plugintools.find_single_match(data, name_subchannel+'(.*?)</channel>')
    info = plugintools.find_single_match(data, '<info>(.*?)</info>')
    title = params.get("title")
    plugintools.add_item( action="" , title='[B]'+title+'[/B] [COLOR yellow]'+info+'[/COLOR]' , folder = False , isPlayable = False )

    subchannel = plugintools.find_multiple_matches(data , '<name>(.*?)</name>')
    for entry in subchannel:
        plugintools.add_item( action="livestreams_subitems" , title=entry , url=params.get("url") , thumbnail=art+'motorsports-xbmc.jpg' , folder = True , isPlayable = False )


# Pendiente de cargar thumbnail personalizado y fanart...
def livestreams_subitems(params):
    plugintools.log("[latinototal-0.1.0].livestreams_subitems "+repr(params))

    title_subchannel = params.get("title")
    data = plugintools.read( params.get("url") )
    source = plugintools.find_single_match(data , title_subchannel+'(.*?)<subchannel>')

    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>').findall(source)
    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")
    
    for entry, quirry, winy in titles:
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = thumbnail , folder = False , isPlayable = True )


def livestreams_items(params):
    plugintools.log("[latinototal-0.1.0].livestreams_items "+repr(params))

    title_subchannel = params.get("title")
    plugintools.log("title= "+title_subchannel)    
    title_subchannel_fixed = title_subchannel.replace("Ã±", "ñ")
    title_subchannel_fixed = title_subchannel_fixed.replace("\\xc3\\xb1", "ñ")    
    title_subchannel_fixed = plugintools.find_single_match(title_subchannel_fixed, '([^[]+)')
    title_subchannel_fixed = title_subchannel_fixed.encode('utf-8', 'ignore')
    plugintools.log("subcanal= "+title_subchannel_fixed)
    if title_subchannel_fixed.find("+") >= 0:
        title_subchannel_fixed = title_subchannel_fixed.split("+")
        title_subchannel_fixed = title_subchannel_fixed[1]
        title_subchannel_fixxed = title_subchannel_fixed[0]
        if title_subchannel_fixed == "":
            title_subchannel_fixed = title_subchannel_fixxed
        
    data = plugintools.read( params.get("url") )
    source = plugintools.find_single_match(data , title_subchannel_fixed+'(.*?)</channel>')
    plugintools.log("source= "+source)
    fanart_channel = plugintools.find_single_match(source, '<fanart>(.*?)</fanart>')
    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>([^<]+)<thumbnail>([^<]+)</thumbnail>').findall(source)
       
    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")
    
    for entry, quirry, winy, xiry, miry in titles:
        plugintools.log("title= "+entry)
        plugintools.log("url= "+winy)
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = miry , fanart = fanart_channel , folder = False , isPlayable = True )


def xml_items(params):
    plugintools.log("[latinototal-0.1.0].xml_items "+repr(params))
    data = plugintools.read( params.get("url") )
    thumbnail = params.get("thumbnail")

    #Todo: Implementar una variable que permita seleccionar qué tipo de parseo hacer
    if thumbnail == "title_link.png":
        matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            url = plugintools.find_single_match(entry,'<link>([^<]+)</link>')
            fanart = plugintools.find_single_match(entry,'<fanart>([^<]+)</fanart>')
            plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )

    if thumbnail == "name_rtmp.png":
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            url = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
            plugintools.add_item( action = "play" , title = title , url = url , fanart = art + 'fanart.jpg' , plot = title , folder = False , isPlayable = True )

             
def simpletv_items(params):
    plugintools.log("[latinototal-0.1.0].simpletv_items "+repr(params))

    saving_url = 0

    # Obtenemos fanart y thumbnail del diccionario
    thumbnail = params.get("thumbnail")
    plugintools.log("thumbnail= "+thumbnail)
    if thumbnail == "" :
        thumbnail = art + 'icon.png'

    # Parche para solucionar un bug por el cuál el diccionario params no retorna la variable fanart
    fanart = params.get("extra")
    if fanart == " " :
        fanart = params.get("fanart")
        if fanart == " " :
            fanart = art + 'fanart.png'
        
    title = params.get("plot")
    texto= params.get("texto")
    busqueda = ""
    if title == 'search':
        title = title + '.txt'
        plugintools.log("title= "+title)
    else:
        title = title + '.m3u'

    if title == 'search.txt':
        busqueda = 'search.txt'
        filename = title
        file = open(tmp + 'search.txt', "r")
        file.seek(0)
        data = file.readline()
        if data == "":
            ok = plugintools.message("latinototal", "Sin resultados")
            return ok
    else:
        title = params.get("title")
        title = parser_title(title)
        ext = params.get("ext")
        title_plot = params.get("plot")
        if title_plot == "":
            filename = title + "." + ext

        if ext is None:
            filename = title
        else:
            plugintools.log("ext= "+ext)
            filename = title + "." + ext
            
        file = open(playlists + filename, "r")
        file.seek(0)
        data = file.readline()
        plugintools.log("data= "+data)
      
    if data == "":
        print "No es posible leer el archivo!"
        data = file.readline()
        plugintools.log("data= "+data)
    else:
        file.seek(0)
        num_items = len(file.readlines())
        print num_items
        plugintools.log("filename= "+filename)
        plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ filename + '[/B][/I][/COLOR]' , url = playlists + title , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = False)

    
    # Lectura de items en lista m3u. ToDo: Control de errores, implementar lectura de fanart y thumbnail

    # Control para evitar error en búsquedas (cat is null)
    cat = ""

    i = -1
    file.seek(0)
    data = file.readline()
    while i <= num_items:
        if data.startswith("#EXTINF:-1") == True:
            title = data.replace("#EXTINF:-1", "")
            title = title.replace(",", "")
            title = title.replace("-AZBOX *", "")
            title = title.replace("-AZBOX-*", "")
            
            if title.startswith("$") == True:  # Control para lanzar scraper IMDB
                title = title.replace("$","")
                images = m3u_items(title)                
                title_fixed = images[3]
                datamovie = {}
                datamovie = getposter(title_fixed)
                save_title(title_fixed, datamovie, filename)
                getdatafilm = 1  # Control para cargar datos de película
                saving_url = 1  # Control para guardar URL
                if datamovie == {}:
                    title = '[COLOR lightyellow][B]'+title+' - [/B][I][COLOR orange][IMDB: [B]'+datamovie["Rating"]+'[/B]][/I][/COLOR] '
                    thumbnail = datamovie["Poster"];fanart = datamovie["Fanart"]

            # Control de la línea del título en caso de búsqueda 
            if busqueda == 'search.txt':
                title_search = title.split('"')
                print 'title',title
                titulo = title_search[0]
                titulo = titulo.strip()
                origen = title_search[1]
                origen = origen.strip()
                data = file.readline()
                i = i + 1      
            else:
                images = m3u_items(title)
                thumbnail = images[0]
                fanart = images[1]
                cat = images[2]
                title = images[3]
                origen = title.split(",")                
                title = title.strip()
                plugintools.log("title= "+title)
                data = file.readline()
                i = i + 1                

            if title.startswith("#") == True:
                title = title.replace("#", "")
                plugintools.add_item(action="", title = title , url = "", thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False)
                data = file.readline()
                print data
                i = i + 1
                continue                

            # Control para determinadas listas de decos sat
            if title.startswith(' $ExtFilter="') == True:
                if busqueda == 'search.txt':
                    title = title.replace('$ExtFilter="', "")
                    title_search = title.split('"')
                    titulo = title_search[1]
                    origen = title_search[2]
                    origen = origen.strip()
                    data = file.readline()
                    i = i + 1                    
                else:
                    title = title.replace('$ExtFilter="', "")
                    category = title.split('"')
                    tipo = category[0]
                    tipo = tipo.strip()
                    title = category[1]
                    title = title.strip()
                    print title
                    data = file.readline()
                    i = i + 1
              
            if data != "":
                title = title.replace("radio=true", "")                                  
                url = data.strip()
                if url.startswith("serie") == True:
                    url = data.strip()
                    if cat == "":
                        if busqueda == 'search.txt':                            
                            url = url.replace("serie:", "")
                            params["fanart"] = fanart
                            plugintools.log("fanart= "+fanart)
                            plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            url = url.replace("serie:", "")
                            params["fanart"] = fanart
                            plugintools.log("fanart= "+fanart)
                            plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue                        
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "longurl" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Serie online][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "longurl" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Serie online][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                
                if data.startswith("http") == True:
                    url = data.strip()
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.log("fanart= "+fanart)
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("allmyvideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + '[COLOR lightyellow] [Allmyvideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("streamcloud") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + title + '[COLOR lightskyblue] [Streamcloud][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("vidspot") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + '[COLOR palegreen] [Vidspot][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("played.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + '[COLOR lavender] [Played.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vk.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + '[COLOR royalblue] [Vk][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("nowvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("tumi") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR orange] [streamin.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)                                 
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue                           

                            elif url.find("www.youtube.com") >= 0:  # Video youtube
                                plugintools.log("linea titulo= "+title_search)
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoid
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [[COLOR red]You[COLOR white]tube Video][I] (' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                                    plugintools.add_item( action="dailym_pl" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]' , fanart=fanart, thumbnail=thumbnail, url=url , folder=True, isPlayable=False)
                                    if saving_url == 1:
                                        plugintools.log("URL= "+url)
                                        save_url(url, filename)
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                
                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]' , url=url , thumbnail = thumbnail , fanart = fanart, isPlayable=True, folder=False )
                                    if saving_url == 1:
                                        plugintools.log("URL= "+url)
                                        save_url(url, filename)                                  
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue                              

                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR purple] [m3u8][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue                            
                            
                            else:
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.log("fanart= "+fanart)
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Serie online][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("allmyvideos") >= 0:                             
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lightyellow] [Allmyvideos][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("streamcloud") >= 0:                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lightskyblue] [Streamcloud][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidspot") == True:                             
                                plugintools.add_item( action = "vidspot" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR palegreen] [Vidspot][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("played.to") >= 0:                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lavender] [Played.to][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("vk") >= 0:                            
                                plugintools.add_item( action = "vk" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR royalblue] [Vk][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue                           

                            elif url.find("nowvideo") >= 0:                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [Nowvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("tumi") >= 0:                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR forestgreen] [Tumi][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [streamin.to][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue                              

                            elif url.find("9stream") >= 0:                            
                                plugintools.add_item( action = "ninestreams" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR green] [9stream][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue                      

                            elif url.find("www.youtube.com") >= 0:  # Video youtube
                                title = title.split('"')
                                title = title[0]
                                title =title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoid
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [[COLOR red]You[COLOR white]tube Video][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue                           
                            
                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    plugintools.log("id_playlist= "+id_playlist)
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    plugintools.add_item( action="dailym_pl" , title='[COLOR red][I]'+cat+' / [/I][/COLOR] '+title+' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]', url=url , fanart = fanart , thumbnail=thumbnail , folder=True, isPlayable=False)
                                    if saving_url == 1:
                                        plugintools.log("URL= "+url)
                                        save_url(url, filename)
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title='[COLOR red][I]' + cat + ' / [/I][/COLOR] '+title+' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]', url=url , thumbnail = thumbnail , fanart= fanart , isPlayable=True, folder=False )
                                    if saving_url == 1:
                                        plugintools.log("URL= "+url)
                                        save_url(url, filename)
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                
                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR purple] [m3u8][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            else:                            
                                plugintools.add_item( action = "longurl" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR blue] [HTTP][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                    # Sin categoría de canales   
                    else:
                        if busqueda == 'search.txt':
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.log("fanart= "+fanart)
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("allmyvideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + '[COLOR lightyellow] [Allmyvideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamcloud") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + titulo + '[COLOR lightskyblue] [Streamcloud][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                       
                            
                            elif url.find("vidspot") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + '[COLOR palegreen] [Vidspot][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            
                            elif url.find("played.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + '[COLOR lavender] [Played.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("vk.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + '[COLOR royalblue] [Vk][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("nowvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("tumi.tv") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("streamin.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR orange] [streamin.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            

                            elif url.find("www.youtube.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoid                            
                                plugintools.add_item( action = "youtube_videos" , title = '[COLOR white][' + title + ' [[COLOR red]You[/COLOR][COLOR white]tube Video][I] (' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'                               
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    plugintools.add_item( action="dailym_pl" , title=title+' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url=url , fanart = fanart , thumbnail=thumbnail , folder=True, isPlayable=False)
                                    if saving_url == 1:
                                        plugintools.log("URL= "+url)
                                        save_url(url, filename)
                                    data = file.readline()
                                    i = i + 1
                                    continue                                    
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title+' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url=url , fanart = fanart , thumbnail = thumbnail , isPlayable=True, folder=False )
                                    if saving_url == 1:
                                        plugintools.log("URL= "+url)
                                        save_url(url, filename)
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                            
                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR purple][m3u8][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            
                            else:                      
                                title = title_search[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + ' [COLOR blue][HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                        else:
                            if url.find("allmyvideos") >= 0:                                
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + ' [COLOR lightyellow][Allmyvideos][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("streamcloud") >= 0:                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + title + ' [COLOR lightskyblue][Streamcloud][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("vidspot") >= 0:                            
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + ' [COLOR palegreen][Vidspot][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue

                            
                            elif url.find("played.to") >= 0:                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + ' [COLOR lavender][Played.to][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("vk.com") >= 0:                            
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + ' [COLOR royalblue][Vk][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("nowvideo") >= 0:                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("tumi.tv") >= 0:                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("streamin.to") >= 0:                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR orange] [streamin.to][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            

                            elif url.find("www.youtube.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                videoid = url.replace("https://www.youtube.com/watch?v=", "")
                                print 'videoid',videoid
                                url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoid                            
                                plugintools.add_item( action = "youtube_videos" , title = '[COLOR white]' + title + ' [[COLOR red]You[/COLOR][COLOR white]tube Video][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue


                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    plugintools.log("id_playlist= "+id_playlist)
                                    thumbnail=art+'/lnh_logo.png'
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"                                    
                                    plugintools.add_item( action="dailym_pl" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]' , url=url , fanart = fanart , thumbnail=thumbnail , folder=True)
                                    if saving_url == 1:
                                        plugintools.log("URL= "+url)
                                        save_url(url, filename)
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    #plugintools.log("url= "+url)
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]' , url=url , thumbnail = thumbnail , fanart = fanart , isPlayable=True, folder=False )
                                    if saving_url == 1:
                                        plugintools.log("URL= "+url)
                                        save_url(url, filename)
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue                        
                            
                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR purple][m3u8][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    plugintools.log("URL= "+url)
                                    save_url(url, filename)
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "longurl" , title = '[COLOR red][I]' + '[/I][/COLOR][COLOR white]' + title + ' [COLOR blue][HTTP][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
              
                if data.startswith("rtmp") == True or data.startswith("rtsp") == True:
                    url = data
                    url = parse_url(url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            params["url"] = url
                            server_rtmp(params)                      
                            server = params.get("server")
                            plugintools.log("params en simpletv" +repr(params) )
                            url = params.get("url")
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + titulo + '[COLOR green] [' + server + '][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = params.get("url") ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            params["server"] = server
                            print url                        
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            params["url"] = url
                            server_rtmp(params)                         
                            server = params.get("server")
                            plugintools.log("params en simpletv" +repr(params) )
                            plugintools.log("fanart= "+fanart)
                            url = params.get("url")
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR green] [' + server + '][/COLOR]' , url = params.get("url") ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            print url                        
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            params["url"] = url
                            server_rtmp(params)                        
                            server = params.get("server")
                            plugintools.log("params en simpletv" +repr(params) )
                            url = params.get("url")                        
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + titulo + '[COLOR green] [' + server + '][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = params.get("url") ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            print url                        
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            params["url"] = url
                            server_rtmp(params)                         
                            server = params.get("server")
                            plugintools.log("fanart= "+fanart)
                            plugintools.log("params en simpletv" +repr(params) )
                            url = params.get("url")                       
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + title + '[COLOR green] ['+ server + '][/COLOR]' , url = params.get("url") ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            print url
                            data = file.readline()
                            i = i + 1
                            continue

                if data.startswith("udp") == True or data.startswith("rtp") == True:
                    # print "udp"
                    url = data
                    url = parse_url(url)
                    plugintools.log("url retornada= "+url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [UDP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [UDP][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [UDP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR red] [UDP][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                if data.startswith("mms") == True or data.startswith("rtp") == True:
                    # print "udp"
                    url = data
                    url = parse_url(url)
                    plugintools.log("url retornada= "+url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [MMS][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [MMS][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [MMS][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR red] [MMS][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue                      

                if data.startswith("plugin") == True:
                    title = title.split('"')
                    title = title[0]
                    title = title.strip()
                    title = title.replace("#EXTINF:-1,", "")
                    url = data
                    url = url.strip()

                    if url.find("youtube") >= 0 :
                        if cat != "":                      
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                            
                        
                    elif url.find("mode=1") >= 0 :
                        if cat != "":
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue] [Acestream][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lightblue] [Acestream][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR lightblue] [Acestream][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightblue] [Acestream][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                            
                        
                    elif url.find("mode=2") >= 0 :
                        if cat != "":
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR darkorange] [Sopcast][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if busqueda == 'search.txt':
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + ' [COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR darkorange] [Sopcast][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                elif data.startswith("magnet") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            url = urllib.quote_plus(data)
                            title = parser_title(title)
                            #plugin://plugin.video.stream/play/<URL_ENCODED_LINK>
                            url = 'plugin://plugin.video.torrentin/?uri=' + url
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orangered] [Torrent][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_url(url, filename)
                            data = file.readline()
                            i = i + 1
                            continue

                        else:
                            #plugin://plugin.video.stream/play/<URL_ENCODED_LINK>
                            data = data.strip()
                            url = urllib.quote_plus(data).strip()                      
                            title = parser_title(title)
                            url = 'plugin://plugin.video.torrentin/?uri=' + url
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR orangered][Torrent][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_url(url, filename)
                            data = file.readline()
                            i = i + 1
                            continue

                    else:
                        if busqueda == 'search.txt':
                            #plugin://plugin.video.stream/play/<URL_ENCODED_LINK>
                            url = urllib.quote_plus(data)
                            url = 'plugin://plugin.video.torrentin/?uri=' + url                            
                            title = parser_title(title)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orangered] [Torrent][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_url(url, filename)
                            data = file.readline()
                            i = i + 1
                            continue

                        else:
                            title = parser_title(title)
                            data = data.strip()
                            url = urllib.quote_plus(data)
                            url = 'plugin://plugin.video.torrentin/?uri=' + url
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR orangered][Torrent][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_url(url, filename)
                            data = file.readline()
                            i = i + 1
                            continue

                        
                elif data.startswith("sop") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            url = url.strip()
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR darkorange][Sopcast][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR darkorange] [Sopcast][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name='
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR darkorange][Sopcast][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue                        

                elif data.startswith("ace") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title = parser_title(title)
                            title = title.strip()
                            title_fixed = title.replace(" ", "+")
                            url = data.replace("ace:", "")
                            url = url.strip()
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name=' + title_fixed
                            plugintools.add_item(action="play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue][Acestream][/COLOR] [COLOR lightblue][I](' + origen + ')[/COLOR][/I]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            print 'data',data
                            url = data.replace("ace:", "")
                            url = url.strip()
                            print 'url',url
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
                            plugintools.add_item(action="play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue][Acestream][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title = parser_title(title)
                            url = data.replace("ace:", "")
                            url = url.strip()
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
                            plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR lightblue][Acestream][/COLOR] [COLOR lightblue][I](' + origen + ')[/COLOR][/I]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            print 'data',data
                            url = data.replace("ace:", "")
                            url = url.strip()
                            print 'url',url
                            url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
                            plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR lightblue][Acestream][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue                        
                
                # Youtube playlist & channel    
                elif data.startswith("yt") == True:
                    if data.startswith("yt_playlist") == True:
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            youtube_playlist = data.replace("yt_playlist(", "")
                            youtube_playlist = youtube_playlist.replace(")", "")
                            plugintools.log("youtube_playlist= "+youtube_playlist)
                            url = 'http://gdata.youtube.com/feeds/api/playlists/' + youtube_playlist
                            plugintools.add_item( action = "youtube_videos" , title = '[[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Playlist][/COLOR] [I][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_url(url, filename)
                            data = file.readline()
                            i = i + 1
                            continue

                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            plugintools.log("title= "+title)
                            youtube_playlist = data.replace("yt_playlist(", "")
                            youtube_playlist = youtube_playlist.replace(")", "")
                            plugintools.log("youtube_playlist= "+youtube_playlist)                    
                            url = 'http://gdata.youtube.com/feeds/api/playlists/' + youtube_playlist
                            plugintools.add_item( action = "youtube_videos" , title = '[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Playlist][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_url(url, filename)
                            data = file.readline()
                            i = i + 1
                            continue
                 

                    elif data.startswith("yt_channel") == True:
                        if busqueda == 'search.txt':
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            youtube_channel = data.replace("yt_channel(", "")
                            youtube_channel = youtube_channel.replace(")", "")
                            plugintools.log("youtube_user= "+youtube_channel)
                            url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_channel + '/playlists?v=2&start-index=1&max-results=30'
                            plugintools.add_item( action = "youtube_playlists" , title = '[[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Channel][/COLOR] [I][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_url(url, filename)
                            data = file.readline()
                            i = i + 1
                            continue

                        else:
                            title = title.split('"')
                            title = title[0]
                            title = title.replace("#EXTINF:-1,", "")
                            plugintools.log("title= "+title)
                            youtube_channel = data.replace("yt_channel(", "")
                            youtube_channel = youtube_channel.replace(")", "")
                            youtube_channel = youtube_channel.strip()                 
                            url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_channel + '/playlists?v=2&start-index=1&max-results=30'
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "youtube_playlists" , title = '[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Channel][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                plugintools.log("URL= "+url)
                                save_url(url, filename)
                            data = file.readline()
                            i = i + 1
                            continue

                        
                elif data.startswith("m3u") == True:
                    if busqueda == 'search.txt':
                        url = data.replace("m3u:", "")
                        plugintools.add_item( action = "getfile_http" , title = title + ' [I][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                        if saving_url == 1:
                            plugintools.log("URL= "+url)
                            save_url(url, filename)
                        data = file.readline()
                        i = i + 1
                        continue

                    else:
                        url = data.replace("m3u:", "")
                        plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR orange][Lista [B]M3U[/B]][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                        if saving_url == 1:
                            plugintools.log("URL= "+url)
                            save_url(url, filename)
                        data = file.readline()
                        i = i + 1
                        continue


                elif data.startswith("plx") == True:
                    if busqueda == 'search.txt':
                        url = data.replace("plx:", "")
                        # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)
                        plugintools.add_item( action = "plx_items" , plot = "" , title = title + ' [I][/COLOR][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                        if saving_url == 1:
                            plugintools.log("URL= "+url)
                            save_url(url, filename)
                        data = file.readline()
                        i = i + 1
                        continue

                    else:
                        url = data.replace("plx:", "")
                        # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)
                        plugintools.add_item( action = "plx_items" , plot = "" , title = title + ' [COLOR orange][Lista [B]PLX[/B]][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                        if saving_url == 1:
                            plugintools.log("URL= "+url)
                            save_url(url, filename)
                        data = file.readline()
                        i = i + 1
                        continue

                
            else:
                data = file.readline()
                i = i + 1
                continue

        else:
            data = file.readline()
            i = i + 1
            

    file.close()
    if title == 'search.txt':
        os.remove(tmp + title)


           
def myplaylists_m3u (params):  # Mis listas M3U
    plugintools.log("[latinototal-0.1.0].myplaylists_m3u "+repr(params))
    thumbnail = params.get("thumbnail")
    plugintools.add_item(action="play" , title = "[COLOR red][B][Tutorial][/B][COLOR lightyellow]: [/COLOR][COLOR blue][I][Youtube][/I][/COLOR]" , thumbnail = art + "icon.png" , url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=8i0KouM-4-U" , folder = False , isPlayable = True )
    plugintools.add_item(action="search_channel" , title = "[B][COLOR lightyellow]Buscador de canales[/COLOR][/B][COLOR lightblue][I] Nuevo![/I][/COLOR]" , thumbnail = art + "search.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows

    # Control paternal
    pekes_no = plugintools.get_setting("pekes_no")
    
    for entry in ficheros:
        plot = entry.split(".")        
        plot = plot[0]
        plugintools.log("entry= "+entry)

        if pekes_no == "true" :
            print "Control paternal en marcha"
            if entry.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")
                
            else:                
                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = playlists + entry , thumbnail = art + 'plx3.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
                    
                if entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
                        
                if entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="simpletv_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                if entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
 
        else:
        
                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = playlists + entry , thumbnail = art + 'plx3.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
                    
                if entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
                        
                if entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="simpletv_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                if entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )



                

def playlists_m3u(params):  # Biblioteca online
    plugintools.log("[latinototal-0.1.0].playlists_m3u "+repr(params))
    data = plugintools.read( params.get("url") )
    name_channel = params.get("plot")
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    online = '[COLOR yellowgreen][I][Auto][/I][/COLOR]'
    params["ext"] = 'm3u'
    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR] - [B][I][COLOR lightyellow]latinototal19@gmail.com [/COLOR][/B][/I]' , thumbnail= art + 'icon.png' , folder = False , isPlayable = False )    
    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    # Sustituir por una lista!!!
    for biny, ciny, diny, winy, pixy, dixy, boxy in subchannel:
        if ciny == "Vcx7 IPTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            params["ext"] = "m3u"
            title = ciny
            params["title"]=title
        elif ciny == "Largo Barbate M3U":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "XBMC Mexico":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "allSat":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "AND Wonder":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "FenixTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        else:
            plot = ciny.split("[")
            plot = plot[0]
            plugintools.add_item( action="getfile_http" , plot = plot , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )



    plugintools.log("[latinototal-0.1.0].playlists_m3u "+repr(params))

    
        
def getfile_http(params):  # Descarga de lista M3U + llamada a simpletv_items para que liste los items
    plugintools.log("[latinototal-0.1.0].getfile_http "+repr(params))
    url = params.get("url")
    params["ext"] = "m3u"
    getfile_url(params)
    simpletv_items(params)
   
    
def parse_url(url):
    # plugintools.log("url entrante= "+url)

    if url != "":
        url = url.strip()
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")        
        return url
    
    else:
        plugintools.log("error en url= ")  # Mostrar diálogo de error al parsear url (por no existir, por ejemplo)

        
                    
def getfile_url(params):
    plugintools.log("[latinototal-0.1.0].getfile_url " +repr(params))
    ext = params.get("ext")
    title = params.get("title")

    if ext == 'plx':
        filename = parser_title(title)
        params["plot"]=filename
        filename = title + ".plx"  # El título del archivo con extensión (m3u, p2p, plx)
    elif ext == 'm3u':
        filename = params.get("plot")
        # Vamos a quitar el formato al texto para que sea el nombre del archivo
        filename = parser_title(title)
        filename = filename + ".m3u"  # El título del archivo con extensión (m3u, p2p, plx)
    else:
        ext == 'p2p'
        filename = parser_title(title)
        filename = filename + ".p2p"  # El título del archivo con extensión (m3u, p2p, plx)
        
    if filename.endswith("plx") == True :
        filename = parser_title(filename)

    plugintools.log("filename= "+filename)
    url = params.get("url")
    plugintools.log("url= "+url)
    
    try:
        response = urllib2.urlopen(url)
        body = response.read()
    except:
        # Control si la lista está en el cuerpo del HTTP
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)

    #open the file for writing
    fh = open(playlists + filename, "wb")

    # read from request while writing to file
    fh.write(body)

    fh.close()

    file = open(playlists + filename, "r")
    file.seek(0)
    data = file.readline()
    data = data.strip()

    lista_items = {'linea': data}
    file.seek(0)
    lista_items = {'plot': data}
    file.seek(0)
    


def header_xml(params):
    plugintools.log("[latinototal-0.1.0].header_xml "+repr(params))

    url = params.get("url")
    params.get("title")
    data = plugintools.read(url)
    # plugintools.log("data= "+data)
    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    author = author.strip()
    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')
    message = plugintools.find_single_match(data, '<message>(.*?)</message>')
    desc = plugintools.find_single_match(data, '<description>(.*?)</description>')
    thumbnail = plugintools.find_single_match(data, '<thumbnail>(.*?)</thumbnail>')
    
    if author != "":
        if message != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR][I] ' + message + '[/I]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
    else:
        if desc != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + desc + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            return fanart


def search_channel(params):
    plugintools.log("[latinototal-0.1.0].search " + repr(params))

    buscar = params.get("plot")
    # plugintools.log("buscar texto: "+buscar)
    if buscar == "":
        last_search = plugintools.get_setting("last_search")
        texto = plugintools.keyboard_input(last_search)
        plugintools.set_setting("last_search",texto)
        params["texto"]=texto
        texto = texto.lower()
        cat = ""
        if texto == "":
            errormsg = plugintools.message("latinototal","Por favor, introduzca el canal a buscar")
            return errormsg
        
    else:
        texto = buscar
        texto = texto.lower()
        plugintools.log("texto a buscar= "+texto)
        cat = ""
    
    results = open(tmp + 'search.txt', "wb")
    results.seek(0)
    results.close()

    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    
    for entry in ficheros:
        if entry.endswith("m3u") == True:
            print "Archivo tipo m3u"
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            filename = plot + '.m3u'
            plugintools.log("Archivo M3U: "+filename)
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            print num_items
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)
            data = arch.readline()
            data = data.strip()
            plugintools.log("data linea= "+data)
            texto = texto.strip()
            plugintools.log("data_antes= "+data)
            plugintools.log("texto a buscar= "+texto)

            data = arch.readline()
            data = data.strip()
            i = i + 1 
            while i <= num_items :
                if data.startswith('#EXTINF:-1') == True:
                    data = data.replace('#EXTINF:-1,', "")  # Ignoramos la primera parte de la línea
                    data = data.replace(",", "")
                    title = data.strip()  # Ya tenemos el título
                                   
                    if data.find('$ExtFilter="') >= 0:
                        data = data.replace('$ExtFilter="', "")

                    if data.find(' $ExtFilter="') >= 0:
                        data = data.replace('$ExtFilter="', "")

                    title = title.replace("-AZBOX*", "")
                    title = title.replace("AZBOX *", "")                        
                        
                    images = m3u_items(title)
                    print 'images',images
                    thumbnail = images[0]
                    fanart = images[1]
                    cat = images[2]
                    title = images[3]
                    plugintools.log("title= "+title)
                    minus = title.lower()                    
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1                   

                    if minus.find(texto) >= 0:
                    # if re.match(texto, title, re.IGNORECASE):
                        # plugintools.log("Concidencia hallada. Obtenemos url del canal: " + texto)
                        if data.startswith("http") == True:
                            url = data.strip()
                            if cat != "":  # Controlamos el caso de subcategoría de canales
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()                            
                                data = arch.readline()
                                i = i + 1                             
                                continue
                            else:
                                results = open(tmp + 'search.txt', "a")                                
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("rtmp") == True:
                            url = data
                            url = parse_url(url)
                            if cat != "":   # Controlamos el caso de subcategoría de canales
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:                            
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("yt") == True:
                            print "CORRECTO"
                            url = data
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        
                else:
                    data = arch.readline()
                    data = data.strip()
                    plugintools.log("data_buscando_title= "+data)
                    i = i + 1
                        
            else:
                data = arch.readline()
                data = data.strip()
                plugintools.log("data_final_while= "+data)
                i = i + 1
                continue
                    


    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    
    for entry in ficheros:
        if entry.endswith('p2p') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.p2p'
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            plugintools.log("archivo= "+filename)
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)            
            while i <= num_items:
                data = arch.readline()
                data = data.strip()
                title = data
                texto = texto.strip()
                plugintools.log("linea a buscar title= "+data)
                i = i + 1

                if data.startswith("#") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data.startswith("default=") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data.startswith("art=") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue                 
                
                if data != "":
                    title = data.strip()  # Ya tenemos el título
                    plugintools.log("title= "+title)
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        plugintools.log("title= "+title)
                        data = arch.readline()
                        i = i + 1
                        #print i
                        plugintools.log("linea a comprobar url= "+data)
                        if data.startswith("sop") == True:
                            # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                            title_fixed = title.replace(" " , "+")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name=' + title_fixed
                            url = url.strip()
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.startswith("magnet") == True:                            
                            # magnet:?xt=urn:btih:6CE983D676F2643430B177E2430042E4E65427...
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            plugintools.log("title magnet= "+title)
                            url = data
                            plugintools.log("url magnet= "+url)
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.find("://") == -1:
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            title_fixed = title.replace(" " , "+")
                            url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=1&name=' + title_fixed
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                    else:
                        plugintools.log("no coinciden titulo y texto a buscar")

                
    for entry in ficheros:
        if entry.endswith('plx') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.plx'
            plugintools.log("archivo PLX: "+filename)
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            print num_items
            i = 0
            arch.seek(0)
            while i <= num_items:
                data = arch.readline()
                data = data.strip()                
                i = i + 1
                print i
                
                if data.startswith("#") == True:
                    continue

                if (data == 'type=video') or (data == 'type=audio') == True:
                    data = arch.readline()
                    i = i + 1
                    print i
                    data = data.replace("name=", "")
                    data = data.strip()
                    title = data
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        plugintools.log("Título coincidente= "+title)
                        data = arch.readline()
                        plugintools.log("Siguiente linea= "+data)
                        i = i + 1
                        print i
                        print "Analizamos..."
                        while data <> "" :
                            if data.startswith("thumb") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue
                            
                            if data.startswith("date") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue
                            
                            if data.startswith("background") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue
                            
                            if data.startswith("URL") == True:
                                data = data.replace("URL=", "")
                                data = data.strip()
                                url = data
                                parse_url(url)
                                plugintools.log("URL= "+url)
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                break                                

                            

                      
    arch.close()
    results.close()
    params["plot"] = 'search'  # Pasamos a la lista de variables (params) el valor del archivo de resultados para que lo abra la función simpletv_items
    params['texto']= texto  # Agregamos al diccionario una nueva variable que contiene el texto a buscar
    simpletv_items(params)
    



def agendatv(params):
    plugintools.log("[latinototal-0.1.0].agendatv "+repr(params))

    hora_partidos = []
    lista_equipos=[]
    campeonato=[]
    canales=[]

    url = params.get("url")        
    data = plugintools.read(url)
    plugintools.log("data= "+data)
	    
    matches = plugintools.find_multiple_matches(data,'<tr>(.*?)</tr>')
    horas = plugintools.find_multiple_matches(data, 'color=#990000>(.*?)</td>')
    txt = plugintools.find_multiple_matches(data, 'color="#000099"><b>(.*?)</td>')
    tv = plugintools.find_multiple_matches(data, '<td align="left"><font face="Verdana, Arial, Helvetica, sans-serif" size="1" ><b>([^<]+)</b></font></td>')

    # <b><a href="indexf.php?comp=Súper Final Argentino">Súper Final Argentino&nbsp;&nbsp;</td>    
    for entry in matches:
        torneo = plugintools.find_single_match(entry, '<a href=(.*?)">')
        torneo = torneo.replace("&nbsp;&nbsp;", "")
        torneo = torneo.replace("indexf.php?comp=", "")
        torneo = torneo.replace('>', "")
        torneo = torneo.replace('"', "")
        torneo = torneo.replace("\n", "")
        torneo = torneo.strip()
        torneo = torneo.replace('\xfa', 'ú')
        torneo = torneo.replace('\xe9', 'é')
        torneo = torneo.replace('\xf3', 'ó')
        torneo = torneo.replace('\xfa', 'ú')
        torneo = torneo.replace('\xaa', 'ª')
        torneo = torneo.replace('\xe1', 'á')
        torneo = torneo.replace('\xf1', 'ñ')
        torneo = torneo.replace('indexuf.php?comp=', "")
        torneo = torneo.replace('indexfi.php?comp=', "")
        plugintools.log("string encoded= "+torneo)
        if torneo != "":
            plugintools.log("torneo= "+torneo)
            campeonato.append(torneo)                    

    # ERROR! Hay que añadir las jornadas, tal como estaba antes!!

    # Vamos a crear dos listas; una de los equipos que se enfrentan cada partido y otra de las horas de juego
    
    for dato in txt:
        lista_equipos.append(dato)
        
    for tiempo in horas:
        hora_partidos.append(tiempo)

    # <td align="left"><font face="Verdana, Arial, Helvetica, sans-serif" size="1" ><b>&nbsp;&nbsp; Canal + Fútbol</b></font></td>
    # <td align="left"><font face="Verdana, Arial, Helvetica, sans-serif" size="1" ><b>&nbsp;&nbsp; IB3</b></font></td>

    for kanal in tv:
        kanal = kanal.replace("&nbsp;&nbsp;", "")
        kanal = kanal.strip()
        kanal = kanal.replace('\xfa', 'ú')
        kanal = kanal.replace('\xe9', 'é')
        kanal = kanal.replace('\xf3', 'ó')
        kanal = kanal.replace('\xfa', 'ú')
        kanal = kanal.replace('\xaa', 'ª')
        kanal = kanal.replace('\xe1', 'á')
        kanal = kanal.replace('\xf1', 'ñ')
        canales.append(kanal)

        
    print lista_equipos
    print hora_partidos  # Casualmente en esta lista se nos ha añadido los días de partido
    print campeonato
    print canales
    
    i = 0       # Contador de equipos
    j = 0       # Contador de horas
    k = 0       # Contador de competición
    max_equipos = len(lista_equipos) - 2
    print max_equipos
    for entry in matches:
        while j <= max_equipos:
            # plugintools.log("entry= "+entry)
            fecha = plugintools.find_single_match(entry, 'color=#990000><b>(.*?)</b></td>')
            fecha = fecha.replace("&#225;", "á")
            fecha = fecha.strip()
            gametime = hora_partidos[i]
            gametime = gametime.replace("<b>", "")
            gametime = gametime.replace("</b>", "")
            gametime = gametime.strip()
            gametime = gametime.replace('&#233;', 'é')
            gametime = gametime.replace('&#225;', 'á')
            gametime = gametime.replace('&#233;', 'é')
            gametime = gametime.replace('&#225;', 'á')  
            print gametime.find(":")
            if gametime.find(":") == 2:
                i = i + 1
                #print i
                local = lista_equipos[j]
                local = local.strip()
                local = local.replace('\xfa', 'ú')
                local = local.replace('\xe9', 'é')
                local = local.replace('\xf3', 'ó')
                local = local.replace('\xfa', 'ú')
                local = local.replace('\xaa', 'ª')
                local = local.replace('\xe1', 'á')
                local = local.replace('\xf1', 'ñ')
                j = j + 1
                print j
                visitante = lista_equipos[j]
                visitante = visitante.strip()
                visitante = visitante.replace('\xfa', 'ú')
                visitante = visitante.replace('\xe9', 'é')
                visitante = visitante.replace('\xf3', 'ó')
                visitante = visitante.replace('\xfa', 'ú')
                visitante = visitante.replace('\xaa', 'ª')
                visitante = visitante.replace('\xe1', 'á')
                visitante = visitante.replace('\xf1', 'ñ')
                local = local.replace('&#233;', 'é')
                local = local.replace('&#225;', 'á')  
                j = j + 1
                print j
                tipo = campeonato[k]
                channel = canales[k]
                channel = channel.replace('\xfa', 'ú')
                channel = channel.replace('\xe9', 'é')
                channel = channel.replace('\xf3', 'ó')
                channel = channel.replace('\xfa', 'ú')
                channel = channel.replace('\xaa', 'ª')
                channel = channel.replace('\xe1', 'á')
                channel = channel.replace('\xf1', 'ñ')
                channel = channel.replace('\xc3\xba', 'ú')
                channel = channel.replace('Canal +', 'Canal+')
                title = '[B][COLOR khaki]' + tipo + ':[/B][/COLOR] ' + '[COLOR lightyellow]' + '(' + gametime + ')[COLOR white]  ' + local + ' vs ' + visitante + '[/COLOR][COLOR lightblue][I] (' + channel + ')[/I][/COLOR]'
                plugintools.add_item(plot = channel , action="contextMenu", title=title , url = "", fanart = art + 'agendatv.jpg', thumbnail = art + 'icon.png' , folder = True, isPlayable = False)
                # diccionario[clave] = valor
                plugintools.log("channel= "+channel)
                params["plot"] = channel
                # plugintools.add_item(plot = channel , action = "search_channel", title = '[COLOR lightblue]' + channel + '[/COLOR]', url= "", thumbnail = art + 'icon.png', fanart = fanart , folder = True, isPlayable = False)
                k = k + 1
                print k
                plugintools.log("title= "+title)
            else:
                plugintools.add_item(action="", title='[B][COLOR red]' + gametime + '[/B][/COLOR]', thumbnail = art + 'icon.png' , fanart = art + 'agendatv.jpg' , folder = True, isPlayable = False)
                i = i + 1
        


def encode_string(url):
    

    d = {    '\xc1':'A',
            '\xc9':'E',
            '\xcd':'I',
            '\xd3':'O',
            '\xda':'U',
            '\xdc':'U',
            '\xd1':'N',
            '\xc7':'C',
            '\xed':'i',
            '\xf3':'o',
            '\xf1':'n',
            '\xe7':'c',
            '\xba':'',
            '\xb0':'',
            '\x3a':'',
            '\xe1':'a',
            '\xe2':'a',
            '\xe3':'a',
            '\xe4':'a',
            '\xe5':'a',
            '\xe8':'e',
            '\xe9':'e',
            '\xea':'e',       
            '\xeb':'e',       
            '\xec':'i',
            '\xed':'i',
            '\xee':'i',
            '\xef':'i',
            '\xf2':'o',
            '\xf3':'o',
            '\xf4':'o',   
            '\xf5':'o',
            '\xf0':'o',
            '\xf9':'u',
            '\xfa':'u',
            '\xfb':'u',               
            '\xfc':'u',
            '\xe5':'a'       
    }
   
    nueva_cadena = url
    for c in d.keys():
        plugintools.log("caracter= "+c)
        nueva_cadena = nueva_cadena.replace(c,d[c])

    auxiliar = nueva_cadena.encode('utf-8')
    url = nueva_cadena
    return nueva_cadena



def plx_items(params):
    plugintools.log("[latinototal-0.1.0].plx_items" +repr(params))

    fanart = ""
    thumbnail = ""

    # Control para elegir el título (plot, si formateamos el título / title , si no existe plot)
    if params.get("plot") == "":
        title = params.get("title").strip() + '.plx'
        title = parser_title(title)
        title = title.strip()
        filename = title
        params["plot"]=filename
        params["ext"] = 'plx'
        getfile_url(params)
        title = params.get("title")
    else:
        title = params.get("plot")
        title = title.strip()
        title = parser_title(title)        
        plugintools.log("Lectura del archivo PLX")

    title = title.replace(" .plx", ".plx")
    title = title.strip()
    file = open(playlists + parser_title(title) + '.plx', "r")
    file.seek(0)
    num_items = len(file.readlines())
    print num_items
    file.seek(0)    
        
    # Lectura del título y fanart de la lista
    background = art + 'fanart.jpg'
    logo = art + 'plx3.png'
    file.seek(0)
    data = file.readline()
    while data <> "":        
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            background = data.strip()
            plugintools.log("background= "+background)
            if background == "":
                background = params.get("extra")
                if background == "":
                    background = art + 'fanart.jpg'
                    
            data = file.readline()
            continue

        if data.startswith("title=") == True:
            name = data.replace("title=", "")
            name = name.strip()
            plugintools.log("name= "+name)
            if name == "Select sort order for this list":
                name = "Seleccione criterio para ordenar ésta lista... "             
            data = file.readline()
            continue

        if data.startswith("logo=") == True:
            data = data.replace("logo=", "")
            logo = data.strip()
            plugintools.log("logo= "+logo)
            title = parser_title(title)
            if thumbnail == "":
                thumbnail = art + 'plx3.png'

            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title + '[/B][/I][/COLOR]', url = playlists + title , thumbnail = logo , fanart = background , folder = False , isPlayable = False)
            plugintools.log("fanart= "+fanart)
            plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = logo , fanart = background , folder = False , isPlayable = False)                
                
            data = file.readline()
            break

        else:
            data = file.readline()

         
    try:        
        data = file.readline()
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            data = data.strip()
            fanart = data
            background = fanart
            plugintools.log("fanart= "+fanart)
        else:
            # data = file.readline()
            if data.startswith("background=") == True:
                print "Archivo plx!"
                data = data.replace("background=", "")
                fanart = data.strip()
                plugintools.log("fanart= "+fanart)
            else:
                if data.startswith("title=") == True:
                    name = data.replace("title=", "")
                    name = name.strip()
                    plugintools.log("name= "+name)
    except:
        plugintools.log("ERROR: Unable to load PLX file")


    data = file.readline()
    try:
        if data.startswith("title=") == True:
            data = data.replace("title=", "")
            name = data.strip()            
            plugintools.log("title= "+title)
            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , thumbnail = logo , fanart = fanart , folder = False , isPlayable = False)
            plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = art + "icon.png" , fanart = fanart , folder = False , isPlayable = False)
    except:
        plugintools.log("Unable to read PLX title")

         
    # Lectura de items

    i = 0
    file.seek(0)
    while i <= num_items:
        data = file.readline()
        data = data.strip()
        i = i + 1
        print i
        
        if data.startswith("#") == True:
            continue
        elif data.startswith("rating") == True:
            continue
        elif data.startswith("description") == True:
            continue

        if (data == 'type=comment') == True:
            data = file.readline()
            i = i + 1
            print i
            
            while data <> "" :
                if data.startswith("name") == True:
                    title = data.replace("name=", "")
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                
                elif data.startswith("thumb") == True:
                    data = data.replace("thumb=", "")
                    data = data.strip()
                    thumbnail = data
                    if thumbnail == "":
                        thumbnail = logo
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                
                elif data.startswith("background") == True:
                    data = data.replace("background=", "")
                    fanart = data.strip()
                    if fanart == "":
                        fanart = background
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
            
            plugintools.add_item(action="", title = title , url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
        
        if (data == 'type=video') or (data == 'type=audio') == True:
            data = file.readline()
            i = i + 1
            print i
            
            while data <> "" :
                if data.startswith("#") == True:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("description") == True:                    
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("rating") == True:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("name") == True:
                    data = data.replace("name=", "")
                    data = data.strip()
                    title = data
                    if title == "[COLOR=FF00FF00]by user-assigned order[/COLOR]" :
                        title = "Seleccione criterio para ordenar ésta lista... "

                    if title == "by user-assigned order" :
                        title = "Según se han agregado en la lista"
                    
                    if title == "by date added, oldest first" :
                        title = "Por fecha de agregación, las más antiguas primero"
                        
                    if title == "by date added, newest first" :
                        title = "Por fecha de agregación, las más nuevas primero"
                        
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                elif data.startswith("thumb") == True:
                    data = data.replace("thumb=", "")
                    data = data.strip()
                    thumbnail = data
                    if thumbnail == "":
                        thumbnail = logo
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("date") == True:
                    data = file.readline()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("background") == True:
                    data = data.replace("background=", "")
                    fanart = data.strip()
                    if fanart == "":
                        fanart = background
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                
                elif data.startswith("URL") == True:
                    # Control para el caso de que no se haya definido fanart en cada entrada de la lista => Se usa el fanart general
                    if fanart == "":
                        fanart = background
                    data = data.replace("URL=", "")
                    data = data.strip()
                    url = data
                    parse_url(url)
                    if url.startswith("yt_channel") == True:
                        youtube_channel = url.replace("yt_channel(", "")
                        youtube_channel = youtube_channel.replace(")", "")
                        url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_channel + '/playlists?v=2&start-index=1&max-results=30'
                        plugintools.add_item(action="youtube_playlists" , title = title + ' [[COLOR red]You[COLOR white]tube Channel][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)
                        break
                    
                    elif url.startswith("yt_playlist") == True:
                        youtube_playlist = url.replace("yt_playlist(", "")
                        youtube_playlist = youtube_playlist.replace(")", "")
                        plugintools.log("youtube_playlist= "+youtube_playlist)
                        url = 'http://gdata.youtube.com/feeds/api/playlists/' + youtube_playlist + '?v=2'
                        plugintools.add_item( action = "youtube_videos" , title = title + ' [COLOR red][You[COLOR white]tube Playlist][/COLOR] [I][COLOR lightblue][/I][/COLOR]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        break
                    # Sintaxis yt(...) a extinguir pero mantengo por Darío:
                    elif url.startswith("yt") == True:
                        url = url.replace("yt(", "")
                        youtube_user = url.replace(")", "")
                        url = 'http://gdata.youtube.com/feeds/api/users/' + youtube_user + '/playlists?v=2&start-index=1&max-results=30'
                        plugintools.log("URL= "+url)
                        plugintools.log("FANART = "+fanart)                        
                        plugintools.add_item(action="youtube_playlists" , title = title + ' [COLOR red][You[COLOR white]tube Playlist][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)
                        break

                    elif url.startswith("serie") == True:
                        url = url.replace("serie:", "")                        
                        plugintools.log("URL= "+url)
                        plugintools.log("FANART = "+fanart)                       
                        plugintools.add_item(action="seriecatcher" , title = title + ' [COLOR purple][Serie online][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , extra = fanart , folder = True , isPlayable = False)
                        break                    

                    elif url.startswith("http") == True:
                        if url.find("allmyvideos") >= 0:
                            plugintools.add_item(action="allmyvideos" , title = title + ' [COLOR lightyellow][Allmyvideos][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break
                    
                        elif url.find("streamcloud") >= 0:
                            plugintools.add_item(action="streamcloud" , title = title + ' [COLOR lightskyblue][Streamcloud][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)                            
                            break
                        
                        elif url.find("played.to") >= 0:
                            plugintools.add_item(action="playedto" , title = title + ' [COLOR lavender][Played.to][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break
                        
                        elif url.find("vidspot") >= 0:
                            plugintools.add_item(action="vidspot" , title = title + ' [COLOR palegreen][Vidspot][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break
                        
                        elif url.find("vk.com") >= 0:
                            plugintools.add_item(action="vk" , title = title + ' [COLOR royalblue][Vk][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break

                        if url.find("nowvideo") >= 0:
                            plugintools.add_item(action="nowvideo" , title = title + ' [COLOR red][Nowvideo][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        if url.find("tumi.tv") >= 0:
                            plugintools.add_item(action="tumi" , title = title + ' [COLOR forestgreen][Tumi][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        if url.find("streamin.to") >= 0:
                            plugintools.add_item(action="streaminto" , title = title + ' [COLOR forestgreen][streamin.to][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break                         

                        elif url.endswith("flv") == True:
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)                            
                            plugintools.add_item( action = "play" , title = title + ' [COLOR cyan][Flash][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            break

                        elif url.endswith("m3u8") == True:
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)                            
                            plugintools.add_item( action = "play" , title = title + ' [COLOR purple][m3u8][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            break

                        elif url.find("youtube.com") >= 0:
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            videoid = url.replace("https://www.youtube.com/watch?v=", "")
                            url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoid
                            plugintools.add_item( action = "play" , title = title + ' [[COLOR red]You[COLOR white]tube Video][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            break                        
                        
                        else:
                            plugintools.log("URL= "+url)
                            plugintools.add_item( action = "play" , title = title + ' [COLOR white][HTTP][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            break
                    
                    elif url.startswith("rtmp") == True:
                        params["url"] = url
                        server_rtmp(params)                         
                        server = params.get("server")                        
                        url = params.get("url")                       
                        plugintools.add_item( action = "launch_rtmp" , title = title + '[COLOR green] [' + server + '][/COLOR]' , url = params.get("url") ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        break
                    
                    elif url.startswith("plugin") == True:
                        if url.find("plugin.video.youtube") >= 0:
                            plugintools.log("URL= "+url)                            
                            plugintools.add_item( action = "play" , title = title + ' [COLOR white] [[COLOR red]You[COLOR white]tube Video][/COLOR][/COLOR]' , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            break
                        if url.find("plugin.video.p2p-streams") >= 0:
                            if url.find("mode=1") >= 0:
                                title = parser_title(title)
                                url = url.strip()
                                plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            elif url.find("mode=2") >= 0:
                                title = parser_title(title)
                                url = url.strip()
                                plugintools.add_item(action="play" , title = title_fixed + ' [COLOR lightblue][Sopcast][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            
                    elif url.startswith("sop") == True:
                        # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                        title = parser_title(title)
                        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=2&name='
                        url = url.strip()
                        plugintools.add_item(action="play" , title = title + ' [COLOR lightgreen][Sopcast][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                        #print i
                        continue

                    elif url.startswith("ace") == True:
                        title = parser_title(title)
                        url = url.replace("ace:", "")
                        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
                        url = url.strip()
                        plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                        #print i
                        continue                    
                    
                    elif url.startswith("magnet") >= 0:
                        url = urllib.quote_plus(data)
                        title = parser_title(title)
                        url = 'plugin://plugin.video.pulsar/play?uri=' + url
                        plugintools.add_item(action="play" , title = title + ' [COLOR orangered][Torrent][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)

                       
                    else:
                        plugintools.add_item(action="play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        plugintools.log("URL = "+url)
                        break                        
                      
                elif data == "" :                    
                    break
                else:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
   
        if (data == 'type=playlist') == True:
            # Control si no se definió fanart en cada entrada de la lista => Se usa fanart global de la lista
            if fanart == "":
                fanart = background
            data = file.readline()
            i = i + 1
            print i
            while data <> "" :                
                if data.startswith("name") == True :
                    data = data.replace("name=", "")
                    title = data.strip()                    
                    if title == '>>>' :
                        title = title.replace(">>>", "[I][COLOR lightyellow]Siguiente[/I][/COLOR]")
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                        
                    elif title == '<<<' :
                        title = title.replace("<<<", "[I][COLOR lightyellow]Anterior[/I][/COLOR]")
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted by user-assigned order") >= 0:
                        title = "[I][COLOR lightyellow]Ordenar listas por...[/I][/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                        
                    elif title.find("Sorted A-Z") >= 0:
                        title = "[I][COLOR lightyellow][COLOR lightyellow]De la A a la Z[/I][/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1                        
                        
                    elif title.find("Sorted Z-A") >= 0:
                        title = "[I][COLOR lightyellow]De la Z a la A[/I][/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1                         

                    elif title.find("Sorted by date added, newest first") >= 0:
                        title = "Ordenado por: Las + recientes primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1   

                    elif title.find("Sorted by date added, oldest first") >= 0:
                        title = "Ordenado por: Las + antiguas primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1   

                    elif title.find("by user-assigned order") >= 0:
                        title = "[COLOR lightyellow]Ordenar listas por...[/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1                        

                    elif title.find("by date added, newest first") >= 0 :
                        title = "Las + recientes primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                    elif title.find("by date added, oldest first") >= 0 :
                        title = "Las + antiguas primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                        
                elif data.startswith("thumb") == True:
                    data = data.replace("thumb=", "")
                    data = data.strip()
                    thumbnail = data
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                
                elif data.startswith("URL") == True:
                    data = data.replace("URL=", "")
                    data = data.strip()
                    url = data
                    parse_url(url)
                    if url.startswith("m3u") == True:
                        url = url.replace("m3u:", "")
                        plugintools.add_item(action="getfile_http" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)
                    elif url.startswith("plx") == True:
                        url = url.replace("plx:", "")
                        plugintools.add_item(action="plx_items" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)
                    
                elif data == "" :
                    break
                
                else:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue


    file.close()


    # Purga de listas erróneas creadas al abrir listas PLX (por los playlists de ordenación que crea Navixtreme)
    
    if os.path.isfile(playlists + 'Siguiente.plx'):
        os.remove(playlists + 'Siguiente.plx')
        print "Correcto!"
    else:
        pass
    
    if os.path.isfile(playlists + 'Ordenar listas por....plx'):
        os.remove(playlists + 'Ordenar listas por....plx')
        print "Ordenar listas por....plx eliminado!"
        print "Correcto!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'A-Z.plx'):
        os.remove(playlists + 'A-Z.plx')
        print "A-Z.plx eliminado!"         
    else:
        print "No es posible!"        
        pass

    if os.path.isfile(playlists + 'De la A a la Z.plx'):
        os.remove(playlists + 'De la A a la Z.plx')
        print "De la A a la Z.plx eliminado!"         
    else:
        print "No es posible!"        
        pass

    if os.path.isfile(playlists + 'Z-A.plx'):
        os.remove(playlists + 'Z-A.plx')
        print "Z-A.plx eliminado!"         
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'De la Z a la A.plx'):
        os.remove(playlists + 'De la Z a la A.plx')
        print "De la Z a la A.plx eliminado!"         
    else:
        print "No es posible!"        
        pass

    if os.path.isfile(playlists + 'Las + antiguas primero....plx'):
        os.remove(playlists + 'Las + antiguas primero....plx')
        print "Las mÃ¡s antiguas primero....plx eliminado!"         
    else:
        print "No es posible!"        
        pass

    if os.path.isfile(playlists + 'by date added, oldest first.plx'):
        os.remove(playlists + 'by date added, oldest first.plx')
        print "by date added, oldest first.plx eliminado!" 
    else:
        print "No es posible!"        
        pass

    if os.path.isfile(playlists + 'Las + recientes primero....plx'):
        os.remove(playlists + 'Las + recientes primero....plx')     
    else:
        print "No es posible!"        
        pass

    if os.path.isfile(playlists + 'by date added, newest first.plx'):
        os.remove(playlists + 'by date added, newest first.plx')
        print "by date added, newest first.plx eliminado!"        
    else:
        print "No es posible!"        
        pass

    if os.path.isfile(playlists + 'Sorted by user-assigned order.plx'):
        os.remove(playlists + 'Sorted by user-assigned order.plx')
        print "Sorted by user-assigned order.plx eliminado!"
    else:
        print "No es posible!"        
        pass    

    if os.path.isfile(playlists + 'Ordenado por.plx'):
        os.remove(playlists + 'Ordenado por.plx')
        print "Correcto!"        
    else:
        print "No es posible!"        
        pass

    if os.path.isfile(playlists + 'Ordenado por'):
        os.remove(playlists + 'Ordenado por')
        print "Correcto!"        
    else:
        print "No es posible!"        
        pass     



def futbolenlatv(params):
    plugintools.log("[latinototal-0.1.0].futbolenlaTV "+repr(params))

    hora_partidos = []
    lista_equipos=[]
    campeonato=[]
    canales=[]

    url = params.get("url")
    print url
    fecha = get_fecha()
    dia_manana = params.get("plot")
    data = plugintools.read(url)
    
    if dia_manana == "":  # Control para si es agenda de hoy o mañana
        plugintools.add_item(action="", title = '[COLOR green][B]FutbolenlaTV.com[/B][/COLOR] - [COLOR lightblue][I]Agenda para el día '+ fecha + '[/I][/COLOR]', folder = False , isPlayable = False )
    else:
        dia_manana = dia_manana.split("-")
        dia_manana = dia_manana[2] + "/" + dia_manana[1] + "/" + dia_manana[0]
        plugintools.add_item(action="", title = '[COLOR green][B]FutbolenlaTV.com[/B][/COLOR] - [COLOR lightblue][I]Agenda para el día '+ dia_manana + '[/I][/COLOR]', folder = False , isPlayable = False )
        
	    
    bloque = plugintools.find_multiple_matches(data,'<span class="cuerpo-partido">(.*?)</div>')
    for entry in bloque:
        category = plugintools.find_single_match(entry, '<i class=(.*?)</i>')
        category = category.replace("ftvi-", "")
        category = category.replace('comp">', '')
        category = category.replace('"', '')
        category = category.replace("-", " ")
        category = category.replace("Futbol", "Fútbol")
        category = category.strip()
        category = category.capitalize()
        plugintools.log("cat= "+category)
        champ = plugintools.find_single_match(entry, '<span class="com-detalle">(.*?)</span>')
        champ = encode_string(champ)
        champ = champ.strip()
        event = plugintools.find_single_match(entry, '<span class="bloque">(.*?)</span>')
        event = encode_string(event)
        event = event.strip()
        momentum = plugintools.find_single_match(entry, '<time itemprop="startDate" datetime=([^<]+)</time>')
        # plugintools.log("momentum= "+momentum)
        momentum = momentum.split(">")
        momentum = momentum[1]

        gametime = plugintools.find_multiple_matches(entry, '<span class="n">(.*?)</span>')
        for tiny in gametime:
            day = tiny
            month = tiny
            
        sport = plugintools.find_single_match(entry, '<meta itemprop="eventType" content=(.*?)/>')
        sport = sport.replace('"', '')
        sport = sport.strip()
        if sport == "Partido de fútbol":
            sport = "Fútbol"
            
        # plugintools.log("sport= "+sport)
        
        gameday = plugintools.find_single_match(entry, '<span class="dia">(.*?)</span>')

        rivals = plugintools.find_multiple_matches(entry, '<span>([^<]+)</span>([^<]+)<span>([^<]+)</span>')
        rivales = ""
        
        for diny in rivals:
            print diny
            items = len(diny)
            items = items - 1
            i = -1
            diny[i].strip()
            while i <= items:
                if diny[i] == "":
                    del diny[0]
                    i = i + 1
                else:
                    print diny[i]
                    rival = diny[i]                        
                    rival = encode_string(rival)
                    rival = rival.strip()
                    plugintools.log("rival= "+rival)
                    if rival == "-":
                        i = i + 1
                        continue
                    else:
                        if rivales != "":
                            rivales = rivales + " vs " + rival
                            plugintools.log("rivales= "+rivales)
                            break
                        else:
                            rivales = rival
                            plugintools.log("rival= "+rival)
                            i = i + 1


        tv = plugintools.find_single_match(entry, '<span class="hidden-phone hidden-tablet canales"([^<]+)</span>')
        tv = tv.replace(">", "")
        tv = encode_string(tv)                  
        if tv == "":
            continue
        else:
            tv = tv.replace("(Canal+, Astra", "")
            tv = tv.split(",")
            tv_a = tv[0]
            tv_a = tv_a.rstrip()
            tv_a = tv_a.lstrip()
            tv_a = tv_a.replace(")", "")
            plugintools.log("tv_a= "+tv_a)
            print len(tv)
            if len(tv) == 2:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                   
                tv = tv_a + " / " + tv_b
                plot = tv
                plugintools.log("plot= "+plot)
                
            elif len(tv) == 3:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                
                tv = tv_a + " / " + tv_b + " / " + tv_c
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 4:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                  
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                   
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")                  
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d            
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 5:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                 
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")                  
                tv_e = tv[4]
                tv_e = tv_e.lstrip()
                tv_e = tv_e.rstrip()
                tv_e = tv_e.replace(")", "")
                tv_e = tv_e.replace("(Bar+ dial 333-334", "")
                tv_e = tv_e.replace("(Canal+", "")                 
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d + " / " + tv_e
                # tv = tv.replace(")", "")                
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 6:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                 
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                  
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")                  
                tv_e = tv[4]
                tv_e = tv_e.lstrip()
                tv_e = tv_e.rstrip()
                tv_e = tv_e.replace(")", "")
                tv_e = tv_e.replace("(Bar+ dial 333-334", "")
                tv_e = tv_e.replace("(Canal+", "")                  
                tv_f = tv[5]
                tv_f = tv_f.lstrip()
                tv_f = tv_f.rstrip()
                tv_f = tv_f.replace(")", "")
                tv_f = tv_f.replace("(Bar+ dial 333-334", "")
                tv_f = tv_f.replace("(Canal+", "")                  
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d + " / " + tv_e + " / " + tv_f
                # tv = tv.replace(")", "")                
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 7:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")                  
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")                  
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")                  
                tv_e = tv[4]
                tv_e = tv_e.lstrip()
                tv_e = tv_e.rstrip()
                tv_e = tv_e.replace(")", "")
                tv_e = tv_e.replace("(Bar+ dial 333-334", "")
                tv_e = tv_e.replace("(Canal+", "")                  
                tv_f = tv[5]
                tv_f = tv_f.lstrip()
                tv_f = tv_f.rstrip()
                tv_f = tv_f.replace(")", "")
                tv_f = tv_f.replace("(Bar+ dial 333-334", "")
                tv_f = tv_f.replace("(Canal+", "")                
                tv_g = tv[6]
                tv_g = tv_g.lstrip()
                tv_g = tv_g.rstrip()
                tv_g = tv_g.replace(")", "")
                tv_g = tv_g.replace("(Bar+ dial 333-334", "")
                tv_g = tv_g.replace("(Canal+", "")                  
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d + " / " + tv_e + " / " + tv_f + " / " + tv_g
                plot = tv
                plugintools.log("plot= "+plot)                
            else:
                tv = tv_a
                plot = tv_a
                plugintools.log("plot= "+plot)
                

            plugintools.add_item(action="contextMenu", plot = plot , title = momentum + "h " + '[COLOR lightyellow][B]' + category + '[/B][/COLOR] ' + '[COLOR green]' + champ + '[/COLOR]' + " " + '[COLOR lightyellow][I]' + rivales + '[/I][/COLOR] [I][COLOR red]' + plot + '[/I][/COLOR]' , thumbnail  = 'http://i2.bssl.es/telelocura/2009/05/futbol-tv.jpg' , fanart = art + 'agenda2.jpg' , folder = True, isPlayable = False)
            # plugintools.add_item(action="contextMenu", title = '[COLOR yellow][I]' + tv + '[/I][/COLOR]', thumbnail = 'http://i2.bssl.es/telelocura/2009/05/futbol-tv.jpg' , fanart = art + 'agenda2.jpg' , plot = plot , folder = True, isPlayable = False)                
                
            # plugintools.add_item(action="contextMenu", title = gameday + '/' + day + "(" + momentum + ") " + '[COLOR lightyellow][B]' + category + '[/B][/COLOR] ' + champ + ": " + rivales , plot = plot , thumbnail = 'http://i2.bssl.es/telelocura/2009/05/futbol-tv.jpg' , fanart = art + 'agenda2.jpg' , folder = True, isPlayable = False)
            # plugintools.add_item(action="contextMenu", title = '[COLOR yellow][I]' + tv + '[/I][/COLOR]' , thumbnail = 'http://i2.bssl.es/telelocura/2009/05/futbol-tv.jpg' , fanart = art + 'agenda2.jpg' , plot = plot , folder = True, isPlayable = False)
               
         

def encode_string(txt):
    plugintools.log("[latinototal-0.1.0].encode_string: "+txt)
    
    txt = txt.replace("&#231;", "ç")
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#241;', 'ñ')
    txt = txt.replace('&#250;', 'ú')
    txt = txt.replace('&#237;', 'í')
    txt = txt.replace('&#243;', 'ó')    
    txt = txt.replace('&#39;', "'")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace('&#39;', "'")
    return txt



def splive_items(params):
    plugintools.log("[latinototal-0.1.0].SPlive_items "+repr(params))
    data = plugintools.read( params.get("url") )

    channel = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
    
    for entry in channel:
        # plugintools.log("channel= "+channel)
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        category = plugintools.find_single_match(entry,'<category>(.*?)</category>')
        thumbnail = plugintools.find_single_match(entry,'<link_logo>(.*?)</link_logo>')
        rtmp = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
        isIliveTo = plugintools.find_single_match(entry,'<isIliveTo>([^<]+)</isIliveTo>')
        rtmp = rtmp.strip()
        pageurl = plugintools.find_single_match(entry,'<url_html>([^<]+)</url_html>')
        link_logo = plugintools.find_single_match(entry,'<link_logo>([^<]+)</link_logo>')
        
        if pageurl == "SinProgramacion":
            pageurl = ""
            
        playpath = plugintools.find_single_match(entry, '<playpath>([^<]+)</playpath>')
        playpath = playpath.replace("Referer: ", "")
        token = plugintools.find_single_match(entry, '<token>([^<]+)</token>')

        iliveto = 'rtmp://188.122.91.73/edge'
        
        if isIliveTo == "0":
            if token == "0":
                url = rtmp
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)
            else:
                url = rtmp + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)

        if isIliveTo == "1":
            if token == "1":                                
                url = iliveto + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)
                
            else:
                url = iliveto + ' swfUrl=' + rtmp +  " playpath=" + playpath + " pageUrl=" + pageurl
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)
                


def get_fecha():

    from datetime import datetime

    ahora = datetime.now()
    anno_actual = ahora.year
    mes_actual = ahora.month
    dia_actual = ahora.day
    fecha = str(dia_actual) + "/" + str(mes_actual) + "/" + str(anno_actual)
    plugintools.log("fecha de hoy= "+fecha)
    return fecha




def p2p_items(params):
    plugintools.log("[latinototal-0.1.0].p2p_items" +repr(params))
    
    # Vamos a localizar el título 
    title = params.get("plot")
    if title == "":
        title = params.get("title")
        
    data = plugintools.read("http://pastebin.com/raw.php?i=n9BF6Cwe")
    subcanal = plugintools.find_single_match(data,'<name>' + title + '(.*?)</subchannel>')
    thumbnail = plugintools.find_single_match(subcanal, '<thumbnail>(.*?)</thumbnail>')
    fanart = plugintools.find_single_match(subcanal, '<fanart>(.*?)</fanart>')
    plugintools.log("thumbnail= "+thumbnail)


    # Controlamos el caso en que no haya thumbnail en el menú de latinototal
    if thumbnail == "":
        thumbnail = art + 'p2p.png'
    elif thumbnail == 'name_rtmp.png':
        thumbnail = art + 'p2p.png'          

    if fanart == "":
        fanart = art + 'p2p.png'

    # Comprobamos si la lista ha sido descargada o no
    plot = params.get("plot")
    
    if plot == "":
        title = params.get("title")
        title = parser_title(title)
        filename = title + '.p2p'
        getfile_url(params)        
    else:
        print "Lista ya descargada (plot no vacío)"
        filename = params.get("plot")
        params["ext"] = 'p2p'
        params["plot"]=filename
        filename = filename + '.p2p'
        plugintools.log("Lectura del archivo P2P")        

    plugintools.add_item(action="" , title='[COLOR lightyellow][I][B]' + title + '[/B][/I][/COLOR]' , thumbnail=thumbnail , fanart=fanart , folder=False, isPlayable=False)

    # Abrimos el archivo P2P y calculamos número de líneas        
    file = open(playlists + filename, "r")
    file.seek(0)
    data = file.readline()
    num_items = len(file.readlines())
    print num_items
    file.seek(0)
    data = file.readline()
    if data.startswith("default") == True:
        data = data.replace("default=", "")
        data = data.split(",")
        thumbnail = data[0]
        fanart = data[1]
        plugintools.log("fanart= "+fanart)
        
    # Leemos entradas
    i = 0
    file.seek(0)
    data = file.readline()
    data = data.strip()
    while i <= num_items:        
        if data == "":
            data = file.readline()
            data = data.strip()
            # plugintools.log("linea vacia= "+data)
            i = i + 1
            #print i
            continue
        
        elif data.startswith("default") == True:
            data = file.readline()
            data = data.strip()
            i = i + 1
            #print i
            continue
        
        elif data.startswith("#") == True:
            title = data.replace("#", "")
            plugintools.log("title comentario= "+title)
            plugintools.add_item(action="play" , title = title , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
            data = file.readline()
            data = data.strip()
            i = i + 1
            continue
            
        else:
            title = data
            title = title.strip()
            plugintools.log("title= "+title)
            data = file.readline()
            data = data.strip()
            i = i + 1
            #print i
            plugintools.log("linea URL= "+data)
            if data.startswith("sop") == True:
                print "empieza el sopcast..."
                # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                title_fixed = parser_title(title)
                title = title.replace(" " , "+")
                url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name=' + title_fixed
                url = url.strip()
                plugintools.add_item(action="play" , title = title_fixed + ' [COLOR lightgreen][Sopcast][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i
                continue
                
            elif data.startswith("magnet") == True:
                print "empieza el torrent..."
                url = urllib.quote_plus(data)
                title_fixed = parser_title(title)
                #plugin://plugin.video.pulsar/play?uri=<URL_ENCODED_LINK>
                url = 'plugin://plugin.video.pulsar/play?uri=' + url
                plugintools.add_item(action="play" , title = title_fixed + ' [COLOR orangered][Torrent][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                continue

            else:
                print "empieza el acestream..."
                # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                title = parser_title(title)                
                print title                
                url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=1&name='
                plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i
                
            


def contextMenu(params):
    plugintools.log("[latinototal-0.1.0].contextMenu " +repr(params))

    dialog = xbmcgui.Dialog()
    plot = params.get("plot")
    canales = plot.split("/")
    len_canales = len(canales)
    print len_canales
    plugintools.log("canales= "+repr(canales))

    if len_canales == 1:        
        tv_a = canales[0]
        tv_a = parse_channel(tv_a)
        search_channel(params)
        selector = ""        
    else:
        if len_canales == 2:
            print "len_2"
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            selector = dialog.select('palcoTV', [tv_a, tv_b])
                    
        elif len_canales == 3:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)        
            selector = dialog.select('latinototal', [tv_a, tv_b, tv_c])
                    
        elif len_canales == 4:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)          
            selector = dialog.select('latinototal', [tv_a, tv_b, tv_c, tv_d])
            
        elif len_canales == 5:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)         
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            selector = dialog.select('latinototal', [tv_a, tv_b, tv_c, tv_d, tv_e])
            
        elif len_canales == 6:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)         
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)       
            selector = dialog.select('latinototal', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f])
                      
        elif len_canales == 7:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)         
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)
            tv_g = canales[6]
            tv_g = parse_channel(tv_g)         
            selector = dialog.select('latinototal', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f, tv_g])
            
    if selector == 0:
        print selector
        if tv_a.startswith("Gol") == True:
            tv_a = "Gol"
        params["plot"] = tv_a
        plugintools.log("tv= "+tv_a)
        search_channel(params)
    elif selector == 1:
        print selector
        if tv_b.startswith("Gol") == True:
            tv_b = "Gol"
        params["plot"] = tv_b
        plugintools.log("tv= "+tv_b)
        search_channel(params)            
    elif selector == 2:
        print selector      
        if tv_c.startswith("Gol") == True:
            tv_c = "Gol"
        params["plot"] = tv_c
        plugintools.log("tv= "+tv_c)
        search_channel(params)
    elif selector == 3:
        print selector       
        if tv_d.startswith("Gol") == True:
            tv_d = "Gol"
        params["plot"] = tv_d
        plugintools.log("tv= "+tv_d)
        search_channel(params)
    elif selector == 4:
        print selector       
        if tv_e.startswith("Gol") == True:
            tv_e = "Gol"
        params["plot"] = tv_e
        plugintools.log("tv= "+tv_e)
        search_channel(params)        
    elif selector == 5:
        print selector        
        if tv_f.startswith("Gol") == True:
            tv_f = "Gol"
        params["plot"] = tv_f
        plugintools.log("tv= "+tv_f)
        search_channel(params)
    elif selector == 6:
        print selector      
        if tv_g.startswith("Gol") == True:
            tv_g = "Gol"
        params["plot"] = tv_g
        plugintools.log("tv= "+tv_g)
        search_channel(params)
    else:
        pass



def magnet_items(params):
    plugintools.log("[latinototal-0.1.0].magnet_items" +repr(params))
    
    plot = params.get("plot")
    

    title = params.get("title")
    fanart = ""
    thumbnail = ""
    
    if plot != "":
        filename = params.get("plot")
        params["ext"] = 'p2p'
        params["plot"]=filename
        title = plot + '.p2p'
    else:
        getfile_url(params)
        title = params.get("title")
        title = title + '.p2p'

    # Abrimos el archivo P2P y calculamos número de líneas
    file = open(playlists + title, "r")
    file.seek(0)
    data = file.readline()
    num_items = len(file.readlines())

    # Leemos entradas
    file.seek(0)
    i = 0
    while i <= num_items:
        data = file.readline()
        i = i + 1
        #print i
        if data != "":
            data = data.strip()
            title = data
            data = file.readline()
            i = i + 1
            #print i
            data = data.strip()
            if data.startswith("magnet:") == True:
                # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                title_fixed = title.replace(" " , "+")
                url_fixed = urllib.quote_plus(link)
                url = url.strip()
                #plugin://plugin.video.pulsar/play?uri=<URL_ENCODED_LINK>
                url = 'plugin://plugin.video.pulsar/play?uri=' + url
                plugintools.add_item(action="play" , title = data + ' [COLOR orangered][Torrent][/COLOR]' , url = url, thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True)
            else:
                data = file.readline()
                i = i + 1
                #print i
        else:
            data = file.readline()
            i = i + 1
            #print i
            

def parse_channel(txt):
    plugintools.log("[latinototal-0.1.0].encode_string: "+txt)

    txt = txt.rstrip()
    txt = txt.lstrip() 
    return txt


def futbolenlatv_manana(params):
    plugintools.log("[latinototal-0.1.0].futbolenlatv " + repr(params))
    
    # Fecha de mañana
    import datetime

    today = datetime.date.today()
    manana = today + datetime.timedelta(days=1)
    anno_manana = manana.year
    mes_manana = manana.month
    if mes_manana == 1:
        mes_manana = "enero"
    elif mes_manana == 2:
        mes_manana = "febrero"
    elif mes_manana == 3:
        mes_manana = "marzo"
    elif mes_manana == 4:
        mes_manana = "abril"
    elif mes_manana == 5:
        mes_manana = "mayo"
    elif mes_manana == 6:
        mes_manana = "junio"
    elif mes_manana == 7:
        mes_manana = "julio"
    elif mes_manana == 8:
        mes_manana = "agosto"
    elif mes_manana == 9:
        mes_manana = "septiembre"
    elif mes_manana == 10:
        mes_manana = "octubre"
    elif mes_manana == 11:
        mes_manana = "noviembre"
    elif mes_manana == 12:
        mes_manana = "diciembre"
         
        
    dia_manana = manana.day
    plot = str(anno_manana) + "-" + str(mes_manana) + "-" + str(dia_manana)
    print manana

    url = 'http://www.futbolenlatv.com/m/Fecha/' + plot + '/agenda/false/false'
    plugintools.log("URL mañana= "+url)
    params["url"] = url
    params["plot"] = plot
    futbolenlatv(params)
    




def parser_title(title):
    plugintools.log("[latinototal-0.1.0].parser_title " + title)

    cyd = title

    cyd = cyd.replace("[COLOR lightyellow]", "")
    cyd = cyd.replace("[COLOR green]", "")
    cyd = cyd.replace("[COLOR red]", "")
    cyd = cyd.replace("[COLOR blue]", "")    
    cyd = cyd.replace("[COLOR royalblue]", "")
    cyd = cyd.replace("[COLOR white]", "")
    cyd = cyd.replace("[COLOR pink]", "")
    cyd = cyd.replace("[COLOR cyan]", "")
    cyd = cyd.replace("[COLOR steelblue]", "")
    cyd = cyd.replace("[COLOR forestgreen]", "")
    cyd = cyd.replace("[COLOR olive]", "")
    cyd = cyd.replace("[COLOR khaki]", "")
    cyd = cyd.replace("[COLOR lightsalmon]", "")
    cyd = cyd.replace("[COLOR orange]", "")
    cyd = cyd.replace("[COLOR lightgreen]", "")
    cyd = cyd.replace("[COLOR lightblue]", "")
    cyd = cyd.replace("[COLOR lightpink]", "")
    cyd = cyd.replace("[COLOR skyblue]", "")
    cyd = cyd.replace("[COLOR darkorange]", "")    
    cyd = cyd.replace("[COLOR greenyellow]", "")
    cyd = cyd.replace("[COLOR yellow]", "")
    cyd = cyd.replace("[COLOR yellowgreen]", "")
    cyd = cyd.replace("[COLOR orangered]", "")
    cyd = cyd.replace("[COLOR grey]", "")
    cyd = cyd.replace("[COLOR gold]", "")
    cyd = cyd.replace("[COLOR=FF00FF00]", "")  
                
    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[Parser]", "")    
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")
    cyd = cyd.replace(" [Multilink]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]PLX[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]M3U[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]", "")

    title = cyd
    title = title.strip()
    if title.endswith(" .plx") == True:
        title = title.replace(" .plx", ".plx")
        
    plugintools.log("title_parsed= "+title)
    return title


def json_items(params):
    plugintools.log("[latinototal-0.1.0].json_items "+repr(params))
    data = plugintools.read(params.get("url"))

    # Título y autor de la lista
    match = plugintools.find_single_match(data, '"name"(.*?)"url"')
    match = match.split(",")
    namelist = match[0].strip()
    author = match[1].strip()
    namelist = namelist.replace('"', "")
    namelist = namelist.replace(": ", "")
    author = author.replace('"author":', "")
    author = author.replace('"', "")
    fanart = params.get("extra")
    thumbnail = params.get("thumbnail")
    plugintools.log("title= "+namelist)
    plugintools.log("author= "+author)
    plugintools.add_item(action="", title = '[B][COLOR lightyellow]' + namelist + '[/B][/COLOR]' , url = "" , thumbnail = thumbnail , fanart = fanart, isPlayable = False , folder = False)

    # Items de la lista
    data = plugintools.find_single_match(data, '"stations"(.*?)]')
    matches = plugintools.find_multiple_matches(data, '"name"(.*?)}')
    for entry in matches:
        if entry.find("isHost") <= 0:
            title = plugintools.find_single_match(entry,'(.*?)\n')
            title = title.replace(": ", "")
            title = title.replace('"', "")
            title = title.replace(",", "")
            url = plugintools.find_single_match(entry,'"url":(.*?)\n')
            url = url.replace('"', "")
            url = url.strip()
            params["url"]=url
            server_rtmp(params)            
            thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
            thumbnail = thumbnail.replace('"', "")
            thumbnail = thumbnail.replace(',', "")
            thumbnail = thumbnail.strip()            
            plugintools.log("thumbnail= "+thumbnail)
            # Control por si en la lista no aparece el logo en cada entrada
            if thumbnail == "" :
                thumbnail = params.get("thumbnail")
                
            plugintools.add_item( action="play" , title = '[COLOR white] ' + title + '[COLOR green] ['+ params.get("server") + '][/COLOR]' , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

        else:
            title = plugintools.find_single_match(entry,'(.*?)\n')
            title = title.replace(": ", "")
            title = title.replace('"', "")
            title = title.replace(",", "")
            url = plugintools.find_single_match(entry,'"url":(.*?)\n')
            url = url.replace('"', "")
            url = url.strip()           

            if url.find("allmyvideos")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "") 
                thumbnail = thumbnail.strip()               
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")
                    
                plugintools.add_item( action="allmyvideos" , title = title + ' [COLOR lightyellow][Allmyvideos][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )
                
            elif url.find("streamcloud") >= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")                
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")
                    
                plugintools.add_item( action="streamcloud" , title = title + ' [COLOR lightskyblue][Streamcloud][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )
                
            elif url.find("played.to") >= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")                
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")
                plugintools.add_item( action="playedto" , title = title + ' [COLOR lavender][Played.to][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )
                
            elif url.find("vidspot") >= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")                
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="vidspot" , title = title + ' [COLOR palegreen][Vidspot][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )                    

            if url.find("vk.com")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "") 
                thumbnail = thumbnail.strip()               
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="vk" , title = title + ' [COLOR royalblue][Vk][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )                    

            if url.find("nowvideo")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "") 
                thumbnail = thumbnail.strip()               
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")
                    
                plugintools.add_item( action="nowvideo" , title = title + ' [COLOR palegreen][Nowvideo][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )                    

            if url.find("tumi")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "") 
                thumbnail = thumbnail.strip()               
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")                    
                    
                plugintools.add_item( action="tumi" , title = title + ' [COLOR forestgreen][Tumi][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("streamin.to")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "") 
                thumbnail = thumbnail.strip()               
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")                    
                    
                plugintools.add_item( action="streaminto" , title = title + ' [COLOR orange][streamin.to][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )                
                
            else:
                # Canales no reproducibles en XBMC (de momento)
                params["url"]=url
                server_rtmp(params)
                plugintools.add_item( action="play" , title = '[COLOR red] ' + title + ' ['+ params.get("server") + '][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )
                
                if title == "":
                    plugintools.log("url= "+url)
                    fanart = params.get("extra")
                    thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                    thumbnail = thumbnail.replace('"', "")
                    thumbnail = thumbnail.replace(',', "")
                    thumbnail = thumbnail.strip()                    
                    plugintools.log("thumbnail= "+thumbnail)
                    if thumbnail == "":
                        thumbnail = params.get("thumbnail")
                        
                    
                


def youtube_playlists(params):
    plugintools.log("[latinototal-0.1.0].youtube_playlists "+repr(params))
    
    data = plugintools.read( params.get("url") )
        
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")
    
    for entry in matches:
        plugintools.log("entry="+entry)
        
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")           
        url = plugintools.find_single_match(entry,"<content type\='application/atom\+xml\;type\=feed' src='([^']+)'/>")
        fanart = art + 'youtube.png'
        
        plugintools.add_item( action="youtube_videos" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , folder=True )
        plugintools.log("fanart= "+fanart)
     


# Muestra todos los vídeos del playlist de Youtube
def youtube_videos(params):
    plugintools.log("[latinototal-0.1.0].youtube_videos "+repr(params))
    
    # Fetch video list from YouTube feed
    data = plugintools.read( params.get("url") )
    plugintools.log("data= "+data)
    
    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")
    
    for entry in matches:
        plugintools.log("entry="+entry)
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        title = title.replace("I Love Handball | ","")
        plot = plugintools.find_single_match(entry,"<summa[^>]+>([^<]+)</summa")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        fanart = art+'youtube.png'
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([0-9A-Za-z_-]{11})")
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="play" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , isPlayable=True, folder=False )



def server_rtmp(params):
    plugintools.log("[latinototal-0.1.0].server_rtmp " + repr(params))

    url = params.get("url")
    plugintools.log("URL= "+url)
    
    if url.find("iguide.to") >= 0:
        params["server"] = 'iguide'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    if url.find("freetvcast.pw") >= 0:
        params["server"] = 'freetvcast'
        return params    

    elif url.find("9stream") >= 0:
        params["server"] = '9stream'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("freebroadcast") >= 0:
        params["server"] = 'freebroadcast'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params    

    elif url.find("goodgame.ru") >= 0:
        params["server"] = 'goodgame.ru'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("hdcast") >= 0:
        params["server"] = 'hdcast'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params    

    elif url.find("sharecast") >= 0:
        params["server"] = 'sharecast'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("cast247") >= 0:
        params["server"] = 'cast247'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("castalba") >= 0:
        params["server"] = 'castalba'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params      

    elif url.find("direct2watch") >= 0:
        params["server"] = 'direct2watch'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params
    
    elif url.find("vaughnlive") >= 0:
        params["server"] = 'vaughnlive'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("streamingfreetv") >= 0:
        params["server"] = 'streamingfreetv'
        return params    

    elif url.find("totalplay") >= 0:
        params["server"] = 'totalplay'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params    

    elif url.find("shidurlive") >= 0:
        params["server"] = 'shidurlive'
        return params        
    
    elif url.find("everyon") >= 0:
        params["server"] = 'everyon'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("iviplanet") >= 0:
        params["server"] = 'iviplanet'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params    

    elif url.find("cxnlive") >= 0:
        params["server"] = 'cxnlive'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params      

    elif url.find("ucaster") >= 0:
        params["server"] = 'ucaster'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("mediapro") >= 0:
        params["server"] = 'mediapro'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("veemi") >= 0:
        params["server"] = 'veemi'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("yukons.net") >= 0:
        params["server"] = 'yukons.net'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params      

    elif url.find("janjua") >= 0:
        params["server"] = 'janjua'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("mips") >= 0:
        params["server"] = 'mips'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("zecast") >= 0:
        params["server"] = 'zecast'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("vertvdirecto") >= 0:
        params["server"] = 'vertvdirecto'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("filotv") >= 0:
        params["server"] = 'filotv'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("dinozap") >= 0:
        params["server"] = 'dinozap'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params    

    elif url.find("ezcast") >= 0:
        params["server"] = 'ezcast'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url
        return params

    elif url.find("flashstreaming") >= 0:
        params["server"] = 'flashstreaming'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("shidurlive") >= 0:
        params["server"] = 'shidurlive'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("multistream") >= 0:
        params["server"] = 'multistream'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("playfooty") >= 0:
        params["server"] = 'playfooty'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("flashtv") >= 0:
        params["server"] = 'flashtv'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("04stream") >= 0:
        params["server"] = '04stream'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("vercosas") >= 0:
        params["server"] = 'vercosasgratis'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("dcast") >= 0:
        params["server"] = 'dcast'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("playfooty") >= 0:
        params["server"] = 'playfooty'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params

    elif url.find("pvtserverz") >= 0:
        params["server"] = 'pvtserverz'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url        
        return params
    
    else:
        params["server"] = 'undefined'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
            params["url"]=url
        return params

def launch_rtmp(params):
    plugintools.log("[latinototal-0.1.0].launch_rtmp " + repr(params))

    url = params.get("url")
    title = params.get("title")
    title = title.replace("[/COLOR]", "")
    title = title.strip()
    plugintools.log("Vamos a buscar en el título: "+title)

    if title.endswith("[9stream]") == True:
        params["server"] = '9stream'
        ninestreams(params)
    
    elif title.endswith("[iguide]") == True:
        plugintools.log("es un iguide!")
        params["server"] = 'iguide'
        # DEBUG: Keyboard: scancode: 0x01, sym: 0x001b, unicode: 0x001b, modifier: 0x0
        #pDialog = xbmcgui.DialogProgress()
        #msg = pDialog.create('latinototal', 'Intentando reproducir RTMP...')
        plugintools.play_resolved_url(url)
        #xbmc.sleep(15000)
        #plugintools.stop_resolved_url(url)

    elif title.endswith("[streamingfreetv]") == True:
        print 'streamingfreetv'
        params["server"] = 'streamingfreetv'
        streamingfreetv(params)       
          

    elif title.endswith("[vercosasgratis]") == True:
        print 'vercosasgratis'
        params["server"] = 'vercosasgratis'
        vercosas(params)

    elif title.endswith("[freebroadcast]") == True:
        print 'freebroadcast'
        params["server"] = 'freebroadcast'
        freebroadcast(params)        

    elif title.endswith("[ucaster]") == True:
        params["server"] = 'ucaster'
        plugintools.play_resolved_url(url)

    elif title.endswith("[direct2watch]") == True:
        params["server"] = 'direct2watch'
        directwatch(params)

    elif title.endswith("[shidurlive]") == True:
        params["server"] = 'shidurlive'
        shidurlive(params)

    elif title.endswith("[cast247]") == True:
        params["server"] = 'cast247'
        castdos(params)

    elif url.find("hdcast") >= 0:
        params["server"] = 'hdcast'
        plugintools.play_resolved_url(url)

    elif url.find("janjua") >= 0:
        params["server"] = 'janjua'
        plugintools.play_resolved_url(url)

    elif url.find("mips") >= 0:
        params["server"] = 'mips'
        plugintools.play_resolved_url(url)

    elif url.find("zecast") >= 0:
        params["server"] = 'zecast'
        plugintools.play_resolved_url(url)

    elif url.find("filotv") >= 0:
        params["server"] = 'filotv'
        print "filotv"
        plugintools.play_resolved_url(url)

    elif url.find("ezcast") >= 0:
        params["server"] = 'ezcast'
        plugintools.play_resolved_url(url)

    elif url.find("flashstreaming") >= 0:
        params["server"] = 'flashstreaming'
        plugintools.play_resolved_url(url)

    elif url.find("shidurlive") >= 0:
        params["server"] = 'shidurlive'
        plugintools.play_resolved_url(url)

    elif url.find("multistream") >= 0:
        params["server"] = 'multistream'
        print "multistream"
        plugintools.play_resolved_url(url)

    elif url.find("playfooty") >= 0:
        params["server"] = 'playfooty'
        plugintools.play_resolved_url(url)

    elif url.find("flashtv") >= 0:
        params["server"] = 'flashtv'
        print "flashtv"
        plugintools.play_resolved_url(url)

    elif url.find("freetvcast") >= 0:
        params["server"] = 'freetvcast'
        print "freetvcast"
        freetvcast(params)

    elif url.find("04stream") >= 0:
        params["server"] = '04stream'
        plugintools.play_resolved_url(url)       

    elif url.find("sharecast") >= 0:
        params["server"] = 'sharecast'
        plugintools.play_resolved_url(url)       

    elif url.find("vaughnlive") >= 0:
        params["server"] = 'vaughnlive'
        resolve_vaughnlive(params)

    elif url.find("goodcast") >= 0:
        params["server"] = 'goodcast'
        plugintools.play_resolved_url(url)       

    elif url.find("dcast.tv") >= 0:
        params["server"] = 'dcast.tv'
        plugintools.play_resolved_url(url)       

    elif url.find("castalba") >= 0:
        params["server"] = 'castalba'
        castalba(params)

    elif url.find("tutelehd.com") >= 0:
        params["server"] = 'tutelehd.com'
        plugintools.play_resolved_url(url)     

    elif url.find("flexstream") >= 0:
        params["server"] = 'flexstream'
        plugintools.play_resolved_url(url)    

    elif url.find("xxcast") >= 0:
        params["server"] = 'xxcast'
        plugintools.play_resolved_url(url)      

    elif url.find("vipi.tv") >= 0:
        params["server"] = 'vipi.tv'
        plugintools.play_resolved_url(url)       

    elif url.find("watchjsc") >= 0:
        params["server"] = 'watchjsc'
        plugintools.play_resolved_url(url)       

    elif url.find("zenex.tv") >= 0:
        params["server"] = 'zenex.tv'
        plugintools.play_resolved_url(url)      

    elif url.find("castto") >= 0:
        params["server"] = 'castto'
        plugintools.play_resolved_url(url)        

    elif url.find("tvzune") >= 0:
        params["server"] = 'tvzune'
        plugintools.play_resolved_url(url)      

    elif url.find("flashcast") >= 0:
        params["server"] = 'flashcast'
        plugintools.play_resolved_url(url)        

    elif url.find("ilive.to") >= 0:
        params["server"] = 'ilive.to'
        print "iliveto"
        plugintools.play_resolved_url(url)       

    elif url.find("Direct2Watch") >= 0:
        params["server"] = 'Direct2Watch'
        print "direct2watch"
        plugintools.play_resolved_url(url)
                
    else:
        print "No ha encontrado launcher"
        params["server"] = 'undefined'
        print "ninguno"
        plugintools.play_resolved_url(url)       
    
  

def peliseries(params):
    plugintools.log("[latinototal-0.1.0].peliseries " +repr(params))

    # Abrimos archivo remoto
    url = params.get("url")
    filepelis = urllib2.urlopen(url)

    # Creamos archivo local para pegar las entradas
    plot = params.get("plot")
    plot = parser_title(plot)
    if plot == "":
        title = params.get("title")
        title = parser_title(title)
        filename = title + ".m3u"
        fh = open(playlists + filename, "wb")
    else:
        filename = params.get("plot") + ".m3u"
        fh = open(playlists + filename, "wb")
   
    plugintools.log("filename= "+filename)
    url = params.get("url")
    plugintools.log("url= "+url)


    #open the file for writing
    fw = open(playlists + filename, "wb")

    #open the file for writing
    fh = open(playlists + 'filepelis.m3u', "wb")
    fh.write(filepelis.read())

    fh.close()

    fw = open(playlists + filename, "wb")
    fr = open(playlists + 'filepelis.m3u', "r")
    fr.seek(0)
    num_items = len(fr.readlines())
    print num_items
    fw.seek(0)
    fr.seek(0)
    data = fr.readline()
    fanart = params.get("extra")
    thumbnail = params.get("thumbnail")
    fw.write('#EXTM3U:"background"='+fanart+',"thumbnail"='+thumbnail)
    fw.write("#EXTINF:-1,[COLOR lightyellow][I]playlists / " + filename + '[/I][/COLOR]' + '\n\n')
    i = 0

    while i <= num_items:

        if data == "":
            data = fr.readline()
            data = data.strip()
            plugintools.log("data= " +data)
            i = i + 1
            print i
            continue

        elif data.find("http") >= 0 :
            data = data.split("http")
            chapter = data[0]
            chapter = chapter.strip()
            url = "http" + data[1]
            url = url.strip()
            plugintools.log("url= "+url)
            fw.write("\n#EXTINF:-1," + chapter + '\n')
            fw.write(url + '\n\n')
            data = fr.readline()
            plugintools.log("data= " +data)
            i = i + 1
            print i
            continue
        
        else:
            data = fr.readline()
            data = data.strip()
            plugintools.log("data= "+data)
            i = i + 1
            print i
            continue        

    fw.close()
    fr.close()
    params["ext"]='m3u'
    filename = filename.replace(".m3u", "")
    params["plot"]=filename
    params["title"]=filename

    # Capturamos de nuevo thumbnail y fanart
    
    os.remove(playlists + 'filepelis.m3u')
    simpletv_items(params)
    

def tinyurl(params):
    plugintools.log("[latinototal-0.1.0].tinyurl "+repr(params))

    url = params.get("url")
    url_getlink = 'http://www.getlinkinfo.com/info?link=' +url

    plugintools.log("url_fixed= "+url_getlink)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url_getlink, headers=request_headers)
    plugintools.log("data= "+body)

    r = plugintools.find_multiple_matches(body, '<dt class="link-effective-url">Effective URL</dt>(.*?)</a></dd>')
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Redireccionando enlace...", 3 , art+'icon.png'))
    
    for entry in r:
        entry = entry.replace("<dd><a href=", "")
        entry = entry.replace('rel="nofollow">', "")
        entry = entry.split('"')
        entry = entry[1]
        entry = entry.strip()
        plugintools.log("vamos= "+entry)
        
        if entry.startswith("http"):
            plugintools.play_resolved_url(entry)



# Conexión con el servicio longURL.org para obtener URL original      
def longurl(params):
    plugintools.log("[latinototal-0.1.0].longURL "+repr(params))

    url = params.get("url")
    url_getlink = 'http://api.longurl.org/v2/expand?url=' +url

    plugintools.log("url_fixed= "+url_getlink)

    try:
        request_headers=[]
        request_headers.append(["User-Agent","Application-Name/3.7"])
        body,response_headers = plugintools.read_body_and_headers(url_getlink, headers=request_headers)
        plugintools.log("data= "+body)

        # <long-url><![CDATA[http://85.25.43.51:8080/DE_skycomedy?u=euorocard:p=besplatna]]></long-url>
        # xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('latinototal', "Redireccionando enlace...", 3 , art+'icon.png'))
        longurl = plugintools.find_single_match(body, '<long-url>(.*?)</long-url>')
        longurl = longurl.replace("<![CDATA[", "")
        longurl = longurl.replace("]]>", "")
        plugintools.log("longURL= "+longurl)
        if longurl.startswith("http"):
            plugintools.play_resolved_url(longurl)

    except:
        play(params)



def opentxt(self):

    texto = xbmcgui.ControlTextBox (100, 250, 300, 300, textColor='0xFFFFFFFF')
    texto.setText('log.txt')

    texto.setVisible(window)
     
   
    
def encode_url(url):
    url_fixed= urlencode(url)
    print url_fixed



def seriecatcher(params):
    plugintools.log("[latinototal-0.1.0].seriecatcher "+repr(params))
    
    url = params.get("url")
    fanart = params.get("extra")
    data = plugintools.read(url)
    temp = plugintools.find_multiple_matches(data, '<i class=\"glyphicon\"></i>(.*?)</a>')
    SelectTemp(params, temp)


def GetSerieChapters(params):
    plugintools.log("[latinototal-0.1.0].GetSerieChapters "+repr(params))

    season = params.get("season")
    data = plugintools.read(params.get("url"))
    
    season = plugintools.find_multiple_matches(data, season + '(.*?)</table>')
    season = season[0]
    
    for entry in season:
        url_cap = plugintools.find_multiple_matches(season, '<a href=\"/capitulo(.*?)\" class=\"color4\"')
        title = plugintools.find_multiple_matches(season, 'class=\"color4\">(.*?)</a>')

    num_items = len(url_cap)    
    i = 1
    
    while i <= num_items:
        url_cap_fixed = 'http://seriesadicto.com/capitulo/' + url_cap[i-1]
        title_fixed = title[i-1]
        fanart = params.get("extra")
        GetSerieLinks(fanart , url_cap_fixed, i, title_fixed)
        i = i + 1
        
        
    
def GetSerieLinks(fanart , url_cap_fixed, i, title_fixed):
    plugintools.log("[latinototal-0.1.0].GetSerieLinks")
    
    data = plugintools.read(url_cap_fixed)
    amv = plugintools.find_multiple_matches(data, 'allmyvideos.net/(.*?)"')
    strcld = plugintools.find_multiple_matches(data, 'streamcloud.eu/(.*?)"')
    vdspt = plugintools.find_multiple_matches(data, 'vidspot.net/(.*?)"')
    plydt = plugintools.find_multiple_matches(data, 'played.to/(.*?)"')
    thumbnail = plugintools.find_single_match(data, 'src=\"/img/series/(.*?)"')
    thumbnail_fixed = 'http://seriesadicto.com/img/series/' + thumbnail
    
    for entry in amv:
        amv_url = 'http://allmyvideos.net/' + entry        
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR lightyellow] [Allmyvideos][/COLOR]', url = amv_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in strcld:
        strcld_url = 'http://streamcloud.eu/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR lightskyblue] [Streamcloud][/COLOR]', url = strcld_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in vdspt:
        vdspt_url = 'http://vidspot.net/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR palegreen] [Vidspot][/COLOR]', url = vdspt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in plydt:
        plydt_url = 'http://played.to/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR lavender] [Played.to][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in plydt:
        plydt_url = 'vk.com' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR royalblue] [Vk][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in plydt:
        plydt_url = 'nowvideo.sx' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR red] [Nowvideo][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)           

    for entry in plydt:
        plydt_url = 'http://tumi.tv/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR forestgreen] [Tumi][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)
        
        

def SelectTemp(params, temp):
    plugintools.log("[latinototal-0.1.0].SelectTemp "+repr(params))

    seasons = len(temp)
    
    dialog = xbmcgui.Dialog()
    
    if seasons == 1:
        selector = dialog.select('latinototal', [temp[0]])
                                             
    if seasons == 2:
        selector = dialog.select('latinototal', [temp[0], temp[1]])
                                             
    if seasons == 3:
        selector = dialog.select('latinototal', [temp[0],temp[1], temp[2]])
                                             
    if seasons == 4:
        selector = dialog.select('latinototal', [temp[0], temp[1],temp[2], temp[3]])
                                             
    if seasons == 5:
        selector = dialog.select('latinototal', [temp[0], temp[1],temp[2], temp[3], temp[4]])
        
    if seasons == 6:
        selector = dialog.select('latinototal', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5]])
        
    if seasons == 7:
        selector = dialog.select('latinototal', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6]])
        
    if seasons == 8:
        selector = dialog.select('latinototal', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7]])
        
    if seasons == 9:
        selector = dialog.select('latinototal', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8]])
        
    if seasons == 10:
        selector = dialog.select('latinototal', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9]])                               

    i = 0
    while i<= seasons :
        if selector == i:
            params["season"] = temp[i]
            GetSerieChapters(params)

        i = i + 1
        

            

def m3u_items(title):
    plugintools.log("[latinototal-0.1.0].m3u_items= "+title)

    thumbnail = art + 'icon.png'
    fanart = art + 'fanart.jpg'
    only_title = title

    if title.find("tvg-logo") >= 0:
        thumbnail = re.compile('tvg-logo="(.*?)"').findall(title)
        num_items = len(thumbnail)
        print 'num_items',num_items
        if num_items == 0:
            thumbnail = 'm3u.png'
        else:        
            thumbnail = thumbnail[0]
            #plugintools.log("thumbnail= "+thumbnail)
            
        only_title = only_title.replace('tvg-logo="', "")
        only_title = only_title.replace(thumbnail, "")        

    if title.find("tvg-wall") >= 0:
        fanart = re.compile('tvg-wall="(.*?)"').findall(title)
        fanart = fanart[0]
        only_title = only_title.replace('tvg-wall="', "")
        only_title = only_title.replace(fanart, "")        

    if title.find("group-title") >= 0:
        cat = re.compile('group-title="(.*?)"').findall(title)
        if len(cat) == 0:
            cat = ""
        else:
            cat = cat[0]
        plugintools.log("m3u_categoria= "+cat)
        only_title = only_title.replace('group-title=', "")
        only_title = only_title.replace(cat, "")
    else:
        cat = ""

    if title.find("tvg-id") >= 0:
        title = title.replace('”', '"')
        title = title.replace('“', '"')
        tvgid = re.compile('tvg-id="(.*?)"').findall(title)
        print 'tvgid',tvgid
        tvgid = tvgid[0]
        plugintools.log("m3u_categoria= "+tvgid)
        only_title = only_title.replace('tvg-id=', "")
        only_title = only_title.replace(tvgid, "")
    else:
        tvgid = ""

    if title.find("tvg-name") >= 0:
        tvgname = re.compile('tvg-name="(.*?)').findall(title)
        tvgname = tvgname[0]
        plugintools.log("m3u_categoria= "+tvgname)
        only_title = only_title.replace('tvg-name=', "")
        only_title = only_title.replace(tvgname, "")
    else:
        tvgname = ""        

    only_title = only_title.replace('"', "")
    #plugintools.log("m3u_thumbnail= "+thumbnail)
    #plugintools.log("m3u_fanart= "+fanart)
    #plugintools.log("only_title= "+only_title)

    return thumbnail, fanart, cat, only_title, tvgid, tvgname




def xml_skin():
    plugintools.log("[latinototal-0.1.0].xml_skin")

    mastermenu = plugintools.get_setting("mastermenu")
    xmlmaster = plugintools.get_setting("xmlmaster")
    SelectXMLmenu = plugintools.get_setting("SelectXMLmenu")

    # values="Latino Total|Pastebin|Personalizado"
    if xmlmaster == 'true':
        if SelectXMLmenu == '0':
            mastermenu = 'http://pastebin.com/raw.php?i=n9BF6Cwe'
            plugintools.log("[PalcoTV.xml_skin: "+SelectXMLmenu)
            # Control para ver la intro de PalcoTV
            ver_intro = plugintools.get_setting("ver_intro")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4') 
        elif SelectXMLmenu == '1':  # Pastebin
            id_pastebin = plugintools.get_setting("id_pastebin")
            if id_pastebin == "":
                plugintools.log("[PalcoTV.xml_skin: No definido")                
                mastermenu = 'http://pastebin.com/raw.php?i=n9BF6Cwe'
            else:                
                mastermenu = 'http://pastebin.com/raw.php?i=' +id_pastebin
                plugintools.log("[PalcoTV.xml_skin: "+mastermenu)
        elif SelectXMLmenu == '2':   # Personalizado
            mastermenu = plugintools.get_setting("mastermenu")
            if mastermenu == "":
                plugintools.log("[PalcoTV.xml_skin: No definido")
                mastermenu = 'http://pastebin.com/raw.php?i=n9BF6Cwe'                
                # Control para ver la intro de PalcoTV
                ver_intro = plugintools.get_setting("ver_intro")
                if ver_intro == "true":
                    xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')
        
    else:
        # xmlmaster = False (no activado), menú por defecto     
        mastermenu = 'http://pastebin.com/raw.php?i=n9BF6Cwe'

        # Control para ver la intro de latinototal
        ver_intro = plugintools.get_setting("ver_intro")
        if ver_intro == "true":
            xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')
        

    return mastermenu





run()

