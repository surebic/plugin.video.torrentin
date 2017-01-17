# -*- coding: utf-8 -*-
#:-----------------------------------------------------------
# Torrentin - XBMC/Kodi Plugin
# por ciberus (algunas rutinas tomadas de la web)
#------------------------------------------------------------

import sys,os,xbmc,zipfile,xbmcaddon,xbmcvfs
__addon__ = xbmcaddon.Addon( id = 'plugin.video.torrentin' )
__cwd__        = __addon__.getAddonInfo('path')
addonspath = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")

def ldlst(lista):
	list_folder=unicode(__addon__.getSetting('torrent_path'),'utf-8')
	itemlist = {}
	if not list_folder: return itemlist
	f = open(os.path.join( list_folder ,  lista),"r")
	line = f.readline()
	if not line.startswith("#EXTM3U"): return itemlist
	for line in f:
		line=line.strip()
		if line.startswith('#EXTINF:'):
			canal = line.split(',')[-1]
		elif (len(line) != 0):
			if not line.startswith("acestream://"): line = "acestream://"+line
			itemlist[canal] = line
	f.close()
	return itemlist

def ldlstall():
	list_folder=unicode(__addon__.getSetting('torrent_path'),'utf-8')
	itemlist = {}
	if not list_folder: return itemlist
	dirList=os.listdir( list_folder )
	for fname in dirList:
		try: fname = fname.encode("utf-8", 'ignore')
		except: continue
		if os.path.isdir(os.path.join( list_folder , fname )): continue
		if fname.endswith('.m3u'):
			f = open(os.path.join( list_folder ,  fname),"r")
			line = f.readline()
			if not line.startswith("#EXTM3U"): continue
			for line in f:
				line=line.strip()
				if line.startswith('#EXTINF:'):
					canal = line.split(',')[-1]
				elif (len(line) != 0):
					itemlist[canal] = line
			f.close()
	return itemlist

def chklst():
	list_folder=unicode(__addon__.getSetting('torrent_path'),'utf-8')
	listas  = []
	if not list_folder: return listas
	try:
		dirList=os.listdir( list_folder )
		for fname in dirList:
			try: fname = fname.encode("utf-8", 'ignore')
			except: continue
			if os.path.isdir(os.path.join( list_folder , fname )): continue
			if fname.endswith('.m3u'):
				listas.append(fname)
	except: pass
	return listas

def latin1_to_ascii (unicrap):
    xlate={0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
        0xc6:'Ae', 0xc7:'C',
        0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',
        0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
        0xd0:'Th', 0xd1:'N',
        0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
        0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
        0xdd:'Y', 0xde:'th', 0xdf:'ss',
        0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
        0xe6:'ae', 0xe7:'c',
        0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
        0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
        0xf0:'th', 0xf1:'n',
        0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
        0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
        0xfd:'y', 0xfe:'th', 0xff:'y',
        0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
        0xa5:'{yen}', 0xa6:'|', 0xa7:'{section}', 0xa8:'{umlaut}',
        0xa9:'{C}', 0xaa:'{a}', 0xab:'<<', 0xac:'{not}',
        0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
        0xb1:'{+/-}', 0xb2:'{2}', 0xb3:'{3}', 0xb4:"'",
        0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*', 0xb8:'{cedilla}',
        0xb9:'{]}', 0xba:'{o}', 0xbb:'>>', 
        0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}', 0xbf:'-',
        0xd7:'-', 0xf7:'-'
        }

    r = ''
    for i in unicrap:
        if xlate.has_key(ord(i)):
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            r += str(i)
    return r.replace(":","")

def remove_non_ascii(text):
    from unidecode import unidecode
    return unidecode(unicode(text, encoding = "utf-8"))

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
     return text.strip(".")

