import os
import torch
ROOT = os.path.join(os.path.expanduser("~"), ".cache", "space") # ckpt at cache, and dir to get embeddings

def _path(folder):
    return os.path.join(ROOT, os.path.basename(folder.rstrip("/")), "embeddings.pt")

def load(folder):
    p = _path(folder)
    return torch.load(p, weights_only=False) if os.path.exists(p) else None

def save(folder, embeds):
    p = _path(folder)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    torch.save(embeds, p)
