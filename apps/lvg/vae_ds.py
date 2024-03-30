# 视频变分自动编码机数据集类
import os
import math
from typing import List, Any
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms

class VaeDs(Dataset):
    def __init__(self, video_folder:str):
        self.name = ''
        self.items = []
        self._add_videos(video_folder=video_folder, items=self.items)

    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        return self.items[index]
    
    def _add_videos(self, video_folder:str, items:List) -> None:
        for root, dirs, files in os.walk(video_folder):
            for fn in files:
                video_fn = f'{root}/{fn}'
                self._process_video(video_fn=video_fn, items=items)
            # 递归处理目录
            for dd in dirs:
                self._add_videos(dd, items)
    
    def _process_video(self, video_fn:str, items:List) -> None:
        img_trans = transforms.ToTensor()
        # Open the video file
        cap = cv2.VideoCapture(video_fn)
        # Get the frames per second
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = 2
        frame_cnt = 16
        n = math.ceil(fps * duration / frame_cnt) # every n-th frame
        count = 0
        frames = None
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            count += 1
            frame = img_trans(frame).unsqueeze(0)
            if (count-1) % n == 0:
                if frames is None:
                    frames = frame
                else:
                    frames = torch.vstack((frames, frame))
        frames = torch.transpose(frames, 0, 1)
        items.append(frames)
    
    @staticmethod
    def segment_video(video_fn:str, out_fn_base:str) ->None:
        # Open the video file
        cap = cv2.VideoCapture(video_fn)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # codec
        # Get the frames per second
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = 2
        frame_cnt = 16
        n = math.ceil(fps * duration / frame_cnt) # every n-th frame
        print(f'### fps: {fps}; n: {n};')
        count = 0
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            count += 1
            frames.append(frame)
            print(f'### {count}: {len(frames)};')
            if len(frames) == frame_cnt*n:
                print(f'    生成视频文件：{out_fn_base}_{count//(frame_cnt*n):08d}.mp4')
                frame_height, frame_width, _ = frames[0].shape
                out = cv2.VideoWriter(f'{out_fn_base}_{count//(frame_cnt*n):08d}.mp4', fourcc, fps, (frame_width,frame_height))
                for frm in frames:
                    out.write(frm)
                out.release()
                frames = []
    @staticmethod
    def check_video(video_fn:str):
        # Open the video file
        cap = cv2.VideoCapture(video_fn)
        # Get the frames per second
        fps = cap.get(cv2.CAP_PROP_FPS)
        jpg_fn_base = './datas/vrcad/tvs/x_'
        num = 0
        while True:
            num += 1
            ret, frame = cap.read()
            if not ret:
                break
            jpg_fn = f'{jpg_fn_base}{num:03d}.jpg'
            cv2.imwrite(jpg_fn, frame)
            print(f'### {num}: {jpg_fn};')

    @staticmethod
    def extract_frames_per_n(video_fn:str, frame_cnt:int = 16) -> List[Any]:
        frames = []
        # Open the video file
        cap = cv2.VideoCapture(video_fn)
        # Get the frames per second
        fps = cap.get(cv2.CAP_PROP_FPS)
        per_n = math.ceil(fps*2/frame_cnt)
        jpg_fn_base = './datas/vrcad/tvs/y_'
        num = 0
        while True:
            num += 1
            ret, frame = cap.read()
            if not ret:
                break
            if (num-1) % per_n == 0:
                jpg_fn = f'{jpg_fn_base}{(num-1)//per_n:03d}.jpg'
                cv2.imwrite(jpg_fn, frame)
            print(f'### frame_{num}:')
        return frames
                


    @staticmethod
    def process_videos(video_path, output_path):
        '''
        将帧号写在视频的左上角
        '''
        frames = VaeDs.extract_frames(video_path)
        height, width, layers = frames[0].shape
        size = (width, height)
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, size)
        for frame in frames:
            out.write(frame)
        out.release()        










    @staticmethod
    def draw_frame_number(frame, frame_num):
        # Load the font
        font = ImageFont.truetype('Sarai', 30)
        # Convert to PIL image for easy manipulation
        imgPil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # Get a drawing context
        draw = ImageDraw.Draw(imgPil)
        # Draw the text on top left corner of the image
        draw.text((10, 30), f"Frame: {frame_num}", font=font, fill=(255, 255, 0))
        # Convert back to OpenCV format
        frame = cv2.cvtColor(np.array(imgPil), cv2.COLOR_RGB2BGR)
        return frame

    @staticmethod
    def extract_frames(video_path):
        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_num = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = VaeDs.draw_frame_number(frame, frame_num)
            frames.append(frame)
            frame_num += 1
            print(f'### fram_num: {frame_num};')
        return frames