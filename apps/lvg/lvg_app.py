# Long Video Generation：长视频生成
import argparse
from apps.lvg.vae_ds import VaeDs
from torch.utils.data import DataLoader 

class LvgApp(object):
    def __init__(self):
        self.name = 'apps.lvg.lvg_app.LvgApp'

    @staticmethod
    def startup(args:argparse.Namespace = {}) -> None:
        print(f'长视频生成 v0.0.1')
        video_fn = 'datas/vrcad/raw_videos/xeq1_1_f10x_20230926_081056.mp4'
        dest_fn = 'datas/vrcad/tvs/v001.mp4'
        # VaeDs.process_videos(video_fn, dest_fn)
        out_fn_base = "datas/vrcad/tvs/a"
        # VaeDs.segment_video(video_fn=dest_fn, out_fn_base=out_fn_base)
        # VaeDs.check_video(video_fn = "datas/vrcad/tvs/a_2.mp4")
        video_fn1 = 'datas/vrcad/tvs/a_00000003.mp4'
        frame_cnt = 16
        # VaeDs.extract_frames_per_n(video_fn=video_fn1, frame_cnt=frame_cnt)
        video_folder = 'datas/vrcad/t001'
        ds = VaeDs(video_folder=video_folder)
        # implementing dataloader on the dataset and printing per batch 
        dataloader = DataLoader(ds, batch_size=2, shuffle=True) 
        for i, batch in enumerate(dataloader): 
            print(f'{i}: {type(batch)}; \n{batch.shape};') 


def main(args:argparse.Namespace = {}) -> None:
    LvgApp.startup(args=args)

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