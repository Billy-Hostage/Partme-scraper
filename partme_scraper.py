import os
import json
import math
import datetime

from schemes import *
from posts import *
from utils import *

locked_post_id = []

def main():
    mkdir(LOCAL_STORE_PATH)
    
    conf = getConfig()
    print(f"Read Config.{json.dumps(conf, indent=4)}")
    print("Accessing sub")

    # TODO 读其他页
    subJ = partmeApiReq(conf, r"https://partme.com/api/v2/subscriptions?page=1&page_size=10", r"https://partme.com/subscriptions")

    subArray = subJ['lists']
    for sub in subArray:
        print(f"============捕获id {sub['id']} 名称 {sub['creator']} 地址 {sub['custom_path']}===================")
        id = sub['id']
        cid = sub['creator_id']
        cpath = sub['custom_path']
        if id not in conf['fetchList']:
            print(f"不在list中，跳过。")
            continue
            
        # 获取信息
        print("开始处理……")
        creatorLocalPath = os.path.join(LOCAL_STORE_PATH, sub['creator'])
        mkdir(creatorLocalPath)
        with open(os.path.join(creatorLocalPath, "date"), 'wt', encoding='utf-8') as fd:
            fd.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fd.flush()
        
        # 写入订阅者信息
        writeJsonUTF8(sub, os.path.join(creatorLocalPath, "meta.json"))
        savePartmeImg(conf, sub['avatar'], r"https://partme.com/subscriptions", creatorLocalPath)

        # 请求schemes
        schemesJson = partmeApiReq(conf, fr"https://partme.com/api/v1/schemes?user={cid}&hidden=true&all=true", fr"https://partme.com/{cpath}")
        mkdir(os.path.join(creatorLocalPath, "schemes"))
        writeJsonUTF8(schemesJson, os.path.join(creatorLocalPath, "schemes", "schemes.json"))
        saveSchemeImg(conf, schemesJson, os.path.join(creatorLocalPath, "schemes"))

        # 请求relations
        relJson = partmeApiReq(conf, fr"https://partme.com/api/v1/im-subscribes/relation?user={cid}", fr"https://partme.com/{cpath}")
        #mkdir(os.path.join(creatorLocalPath, "relations"))
        writeJsonUTF8(relJson, os.path.join(creatorLocalPath, "relations.json"))

        # 请求posts
        postsDirPath = os.path.join(creatorLocalPath, "posts")
        mkdir(postsDirPath)
        postSample = partmeApiReq(conf, fr"https://partme.com/api/v2/posts?page=1&page_size={BATCH_PAGE_SEG}&location=home_page&creator={cid}&cacheTime=1", fr"https://partme.com/{cpath}")
        totalPostCount = postSample['total']
        print(f"共{totalPostCount}个post")
        segCount = math.ceil(totalPostCount / BATCH_PAGE_SEG)
        for seg in range(1, segCount + 1):
            print(f"\t处理第{seg}页数据，共{segCount}页")
            segJson = partmeApiReq(conf, fr"https://partme.com/api/v2/posts?page={seg}&page_size={BATCH_PAGE_SEG}&location=home_page&creator={cid}&cacheTime=1", fr"https://partme.com/{cpath}")
            #writeJsonUTF8(segJson, os.path.join(postsDirPath, f"posts_{seg}.json"))
            posts = segJson['lists']
            for eachPost in posts:
                if eachPost['unlock'] == False:
                    print(rf"！！！文章{eachPost['id']}未解锁")
                    locked_post_id.append(eachPost['id'])
                processPost(conf, eachPost, postsDirPath)
                



if __name__ == "__main__":
    main()
    print(f"locked_post_id:{locked_post_id}")
