#!/usr/bin/python
# -*- coding: utf-8 -*-
# Torrentin - XBMC/Kodi Add-On
# Play torrent & magnet  on Android (Windows only AceStream & plugins)
# by ciberus
# You can copy, distribute, modify blablabla.....
# v.0.5.4 (Enero 2017)

import sys,os,xbmc, xbmcaddon,urllib,xbmcgui,xbmcplugin

__addon__ = xbmcaddon.Addon( id = 'plugin.video.torrentin' )
__author__     = __addon__.getAddonInfo('author')
__scriptid__   = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__        = __addon__.getAddonInfo('path')
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString

sys.path.append( os.path.join( __addon__.getAddonInfo( 'path' ), 'core') )
sys.path.append( os.path.join( __addon__.getAddonInfo( 'path' ), 'resources','lib') )
if (sys.platform == 'win32') or (sys.platform == 'win64'): oswin = True
else: oswin = False
import torrents
import tools

if not __addon__.getSetting('torrent_path'):
    if xbmc.getCondVisibility('system.platform.Android'):
        if not os.path.exists("/mnt/sdcard/Torrents"):
            os.mkdir("/mnt/sdcard/Torrents")
        __addon__.setSetting('torrent_path',"/mnt/sdcard/Torrents")
    else:
        while not __addon__.getSetting('torrent_path'):
            __addon__.openSettings()
            xbmc.sleep(300)
            if not __addon__.getSetting('torrent_path'): xbmcgui.Dialog().ok("Torrentin" , "El Add-On No funcionará hasta que no configures","el directorio de descarga de torrents,","es OBLIGATORIO seleccionar un directorio.")
            xbmc.sleep(300)

gestores = {
1 : ["Custom" , __addon__.getSetting("tordowncust")],
2 : ["uTorrent","com.utorrent.client"],
3 : ["uTorrent Pro","com.utorrent.client.pro" ], 
4 : ["tTorrent","hu.tagsoft.ttorrent.lite"], 
5 : ["tTorrent Pro","hu.tagsoft.ttorrent.pro" ],
6 : ["BitTorrent","com.bittorrent.client"],
7 : ["Flud","com.delphicoder.flud"],
8 : ["Vuze","com.vuze.torrent.downloader"],
9 : ["aTorrent","com.mobilityflow.torrent"]
}
addons = {
"xbmctorrent" : "xbmct" ,
"stream" : "strm" ,
"kmediatorrent" : "kmed" ,
"pulsar" : "pulsar" ,
"quasar" : "quasar" ,
"p2p-streams" : "p2p" ,
"torrenter" : "tter" ,
"yatp" : "yatp"
}

gestornames = gestores.get(int(__addon__.getSetting("tordown")),["",""])
menu = 20
print "[Torrentin] v"+ __version__ + " by " + __author__ + " - SYS ARGV: " + str(sys.argv)

def main():
    uri=None
    funcion=None
    params=get_params()
    try: uri=urllib.unquote_plus(params["uri"])
    except: pass
    try: image=urllib.unquote_plus(params["image"])
    except: image = ""
    try: player=int(params["player"])
    except: player = int(__addon__.getSetting("defplayer"))
    try: funcion=urllib.unquote_plus(params["funcion"])
    except: primer(uri,player,image)
    try: funcionexe = globals()[funcion]
    except: funcionexe = None
    if funcionexe: funcionexe(uri,player,image)
    #print(">>>> URI: "+str(uri))
    #print(">>>> PLAYER: "+str(player))
    #print(">>>> IMAGEN: "+str(image))

def playfile(uri,player,image=""):
    applaunch(uri,player,image)
    return
    #Quitar el resto ya no es necesario porque no reproduce torrents de directorios ocultos. (temp de kodi). (YA NO SE USA).
    destino = unicode(os.path.join(__addon__.getSetting('torrent_path') , "torrentin.torrent" ),'utf-8')
    ok = copytorrent(uri.replace("file://",""),image)
    if ok:
        #torrents.SaveImgLink(image)
        applaunch("file://"+destino,player,image)
    else: mensaje('Error al copiar el fichero torrent.', 3000)

"""
def playweb(uri,player,image=""): #obsoleto, se descargan todos los torrents en el arranque  (YA NO SE USA).
    destino = os.path.join( unicode(__addon__.getSetting('torrent_path'),'utf-8') , "torrentin.torrent" ).decode("utf-8")
    guarda = torrents.dltorrent(uri,player,image)
    if guarda:
        applaunch("file://"+destino,player,image)
    else: mensaje('Error al descargar el torrent.', 3000)
"""

def playmagnet(magnet,player,imagen=""):
    #copymagnet(magnet,imagen) #DESACTIVADO, SE COPIA ANTES DE MOSTRAR EL MENU
    if MagnetPlayers(player):
        res = xbmcgui.Dialog().yesno("Torrentin" , "El reproductor seleccionado no admite enlaces magnet","Elige los que aparecen en verde.","Cambiar de reproductor?")
        if res:
            player =menu
            player = askplayer(magnet,player,imagen)
            if MagnetPlayers(player):
                mensaje('Reproductor incorrecto para magnet', 3000)
                return
            applaunch(magnet,player,imagen)
    else:
        applaunch(magnet,player,imagen)

def playace(uri,player,imagen=""):
    if ChkAcePlayers(player):
        res = xbmcgui.Dialog().yesno("Torrentin" , "El reproductor seleccionado no admite enlaces acestream","Elige los que aparecen en verde.","Cambiar de reproductor?")
        if res:
            player =menu
            player = askplayer(uri,player,imagen)
    if player == 1:
        torrents.play_acelive(uri,imagen)
    elif player == 7 or player == 8:
        torrents.plexus(uri,player,imagen)
    elif player == 9:
        torrents.torrenter(uri,player,imagen)
    elif player == 15:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("ru.vidsoftware.acestreamcontroller.free","android.intent.action.VIEW","","'+uri+'")')
    elif player == 16:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("org.acestream","android.intent.action.VIEW","","'+uri+'")')
    else:
        mensaje('Reproductor incorrecto para AceLive', 3000)

