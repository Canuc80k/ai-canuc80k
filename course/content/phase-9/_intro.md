# Mở rộng: hành động, suy luận và lập luận bằng toán

Trong lập trình thi đấu, đề thường cho đủ quy tắc: trạng thái nào đi tới trạng thái nào, mỗi bước tốn bao nhiêu, đáp án đúng là gì. Trong AI, có lúc ta vẫn biết các quy tắc ấy; có lúc chỉ được thử một hành động rồi quan sát kết quả; và có lúc đề không cần code, chỉ cần một lời giải viết ra mà người chấm kiểm được từng bước. Chương cuối đi qua cả ba trường hợp.

::: goal Mục tiêu của chương
- Đặt một bài toán ra quyết định thành MDP, tính giá trị bằng phương trình Bellman, học Q từ tương tác và hiểu ý tưởng của policy gradient.
- Chọn trạng thái đúng rồi mới chọn thuật toán: A* với heuristic chấp nhận được (admissible), minimax khi có đối thủ, ràng buộc và logic để kiểm kết luận.
- Trình bày lời giải lý thuyết về xác suất, đại số tuyến tính, gradient, shape của mạng, attention và đánh giá sao cho người đọc kiểm được.
:::

| Bài | Câu hỏi trung tâm |
|---|---|
| 9.1 — Reinforcement learning | Khi chỉ được thử rồi quan sát, làm sao một bước ở xa đích vẫn được đánh giá là có ích? |
| 9.2 — Tìm kiếm và suy luận | Khi đã biết quy tắc, tổ chức việc tìm thế nào cho bản đồ lớn, trò chơi có đối thủ và bài có ràng buộc? |
| 9.3 — Bài tập lý thuyết | Một lời giải viết cần những gì để người chấm kiểm được từng bước? |

Hai bài đầu đi cùng một robot chuyển sách trong thư viện. Ở 9.1, robot học từ những lần đi thử; ở 9.2, nhà trường đưa bản đồ đầy đủ và bài toán trở về tìm kiếm. BFS, Dijkstra và quay lui từ lập trình thi đấu là cầu nối tự nhiên; điều mới là heuristic có thể là một model, đối thủ chọn bước tiếp theo, và kết luận cần được kiểm bằng logic. Bài 9.3 gom các phép tính đã gặp ở những chương trước thành bài tập kiểu đề thi viết.

Trước khi vào chương, nên ôn gradient descent, logits và cross-entropy, attention và cách chia validation. Code trong chương chạy trên CPU với bài toán nhỏ, để mọi bảng Q, mọi nút được mở rộng và mọi đáp án đều tính tay được; câu cuối bài ưu tiên đề thật có ghi nguồn. Đây là phần mở rộng: mức ưu tiên của từng chủ đề tùy syllabus của kỳ thi bạn nhắm tới.

Chương này khép lại giáo trình. Điều nên mang vào phòng thi không phải một danh sách model, mà là thói quen của mọi chương: đọc đúng đề, kiểm bằng ví dụ nhỏ, và chỉ tin con số có bằng chứng.