def pchpelis(tipo):
	version = chkpelis()
	if version == "42": patchedfile = "platformtools"
	elif version == "41": patchedfile = "xbmctools"
	else: return 3
	
	origen = os.path.join(addonspath,"plugin.video.pelisalacarta","platformcode",patchedfile+".py")
	destino = os.path.join(addonspath,"plugin.video.pelisalacarta","platformcode",patchedfile+".py.pch")
	backup = os.path.join(addonspath,"plugin.video.pelisalacarta","platformcode",patchedfile+".py.bkp")
	parcheado = False
	try:
		fo = open(origen,"r")
		fd = open(destino,"w")
	except: return 0

	fd.writelines('# -*- coding: utf-8 -*-'+'\n'+'# Parcheado por Torrentin'+'\n')
	line = fo.readline()
	for line in fo:
		if line.startswith('# Parcheado por Torrentin'):
			parcheado = True
			break
		fd.writelines(line)
		if tipo == 2:
			if line.startswith('    if puedes:'):
				fd.writelines('        if item.server == "torrent":'+'\n')
				if version == "42":
					fd.writelines('            xbmc.executebuiltin("XBMC.RunPlugin(" + "plugin://plugin.video.torrentin/?uri=%s&image=%s" % (urllib.quote_plus(item.url) , urllib.quote_plus(item.thumbnail) ) + ")")'+'\n'+'            return opciones, video_urls, seleccion, True'+'\n')
				elif version == "41":
					fd.writelines('            xbmc.executebuiltin("XBMC.RunPlugin(" + "plugin://plugin.video.torrentin/?uri=%s&image=%s" % (urllib.quote_plus(item.url) , urllib.quote_plus(item.thumbnail) ) + ")")'+'\n'+'            return'+'\n')
		#elif tipo ==3: #otro tipo de parche, bypass 2º menu, funciona pero no se va a utilizar
			#if line.startswith('    elif item.server=="torrent":'):
				#fd.writelines('        xbmc.executebuiltin("XBMC.RunPlugin(" + "plugin://plugin.video.torrentin/?uri=%s&image=%s" % (urllib.quote_plus(item.url) , urllib.quote_plus(item.thumbnail) ) + ")")'+'\n'+'        return'+'\n')
		elif tipo == 1:
			if version == "42":
				if line.startswith('        mediaurl = urllib.quote_plus(item.url)'):
					fd.writelines('        if "torrentin" in torrent_options[seleccion][1]: xbmc.executebuiltin( "PlayMedia(" + torrent_options[seleccion][1] % mediaurl + urllib.quote_plus( item.thumbnail )+")" )' + '\n        else:')
			elif version == "41":
				if line.startswith('            mediaurl = urllib.quote_plus(item.url)'):
					fd.writelines('            if "torrentin" in torrent_options[seleccion][1]: xbmc.executebuiltin( "PlayMedia(" + torrent_options[seleccion][1] % mediaurl + urllib.quote_plus( item.thumbnail )+")" )' + '\n            else:')
	fo.close()
	fd.close()
	if not parcheado:
		xbmcvfs.copy(origen , backup)
		xbmcvfs.copy(destino , origen)
		os.remove(destino)
		addchannels()
		__addon__.setSetting('parche','true')
		return 1
	else:
		xbmcvfs.copy(backup , origen)
		os.remove(backup)
		os.remove(destino)
		removechannels()
		__addon__.setSetting('parche','false')
		return 2

def addchannels():
	origen = os.path.join(__cwd__ , "resources" , "parches" , "pelisalacarta" )
	destino = os.path.join(addonspath,"plugin.video.pelisalacarta","channels")
	xbmcvfs.copy(os.path.join(destino,"elitetorrent.py") , os.path.join(destino,"elitetorrent.py.bkp"))
	xbmcvfs.copy(os.path.join(destino,"elitetorrent.xml") , os.path.join(destino,"elitetorrent.xml.bkp"))
	xbmcvfs.copy(os.path.join(destino,"newpct.xml") , os.path.join(destino,"newpct.xml.bkp"))
	ciberus_channels = zipfile.ZipFile(os.path.join(origen,"newpct.py" ), 'r')
	ciberus_channels.extractall(destino)