def MagnetPlayers(player):
    if (player == 1 or player == 7 or  player ==8  or player == 16): return True
    else: return False

def ChkAcePlayers(player):
    if (player == 1 or player == 7 or  player ==8  or player == 9 or player == 15 or player == 16): return False
    else: return True

def applaunch(uri,player,imagen =""):
    if player == 1:
        torrents.play_torrent_from_file(uri.replace("file://",""),imagen)
    elif player == 2 or player == 3 or player == 4 or player == 5 or player == 6:
        torrents.SteeveClones(uri,player,imagen)
    elif player == 7 or player == 8:
        torrents.plexus(uri,player,imagen)
    elif player == 9:
        torrents.torrenter(uri,player,imagen)
    elif player == 10:
        torrents.yatp(uri,player,imagen)
    elif player == 11:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("com.mobilityflow.tvp","android.intent.action.VIEW","","'+uri+'")')
    elif player == 12:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("com.mobilityflow.tvp.prof","android.intent.action.VIEW","","'+uri+'")')
    elif player == 13:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("tv.bitx.media","android.intent.action.VIEW","","'+uri+'")')
    elif player == 14:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("tv.bitfalcon.media","android.intent.action.VIEW","","'+uri+'")')
    elif player == 15:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("ru.vidsoftware.acestreamcontroller.free","android.intent.action.VIEW","torrent","'+uri+'")')
    elif player == 16:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("org.acestream","android.intent.action.VIEW","torrent","'+uri+'")')
    elif player == 17:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("com.mtorrent.player.gp","android.intent.action.VIEW","torrent","'+uri+'")')
    elif player == 18:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("com.mdc.mtorrent.player","android.intent.action.VIEW","","'+uri+'")')
    elif player == 19:
        xbmc.executebuiltin('XBMC.StartAndroidActivity("'+gestornames[1]+'","android.intent.action.VIEW","","'+uri+'")')

# YA NO SE USA
def copytorrent(origen,image):
#        if xbmcvfs.copy(origen,destino): return True
#        else: return False
        destino = unicode(os.path.join(__addon__.getSetting('torrent_path') , "torrentin.torrent" ),'utf-8')
        try:
            f = open(origen, 'rb')
            torrent_data=f.read()
            f.close
        except:
            return False
        try:
            f = open(destino , "wb+")
            f.write(torrent_data)
            f.close()
        except:
            return False
        torrents.SaveImgLink(image)
        return True

def copymagnet(magnet,image):
    destino = unicode(os.path.join(__addon__.getSetting('torrent_path') , "torrentin.magnet" ),'utf-8')
    destinoimg = unicode(os.path.join(__addon__.getSetting('torrent_path') , "torrentin.magnet.img" ),'utf-8')
    if image.startswith("http:") or image == "":
        try:
            f = open(destino , "wb+")
            f.write(magnet)
            f.close()
        except: return False
        if image !="":
            try:
                f = open(destinoimg , "wb+")
                f.write(image)
                f.close()
            except: return False
        else:
            try:
                #default = os.path.join( __cwd__ ,"resources","images","magnetlogo.png") 
                f = open(destinoimg , "wb+")
                f.write("http://i.imgur.com/H3xpR22.png")
                f.close()
            except: return False

def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]                 
      return param

