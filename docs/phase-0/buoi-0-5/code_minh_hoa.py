# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# Cùng dữ liệu nhưng hai biểu đồ trả lời hai câu hỏi khác nhau.
names = ["An", "Binh", "Chi", "Dung"]
scores = np.array([8.5, 6.0, 7.0, 9.0])
fig, axes = plt.subplots(1, 2, figsize=(8, 3), layout="constrained")
axes[0].bar(names, scores)
axes[0].set(title="Diem tung hoc sinh", ylabel="Diem / 10", ylim=(0,10))
axes[1].hist(scores, bins=[0,5,7,9,10], edgecolor="black")
axes[1].set(title="Phan bo diem", xlabel="Diem", ylabel="So hoc sinh")
fig.savefig("demo_plot.png", dpi=120)
plt.close(fig)
print("Điểm trung bình:", scores.mean())
print("Số mẫu:", len(scores))
print("Biểu đồ đã lưu: demo_plot.png")