def removechannels():
	destino = os.path.join(addonspath,"plugin.video.pelisalacarta","channels")
	ciberus_channels = [ "divxtotal.py" , "divxtotal.xml" , "elitetorrent.py" , "elitetorrent.xml" , "estrenosdtl.py" , "estrenosdtl.xml" , "estrenosya.py" , "estrenosya.xml" , "newpct.xml" , "yify.py" , "yify.xml" ]
	for f in ciberus_channels:
		if os.path.isfile(os.path.join(destino,f)): os.remove(os.path.join(destino,f))
	xbmcvfs.copy(os.path.join(destino,"elitetorrent.py.bkp") , os.path.join(destino,"elitetorrent.py"))
	xbmcvfs.copy(os.path.join(destino,"elitetorrent.xml.bkp") , os.path.join(destino,"elitetorrent.xml"))
	xbmcvfs.copy(os.path.join(destino,"newpct.xml.bkp") , os.path.join(destino,"newpct.xml"))

def pchpelisold(tipo):
	try:
		f = open(os.path.join(addonspath,"plugin.video.pelisalacarta","addon.xml"), 'r')
		AddOnId=f.read()
		f.close
	except:
		return False
	if not 'version="4.0.6"' in AddOnId: return False
	destino = os.path.join(addonspath,"plugin.video.pelisalacarta","servers","torrent.py")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "pelisalacarta" , "torrent.py") , destino) : return False
	else: return False
	destino = os.path.join(addonspath,"plugin.video.pelisalacarta","platformcode","xbmctools.py")
	if os.path.isfile(destino):
		if tipo == 1:
			if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "pelisalacarta" , "xbmctools.py") , destino) : return False
		if tipo == 2:
			if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "pelisalacarta" , "xbmctools(2).py") , destino) : return False
	else: return False

	destino = os.path.join(addonspath,"plugin.video.pelisalacarta","channels","newpct.xml")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "pelisalacarta" , "newpct.xml") , destino) : return False
	else: return False
	destino = os.path.join(addonspath,"plugin.video.pelisalacarta","channels","newpct1.xml")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "pelisalacarta" , "newpct1.xml") , destino) : return False
	else: return False
	'''
	destino = os.path.join(addonspath,"plugin.video.pelisalacarta","channels","elitetorrent.xml")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "pelisalacarta" , "elitetorrent.xml") , destino) : return False
	else: return False
	destino = os.path.join(addonspath,"plugin.video.pelisalacarta","channels","elitetorrent.py")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "pelisalacarta" , "elitetorrent.py") , destino) : return False
	else: return False
	'''
	return True

def chkpelis():
	try:
		f = open(os.path.join(addonspath,"plugin.video.pelisalacarta","addon.xml"), 'r')
		AddOnId=f.read()
		f.close
	except:
		return "0"
	if '    version="4.2.' in AddOnId: return "42"
	elif '    version="4.1.' in AddOnId: return "41"
	elif '    version="4.0.' in AddOnId: return "40"
	else: return "0"
    
def pchlatino():
	try:
		f = open(os.path.join(addonspath,"plugin.video.latinototal","addon.xml"), 'r')
		AddOnId=f.read()
		f.close
	except:
		return False
	if not 'version="0.2.0"' in AddOnId: return False
	destino = os.path.join(addonspath,"plugin.video.latinototal","default.py")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "latinototal" , "default.py") , destino) : return False
		else: return True
	else: return False

def pchp2p():
	try:
		f = open(os.path.join(addonspath,"plugin.video.p2p-streams","addon.xml"), 'r')
		AddOnId=f.read()
		f.close
	except:
		return False
	if not 'version="1.2.0b"' in AddOnId: return False
	destino = os.path.join(addonspath,"plugin.video.p2p-streams","resources","settings.xml")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "p2p-streams" , "settings.xml") , destino) : return False
	else: return False
	destino = os.path.join(addonspath,"plugin.video.p2p-streams","resources","core","acestream.py")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "p2p-streams" , "acestream.py") , destino) : return False
	else: return False
	return True