def askplayer(uri,player,image):
    torrent_folder=unicode(__addon__.getSetting('torrent_path'),'utf-8')
    torrent_folder2=unicode(__addon__.getSetting('torrent_path_tvp'),'utf-8')
    colorace = "lime"
    colornormal = "lime"
    colorall = "lime"
    guardar = True
    torr = True
    descargar = True
    tipo = "Torrent"
    if uri.startswith("magnet:"):
        colorace = "red"
        tipo = "Magnet"
    if uri.startswith("acestream://"):
        if __addon__.getSetting('aceplay') == "true": return 1
        colornormal = "red"
        guardar = False
        torr = False
        descargar = False
    try:
        if torrent_folder2 and (torrent_folder2 in uri or torrent_folder2 in image) : guardar = False 
        if not "torrentin.torrent" in uri and (torrent_folder in uri or torrent_folder in image): guardar = False
    except: pass
    info = torrents.torrent_info(uri , 0)
    players = [info]
    #players.append("[COLOR yellow]img: [/COLOR]"+image)
    if not "No Video" in info:
        if __addon__.getSetting("aces") == "true":    players.append("[COLOR " + colorace + "][engine]    AceStream[/COLOR]")
        if __addon__.getSetting("quasar") == "true": players.append("[COLOR " + colornormal + "][add-on]    Quasar[/COLOR]")
        if __addon__.getSetting("pulsar") == "true":  players.append("[COLOR " + colornormal + "][add-on]    Pulsar[/COLOR]")
        if __addon__.getSetting("yatp") == "true":     players.append("[COLOR " + colornormal + "][add-on]    Yet Another Torrent Player[/COLOR]")
        if __addon__.getSetting("tter") == "true":       players.append("[COLOR " + colorall + "][add-on]    Torrenter[/COLOR]")
        if __addon__.getSetting("kmed") == "true":   players.append("[COLOR " + colornormal + "][add-on]    KmediaTorrent[/COLOR]")
        if __addon__.getSetting("plexus") == "true": players.append("[COLOR " + colorace + "][add-on]    Plexus[/COLOR]")
        if __addon__.getSetting("xbmct") == "true":  players.append("[COLOR " + colornormal + "][add-on]    XBMCtorrent[/COLOR]")
        if __addon__.getSetting("strm") == "true":     players.append("[COLOR " + colornormal + "][add-on]    Stream[/COLOR]")
        if __addon__.getSetting("p2p") == "true":      players.append("[COLOR " + colorace + "][add-on]    p2p-Streams[/COLOR]")
        if xbmc.getCondVisibility('System.Platform.Android'): 
            if __addon__.getSetting("tvp") == "true":         players.append("[COLOR " + colornormal + "][app]          Torrent Video Player[/COLOR]")
            if __addon__.getSetting("tvpp") == "true":       players.append("[COLOR " + colornormal + "][app]          Torrent Video Player Pro[/COLOR]")
            if __addon__.getSetting("bitx") == "true":        players.append("[COLOR " + colornormal + "][app]          BitX[/COLOR]")
            if __addon__.getSetting("bfalc") == "true":      players.append("[COLOR " + colornormal + "][app]          BitFalcon[/COLOR]")
            if __addon__.getSetting("tsc") == "true":          players.append("[COLOR " + colorall + "][app]          Torrent Stream Controller[/COLOR]")
            if __addon__.getSetting("acep") == "true":       players.append("[COLOR " + colorace + "][app]          AcePlayer[/COLOR]")
            if __addon__.getSetting("mtorg") == "true":       players.append("[COLOR " + colornormal + "][app]          mTorrent (GP)[/COLOR]")
            if __addon__.getSetting("mtorm") == "true":       players.append("[COLOR " + colornormal + "][app]          mTorrent (MDC)[/COLOR]")
    if descargar and int(__addon__.getSetting("tordown")) != 0 and xbmc.getCondVisibility('System.Platform.Android') : players.append("[COLOR orange]     ----====[  Descargar con "+gestornames[0]+"  ]====----[/COLOR]")
    if guardar: players.append("[COLOR orange]     ----====[  Guardar el "+tipo+"  ]====----[/COLOR]")
    elif torr : players.append("[COLOR orange]     ----====[  Borrar el "+tipo+"  ]====----[/COLOR]")
    if "No Video" in info:
        if not xbmcgui.Dialog().yesno("Torrentin" , "                                         [COLOR red][B]¡¡¡ ATENCION !!![/COLOR][/B]","[COLOR orange]No se ha encontrado ningún archivo de video en el torrent.[/COLOR]","       [COLOR lime]¿ Quieres continuar para guardarlo o descargarlo ?[/COLOR]"): return menu
    seleccion = xbmcgui.Dialog().select("Torrentin - Seleccionar Reproductor", players)
    reproductor = players[seleccion]
    if seleccion != -1:
        if seleccion == 0:
            if xbmcgui.Dialog().yesno("Torrentin" , info,"¿ Resproducir ?"): principal(uri,player,image)
            else: return menu
        elif "]    AceStream" in reproductor: return 1
        elif "]    XBMCtorrent" in reproductor: return 2
        elif "]    Stream" in reproductor: return 3
        elif "]    KmediaTorrent" in reproductor: return 4
        elif "]    Pulsar" in reproductor: return 5
        elif "]    Quasar" in reproductor: return 6
        elif "]    p2p-Streams" in reproductor: return 7
        elif "]    Plexus" in reproductor: return 8
        elif "]    Torrenter" in reproductor: return 9
        elif "]    Yet Another" in reproductor: return 10
        elif "]          Torrent Video Player Pro" in reproductor: return 12
        elif "]          Torrent Video Player" in reproductor: return 11
        elif "]          BitX" in reproductor: return 13
        elif "]          BitFalcon" in reproductor: return 14
        elif "]          Torrent Stream Controller" in reproductor: return 15
        elif "]          AcePlayer" in reproductor: return 16
        elif "]          mTorrent (GP)" in reproductor: return 17
        elif "]          mTorrent (MDC)" in reproductor: return 18
        elif "[  Descargar" in reproductor: return 19
        elif "[  Guardar" in reproductor: guardar_torrent(uri,player,image)
        elif "[  Borrar" in reproductor:
            borrar_torrent(uri,player,image)
            return menu
        #return seleccion
        else: return menu
    else: return menu

def borrar_torrent(uri,player,image):
    try:
        if uri.startswith("file://"):
            file = uri.replace("file://","")
            os.remove(file)
            xbmc.executebuiltin('XBMC.Container.Update(%s,"")' % file)
        elif uri.startswith("magnet:"):
            file = image.replace(u'.jpg',u'.magnet')
            os.remove(file)
            xbmc.executebuiltin('XBMC.Container.Update(%s,"")' % file)
            file = image.replace(u'.png',u'.magnet')
            os.remove(file)
            xbmc.executebuiltin('XBMC.Container.Update(%s,"")' % file)
        os.remove(image)
    except: pass

def guardar_magnet(uri,player,image,torr_folder,teclado=False):
    title =""
    try:
        title = uri.rsplit("dn=")[1] 
        title = title.rsplit("&")[0] 
        title = urllib.unquote_plus(title)
        title = title.replace("+"," ").replace(",","").replace("¿","").replace("?","").replace("*","")
        title = unicode(title,'utf-8')
        title = tools.latin1_to_ascii(title)
    except: pass
    if title == "" or teclado:
        keyboard = xbmc.Keyboard(title)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            title = keyboard.getText()
        else: return
    if title == "":
        xbmcgui.Dialog().ok("Torrentin" , "Tienes que escribir un nombre para el magnet,","Repite el proceso y escribelo con el teclado.")
        if __addon__.getSetting('reopen') == "true": principal(uri,player,image)
        return
    try:
        f = open(os.path.join( torr_folder , title + ".magnet") , "wb+")
        f.write(uri)
        f.close()
    except:
        mensaje('ERROR al guardar el magnet, revisa el nombre.', 5000)
        guardar_magnet(uri,player,image,torr_folder,True)
        return
    # Guardamos la caratula
    if image != "":
        image_data = ""
        if image.startswith("http"):
            image_data = torrents.url_get(image)
        else:
            try:
                f = open(image, "rb+")
                image_data=f.read()
                f.close()
            except: pass
        if image_data =="":
            mensaje('ERROR al obtener la caratula.', 4000)
            try:
                f = open(os.path.join( __cwd__ ,"resources","images","magnetlogo.png") , "rb+")
                image_data=f.read()
                f.close()
                f = open(os.path.join( torr_folder , title + ".png" ) , "wb+")
                f.write(image_data)
                f.close()
            except: pass
            if __addon__.getSetting('reopen') == "true": principal(uri,player,image)
            return
        if ".png" in image.lower(): ext=".png"
        elif ".gif" in image.lower(): ext=".gif"
        elif ".jpg" in image.lower(): ext= ".jpg"
        else: ext = ".img"
        try:
            f = open(os.path.join( torr_folder , title + ext ) , "wb+")
            f.write(image_data)
            f.close()
        except:
            mensaje('ERROR al guardar la caratula.', 3000)
            if __addon__.getSetting('reopen') == "true": principal(uri,player,image)
            return
    else:
        try:
            f = open(os.path.join( __cwd__ ,"resources","images","magnetlogo.png") , "rb+")
            image_data=f.read()
            f.close()
            f = open(os.path.join( torr_folder , title + ".png" ) , "wb+")
            f.write(image_data)
            f.close()
        except:
            mensaje('ERROR al guardar la caratula.', 3000)
            if __addon__.getSetting('reopen') == "true": principal(uri,player,image)
            return
    show_Msg('Magnet y Caratula guardados:',title,5000)
    if __addon__.getSetting('reopen') == "true": principal(uri,player,image)

