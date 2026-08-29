import os
import torch
from PIL import Image
from tqdm import tqdm
from transformers import AutoImageProcessor, AutoModel

MODEL = "facebook/dinov2-small"
# can change to facebook/dinov2-base, facebook/dinov2-large, facebook/dinov2-giant
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}

class Embedder:
    def __init__(self, device=None):
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        self.processor = AutoImageProcessor.from_pretrained(MODEL)
        self.model = AutoModel.from_pretrained(MODEL).to(self.device).eval()

    def one(self, path):
        img = Image.open(path).convert("RGB")
        inputs = self.processor(images=img, return_tensors="pt").to(self.device)
        with torch.no_grad():
            out = self.model(**inputs)
        return out.last_hidden_state.cpu().numpy().flatten()

    def folder(self, path):
        files = sorted(f for f in os.listdir(path) if os.path.splitext(f.lower())[1] in IMG_EXTS)
        return {f: self.one(os.path.join(path, f)) for f in tqdm(files, desc=os.path.basename(path))}
