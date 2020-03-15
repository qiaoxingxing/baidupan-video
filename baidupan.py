# encoding:utf8
import os
import time
from bypy import ByPy

bp = ByPy(verify=False)
remote_root = r"/视频"
local_root = r"./video-pan"

def get_file_bytes(video_name, file_name):
    print("baidu 下载开始")
    start_time = time.time()
    remote_path = remote_root + r"/"+video_name+"/"+file_name
    local_path = local_root
    bp.downfile(remote_path, local_path)
    local_file = os.path.join(local_path, file_name)
    end_time = time.time()
    file_bytes = open(local_file, "rb").read()
    speed = len(file_bytes)/1024/((end_time-start_time))
    print("baidu 下载完成: %s kb/s" % int(speed))
    return file_bytes


def get_dir_list():
    '''
    获取视频下的目录列表, 每个目录对应一个视频
    '''
    result = bp.list(remote_root)
    if result != 0:
        print("请求错误")
        return []
    dir_list = []
    for item in bp.jsonq[-1]['list']:
        if item['isdir'] == 1:
            dir_list.append(item['server_filename'])
    return dir_list


if __name__ == "__main__":
    pass
    # get_list()