def guardar_torrent(uri,player,image):
    carat = True
    #if not __addon__.getSetting('parche')=="true":
    if not (__addon__.getSetting('pchpelis') == "On" or __addon__.getSetting('pchpelis2') == "On" ):
        carat = False
        sel = xbmcgui.Dialog().yesno("Torrentin" , "Si no parcheas el pelisalacarta no se guardará la carátula","El parche es reversible desde Configuración/Parches","¿ Parchear ahora Pelisalacarta ?")
        if sel:
            pchpelis()
            xbmcgui.Dialog().ok("Torrentin" , "Vuelve a cargar el Torrent para que se guarde completo.")
            return
    if __addon__.getSetting("saveopt") == "0" : torr_folder = unicode(__addon__.getSetting('torrent_path'),'utf-8')
    else:
        if __addon__.getSetting('torrent_path_tvp'):
            torr_folder=unicode(__addon__.getSetting('torrent_path_tvp'),'utf-8')
        else:
            xbmcgui.Dialog().ok("Torrentin" , "Directorio secundario de torrents no configurado","Configuralo y vuelve a darle a Guardar")
            settings("","","")
            return
    if uri.startswith("magnet:"): 
        guardar_magnet(uri,player,image,torr_folder,False)
        return
    save = torrents.savetorrent(uri,image,torr_folder,1)
    if not save:
        res = xbmcgui.Dialog().yesno("Torrentin" , "Ha habido un error al guardar el torrent/caratula","Probablemente por algún caracter no válido","Reintentar con el teclado?")
        if res:
            save = torrents.savetorrent(uri,image,torr_folder,2)
            if not save: xbmcgui.Dialog().ok("Torrentin" , "Ha habido un error desconocido al guardar el torrent/caratula")
    else:
        if carat:
            if save.startswith("nocarat"):
                show_Msg("Torrent guardado (sin carátula): ", save.replace("nocarat",""),5000)
            else: show_Msg("Torrent y carátula guardados: ", save,5000)
        else: show_Msg("Torrent guardado (sin carátula): ", save.replace("nocarat",""),5000)
    if __addon__.getSetting('reopen') == "true": principal(uri,player,image)

def autoconf(uri="",player="",image=""):
    for k,v in addons.iteritems():
        if  xbmc.getCondVisibility('System.HasAddon("plugin.video.' + k + '")'):  __addon__.setSetting(v,"true")
        else: __addon__.setSetting(v,"false")
    if  xbmc.getCondVisibility('System.HasAddon("program.plexus")'):  __addon__.setSetting("plexus","true")
    else: __addon__.setSetting("plexus","false")

def settings(uri="",player="",image=""):
    if tools.chkps() == 1:  __addon__.setSetting("pchplexusstreams","On")
    else: __addon__.setSetting("pchplexusstreams","Off")
    if tools.chkpchpelis() == 0:
        __addon__.setSetting('pchpelis','Off')
        __addon__.setSetting('pchpelis2','Off')
    __addon__.openSettings()
    for k,v in addons.iteritems():
        if __addon__.getSetting(v) == "true":
            if chkplugin(k):  __addon__.setSetting(v,"false")
    if __addon__.getSetting("plexus") == "true":
        if chkprogram("plexus"):  __addon__.setSetting("plexus","false")
    if xbmc.getCondVisibility("System.HasAddon(plugin.video.pulsar)") and xbmc.getCondVisibility("System.HasAddon(plugin.video.quasar)"): xbmcgui.Dialog().ok("Torrentin" , "Los Add-Ons Pulsar y Quasar NO se pueden tener ", "instalados juntos en un mismo Kodi, ya que se crean","conflictos entre ellos, desinstala o inhabilita alguno de los dos.")
#    if xbmc.getCondVisibility('System.Platform.Android'): 
#        if __addon__.getSetting("save") == "true" and __addon__.getSetting("aceold")=="1":
#            if xbmcgui.Dialog().yesno("Torrentin" , "Con las nuevas versiones del motor AceStream  (3.1.x) ", "NO funciona la opción de guardar el video reproducido","en disco o tarjeta.   ¿ Quieres desactivar esta opción ?"):
#                __addon__.setSetting("save","false")
    xbmc.executebuiltin('Container.Refresh')

def chkprogram(name):
    if  xbmc.getCondVisibility('System.HasAddon("program.' + name + '")'): return False
    else:
        return xbmcgui.Dialog().yesno("Torrentin" , "El Add-On  "+name.upper()+"  está activado en el menú ","de reproductores y está deshabilitado o no instalado.","¿ Quieres desactivarlo en el menú de reproductores ?")

def chkplugin(name):
    if  xbmc.getCondVisibility('System.HasAddon("plugin.video.' + name + '")'): return False
    else:
        return xbmcgui.Dialog().yesno("Torrentin" , "El Add-On  "+name.upper()+"  está activado en el menú ","de reproductores y está deshabilitado o no instalado.","¿ Quieres desactivarlo en el menú de reproductores ?")

def dellst(uri="",player="",image=""):
    torrent_folder=unicode(__addon__.getSetting('torrent_path'),'utf-8')
    if xbmcgui.Dialog().yesno("Torrentin" ," \n                               ¿ Borrar todas las listas M3U ?"):
        lst = tools.chklst()
        for lista in lst:
            os.remove(os.path.join( torrent_folder , lista ))
            xbmc.executebuiltin('XBMC.Container.Update(%s,"")' % os.path.join( torrent_folder , lista ) )

