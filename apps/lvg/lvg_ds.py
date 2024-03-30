#
import cv2
from torch.utils.data import Dataset

class LvgDs(Dataset):
    def __init__(self):
        self.name = ''

    def __len__(self):
        return 0
    
    def __getitem__(self, index):
        return None