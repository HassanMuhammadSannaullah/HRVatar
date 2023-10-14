import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
checkpoint_path = "hrvatar\\wav2lip\checkpoints\\wav2lip_gan.pth"

if device == "cuda":
    print("loading checkpoint in cuda")
    wav_2_lip_checkpoint = torch.load(checkpoint_path)
else:
    print("loading checkpoint in cpu")
    wav_2_lip_checkpoint = torch.load(
        checkpoint_path, map_location=lambda storage, loc: storage
    )
