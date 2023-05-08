
import os
import subprocess
import shutil

PARTME_DIR = ".\\partme"
ROOT_TS_DIR = ".\\ts"
OUT_MKV_DIR = ".\\mkv"

def copy_ts():
    if not os.path.exists(ROOT_TS_DIR):
        os.mkdir(ROOT_TS_DIR)

    for root, dirs, files in os.walk(PARTME_DIR):
        # same dir under here
        found_m3 = None
        target_ts_name = "None"
        for file in files:
            if file.endswith('.m3u8'):
                print(file)
                found_m3 = file
                target_ts_name = found_m3.replace(".m3u8", ".ts")
        for file in files:
            if file == "vid.ts":
                shutil.copyfile(os.path.join(root, "vid.ts"), os.path.join(ROOT_TS_DIR, target_ts_name))

def batch_transform_mkv():
    if not os.path.exists(OUT_MKV_DIR):
        os.mkdir(OUT_MKV_DIR)
    file_list = []
    for root, dirs, files in os.walk(ROOT_TS_DIR):
        for f in files:
            file_list.append(os.path.join(ROOT_TS_DIR, f))

    for full_file_path in file_list:
        target_file_path = os.path.join(OUT_MKV_DIR, os.path.basename(full_file_path).replace(".ts", ".mkv"))
        if os.path.exists(target_file_path):
            print(f"=======Skip {target_file_path} ============")
            continue
        subprocess.run(["ffmpeg", "-fflags", "+discardcorrupt", "-i", full_file_path,
                        "-map", "0", "-c", "copy", target_file_path])

#copy_ts()
batch_transform_mkv()