def lst(uri="",player="",image=""):
    lst = tools.chklst()
    img=os.path.join( __cwd__ ,"resources","images","delete.png")
    li = xbmcgui.ListItem("[B][COLOR red]Borrar todas las listas[/COLOR][/B]",img,img)
    command = '%s?funcion=dellst&%s' % (sys.argv[0], sys.argv[2])
    li.setProperty('fanart_image',os.path.join(__cwd__,"fanart.jpg"))
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, True)
    for lista in lst:
        img=os.path.join( __cwd__ ,"resources","images","m3u.png")
        li = xbmcgui.ListItem("[B][COLOR orange]"+lista.replace(".m3u","")+"[/COLOR][/B]",img,img)
        command = '%s?funcion=lst2&uri=%s&%s' % (sys.argv[0], urllib.quote_plus(lista), sys.argv[2])
        li.setProperty('fanart_image',os.path.join(__cwd__,"fanart.jpg"))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, True)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def lst2(uri="",player="",image=""):
    lista = tools.ldlst(uri)
    img=os.path.join( __cwd__ ,"resources","images","acestreamlogo.png")
    for k,v in lista.iteritems():
        li = xbmcgui.ListItem("[B][COLOR orange]"+k+"[/COLOR][/B]",img,img)
        command = '%s?funcion=principal&uri=%s' % (sys.argv[0], urllib.quote_plus(v))
        li.setProperty('fanart_image',os.path.join(__cwd__,"fanart.jpg"))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, False)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def cargarlocal(uri="",player="",image=""):
    uri,image = torrents.cargar()
    if uri: principal("file://"+uri,player,image)

def browselocal(uri="",player="",image=""):
    lista = torrents.browsear(1)
    defimg=os.path.join( __cwd__ ,"resources","images","torrentlogo.png")
    for k,v in lista.iteritems():
        if not oswin: titulo = k.split("/")[-1]
        else: titulo = k.split("\\")[-1]
        #if v == "": li = xbmcgui.ListItem("[B][COLOR lime]"+titulo.replace(u'.torrent',u'').replace(u'.magnet',u'')+"[/COLOR][/B]",defimg,defimg)
        #else: li = xbmcgui.ListItem("[B][COLOR lime]"+titulo.replace(u'.torrent',u'').replace(u'.magnet',u'')+"[/COLOR][/B]",v,v)
        if k.endswith(".magnet"):
            if v == "": li = xbmcgui.ListItem("[B][COLOR lime]"+titulo.replace(u'.magnet',u'')+"  [COLOR green][/B](m)[/COLOR]",defimg,defimg)
            else: li = xbmcgui.ListItem("[B][COLOR lime]"+titulo.replace(u'.magnet',u'')+"  [COLOR green][/B](m)[/COLOR]",v,v)
            f = open(k , "rb+")
            magnet_data=f.read()
            f.close()
            command = '%s?funcion=principal&uri=%s&image=%s' % (sys.argv[0], urllib.quote_plus(magnet_data),urllib.quote_plus(v))
        else:
            if v == "": li = xbmcgui.ListItem("[B][COLOR lime]"+titulo.replace(u'.torrent',u'')+"  [COLOR green][/B](t)[/COLOR]",defimg,defimg)
            else: li = xbmcgui.ListItem("[B][COLOR lime]"+titulo.replace(u'.torrent',u'')+"  [COLOR green][/B](t)[/COLOR]",v,v)
            command = '%s?funcion=principal&uri=%s&image=%s' % (sys.argv[0], urllib.quote_plus("file://"+k),urllib.quote_plus(v))
        li.setProperty('fanart_image',os.path.join(__cwd__,"fanart.jpg"))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, False)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def browselocaltvp(uri="",player="",image=""):
    lista = torrents.browsear(2)
    defimg=os.path.join( __cwd__ ,"resources","images","torrentlogo.png")
    for k,v in lista.iteritems():
        if not oswin: titulo = k.split("/")[-1]
        else: titulo = k.split("\\")[-1]
        #if v == "": li = xbmcgui.ListItem("[B][COLOR orange]"+titulo.replace(u'.torrent',u'').replace(u'.magnet',u'')+"[/COLOR][/B]",defimg,defimg)
        #else: li = xbmcgui.ListItem("[B][COLOR orange]"+titulo.replace(u'.torrent',u'').replace(u'.magnet',u'')+"[/COLOR][/B]",v,v)
        if k.endswith(".magnet"):
            if v == "": li = xbmcgui.ListItem("[B][COLOR limegreen]"+titulo.replace(u'.magnet',u'')+"  [COLOR forestgreen][/B](m)[/COLOR]",defimg,defimg)
            else: li = xbmcgui.ListItem("[B][COLOR limegreen]"+titulo.replace(u'.magnet',u'')+"  [COLOR forestgreen][/B](m)[/COLOR]",v,v)
            f = open(k , "rb+")
            magnet_data=f.read()
            f.close()
            command = '%s?funcion=principal&uri=%s&image=%s' % (sys.argv[0], urllib.quote_plus(magnet_data),urllib.quote_plus(v))
        else:
            if v == "": li = xbmcgui.ListItem("[B][COLOR limegreen]"+titulo.replace(u'.torrent',u'')+"  [COLOR forestgreen][/B](t)[/COLOR]",defimg,defimg)
            else: li = xbmcgui.ListItem("[B][COLOR limegreen]"+titulo.replace(u'.torrent',u'')+"  [COLOR forestgreen][/B](t)[/COLOR]",v,v)
            command = '%s?funcion=principal&uri=%s&image=%s' % (sys.argv[0], urllib.quote_plus("file://"+k),urllib.quote_plus(v))
        li.setProperty('fanart_image',os.path.join(__cwd__,"fanart.jpg"))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, False)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def show_Msg(heading, message, time = 6000, pic = os.path.join(__cwd__ , "icon.png")):
    try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading, message, time, pic))
    except: pass

