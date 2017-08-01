# -*- coding: utf-8 -*-
import json, os, re, requests, sys, urllib2, urllib, urlresolver, xbmc, xbmcaddon, xbmcgui, xbmcplugin
from resources import client  ###THANKS TO TWILIGHT FOR HIS CODE!!!
from resources import hqqresolver ###THANKS TO WEIIGO FOR HIS CODE!!!
###THANKS TO DANDYMedia to use his addon as template and making this addon that makes happy my wife!!!

s = requests.session() 
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'



ADDON       = xbmcaddon.Addon()
ADDON_DATA  = ADDON.getAddonInfo('profile')
ADDON_PATH  = ADDON.getAddonInfo('path')
DESCRIPTION = ADDON.getAddonInfo('description')
FANART      = ADDON.getAddonInfo('fanart')
ICON        = ADDON.getAddonInfo('icon')
ID          = ADDON.getAddonInfo('id')
NAME        = ADDON.getAddonInfo('name')
VERSION     = ADDON.getAddonInfo('version')

SHID        = ID.replace('plugin.video.','')
ART         = ADDON_PATH + "/resources/icons/"
BASEURL     = 'http://mastelenovelashd.net/'

def Main_menu():
    addDir('[B][COLOR white]Últimos capítulos agregados[/COLOR][/B]',BASEURL,7,ART + 'latest.jpg',FANART,'')
    addDir('[B][COLOR white]Telenovelas en Emisión[/COLOR][/B]',BASEURL+'page/telenovelas-en-emision/',6,ART + 'new.jpg',FANART,'')
    addDir('[B][COLOR white]Lista de Telenovelas[/COLOR][/B]',BASEURL,3,ART + 'lista.jpg',FANART,'')
    addDir('[B][COLOR white]Navegar por letras[/COLOR][/B]',BASEURL ,9,ART + 'genres.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_lista(url): #3
    OPEN = client.request(url)
    Regex = re.compile('<li><a title="(.+?)" href="(.+?)">',re.DOTALL).findall(OPEN)
    for name,url in Regex:
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,8,ICON,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_letras(url): #9
    OPEN = client.request(url)
    Regex = re.compile('\'letras\'(.+?)</ul>',re.DOTALL).findall(OPEN)[0]
    Regex2 = re.compile('href="(.+?)".+?">(.+?)</a>',re.DOTALL).findall(str(Regex))
    for url,name in Regex2:
        if len(name) < 2:
           addDir('[B][COLOR white]Telenovelas de %s[/COLOR][/B]' %name,url,5,ICON,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')


def Get_content(url): #5
    OPEN = client.request(url)
    Regex = re.compile('"imagen">.+?<a href="(.+?)".+?src="(.+?)".+?alt="(.+?)">',re.DOTALL).findall(OPEN)
    for url,icon,name in Regex:
        name=name.replace('&#39;','\'').replace('amp;','')
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,8,icon,FANART,'')
    np = re.compile('<ul class="paginacionm">(.+?)</ul>',re.DOTALL).findall(OPEN)
    np2 = re.compile('<li><a href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(np))
    for url2,name in np2:
        if 'Siguiente' in name:
            letra = re.compile('\?q=(\w{,2})').findall(str(url2))
            for letra in letra:
                url = BASEURL+'/letra/'+letra+'.html'+url2
                addDir('[B][COLOR red]Siguiente>>>[/COLOR][/B]',url,5,ART + 'nextpage.jpg',FANART,'')
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def Browse_content(url): #6
    OPEN = client.request(url)
    Regex = re.compile('"imagen">.+?<a href="(.+?)".+?src="(.+?)".+?alt="(.+?)">',re.DOTALL).findall(OPEN)
    for url,icon,name in Regex:
        name=name.replace('&#39;','\'').replace('amp;','')
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,8,icon,FANART,'')
    np = re.compile('<ul class="paginacionm">(.+?)</ul>',re.DOTALL).findall(OPEN)
    np2 = re.compile('<li><a href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(np))
    for url2,name in np2:
        if 'Siguiente' in name:
            url += url2
            addDir('[B][COLOR red]Siguiente>>>[/COLOR][/B]',url,6,ART + 'nextpage.jpg',FANART,'')
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def Get_trending(url):
    OPEN = client.request(url)
    Regex = re.compile('href="(.+?)".+?<div class="slide">.+?src="(.+?)".=?alt="(.+?)">',re.DOTALL).findall(OPEN)
    for url,icon,name in Regex:
        name=name.replace('&#39;','\'').replace('amp;','')
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,8,icon,FANART,'')
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def Get_lat_ep(url): #7
    OPEN = client.request(url)
    Regex = re.compile('"imagen">.+?<a href="(.+?)".+?src="(.+?)".+?alt="(.+?)">',re.DOTALL).findall(OPEN)
    for url,icon,name in Regex:
        name=name.replace('&#39;','\'').replace('amp;','')
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,10,icon,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    np = re.compile('<ul class="paginacionm">(.+?)</ul>',re.DOTALL).findall(OPEN)
    np2 = re.compile('<li><a href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(np))
    for url2,name in np2:
        if 'Siguiente' in name:
            url = BASEURL + url2
            addDir('[B][COLOR red]Siguiente>>>[/COLOR][/B]',url,7,ART + 'nextpage.jpg',FANART,'')
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def Episodes(url): #8
    OPEN = client.request(url)
    Regex = re.compile('<li><a href="(.+?)".+?itle="(.+?)">',re.DOTALL).findall(OPEN)
    get_icon = re.compile('<img class="transparent" src="(.+?)" alt=".+?">',re.DOTALL).findall(OPEN)[0]
    for url,title in Regex[::-1]:
        if 'capitulo' in url:
            addDir(title,url,10,get_icon,FANART,'')
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def Get_links(name,url): #10
    OPEN = client.request(url)
    Regex = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(OPEN)
    for url in Regex:
        vid_id = re.compile('http[s]?://(.+?)\.',re.DOTALL).findall(url)
        if 'sebuscar' in vid_id:
            continue
        for id in vid_id:
            name = name + ' [B]|'+id
            addDir('[B][COLOR white]Ver en [COLOR lime]%s[/COLOR][/B]'%name,url,100,iconimage,FANART,name)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')


def resolve(name,url,iconimage,description):
    host = url
    stream_url = evaluate(host)
    name = name.split(' [B]|')[0]
    try:
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(stream_url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red]Dead Link[/COLOR],[COLOR white]Please Try Another[/COLOR] ,2000)")

def evaluate(host):
    try:
        if 'openload' in host:
            host = urlresolver.resolve(host)

        elif 'gamovideo' in host:
            cookie = client.request(host, output='cookie', close=False)
            OPEN = client.request(host, cookie=cookie, referer=BASEURL)
            host = re.compile('file: "(.+?)"',re.DOTALL).findall(OPEN)[1]

        elif 'hqq.watch/player/' in host:
            vid = host.split('=')[1]
            hqqvidresolver = hqqresolver.hqqResolver()
            host = hqqvidresolver.resolve(vid)


        elif urlresolver.HostedMediaFile(host):
            host = urlresolver.resolve(host)

        return host
    except:pass



def Open_Url(url):
    headers = {}
    headers['User-Agent'] = User_Agent
    link = s.get(url, headers=headers).text
    link = link.encode('ascii', 'ignore')
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addDir(name,url,mode,iconimage,fanart,description):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
    liz.setProperty('fanart_image', fanart)
    if mode==100:
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok


def OPEN_UrlRez():
        xbmcaddon.Addon('script.module.urlresolver').openSettings()


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
    return param

params=get_params()
url=BASEURL
name=NAME
iconimage=ICON
mode=None
fanart=FANART
description=DESCRIPTION
query=None


try   : url=urllib.unquote_plus(params["url"])
except: pass
try   : name=urllib.unquote_plus(params["name"])
except: pass
try   : iconimage=urllib.unquote_plus(params["iconimage"])
except:pass
try   : mode=int(params["mode"])
except: pass
try   : fanart=urllib.unquote_plus(params["fanart"])
except: pass
try   : description=urllib.unquote_plus(params["description"])
except: pass
try   : query=urllib.unquote_plus(params["query"])
except: pass


print SHID + ': ' + VERSION
print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "IconImage: " + str(iconimage)
#########################################################

if   mode == None : Main_menu()
elif mode == 3    : Get_lista(url)
elif mode == 4    : Get_trending(url)
elif mode == 5    : Get_content(url)
elif mode == 6    : Browse_content(url)
elif mode == 7    : Get_lat_ep(url)
elif mode == 8    : Episodes(url)
elif mode == 9    : Get_letras(url)
elif mode == 10   : Get_links(name,url)
elif mode == 100  : resolve(name,url,iconimage,description)
xbmcplugin.endOfDirectory(int(sys.argv[1]))