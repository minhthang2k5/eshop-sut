# Quy tắc viết một mục checklist

Các quy tắc này rút ra khi review output AI trong pilot. Dán chúng vào mọi prompt sinh mục và dùng làm tiêu chí khi review.

1. **Một mục, một điểm kiểm tra.** Thực hiện được trong vài phút và có kết quả Passed hoặc Failed. Nếu một mục chứa hai phép đo độc lập (ví dụ kích thước vùng bấm và tên truy cập) thì tách đôi.
2. **Kết quả mong đợi chỉ có MỘT tiêu chí đo được.** Tránh "A hoặc B", "nếu... thì...", "và/hoặc", "dễ hiểu", "rõ ràng", "hợp lý" mà không có ngưỡng. Chấp nhận "hoặc" chỉ khi liệt kê các phương án hợp lệ cụ thể (ví dụ ký hiệu "—" hoặc "Chưa cập nhật").
3. **Không viết sẵn kết luận.** Không ghi "nếu không thì Failed". Kết quả mong đợi là chuẩn tham chiếu, không phải đáp án.
4. **Nêu cách thực hiện cụ thể.** Có chuỗi thử cụ thể (ví dụ 300 chữ "W"), công cụ (DevTools > Network > Block request URL), kích thước (375×812), ngưỡng (≥ 4.5:1).
5. **Mục cần giả lập phải ghi rõ cách giả lập** và cách khôi phục dữ liệu. Ưu tiên chặn request bằng DevTools thay vì tắt backend. Nếu backend seed lại DB mỗi lần khởi động thì không tắt/bật để giả lập lỗi.
6. **Không lặp.** Mỗi prompt sau nhận danh sách ý đã phủ ở prompt trước. Hai mục cùng thao tác, chỉ khác điểm quan sát thì gộp.
7. **Không bịa tính năng.** Chỉ kiểm những gì có trong mô tả. Với tính năng không có, chỉ sinh mục khi việc thiếu nó là vấn đề đáng kiểm tra và ghi rõ như vậy.
8. **So sánh với tab khác chỉ để kiểm tra nhất quán**, không kiểm tra sâu chức năng của tab đó (có thể thuộc người khác).
9. **Mỗi mục có nguồn:** nguyên tắc (Nielsen/Norman/Shneiderman/WCAG) hoặc tên checklist control.
10. **Gắn nhãn nguồn gốc:** AI sinh, AI đã sửa, tự thêm, tự thêm đã xác nhận khi chạy.
11. **Mỗi prompt tự chứa đủ ngữ cảnh** (mô tả màn hình, quy tắc, danh sách đã phủ), không phụ thuộc trí nhớ của cuộc hội thoại.
12. **Cuối mỗi prompt yêu cầu** liệt kê control không áp dụng và khía cạnh chưa phủ; dùng chính danh sách này cho bước bổ sung.
