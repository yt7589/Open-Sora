# 数据集处理程序入口
import os
import argparse
from typing import List
import json
import cv2

def get_min_json():
    '''
    截取个视频作为创建最小数据集用
    '''
    json_rfn = 'datas/hd_vg_130m/metafiles/hdvg_0.json'
    dest_dict = {}
    num = 0
    with open(json_rfn, 'r', encoding='utf-8') as fd:
        data = json.load(fd)
    print(f'data: {type(data)};')
    for k, v in data.items():
        dest_dict[k] = v
        num += 1
        if num > 10:
            break
    with open('./datas/a1.json', 'w', encoding='utf-8') as wfd:
        json.dump(dest_dict, wfd)/home/psdz/yantao/awork/Open-Sora/datas/vrcad/videos/xeq1_1_f10x_20230926_081056_0.mp4
    print(f'########### ^_^ The End! ^_^ ##################')

def get_video_url(json_fn:str) -> List[str]:
    '''
    获取Json文件中的视频URL列表
    '''
    with open(json_fn, 'r', encoding='utf-8') as fd:
        data = json.load(fd)
    video_urls = []
    for k, v in data.items():
        video_urls.append(v['url'])
    return video_urls

def cut_video(video_fn:str, frame_cnt:int = 150) -> None:
    '''
    截取视频从start帧开始到end帧结束，并以dest_video_fn为文件名
    '''
    # 读取视频
    raw_video_folder = 'datas/vrcad/raw_videos'
    video_folder = 'datas/vrcad/videos'
    cap = cv2.VideoCapture(f'{raw_video_folder}/{video_fn}')
    # 读取视频帧率
    fps_video = cap.get(cv2.CAP_PROP_FPS)
    # 设置写入视频的编码格式
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # 获取视频宽度和高度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    count = 0
    # 设置写视频的对象
    videoWriter = cv2.VideoWriter(f'{video_folder}/{video_fn[:-4]}_{count}.mp4', fourcc, fps_video, (frame_width, frame_height))
    while (cap.isOpened()):
        # 读取视屏里的图片
        ret, frame = cap.read()
        # 如果视屏没有读取结束
        if ret == True:
            # 计数器加一
            count += 1
            if count % 150 == 0:
                videoWriter.release()
                videoWriter = cv2.VideoWriter(f'{video_folder}/{video_fn[:-4]}_{count // 150}.mp4', fourcc, fps_video, (frame_width, frame_height))
            videoWriter.write(frame)
            print(f'    处理第{count}帧')
        else:
            # 写入视屏结束
            videoWriter.release()
            break

def prepare_videos():
    raw_video_folder = 'datas/vrcad/raw_videos'
    for root, dirs, files in os.walk(raw_video_folder):
        for fn in files:
            print(f'正在处理{fn}')
            cut_video(fn)

def get_vrcad_bl():
    import random
    import csv
    csv_rfn = 'datas/vrcad/output001.csv'
    prompts = []
    with open(csv_rfn, 'r', encoding='utf-8') as fd:
        csv_reader = csv.reader(fd)
        for row in csv_reader:
            # print(f'{type(row)}: {row};')
            prompts.append(row)
    cnt = len(prompts)
    num = 0
    for i in range(10):
        rv = random.randint(0, cnt-1)
        print(f'{prompts[rv][0]}: {prompts[rv][1]} ;')



def main(args:argparse.Namespace = {}) -> None:
    print(f'数据集处理程序 v0.0.3')
    get_vrcad_bl()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--run_mode', action='store',
        type=int, default=1, dest='run_mode',
        help='run mode'
    )
    return parser.parse_args()

if '__main__' == __name__:
    args = parse_args()
    main(args=args)