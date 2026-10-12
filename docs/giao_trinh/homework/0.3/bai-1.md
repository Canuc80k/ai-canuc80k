# Sắp cột

Nhóm bạn lưu danh sách Pokemon trong tệp `pokemon.csv`. Mỗi người mở tệp bằng một phần mềm khác nhau, và giờ các cột đã bị xáo lộn. Hãy đọc tệp bằng pandas, xếp lại các cột theo thứ tự `name, type, hp, evolution, pokedex`, rồi ghi ra CSV. Thứ tự các hàng giữ nguyên.

Hàm `solve` trả về nội dung CSV dưới dạng một chuỗi, `starter.py` sẽ ghi chuỗi ấy ra tệp. `frame[[...]]` với một list tên cột cho ta bảng có các cột đúng thứ tự trong list. `to_csv` không kèm tên tệp thì trả về chuỗi. Nhớ thêm `index=False`, nếu không pandas ghi thêm một cột số thứ tự ở đầu.

## Dữ liệu vào

Mỗi thư mục test có tệp `pokemon.csv` với năm cột trên, theo một thứ tự bất kỳ.

## Kết quả

Nội dung CSV với dòng đầu `name,type,hp,evolution,pokedex`.

## Giới hạn

- Có từ $1$ đến $20$ Pokemon. `hp` là số nguyên từ $1$ đến $200$, các cột khác là chữ.

## Chấm điểm

Có 20 test, mỗi test 5 điểm. Cột `hp` được so như số, nên `45` hay `45.0` đều được.

## Ví dụ

```input
pokemon.csv:
pokedex,evolution,type,name,hp
yes,Ivysaur,grass,Bulbasaur,45
no,Charmeleon,fire,Charmander,39
yes,Wartortle,water,Squirtle,44
no,Metapod,bug,Caterpie,45
```

```output
name,type,hp,evolution,pokedex
Bulbasaur,grass,45,Ivysaur,yes
Charmander,fire,39,Charmeleon,no
Squirtle,water,44,Wartortle,yes
Caterpie,bug,45,Metapod,no
```

::: goal Nộp bài
Tải bộ kit ở nút **Dữ liệu** rồi giải nén. Viết hàm `solve` trong `starter.py` hoặc `starter.ipynb` rồi chạy. Chương trình tự đi qua các thư mục `inputs/01`, `inputs/02`, … và gói kết quả thành `output/submission.zip`, gồm các tệp `01.csv`, `02.csv`, …, `20.csv`. Nộp tệp ZIP ấy, chọn **Output**.
:::
