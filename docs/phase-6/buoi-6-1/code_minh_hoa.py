# -*- coding: utf-8 -*-
import numpy as np

# Tone tổng hợp 440Hz: để hiểu waveform và sample rate, không giọng thật.
sample_rate=8000; duration=.1
t=np.arange(int(sample_rate*duration))/sample_rate
wave=np.sin(2*np.pi*440*t)
window=np.hanning(len(wave))
spectrum=np.abs(np.fft.rfft(wave*window))
frequencies=np.fft.rfftfreq(len(wave),d=1/sample_rate)
peak=frequencies[spectrum.argmax()]
print("Samples:",len(wave),"duration:",len(wave)/sample_rate)
print("Peak frequency:",peak)
assert peak==440
# FFT phổ này chưa phải Mel spectrogram: cần nhiều frames và Mel filter bank.
