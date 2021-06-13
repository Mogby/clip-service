from typing import List

import clip
import torch

from PIL import Image


class ClipEmbedder:
    def __init__(self, model_name='ViT-B/32'):
        assert model_name in clip.available_models()
        self.model, self.preprocess = clip.load(model_name)

    def embed_image(self, image: Image.Image) -> torch.tensor:
        with torch.no_grad():
            image = self.preprocess(image)
            image_batch = image.unsqueeze(0)
            out_batch = self.model.encode_image(image_batch)
            out = out_batch.squeeze(0)
        return out

    def embed_text(self, text: str) -> torch.tensor:
        with torch.no_grad():
            text_batch = clip.tokenize([text])
            out_batch = self.model.encode_text(text_batch)
            out = out_batch.squeeze(0)
        return out

