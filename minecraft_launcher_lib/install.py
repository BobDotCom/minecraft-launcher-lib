from .natives import extract_natives_file, get_natives
from .helper import parseRuleList, inherit_json
from .utils import get_library_version
import requests
import shutil
import json
import os

def empty(arg):
    pass

def download_file(url,path,callback):
    if os.path.isfile(path):
        return
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    callback.get("setStatus",empty)("Download " + os.path.basename(path))
    r = requests.get(url, stream=True, headers={"user-agent": "minecraft-launcher-lib/" + get_library_version()})
    with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

def install_libraries(data,path,callback):
    callback.get("setMax",empty)(len(data["libraries"]))
    for count, i in enumerate(data["libraries"]):
        #Check, if the rules allow this lib for the current system
        if not parseRuleList(i,"rules",{}):
            continue
        #Turn the name into a path
        currentPath = ""#os.path.join(path,"libraries")
        libPath, name, version = i["name"].split(":")
        for l in libPath.split("."):
            currentPath = os.path.join(currentPath,l)
        currentPath = os.path.join(currentPath,name,version)
        downloadUrl = "https://libraries.minecraft.net/" + currentPath
        currentPath = os.path.join(path,"libraries",currentPath)
        native = get_natives(i)
        #Check if there is a native file
        if native != "":
            jarFilenameNative = name + "-" + version + "-" + native + ".jar"
        jarFilename = name + "-" + version + ".jar"
        downloadUrl = downloadUrl + "/" + jarFilename
        #Try to download the lib
        try:
            download_file(downloadUrl,os.path.join(currentPath,jarFilename),callback)
        except:
            pass
        if not "downloads" in i:
            if "extract" in i:
                extract_natives_file(os.path.join(currentPath,jarFilenameNative),os.path.join(path,"versions",data["id"],"natives"),i["extract"])
            continue
        if "artifact" in i["downloads"]:
            download_file(i["downloads"]["artifact"]["url"],os.path.join(currentPath,jarFilename),callback)
        if native != "":
            download_file(i["downloads"]["classifiers"][native]["url"],os.path.join(currentPath,jarFilenameNative),callback)
            if "extract" in i:
                extract_natives_file(os.path.join(currentPath,jarFilenameNative),os.path.join(path,"versions",data["id"],"natives"),i["extract"])
        callback.get("setProgress",empty)(count)

def install_assets(data,path,callback):
    #Old versions dosen't have this
    if not "assetIndex" in data:
        return
    #Download all assets
    download_file(data["assetIndex"]["url"],os.path.join(path,"assets","indexes",data["assets"] + ".json"),callback)
    with open(os.path.join(path,"assets","indexes",data["assets"] + ".json")) as f:
        assets_data = json.load(f)
    #The assets gas a hash. e.g. c4dbabc820f04ba685694c63359429b22e3a62b5
    #With this hash, it can be download from https://resources.download.minecraft.net/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    #And saved at assets/objects/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    callback.get("setMax",empty)(len(assets_data["objects"]))
    count = 0
    for key,value in assets_data["objects"].items():
        download_file("https://resources.download.minecraft.net/" + value["hash"][:2] + "/" + value["hash"],os.path.join(path,"assets","objects",value["hash"][:2],value["hash"]),callback)
        count += 1
        callback.get("setProgress",empty)(count)

def do_version_install(versionid,path,callback,url=None):
    #Download and read versions.json
    if url:
        download_file(url,os.path.join(path,"versions",versionid,versionid + ".json"),callback)
    with open(os.path.join(path,"versions",versionid,versionid + ".json")) as f:
        versiondata = json.load(f)
    #For Forge
    if "inheritsFrom" in versiondata:
        versiondata = inherit_json(versiondata,path)
    install_libraries(versiondata,path,callback)
    install_assets(versiondata,path,callback)
    #Download minecraft.jar
    if "downloads" in versiondata:
        download_file(versiondata["downloads"]["client"]["url"],os.path.join(path,"versions",versiondata["id"],versiondata["id"] + ".jar"),callback)
    #Need to copy jar for old forge versions
    if not os.path.isfile(os.path.join(path,"versions",versiondata["id"],versiondata["id"] + ".jar")) and "inheritsFrom" in versiondata:
        inheritsFrom = versiondata["inheritsFrom"]
        shutil.copyfile(os.path.join(path,"versions",versiondata["id"],versiondata["id"] + ".jar"),os.path.join(path,"versions",inheritsFrom,inheritsFrom + ".jar"))

def install_minecraft_version(versionid,path,callback=None):
    if callback == None:
        callback = {}
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    for i in version_list["versions"]:
        if i["id"] == versionid:
            do_version_install(versionid,path,callback,url=i["url"])
            return True
    if not os.path.isdir(os.path.join(path,"versions")):
        return False
    for i in os.listdir(os.path.join(path,"versions")):
        if i == versionid:
            do_version_install(versionid,path,callback)
            return True
    return False
