# Code mẫu — Kiểm tra khóa 1

Buổi ôn này ghép mọi bước đã học thành một quy trình trọn vẹn: dữ liệu, cách chia, baseline, model, rồi tới bảng kết quả nộp bài. Ví dụ thứ hai tập trung vào những lỗi mà một con số accuracy hay MAE tổng có thể che mất.

## Ví dụ 1: Dự đoán điểm buổi luyện từ một bảng thiếu dữ liệu

Mỗi hàng là một học viên giả lập, độc lập với các hàng khác. Có ba cột đầu vào: điểm buổi trước, số giờ tự học, và hình thức luyện, học nhóm hoặc tự học. Target là điểm của buổi mới. Khi nhập liệu, điểm cũ và giờ tự học đôi khi bị bỏ trống. Mỗi hàng là một người khác nhau nên chia ngẫu nhiên là hợp lý. Nếu một người có nhiều hàng, ta phải chia theo người, hoặc theo thời gian, tùy mục tiêu.

Bước đầu: sinh dữ liệu, tách riêng test, rồi in vài hàng để kiểm các cột. Target được tính từ dữ liệu đầy đủ. Sau đó một số ô đầu vào mới bị xóa thành NaN, giống như nhập liệu bị sót.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(41)
previous = rng.uniform(3, 9, 120)
hours = rng.uniform(0, 8, 120)
mode = np.where(np.arange(120) % 2 == 0, "group", "solo")
target = 0.65 * previous + 0.4 * hours + 0.7 * (mode == "group") + rng.normal(0, 0.3, 120)
frame = pd.DataFrame({"id": np.arange(1000, 1120), "previous": previous,
                      "hours": hours, "mode": mode})
frame.loc[::13, "previous"] = np.nan
frame.loc[::17, "hours"] = np.nan
dev, test, y_dev, y_test = train_test_split(frame, target, test_size=0.25, random_state=2)
feature_columns = ["previous", "hours", "mode"]
X_dev, X_test = dev[feature_columns], test[feature_columns]
print("số hàng phát triển / test:", len(dev), len(test))
print("4 hàng phát triển:")
print(X_dev.head(4).round(2).to_string(index=False))
print("số NaN phát triển:", X_dev[["previous", "hours"]].isna().sum().to_dict())
assert set(dev["id"]).isdisjoint(set(test["id"]))
```

```output
số hàng phát triển / test: 90 30
4 hàng phát triển:
 previous  hours  mode
     8.57   5.03 group
      NaN    NaN group
     8.38   0.73  solo
     5.17   2.75  solo
số NaN phát triển: {'previous': 9, 'hours': 8}
```

Cột `id` chỉ dùng để biết hàng nào là ai và để xếp bảng kết quả, không được đưa vào làm feature. Hàng thứ hai thiếu cả hai đầu vào nhưng vẫn có target. Điều này hợp lý: nhập sót điểm cũ không làm mất điểm của buổi mới. Test được tách ra ngay từ đầu, trước mọi bước chọn model, để không vô tình học từ nó.

Tiếp theo là so các ứng viên. Baseline đoán bằng trung vị, vì metric là MAE. Hai model thật là Ridge có chuẩn hóa và một cây quyết định bị giới hạn độ sâu. Cả ba được chấm trên cùng ba fold. Bước tiền xử lý nằm trong từng Pipeline, nên giá trị trung vị để điền chỗ trống và danh sách hình thức luyện đều chỉ học từ phần train của mỗi fold.

```python
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

def make_preprocessor(scale):
    number_steps = [SimpleImputer(strategy="median", add_indicator=True)]
    if scale:
        number_steps.append(StandardScaler())
    return ColumnTransformer([
        ("number", make_pipeline(*number_steps), ["previous", "hours"]),
        ("mode", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["mode"]),
    ])

candidates = {
    "median": DummyRegressor(strategy="median"),
    "ridge": make_pipeline(make_preprocessor(True), Ridge(alpha=1.)),
    "tree": make_pipeline(make_preprocessor(False),
                           DecisionTreeRegressor(max_depth=4, min_samples_leaf=5, random_state=0)),
}
folds = list(KFold(3, shuffle=True, random_state=9).split(X_dev))
cv_errors = {}
for name, model in candidates.items():
    errors = -cross_val_score(model, X_dev, y_dev, cv=folds,
                              scoring="neg_mean_absolute_error", n_jobs=1)
    cv_errors[name] = errors.mean()
    print(name, "MAE từng fold:", errors.round(3).tolist(), "mean:", round(float(errors.mean()), 3))
selected_name = min(cv_errors, key=cv_errors.get)
print("chọn từ CV:", selected_name)
```

```output
median MAE từng fold: [1.077, 1.213, 1.56] mean: 1.283
ridge MAE từng fold: [0.405, 0.383, 0.324] mean: 0.371
tree MAE từng fold: [0.791, 0.619, 0.631] mean: 0.68
chọn từ CV: ridge
```

Ridge thắng ở cả ba fold, MAE trung bình 0.371, so với 1.283 của baseline và 0.680 của cây. Điều này hợp với dữ liệu, vì target vốn được tạo bằng một công thức tuyến tính. Dấu trừ trước `cross_val_score` là để đổi lại thành MAE, vì scikit-learn quy ước score càng lớn càng tốt nên trả về MAE âm. `add_indicator=True` thêm một cột đánh dấu ô nào từng bị trống, để model biết giá trị ở đó là điền vào chứ không phải đo thật.

Giờ fit Ridge trên toàn bộ 90 hàng phát triển, chấm test đúng một lần, rồi lập bảng kết quả theo ID và đúng thứ tự của test. Ta chỉ in vài hàng để kiểm, không cần ghi file.

```python
from sklearn.metrics import mean_absolute_error

