
import os
import requests

from utils import savePartmeImg

def saveSchemeImg(conf, scheme, creatorLocalSchemePath):
    assert(os.path.exists(creatorLocalSchemePath))
    l:list[dict] = scheme['lists']
    for eachSche in l:
        v = eachSche.values()
        for possibleUrl in v:
            if type(possibleUrl) is not str:
                continue
            elif not possibleUrl.startswith("http") or not possibleUrl.endswith(("jpeg", "png")):
                continue
            print(f"\t保存图像 {possibleUrl}")
            savePartmeImg(conf, possibleUrl, "https://partme.com/", creatorLocalSchemePath)
