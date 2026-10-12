# Bộ nhớ GPU

Huấn luyện ResNet-50 với batch $128$ trên GPU $16$ GiB báo hết bộ nhớ. Nên đổi sang mixed precision, dùng gradient checkpointing, hay giảm batch? Bài này ước lượng bằng một mô hình bộ nhớ đơn giản.

Mô hình có $P$ tham số và $L$ lớp; lớp $l$ tạo ra $a_l$ giá trị activation cho mỗi mẫu. Với một cấu hình, bộ nhớ gồm hai phần.

**Phần cố định**, tính theo byte:

| | `fp32` | `mixed` |
|---|---|---|
| Trọng số | $4P$ | $4P$ bản FP32 cộng $2P$ bản FP16 |
| Gradient | $4P$ | $2P$ |

Cộng thêm trạng thái optimizer, luôn ở FP32: `sgd` không có, `momentum` là $4P$, `adam` là $8P$.

**Phần activation**, cho mỗi mẫu: số giá trị cần giữ nhân $4$ byte (`fp32`) hoặc $2$ byte (`mixed`).

- Không checkpointing (`checkpoint` bằng $0$): giữ mọi lớp, tức $\sum_l a_l$.
- Checkpointing với tham số $k\ge1$: chia các lớp thành các đoạn liên tiếp $k$ lớp (đoạn cuối có thể ngắn hơn). Chỉ giữ đầu ra của các lớp có số thứ tự chia hết cho $k$ (đánh số từ $1$), cộng thêm toàn bộ một đoạn khi tính lại đoạn ấy lúc backward. Số giá trị cần giữ là tổng $a_l$ của các lớp $l$ chia hết cho $k$, cộng tổng lớn nhất của một đoạn.

Bộ nhớ khi học với batch $B$ là phần cố định cộng $B$ nhân phần activation của một mẫu.

Với mỗi cấu hình, hãy báo phần cố định, phần activation của một mẫu, tổng bộ nhớ với `batch_size` đã cho, nó có vừa GPU hay không, và batch lớn nhất vừa GPU (bằng $0$ nếu không batch nào vừa).

## Dữ liệu vào

Một đối tượng JSON gồm `parameters` ($P$), `activations` (các $a_l$), `gpu_bytes`, `batch_size` và `configs`, mỗi cấu hình là `{"precision": "fp32" | "mixed", "optimizer": "sgd" | "momentum" | "adam", "checkpoint": k}`.

## Kết quả

Một đối tượng JSON `{"configs": [...]}`, mỗi phần tử là `{"fixed_bytes": ..., "activation_bytes_per_sample": ..., "total_bytes": ..., "fits": true | false, "max_batch": ...}`.

## Giới hạn

- Không quá $50$ lớp và $5$ cấu hình. Mọi số là số nguyên.

## Chấm điểm

Có 20 test, mỗi test 5 điểm.

## Ví dụ

```input
{
  "parameters": 25557032,
  "activations": [
    2408448, 2408448, 2408448, 2408448, 2408448, 2408448, 2408448,
    2408448, 2408448, 2408448, 2408448, 2408448, 2408448, 2408448,
    2408448, 2408448
  ],
  "gpu_bytes": 17179869184,
  "batch_size": 128,
  "configs": [
    {"precision": "fp32", "optimizer": "adam", "checkpoint": 0},
    {"precision": "mixed", "optimizer": "adam", "checkpoint": 0},
    {"precision": "fp32", "optimizer": "adam", "checkpoint": 4},
    {"precision": "fp32", "optimizer": "sgd", "checkpoint": 0}
  ]
}
```

```output
{
  "configs": [
    {
      "fixed_bytes": 408912512,
      "activation_bytes_per_sample": 154140672,
      "total_bytes": 20138918528,
      "fits": false,
      "max_batch": 108
    },
    {
      "fixed_bytes": 408912512,
      "activation_bytes_per_sample": 77070336,
      "total_bytes": 10273915520,
      "fits": true,
      "max_batch": 217
    },
    {
      "fixed_bytes": 408912512,
      "activation_bytes_per_sample": 77070336,
      "total_bytes": 10273915520,
      "fits": true,
      "max_batch": 217
    },
    {
      "fixed_bytes": 204456256,
      "activation_bytes_per_sample": 154140672,
      "total_bytes": 19934462272,
      "fits": false,
      "max_batch": 110
    }
  ]
}
```

::: goal Nộp bài
Bộ kit ở nút **Dữ liệu** có sẵn `starter.py` và vài test mẫu trong `samples/`. Viết hàm `solve`, chạy thử bằng `python starter.py < samples/01.in`, rồi nộp `starter.py` với ngôn ngữ **Python 3**. Nhớ xóa các lệnh `print` dùng để gỡ lỗi, vì chương trình chỉ được in kết quả.
:::

::: note Nguồn
Phỏng theo [NOAI 2026 Vòng sơ loại, câu 285](https://aisingapore.org/wp-content/uploads/2026/04/NOAI-2026-Preliminary-Round-Assessment-300-MCQs-Google-Forms.pdf#page=108).
:::
