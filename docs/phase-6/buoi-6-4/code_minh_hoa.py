# -*- coding: utf-8 -*-
import numpy as np

# Hai modalities có scores cho cùng hai lớp: late fusion có trọng số.
text_prob=np.array([.8,.2]); audio_prob=np.array([.3,.7])
alpha=.6
fused=alpha*text_prob+(1-alpha)*audio_prob
print("Text:",text_prob.tolist(),"Audio:",audio_prob.tolist())
print("Fused:",fused.round(4).tolist(),"Label:",int(fused.argmax()))
assert np.isclose(fused.sum(),1)
# Đây là late-fusion fixture, không Qwen/Voxtral. Code model thật có trong tệp bổ sung.
