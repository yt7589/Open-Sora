# 数据集处理程序入口
import argparse
from typing import List
import json

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
        json.dump(dest_dict, wfd)
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

def cut_video(video_fn:str, dest_video_fn:str, seq:int, start:int, end:int) -> None:
    '''
    截取视频从start帧开始到end帧结束，并以dest_video_fn为文件名
    '''

def main(args:argparse.Namespace = {}) -> None:
    print(f'数据集处理程序 v0.0.1')
    json_fn = 'datas/a1.json'
    video_urls = get_video_url(json_fn)
    print(f'video_urls: \n{video_urls};')

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