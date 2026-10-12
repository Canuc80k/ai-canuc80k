# -*- coding: utf-8 -*-
# Chạy: python audioqa_demo.py --model local_qwen2audio --audio sample.flac --question "Describe this sound"
import argparse,math
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
import torch
from transformers import AutoProcessor,Qwen2AudioForConditionalGeneration
ap=argparse.ArgumentParser();ap.add_argument("--model",required=True);ap.add_argument("--audio",required=True);ap.add_argument("--question",required=True);args=ap.parse_args()
processor=AutoProcessor.from_pretrained(args.model,local_files_only=True)
model=Qwen2AudioForConditionalGeneration.from_pretrained(args.model,local_files_only=True,
    trust_remote_code=False,device_map="auto")
audio,sr=sf.read(args.audio)
if audio.ndim==2:audio=audio.mean(axis=1)
target_sr=processor.feature_extractor.sampling_rate
if sr!=target_sr:
    g=math.gcd(sr,target_sr);audio=resample_poly(audio,target_sr//g,sr//g)
conversation=[{"role":"user","content":[{"type":"audio","audio_url":args.audio},
    {"type":"text","text":args.question}]}]
text=processor.apply_chat_template(conversation,add_generation_prompt=True,tokenize=False)
inputs=processor(text=text,audio=[np.asarray(audio)],return_tensors="pt",padding=True).to(model.device)
with torch.no_grad():ids=model.generate(**inputs,max_new_tokens=128)
ids=ids[:,inputs.input_ids.shape[1]:]
print(processor.batch_decode(ids,skip_special_tokens=True)[0])
# Cần checkpoint Qwen2Audio Instruct và máy đủ RAM/VRAM; không coi fixture tones là lời nói thật.