chosen = candidates[selected_name].fit(X_dev, y_dev)
pred = chosen.predict(X_test)
submission = pd.DataFrame({"id": test["id"].to_numpy(), "prediction": pred})
assert pred.shape == y_test.shape and np.isfinite(pred).all()
assert submission["id"].is_unique
assert np.array_equal(submission["id"], test["id"])
print("test MAE:", round(mean_absolute_error(y_test, pred), 3))
print("5 hàng đầu ra:")
print(submission.head(5).round(3).to_string(index=False))
missing = X_test[["previous", "hours"]].isna().any(axis=1).to_numpy()
for label, mask in [("đủ input", ~missing), ("thiếu input", missing)]:
    if mask.any():
        print(label, "n =", int(mask.sum()), "MAE =",
              round(mean_absolute_error(y_test[mask], pred[mask]), 3))
```

```output
test MAE: 0.248
5 hàng đầu ra:
  id  prediction
1041       3.516
1106       6.092
1074       5.183
1024       8.740
1055       8.548
đủ input n = 29 MAE = 0.222
thiếu input n = 1 MAE = 1.006
```

MAE test là 0.248. Tách ra thì 29 hàng đủ dữ liệu có MAE 0.222, còn hàng duy nhất bị thiếu lệch tới 1.006. Một hàng thì chưa đủ để kết luận về mọi hàng thiếu dữ liệu, nhưng nó chỉ đúng chỗ cần xem: điền trung vị không thể trả lại thông tin đã mất. Nếu sau khi xem bảng này mà ta sửa cấu hình, thì test đã góp phần vào việc chọn, và muốn có một con số khách quan sẽ cần thêm một tập đánh giá khác.

## Ví dụ 2: Lỗi shape và lỗi ID đều chạy được, không báo gì

Ba mẫu có ID `103, 101, 102`, nhãn `[2, 4, 8]`, và dự đoán `[3, 4, 7]`. MAE đúng là `(1 + 0 + 1) / 3`. Ta cố tình gây hai lỗi. Lỗi thứ nhất: biến dự đoán thành một cột, nhưng quên làm vậy với nhãn. Lỗi thứ hai: sắp lại cột ID mà không sắp dự đoán theo.

```python
import numpy as np
import pandas as pd

ids = np.array([103, 101, 102])
truth = np.array([2., 4., 8.])
pred = np.array([3., 4., 7.])
pred_column = pred[:, None]
wrong_difference = pred_column - truth
print("shape lỗi:", wrong_difference.shape)
print("MAE sai do broadcasting:", round(float(np.abs(wrong_difference).mean()), 3))
print("MAE đúng:", round(float(np.abs(pred_column.ravel() - truth).mean()), 3))
assert pred_column.ravel().shape == truth.shape

correct = pd.DataFrame({"id": ids, "prediction": pred})
wrong = pd.DataFrame({"id": np.sort(ids), "prediction": pred})
reference = pd.DataFrame({"id": ids, "truth": truth})
for name, table in [("giữ cặp ID–pred", correct), ("sort chỉ ID", wrong)]:
    checked = reference.merge(table, on="id", validate="one_to_one", sort=False)
    mae = np.abs(checked["prediction"] - checked["truth"]).mean()
    print(name, "MAE ghép theo ID:", round(float(mae), 3))
print("bảng đúng sau khi sort cả hàng:")
print(correct.sort_values("id").to_string(index=False))
```

```output
shape lỗi: (3, 3)
MAE sai do broadcasting: 2.444
MAE đúng: 0.667
giữ cặp ID–pred MAE ghép theo ID: 0.667
sort chỉ ID MAE ghép theo ID: 3.333
bảng đúng sau khi sort cả hàng:
 id  prediction
101         4.0
102         7.0
103         3.0
```

MAE đúng là 0.667. Ở lỗi thứ nhất, một cột trừ cho một hàng tạo ra ma trận `(3, 3)`, tức mỗi dự đoán bị trừ cho cả ba nhãn, và MAE thành 2.444. Python không báo lỗi gì.

Ở lỗi thứ hai, mọi thứ trông vẫn ổn: đủ ba hàng, ID không trùng, các giá trị dự đoán y nguyên. Nhưng dự đoán đã bị gán nhầm người, và MAE vọt lên 3.333. Nếu đề yêu cầu ID tăng dần, phải sắp cả hàng, như bảng cuối. Nếu đề yêu cầu giữ thứ tự của file test, thì giữ nguyên thứ tự ấy. Kiểm bảng kết quả phải theo đúng yêu cầu của đề, chứ không chỉ kiểm model chạy xong.
