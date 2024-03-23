num_frames = 16
frame_interval = 3
image_size = (256, 256)

# Define dataset
root = None
data_path = "CSV_PATH"
use_image_transform = False
num_workers = 4

# Define acceleration
dtype = "bf16"
grad_checkpoint = True
plugin = "zero2"
sp_size = 1

# Define model
model = dict(
    type="STDiT-XL/2",
    space_scale=0.5,
    time_scale=1.0,
    from_pretrained="/home/psdz/yantao/awork/Open-Sora/opensora/models/Open-Sora/OpenSora-v1-HQ-16x256x256.pth",
    enable_flashattn=True,
    enable_layernorm_kernel=True,
)
vae = dict(
    type="VideoAutoencoderKL",
    from_pretrained="/home/psdz/yantao/awork/Open-Sora/opensora/models/sd-vae-ft-ema",
)
text_encoder = dict(
    type="t5",
    from_pretrained="/home/psdz/yantao/awork/Open-Sora/opensora/models/text_encoder",
    model_max_length=120,
    shardformer=True,
)
scheduler = dict(
    type="iddpm",
    timestep_respacing="",
)

# Others
seed = 42
outputs = "outputs"
wandb = False

epochs = 1000
log_every = 10
ckpt_every = 1000
load = None

batch_size = 1
lr = 2e-5
grad_clip = 1.0
