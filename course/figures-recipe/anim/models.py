"""Model có sẵn trong cache của máy (không tải mạng): ResNet-18 ImageNet, CLIP ViT-B/32, MiniLM, Qwen2.5-0.5B, wav2vec2.
Hàm nào cũng chạy CPU, seed cố định."""
import os
os.environ.setdefault('HF_HUB_OFFLINE', '1')
os.environ.setdefault('TRANSFORMERS_OFFLINE', '1')
import numpy as np
import torch
from PIL import Image

_cache = {}


def resnet18():
    if 'r18' not in _cache:
        from torchvision.models import resnet18 as R, ResNet18_Weights as W
        m = R(weights=W.IMAGENET1K_V1).eval()
        _cache['r18'] = (m, W.IMAGENET1K_V1.meta['categories'])
    return _cache['r18']


MEAN = np.array([0.485, 0.456, 0.406])
STD = np.array([0.229, 0.224, 0.225])


def center224(img):
    """Resize cạnh ngắn 256, cắt giữa 224 như preprocessing ImageNet; trả uint8 224x224x3."""
    im = Image.fromarray(np.asarray(img)).convert('RGB')
    w, h = im.size
    s = 256 / min(w, h)
    im = im.resize((round(w * s), round(h * s)), Image.BILINEAR)
    w, h = im.size
    l, t = (w - 224) // 2, (h - 224) // 2
    return np.asarray(im.crop((l, t, l + 224, t + 224)))


def to_tensor(rgb224):
    x = (np.asarray(rgb224, float) / 255 - MEAN) / STD
    return torch.tensor(x.transpose(2, 0, 1)[None], dtype=torch.float32)


def clip():
    if 'clip' not in _cache:
        from sentence_transformers import SentenceTransformer
        _cache['clip'] = SentenceTransformer('clip-ViT-B-32', device='cpu')
    return _cache['clip']


FASHION_VI = ['áo thun', 'quần dài', 'áo len', 'váy', 'áo khoác', 'xăng-đan', 'áo sơ mi', 'giày thể thao', 'túi xách', 'bốt']
CIFAR_VI = ['máy bay', 'ô tô', 'chim', 'mèo', 'hươu', 'chó', 'ếch', 'ngựa', 'tàu thủy', 'xe tải']


def fashion(split='train'):
    """Fashion-MNIST (Zalando, MIT) từ cache Keras trên máy: (N, 28, 28) uint8 và nhãn."""
    import gzip
    from pathlib import Path
    d = Path.home() / '.keras/datasets/fashion-mnist'
    pre = 'train' if split == 'train' else 't10k'
    with gzip.open(d / f'{pre}-images-idx3-ubyte.gz') as f:
        X = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28, 28)
    with gzip.open(d / f'{pre}-labels-idx1-ubyte.gz') as f:
        y = np.frombuffer(f.read(), np.uint8, offset=8)
    return X, y.astype(int)


def cifar(batch='data_batch_1'):
    """CIFAR-10 (Krizhevsky 2009) từ cache Keras trên máy: (N, 32, 32, 3) uint8 và nhãn."""
    import pickle
    from pathlib import Path
    p = Path.home() / '.keras/datasets/cifar-10-batches-py-target/cifar-10-batches-py' / batch
    with open(p, 'rb') as f:
        d = pickle.load(f, encoding='bytes')
    X = d[b'data'].reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
    return X, np.array(d[b'labels'])
