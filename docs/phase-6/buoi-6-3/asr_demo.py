# -*- coding: utf-8 -*-
# Chạy: python asr_demo.py --model tiny.en.pt --audio ../../data/asr/audio/valid_0000.flac
import argparse
from pathlib import Path
import whisper
ap=argparse.ArgumentParser();ap.add_argument("--model",required=True);ap.add_argument("--audio",required=True);args=ap.parse_args()
if not Path(args.model).is_file():raise FileNotFoundError("Cần Whisper .pt checkpoint được cấp/cache")
if not Path(args.audio).is_file():raise FileNotFoundError("Cần file audio được cấp")
model=whisper.load_model(args.model,device="cpu")
result=model.transcribe(args.audio,language="en",fp16=False)
print(result["text"].strip())
# Library dùng ffmpeg để đọc audio; cần ffmpeg trong PATH. Không download model tự động ở script này.
# Đối chiếu transcript với valid_answers bằng normalizer/metric của bài.
