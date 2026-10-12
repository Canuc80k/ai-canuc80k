# -*- coding: utf-8 -*-
import json

# Không gọi API: minh họa hợp đồng structured output trong lab lớp.
allowed={"weather","sport"}
responses=['{"label":"weather"}','{"label":"music"}','label: sport']
for text in responses:
    try:
        obj=json.loads(text)
        if set(obj)!={"label"} or obj["label"] not in allowed:
            raise ValueError("Sai schema/label")
        print("Hợp lệ:",obj["label"])
    except (ValueError,TypeError,json.JSONDecodeError):
        print("Không hợp lệ:",text)
# VLM thật có ảnh+question; không chỉ một câu text. Nguồn AIO39 có ví dụ đầy đủ.