def mensaje(mensaje,time):
    show_Msg('          ---===[ Torrentin ]===---',mensaje,time)

def principal(uri,player,image):
    torrent_folder=unicode(__addon__.getSetting('torrent_path'),'utf-8')
    destino = os.path.join( torrent_folder , "torrentin.torrent" ).decode("utf-8")
    bajado = False
    listitem = xbmcgui.ListItem(label="Torrentin", iconImage="", thumbnailImage="", path=str(sys.argv))
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
    if int(xbmc.getInfoLabel("System.BuildVersion" )[0:2]) >= 13:
        if uri:
            if uri.startswith("http://") or uri.startswith("https://"):
                guarda = torrents.dltorrent(uri,player,image)
                if guarda:
                    uri = "file://"+destino
                    bajado = True
                else:
                    return
            elif uri.startswith("magnet:"): copymagnet(uri,image)
#            elif uri.startswith("file://"): copytorrent(uri.replace("file://",""),image)
            if player == 0:
                if xbmcgui.Dialog().yesno("Torrentin" , torrents.torrent_info(uri , 0),"¿ Reproducir ?"): player = menu
                else: return
            if (oswin and player >=12): player = askplayer(uri,player,image)
            elif (not oswin and player==menu): player = askplayer(uri,player,image)
            if player == menu: return
            if bajado:
                applaunch(uri,player,image)
                return
            elif uri.startswith("file://"): playfile(uri,player,image)
            elif uri.startswith("magnet:"): playmagnet(uri,player,image)
            elif uri.startswith("acestream://"): playace(uri,player,image)
#            elif uri.startswith("http://") or uri.startswith("https://"): playweb(uri,player,image)  #obsoleto
            else: mensaje('Enlace no valido', 3000)
        else: mensaje('Ningun enlace a reproducir', 3000)
    else: xbmcgui.Dialog().ok("Torrentin" , "Este Add-On no funciona en versiones Frodo","Actualiza tu XBMC....")

def primer(uri,player,image):
    if uri: principal(uri,player,image)
#    if uri:
#        xbmc.executebuiltin('xbmc.RunPlugin("plugin://plugin.video.torrentin/?funcion=principal&' + sys.argv[2].replace("?","") + '")')
    torrent_folder=unicode(__addon__.getSetting('torrent_path'),'utf-8')
    destino = os.path.join( torrent_folder , "torrentin.torrent" ).decode("utf-8")
    destinomag = os.path.join( torrent_folder , "torrentin.magnet" ).decode("utf-8")
    fanartimage = os.path.join(__cwd__,"fanart.jpg")
    
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.pelisalacarta")'):
        img=xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.pelisalacarta','icon.png')).decode("utf-8")
        if __addon__.getSetting("pelismenu") == "1":
            li = xbmcgui.ListItem("[B][COLOR khaki]Ir a canales torrent de pelisalacarta[/COLOR][/B]",img,img)
            version = tools.chkpelis()
            if version == "42":
                command = 'plugin://plugin.video.pelisalacarta/?action=filterchannels&category=torrent&channel=channelselector&channel_type=torrent'
            else:
                command = 'plugin://plugin.video.pelisalacarta/?action=listchannels&category=torrent&channel=channelselector'
        elif __addon__.getSetting("pelismenu") == "0":
            li = xbmcgui.ListItem("[B][COLOR khaki]Ir a pelisalacarta[/COLOR][/B]",img,img)
            command = 'plugin://plugin.video.pelisalacarta'
        li.setProperty('fanart_image',fanartimage)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, True)        
    
    lst = tools.chklst()
    if len(lst) >=1:
        img=os.path.join( __cwd__ ,"resources","images","m3u.png")
        li = xbmcgui.ListItem("[B][COLOR orange]Listas AceLive M3U[/COLOR][/B]",img,img)
        command = '%s?funcion=lst&%s' % (sys.argv[0], sys.argv[2])
        li.setProperty('fanart_image',fanartimage)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, True)

    if os.path.isfile (destino):
        img=os.path.join( __cwd__ ,"resources","images","torrentlogo.png")  # torrentin.png
        if os.path.isfile(os.path.join( torrent_folder , "torrentin.torrent.img")):
            f = open(os.path.join( torrent_folder , "torrentin.torrent.img") , "rb+")
            img=f.read()
            f.close()
        li = xbmcgui.ListItem("[B][COLOR greenyellow]Reproducir último torrent[/COLOR][/B]",img,img)
        command = '%s?funcion=principal&uri=file://%s&image=%s' % (sys.argv[0], urllib.quote_plus(destino),urllib.quote_plus(img))
        li.setProperty('fanart_image',fanartimage)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, False)

    if os.path.isfile (destinomag):
        f = open(destinomag , "rb+")
        magnet_data=f.read()
        f.close()
        img=os.path.join( __cwd__ ,"resources","images","magnetlogo.png")
        if os.path.isfile(os.path.join( torrent_folder , "torrentin.magnet.img")):
            f = open(os.path.join( torrent_folder , "torrentin.magnet.img") , "rb+")
            img=f.read()
            f.close()
        li = xbmcgui.ListItem("[B][COLOR greenyellow]Reproducir último magnet[/COLOR][/B]",img,img)
        command = '%s?funcion=principal&uri=%s&image=%s' % (sys.argv[0], urllib.quote_plus(magnet_data),urllib.quote_plus(img))
        li.setProperty('fanart_image',fanartimage)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, False)

    img=os.path.join( __cwd__ ,"resources","images","torrentloader.png")
    li = xbmcgui.ListItem("[B][COLOR greenyellow]Reproducir un torrent local[/COLOR][/B]",img,img)
    command = '%s?funcion=cargarlocal&%s' % (sys.argv[0], sys.argv[2])
    li.setProperty('fanart_image',fanartimage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, False)

    img=os.path.join( __cwd__ ,"resources","images","torrentfolder.png")
    li = xbmcgui.ListItem("[B][COLOR lime]Directorio Principal[/COLOR][/B]",img,img)
    command = '%s?funcion=browselocal&%s' % (sys.argv[0], sys.argv[2])
    li.setProperty('fanart_image',fanartimage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, True)

    img=os.path.join( __cwd__ ,"resources","images","torrent.png")	
    li = xbmcgui.ListItem("[B][COLOR limegreen]Directorio Secundario[/COLOR][/B]",img,img)
    command = '%s?funcion=browselocaltvp&%s' % (sys.argv[0], sys.argv[2])
    li.setProperty('fanart_image',fanartimage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, True)

    img=os.path.join( __cwd__ ,"resources","images","settings3d.png")
    li = xbmcgui.ListItem("[B][COLOR deepskyblue]Configuración[/COLOR][/B]",img,img)
    command = '%s?funcion=settings&%s' % (sys.argv[0], sys.argv[2])
    li.setProperty('fanart_image',fanartimage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), command, li, False)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def pchpelis(uri="",player="",image=""):
    parche = tools.pchpelis(2)
    if parche == 0:
        xbmcgui.Dialog().ok("Error al parchear" , "El parche no se ha aplicado, No está instalado pelisalacarta","o es una versión antigua o no ha sido posible encontrarle.","Instala la última versión de pelisalacarta y vuelve a parchear.")
        __addon__.setSetting('pchpelis','Off')
        __addon__.setSetting('pchpelis2','Off')
    elif parche == 1:
        xbmcgui.Dialog().ok("Torrentin" , "[COLOR lime]Pelisalacarta parcheado con éxito,[/COLOR][COLOR yellow] se añadirán las carátulas", "a los videos por torrent y se auto-arrancarán con Torrentin.[/COLOR]", "[COLOR cyan]Añadidos los canales torrent: EliteTorrent(mod), DivxTotal,\nEstrenosDTL, EstrenosGO y Yify-Torrents.[/COLOR]")
        __addon__.setSetting('pchpelis','On')
        __addon__.setSetting('pchpelis2','Off')
    elif parche == 2:
        xbmcgui.Dialog().ok("Torrentin" , "[COLOR yellow]        Pelisalacarta ya ha sido parcheado anteriormente,[/COLOR]", "[COLOR lime]        se ha restaurado una copia de seguridad y el parche","        y los canales torrent añadidos han sido eliminados.[/COLOR]")
        __addon__.setSetting('pchpelis','Off')
        __addon__.setSetting('pchpelis2','Off')
    elif parche == 3:
        xbmcgui.Dialog().ok("Error al parchear" , "El parche no se ha aplicado, esta parche SOLO vale","para las versiones  4.1.x  y  4.2.x  de pelisalacarta,","Instala la última versión de pelisalacarta y vuelve a parchear.")
        __addon__.setSetting('pchpelis','Off')
        __addon__.setSetting('pchpelis2','Off')