def pchplexus():
	try:
		f = open(os.path.join(addonspath,"program.plexus","addon.xml"), 'r')
		AddOnId=f.read()
		f.close
	except:
		return False
	if not 'version="0.1.4"' in AddOnId: return False
	destino = os.path.join(addonspath,"program.plexus","resources","settings.xml")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "plexus" , "settings.xml") , destino) : return False
	else: return False
	destino = os.path.join(addonspath,"program.plexus","resources","plexus","acestream.py")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "plexus" , "acestream.py") , destino) : return False
	else: return False
	destino = os.path.join(addonspath,"program.plexus","resources","plexus","acecore.py")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "plexus" , "acecore.py") , destino) : return False
	else: return False
	return True

def pchplexusstreams():
	proceso = 0
	proceso2 = 0
	destinoset = os.path.join(addonspath,"plugin.video.plexus-streams","resources","settings.xml")
	if os.path.isfile(destinoset):
		md5sum = txtmd5(destinoset)
		if md5sum == "d9ff4538382826cb676f83fad177d8a9":
			proceso = 1
		elif md5sum == "bde9fe5ba3d7d0159f0c5b127a5e0181":
			proceso = 2
		else: proceso = 3
	else: proceso = 0

	destinoace = os.path.join(addonspath,"plugin.video.plexus-streams","resources","core","acestream.py")
	if os.path.isfile(destinoace):
		md5sum = txtmd5(destinoace)
		if md5sum == "5e06800233f5d49fa2e11353ef33533f":
			proceso2 = 1
		elif md5sum == "63267830d43361a408e8b34695cbb073":
			proceso = 2
		else: proceso = 3
	else: proceso = 0

	if proceso == 1 and proceso2 == 1:
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "plexus-streams" , "settings.xml") , destinoset) : return 0
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "plexus-streams" , "acestream.py") , destinoace) : return 0
		return proceso
	else: return proceso

#orig settings.xml  d9ff4538382826cb676f83fad177d8a9
#orig acestream.py  5e06800233f5d49fa2e11353ef33533f
#patched settings.xml  bde9fe5ba3d7d0159f0c5b127a5e0181
#patched acestream.py  63267830d43361a408e8b34695cbb073

def pchkmedia():
	try:
		KmediaDir = "plugin.video.kmediatorrent"
		f = open(os.path.join(addonspath,KmediaDir,"addon.xml"), 'r')
		AddOnId=f.read()
		f.close
	except:
		try:
			KmediaDir = "plugin.video.kmediatorrent-2.3.7"
			f = open(os.path.join(addonspath,KmediaDir,"addon.xml"), 'r')
			AddOnId=f.read()
			f.close
		except:
			return False
	#if AddOnId == "" : return False
	if not 'version="2.3.7"' in AddOnId: return False
	destino = os.path.join(addonspath,KmediaDir,"resources","settings.xml")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "kmediatorrent" , "settings.xml") , destino) : return False
	else: return False
	destino = os.path.join(addonspath,KmediaDir,"resources","site-packages","kmediatorrent","player.py")
	if os.path.isfile(destino):
		if not xbmcvfs.copy(os.path.join(__cwd__ , "resources" , "parches" , "kmediatorrent" , "player.py") , destino) : return False
	else: return False
	return True

def recursive_overwrite(src, dest, ignore=None):
    import shutil
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)

def txtmd5(file):
    import hashlib
    md5 = hashlib.md5()
    f = open(file)
    for line in f:
        md5.update(line)
    f.close()
    #print "TORRENTIN_MD5: "+ file + "  " + md5.hexdigest()
    return md5.hexdigest()

#hashlib.md5(open(file,'rb').read()).hexdigest()
