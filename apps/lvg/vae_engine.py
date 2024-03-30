# VAE使用类，包括训练、推理
from typing import Any
import torch
from opensora.registry import MODELS, SCHEDULERS, build_module
from opensora.models.vae import VideoAutoencoderKL

class VaeEngine(object):
    def __init__(self):
        self.name = 'apps.lvg.vae_engine.VaeEngine'

    @staticmethod
    def build_model() -> VideoAutoencoderKL:
        vae = build_module('VideoAutoencoderKL', MODELS)
        return vae
    
    @staticmethod
    def encode(vae:VideoAutoencoderKL, x:torch.Tensor) -> torch.Tensor:
        '''
        x: [B, C, T, H, W]
        '''
        return vae.encode(x)  # [B, C, T, H/P, W/P]