def pchpelis2(uri="",player="",image=""):
    parche = tools.pchpelis(1)
    if parche == 0:
        xbmcgui.Dialog().ok("Error al parchear" , "El parche no se ha aplicado, No está instalado pelisalacarta","o es una versión antigua o no ha sido posible encontrarle.","Instala la última versión de pelisalacarta y vuelve a parchear.")
        __addon__.setSetting('pchpelis2','Off')
        __addon__.setSetting('pchpelis','Off')
    elif parche == 1:
        xbmcgui.Dialog().ok("Torrentin" , "[COLOR lime]Pelisalacarta parcheado con éxito,[/COLOR][COLOR yellow] se añadirán las carátulas", "a los torrents reproducidos o guardados con Torrentin.[/COLOR]", "[COLOR cyan]Añadidos los canales torrent: EliteTorrent(mod), DivxTotal,\nEstrenosDTL, EstrenosGO y Yify-Torrents.[/COLOR]")
        __addon__.setSetting('pchpelis2','On')
        __addon__.setSetting('pchpelis','Off')
    elif parche == 2:
        xbmcgui.Dialog().ok("Torrentin" , "[COLOR yellow]        Pelisalacarta ya ha sido parcheado anteriormente,[/COLOR]", "[COLOR lime]        se ha restaurado una copia de seguridad y el parche","        y los canales torrent añadidos han sido eliminados.[/COLOR]")
        __addon__.setSetting('pchpelis2','Off')
        __addon__.setSetting('pchpelis','Off')
    elif parche == 3:
        xbmcgui.Dialog().ok("Error al parchear" , "El parche no se ha aplicado, esta parche SOLO vale","para las versiones  4.1.x  y  4.2.x  de pelisalacarta,","Instala la última versión de pelisalacarta y vuelve a parchear.")
        __addon__.setSetting('pchpelis2','Off')
        __addon__.setSetting('pchpelis','Off')

def pchlatino(uri="",player="",image=""):
    parche = tools.pchlatino()
    if parche: xbmcgui.Dialog().ok("Torrentin" , "Add-On LatinoTotal parcheado con éxito.","Se usará Torrentin para reproducir los videos por torrent.")
    else: xbmcgui.Dialog().ok("Error al parchear" , "La versión instalada no coincide con la del parche,","o no se han encontrado los ficheros de destino.","¿Esta instalado el Add-On LatinoTotal?")

def pchp2p(uri="",player="",image=""):
    parche = tools.pchp2p()
    if parche: xbmcgui.Dialog().ok("Torrentin" , "Add-On p2p-Streams parcheado con éxito.","Ahora puedes  configurar Torrentin para reproducir los","videos y guardar los enlaces AceLive en las listas.")
    else: xbmcgui.Dialog().ok("Error al parchear" , "La versión instalada no coincide con la del parche,","o no se han encontrado los ficheros de destino.","¿Esta instaladol el Add-On p2p-Streams?")

def pchplexus(uri="",player="",image=""):
    parche = tools.pchplexus()
    if parche: xbmcgui.Dialog().ok("Torrentin" , "Add-On plexus parcheado con éxito.","Ahora puedes  configurar Torrentin para reproducir los","videos, guardar los enlaces AceLive en las listas y\nseleccionar el tipo de motor externo (antiguo o nuevo).")
    else: xbmcgui.Dialog().ok("Error al parchear" , "La versión instalada no coincide con la del parche,","o no se han encontrado los ficheros de destino.","¿Esta instalado el Add-On plexus?")

