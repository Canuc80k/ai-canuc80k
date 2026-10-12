# -*- coding: utf-8 -*-

# Decoder input và target lệch một vị trí; source là một chuỗi khác.
source=["xin","chào"]
translation=["hello","there"]
decoder_input=["BOS"]+translation
decoder_target=translation+["EOS"]
print("Encoder source:",source)
print("Decoder input:",decoder_input)
print("Decoder target:",decoder_target)
# Decoder chỉ thấy các target tokens trước đó ở training (teacher forcing).
for step,(previous,wanted) in enumerate(zip(decoder_input,decoder_target)):
    print("step",step,"previous",previous,"wanted",wanted)
assert len(decoder_input)==len(decoder_target)
