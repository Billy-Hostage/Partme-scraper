import requests
import os
import json
import shutil

CONFIG_FILE_PATH = "./config.json"
LOCAL_STORE_PATH = "./partme"
BATCH_PAGE_SEG = 8
BATCH_COMM_PAGE_SEG = 8
CLEAN_DUMP = False

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
def getConfig():
    with open(CONFIG_FILE_PATH, 'rt') as f:
        return json.load(f)
def getCommonHeader(conf, ref):
    return {
            "Connection": "keep-alive",
            "User-Agent": conf['ua'],
            "sec-ch-ua": r'"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "Referer": ref,
            "Accept": "application/json",
            "Host": "partme.com",
            "DNT": "1",
            "Authorization": conf['auth'],
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Accept-Encoding": "gzip, deflate, br"
        }
def getMinimalHeader(conf, ref):
    return {
        "Referer": ref,
        "Authorization": conf['auth']
    }
def writeJsonUTF8(jobj, path, indent = 4):
    with open(path, 'wt', encoding='utf-8') as f:
        f.write(json.dumps(jobj, ensure_ascii=False, indent=indent))
        f.flush()

def partmeApiReq(conf, url, ref, method='GET'):
    print(f"请求 {url}")
    r = requests.request(
        method=method,
        url=url,
        headers=getCommonHeader(conf, ref)
    )
    j = r.json()
    assert(j['code'] == 1000)
    print(f"响应msg{j['msg']}")
    return j['data']
    
def savePartmeImg(conf, url, ref, path):
    fileName = os.path.basename(url)
    assert(os.path.exists(path))
    if os.path.exists(os.path.join(path, fileName)) and not CLEAN_DUMP:
        print(f"\t\t{fileName} 已存在")
        return
    
    r = requests.request(
        method='GET',
        url=url,
        headers=getMinimalHeader(conf, ref),
    )

    with open(os.path.join(path, fileName), 'wb') as out_file:
        out_file.write(r.content)
        out_file.flush()
    del r

def savePartmeM3U8(conf, signedUrl, originalUrl, saveDirPath) -> str:
    m3Filename = os.path.basename(originalUrl)
    assert(os.path.exists(saveDirPath))
    if os.path.exists(os.path.join(saveDirPath, m3Filename)) and not CLEAN_DUMP:
        print(f"\t\t{m3Filename} 已存在")
        return os.path.join(saveDirPath, m3Filename)
    
    r = requests.request(
        method='GET',
        url=signedUrl,
        headers={
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Origin": "https://partme.com",
            "Referer": "https://partme.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
             "Sec-Fetch-Site": "same-site",
             "sec-ch-ua": r'"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
             "sec-ch-ua-mobile": "?0",
             "sec-ch-ua-platform": r'"Windows"',
             "User-Agent": conf['ua'],
             "Host": "yundun.partme.com"
        },
        timeout=30
    )
    assert(r.status_code == 200)
    with open(os.path.join(saveDirPath, m3Filename), 'wb') as out_file:
        out_file.write(r.content)
        out_file.flush()
    del r
    return os.path.join(saveDirPath, m3Filename)

def saveTsSegments(conf, url, saveTsPath, isStart = False, overwrite = False):
    if isStart:
        if os.path.exists(saveTsPath):
            if overwrite or CLEAN_DUMP:
                os.remove(saveTsPath)
            else:
                print(f"\t\t{os.path.basename(saveTsPath)} 已存在")
                return False

    r = requests.request(
        method='GET',
        url=url,
        headers={
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Origin": "https://partme.com",
            "Referer": "https://partme.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
             "Sec-Fetch-Site": "same-site",
             "sec-ch-ua": r'"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
             "sec-ch-ua-mobile": "?0",
             "sec-ch-ua-platform": r'"Windows"',
             "User-Agent": conf['ua'],
             "Host": "yundun.partme.com"
        },
        timeout=30,
    )
    assert(r.status_code == 200)
    offset_after_write = None
    with open(saveTsPath, 'ab') as out_file:
        out_file.write(r.content)
        out_file.flush()
        offset_after_write = out_file.tell()
    del r
    return offset_after_write