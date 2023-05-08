import os
import math
import time

from utils import *
from sign_generator import getURLSign

import m3u8

def processPost(conf, postObj, postDir):
    pid = str(postObj['id'])
    print(f"\t\t处理post {pid}")
    currentPostDir = os.path.join(postDir, pid)
    mkdir(currentPostDir)
    
    internalPost = partmeApiReq(conf, fr"https://partme.com/api/v2/posts/{pid}", fr"https://partme.com/posts/{pid}")
    writeJsonUTF8(internalPost, os.path.join(currentPostDir, "post.json"))

    # 保存评论
    commentsSample = partmeApiReq(conf, fr"https://partme.com/api/v1/post-comments?page=1&&page_size={BATCH_COMM_PAGE_SEG}&&post={pid}", fr"https://partme.com/posts/{pid}")
    totalComCount = commentsSample['total']
    print(f"共{totalComCount}个comments")
    segCount = math.ceil(totalComCount / BATCH_COMM_PAGE_SEG)
    for seg in range(1, segCount + 1):
        if seg == 1:
            segCommJson = commentsSample
        else:
            segCommJson = partmeApiReq(conf, fr"https://partme.com/api/v1/post-comments?page={seg}&&page_size={BATCH_COMM_PAGE_SEG}&&post={pid}", fr"https://partme.com/posts/{pid}")
        writeJsonUTF8(segCommJson, os.path.join(currentPostDir, f"comments_{seg}.json"))

    # 保存图片
    imageList = internalPost['post_images'] if 'post_images' in internalPost  else []
    if imageList:
        mkdir(os.path.join(currentPostDir, "images"))
    else:
        print("\t\t\t暂无图片")
    for i in imageList:
        print(f"\t\t\t保存图片 {i['uid']}")
        savePartmeImg(conf, i['pic_view_url'], fr"https://partme.com/posts/{pid}", os.path.join(currentPostDir, "images"))

    # 保存视频m3u8
    postVid = internalPost['post_video']
    if not postVid:
        print("\t\t\t暂无视频")
        return
    vidM3U8: str = postVid['m3u8_url']
    if 'sign=' in vidM3U8:
        vidM3U8 = vidM3U8[:len(vidM3U8) - 61] # 61 constant as len(sign） + len('?sign=')
    signedM3U8Url = getURLSign(vidM3U8)
    vidDirPath = os.path.join(currentPostDir, "video")
    mkdir(vidDirPath)
    print(f"\t\t\t保存M3U8 {vidM3U8}")
    localM3u8Path = savePartmeM3U8(conf, signedM3U8Url, vidM3U8, vidDirPath)
    #now readback m3u8
    with open(localM3u8Path, mode='rt', encoding='utf8') as mf:
        m3u8Content = mf.read()
    
    playlist = m3u8.loads(m3u8Content, "https://yundun.partme.com/")
    saveTsPath = os.path.join(vidDirPath, "vid.ts")

    # 处理done mark
    if os.path.exists(os.path.join(vidDirPath, '.done')):
        # 存在已有的donemark
        if CLEAN_DUMP:
            # 删掉
            os.remove(os.path.join(vidDirPath, '.done'))

    has_done_mark = os.path.exists(os.path.join(vidDirPath, '.done'))
    completed_download = True
    for idx, seg in enumerate(playlist.segments):
        print(f"\t\t\t下载分块 {idx + 1}/{len(playlist.segments)}")
        absTsUrl = seg.absolute_uri
        out_offset = saveTsSegments(conf, absTsUrl, saveTsPath, idx == 0, not has_done_mark)
        if out_offset == False:
            completed_download = False
            break
        # TODO write progress
        time.sleep(0.7)

    # 写入done mark
    if completed_download:
        with open(os.path.join(vidDirPath, '.done'), mode='wt') as doneMark:
            doneMark.write("Done")
            doneMark.flush()