def pchplexusstreams(uri="",player="",image=""):
    parche = tools.pchplexusstreams()
    if parche == 0:
        xbmcgui.Dialog().ok("Error al parchear" , "El Add-On plexus-streams  no esta instalado","o no se encuentran los ficheros de destino","o no han podido copiarse los ficheros.")
        __addon__.setSetting("pchplexusstreams","Off")
    elif parche == 1:
        xbmcgui.Dialog().ok("Torrentin" , "Add-On plexus-streams parcheado con éxito.","Ahora puedes  configurar Torrentin o Plexus para ","reproducir los enlaces AceLive y torrents locales.")
        __addon__.setSetting("pchplexusstreams","On")
    elif parche == 2:
        xbmcgui.Dialog().ok("Torrentin" , "El Add-On plexus-streams ya ha sido parcheado","anteriormente, no es necesario volver a parchearlo.")
        __addon__.setSetting("pchplexusstreams","On")
    elif parche == 3:
        xbmcgui.Dialog().ok("Error al parchear" , "La versión instalada no coincide con la del parche o han","cambiado los ficheros de destino al actualizarse el add-on.","El parche no se ha aplicado.")
        __addon__.setSetting("pchplexusstreams","Off")
'''
0 no esta insalado o no se encuentra o no se copia
1 parcheado
2 ya esta parcheado
3 no coincide
'''
def pchkmedia(uri="",player="",image=""):
    parche = tools.pchkmedia()
    if parche: xbmcgui.Dialog().ok("Torrentin" , "Add-On KmediaTorrent parcheado con éxito.","Ahora  puedes  descargar  videos .avi completos antes","de reproducirlos y poner el caché en FAT32")
    else: xbmcgui.Dialog().ok("Error al parchear" , "La versión instalada no coincide con la del parche,","o no se han encontrado los ficheros de destino.","¿Esta instalado el Add-On KmediaTorrent?")
    
def chkupdate(uri="",player="",image=""):
	#url = "https://raw.githubusercontent.com/surebic/plugin.video.torrentin/master/archives/version.txt"
	urlhtcm = "http://www.htcmania.com/showthread.php?t=995348"
	url = "https://goo.gl/6iILX9"
	remote = torrents.url_get(url).replace("\n","")
	actual = __version__
	if "beta" in actual or "rc" in actual:
		actualrc = actual.split(" ")[0]
		beta = actual.split(" ")[1]
		actual = actualrc
		
		if xbmcgui.Dialog().yesno("Torrentin - Gracias por colaborar !!!" , "Estás usando una versión beta o RC: " + actualrc + " " + beta,"No está disponible la actualización automática de ","versiones beta, ¿ Quieres ir a htcmania para actualizar ?"):
			if xbmc.getCondVisibility('system.platform.Android'):
				if xbmcgui.Dialog().yesno("Torrentin" , "¿ Tienes instalado Chrome en tu android ?","Si = Abrir con Google Chrome.","No = Abrir con navegador nativo."):
					xbmc.executebuiltin('XBMC.StartAndroidActivity("com.android.chrome","android.intent.action.VIEW","","'+urlhtcm+'")')
				else:
					xbmc.executebuiltin('XBMC.StartAndroidActivity("com.android.browser","android.intent.action.VIEW","","'+urlhtcm+'")')
			else: xbmcgui.Dialog().ok("Torrentin" , "Abre tu navegador y visita: ",urlhtcm)
		
		if xbmcgui.Dialog().yesno("Torrentin" , "Gracias por colaborar en el desarollo del AddOn.","Quieres cambiar la versión beta por la última","publicada y así poder actualizar automáticamente ?"):
			actual = "0.0.0"
		else:
			return
	if int(remote.replace(".","")) > int(actual.replace(".","")):
		if xbmcgui.Dialog().yesno("Torrentin" , "Versión instalada: " + actual,"Actualización disponible: " + remote,"¿ Actualizar Torrentin ?"):
			try:
				destino = os.path.join(xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8"),"packages")
				origen = "https://raw.githubusercontent.com/surebic/plugin.video.torrentin/master/archives/" + "plugin.video.torrentin-" + remote + ".zip?raw=true"
				bajada = torrents.url_get(origen)
				f = open(os.path.join( destino , "plugin.video.torrentin-" + remote + ".zip") , "wb+")
				f.write(bajada)
				f.close()
				import zipfile
				update = zipfile.ZipFile(os.path.join( destino , "plugin.video.torrentin-" + remote + ".zip"), 'r')
				update.extractall(xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8"))
				xbmcgui.Dialog().ok("Torrentin" , "Torrentin actualizado a la versión " + remote,"Ya puedes cerrar la ventana de configuración,","También seria conveniente reiniciar KODI.")
				xbmc.executebuiltin('Container.Refresh')
			except:
				if xbmcgui.Dialog().yesno("Torrentin" , "Ha ocurrido un error durante la actualización.","Tienes que instalar manuálmente la nueva versión.","¿ Quieres ir al foro de htcmania para descargarla ?"):
					if xbmc.getCondVisibility('system.platform.Android'):
						if xbmcgui.Dialog().yesno("Torrentin" , "¿ Tienes instalado Chrome en tu android ?","Si = Abrir con Google Chrome.","No = Abrir con navegador nativo."):
							xbmc.executebuiltin('XBMC.StartAndroidActivity("com.android.chrome","android.intent.action.VIEW","","'+urlhtcm+'")')
						else:
							xbmc.executebuiltin('XBMC.StartAndroidActivity("com.android.browser","android.intent.action.VIEW","","'+urlhtcm+'")')
					else: xbmcgui.Dialog().ok("Torrentin" , "Abre tu navegador y visita: ",urlhtcm)
	elif int(remote.replace(".","")) < int(actual.replace(".","")): xbmcgui.Dialog().ok("Torrentin" , "Versión actual: " + remote,"Versión instalada: " + actual,"Tienes instalada una versión más nueva que la última publicada.")
	else: xbmcgui.Dialog().ok("Torrentin" , "Versión actual: " + remote,"Versión instalada: " + actual,"Tienes instalada la última versión.")

# EOF (01-17)

