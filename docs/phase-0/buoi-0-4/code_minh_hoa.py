# -*- coding: utf-8 -*-
import pandas as pd

# Bốn học sinh là fixture minh họa, không phải hồ sơ cá nhân.
students = pd.DataFrame({"id":[1,2,3,4], "class":["A","A","B","B"],
                         "score":[8.0,None,6.0,10.0]})
teachers = pd.DataFrame({"class":["A","B"], "teacher":["Mai","Son"]})
# transform trả một median cho từng dòng thuộc đúng nhóm.
median = students.groupby("class")["score"].transform("median")
students["score"] = students["score"].fillna(median)
# validate ngăn merge làm tăng số dòng do khóa trùng.
full = students.merge(teachers, on="class", validate="many_to_one")
print(full.to_string(index=False))
print("Điểm trung bình mỗi lớp:")
print(full.groupby("class")["score"].mean().to_string())
assert len(full) == 4 and full["score"].notna().all()
