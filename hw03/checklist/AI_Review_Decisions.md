# Review 61 mục AI sinh

Thống kê: Giữ: 24, Sửa: 22, Tách: 2, Gộp: 5, Gộp vào: 5, Bỏ: 3.  
61 mục nháp → 55 mục AI trong checklist cuối (3 bỏ, 5 bị gộp vào mục khác, 2 được tách đôi).

| ID nháp | Nguồn AI | Mục (tóm tắt) | Quyết định | Lý do | ID mới |
|---|---|---|---|---|---|
| D-001 | Prompt 2 (Lần 2) – AI-01-01 | Bố cục tổng thể: Mở tab "Người dùng" ở độ rộng 1366 và 1920 | Giữ | Đo được, Pass/Fail rõ. | GUI-010 |
| D-002 | Prompt 2 (Lần 2) – AI-01-02 | Phân cấp chữ: So sánh cỡ chữ, độ đậm của tiêu đề "Quản lý Người dùng", tiêu đề cột v… | Giữ | Rõ ràng, so sánh trực quan được. | GUI-011 |
| D-003 | Prompt 2 (Lần 2) – AI-01-03 | Ngôn ngữ nhãn: Đọc các nhãn "Email", "Role", "Số ĐT", "Hành động" và tên các mục menu | Giữ | Có cơ sở thực tế: 'Role', 'Dashboard', '(Delivered)' trộn với nhãn tiếng Việt. | GUI-012 |
| D-004 | Prompt 2 (Lần 2) – AI-01-04 | Chính tả, dấu tiếng Việt: Đọc toàn bộ chữ trên màn hình, kiểm tra dấu và từ viết tắt "ĐT" | Sửa | Vế 'từ viết tắt dễ hiểu' mang tính cảm tính, không có ngưỡng Pass/Fail. Bỏ vế đó, chỉ giữ tiêu chí đếm được. | GUI-013 |
| D-005 | Prompt 2 (Lần 2) – AI-01-05 | Tương phản nút "Xóa": Đo tương phản chữ trắng trên nền đỏ của nút Xóa (công cụ đo tương phản… | Gộp | Gộp với D-006: cùng một phép đo tương phản, cùng công cụ, cùng ngưỡng 4.5:1. Bổ sung tên công cụ cụ thể để lặp lại được. | GUI-014 |
| D-006 | Prompt 2 (Lần 2) – AI-01-06 | Tương phản menu: Đo tương phản chữ xanh của mục đang chọn và chữ đỏ "Đăng xuất" trên nề… | Gộp vào D-005 | Trùng phép đo với D-005 (AI-01-06 với AI-01-05). | GUI-014 |
| D-007 | Prompt 2 (Lần 2) – AI-01-07 | Căn lề bảng: Quan sát tiêu đề cột so với dữ liệu cùng cột | Giữ | Quan sát trực tiếp, Pass/Fail rõ. | GUI-015 |
| D-008 | Prompt 2 (Lần 2) – AI-01-08 | Dữ liệu dài: Tạo người dùng có email rất dài (khoảng 60 ký tự) và quan sát cột Emai… | Sửa | Không khả thi như AI viết: tab Người dùng không có chức năng tạo người dùng. Đổi bước sang tạo qua API /api/register; bỏ nhánh 'nếu bị cắt thì...' để có một tiêu chí. | GUI-016 |
| D-009 | Prompt 2 (Lần 2) – AI-01-09 | Ô Số ĐT trống: Xem dòng người dùng chưa có số điện thoại | Sửa | Làm rõ dữ liệu: seed không có số điện thoại nên mọi dòng đều trống; ghi rõ ký hiệu chấp nhận được để có Pass/Fail. | GUI-017 |
| D-010 | Prompt 2 (Lần 2) – AI-01-10 | Nút "Xóa": So sánh màu, kích thước, bo góc, cỡ chữ của các nút "Xóa" giữa các dòn… | Giữ | Đo được bằng DevTools (kích thước, cỡ chữ). | GUI-018 |
| D-011 | Prompt 3 – C3-09 | Nút "Xóa": Rê chuột lên nút Xóa | Sửa | Kết quả 'và/hoặc' cho phép Pass khi chỉ đạt một nửa; chốt cả hai dấu hiệu (con trỏ và màu nền). | GUI-019 |
| D-012 | Prompt 3 – C3-10 | Nút "Xóa": Xem nhãn "Xóa" khi bảng có nhiều dòng; kiểm tra tên truy cập của nút | Sửa | Gộp hai tiêu chí khác bản chất (ngữ cảnh nhìn thấy và tên truy cập) dễ gây tranh cãi khi chấm. Giữ tiêu chí đo được: tên truy cập. | GUI-023 |
| D-013 | Prompt 3 – C3-11 | Bảng/Grid (tiêu đề cột): Click lên tiêu đề các cột và rê chuột lên đó | Bỏ | Kết quả kiểu 'Nếu không sắp xếp thì...'. Màn hình không có tính năng sắp xếp, mục chỉ kiểm tra sự vắng mặt của một hành vi nên giá trị rất thấp; nhu cầu tìm/sắp xếp đã được phủ bởi mục tự thêm về ô tìm kiếm và bảng lớn. | — |
| D-014 | Prompt 3 – C3-12 | Bảng/Grid (dữ liệu): So sánh số dòng trên bảng với số người dùng thực tế; tải lại trang | Sửa | 'Số người dùng thực tế' chưa nói lấy từ đâu; thêm nguồn đối chiếu để kiểm lại được. | GUI-020 |
| D-015 | Prompt 3 – C3-13 | Favicon và tiêu đề tab: Quan sát favicon và tiêu đề tab trình duyệt | Giữ | Pass/Fail rõ (tiêu đề hiện tại là tên kỹ thuật). | GUI-021 |
| D-016 | Prompt 3 – C3-14 | Mục menu: Ctrl+click (hoặc chuột giữa) lên một mục menu | Sửa | C3-14 không có Pass/Fail rõ ('nếu là liên kết... nếu không...'). Chọn chuẩn: mục menu điều hướng phải là liên kết thật. | GUI-032 |
| D-017 | Prompt 3 – C3-01 | Checkbox (tiêu đề): Tick ô checkbox ở hàng tiêu đề | Giữ | Hành vi rõ, kiểm được ngay. | GUI-024 |
| D-018 | Prompt 3 – C3-02 | Checkbox: Mở lại trang (F5) rồi quan sát mọi checkbox | Giữ | Rõ ràng. | GUI-025 |
| D-019 | Prompt 3 – C3-03 | Checkbox: Dùng Tab để focus một checkbox rồi nhấn Space | Giữ | Rõ ràng. | GUI-026 |
| D-020 | Prompt 3 – C3-04 | Checkbox: Nhấn Tab liên tiếp từ checkbox tiêu đề xuống các dòng | Giữ | Khác D-019 (thứ tự Tab, không phải phím Space) nên không gộp. | GUI-027 |
| D-021 | Prompt 3 – C3-05 | Checkbox: Đo kích thước vùng bấm của checkbox; kiểm tra tên truy cập bằng công c… | Tách | Một mục chứa hai phép đo độc lập (kích thước vùng bấm và tên truy cập); có thể đạt cái này trượt cái kia. | GUI-028, GUI-029 |
| D-022 | Prompt 3 – C3-06 | Checkbox (tiêu đề): Chọn một dòng (không chọn tất cả) rồi xem ô tiêu đề | Sửa | Kết quả 'trung gian hoặc bỏ chọn' cho phép hai đáp án. Chọn chuẩn phổ biến là trạng thái trung gian. | GUI-030 |
| D-023 | Prompt 3 – C3-07 | Nút "Xóa": Nhấn Tab liên tiếp để tới nút Xóa | Gộp | Gộp với D-024 (C3-07 + C3-08): cùng một thao tác bàn phím trên cùng nút, tách ra chỉ làm trùng bước. | GUI-031 |
| D-024 | Prompt 3 – C3-08 | Nút "Xóa": Focus nút Xóa của người dùng thử rồi nhấn Enter; làm lại với Space (dù… | Gộp vào D-023 | Trùng ý với D-023 (C3-08 với C3-07). | GUI-031 |
| D-025 | Prompt 2 (Lần 2) – AI-03-01 | Menu trái: Đếm các mục menu khi ở tab Người dùng | Giữ | Đếm được. | GUI-033 |
| D-026 | Prompt 2 (Lần 2) – AI-03-02 | Mục đang chọn: Lần lượt mở từng tab, quan sát mục menu được nổi bật | Giữ | Quan sát được. | GUI-034 |
| D-027 | Prompt 2 (Lần 2) – AI-03-03 | Hover menu: Rê chuột qua từng mục menu | Sửa | Kết quả 'và/hoặc' cho phép Pass khi chỉ đạt một nửa; chốt cả hai dấu hiệu (lưu ý mục Đăng xuất). | GUI-035 |
| D-028 | Prompt 2 (Lần 2) – AI-03-04 | Bàn phím: Nhấn Tab để di chuyển qua các mục menu | Gộp | Gộp với D-029 (AI-03-04 + AI-03-05): focus và kích hoạt bằng Enter là một chuỗi thao tác. | GUI-036 |
| D-029 | Prompt 2 (Lần 2) – AI-03-05 | Kích hoạt bằng bàn phím: Khi mục menu đang focus, nhấn Enter | Gộp vào D-028 | Trùng ý với D-028 (AI-03-05 với AI-03-04). | GUI-036 |
| D-030 | Prompt 2 (Lần 2) – AI-03-06 | Nhãn menu so với trang: Bấm "Người dùng" và đối chiếu với tiêu đề trang đích | Giữ | Rõ ràng. | GUI-037 |
| D-031 | Prompt 2 (Lần 2) – AI-03-07 | Nút Back trình duyệt: Chuyển qua vài tab rồi bấm Back của trình duyệt | Giữ | Rõ ràng. | GUI-038 |
| D-032 | Prompt 2 (Lần 2) – AI-03-08 | Tải lại trang: Đang ở tab Người dùng, nhấn F5 và quan sát địa chỉ URL trước/sau | Giữ | Rõ ràng. | GUI-039 |
| D-033 | Prompt 2 (Lần 2) – AI-03-09 | Đăng xuất: Bấm "Đăng xuất" | Sửa | Vế 'dễ tìm và tách biệt' là cảm tính. Thay bằng tiêu chí kiểm được (Back sau khi đăng xuất). | GUI-040 |
| D-034 | Prompt 2 (Lần 2) – AI-04-01 | Đang tải: Giả lập mạng chậm (Slow 3G trong DevTools) rồi mở tab Người dùng | Giữ | Khả thi: chỉ cần DevTools > Network > Slow 3G. | GUI-041 |
| D-035 | Prompt 2 (Lần 2) – AI-04-02 | Lỗi tải dữ liệu: Tắt backend rồi tải lại tab Người dùng | Sửa | Tắt backend rồi bật lại sẽ CHẠY LẠI SEED và xóa sạch dữ liệu (database.js drop table mỗi lần khởi động). Đổi sang chặn request bằng DevTools, nhẹ và không mất dữ liệu. | GUI-042 |
| D-036 | Prompt 2 (Lần 2) – AI-04-03 | Trạng thái rỗng: Giả lập danh sách người dùng rỗng (xóa hết người dùng thử hoặc dùng DB… | Bỏ | Giả lập quá nặng: muốn danh sách rỗng phải xóa cả tài khoản admin đang đăng nhập (tự khóa mình). Ý 'trạng thái rỗng' được kiểm ở tab Đơn hàng, nơi seed có sẵn 0 đơn (mục tự thêm). | — |
| D-037 | Prompt 2 (Lần 2) – AI-04-04 | Xác nhận khi xóa: Bấm "Xóa" ở một người dùng thử nghiệm | Gộp | Gộp với D-038: nội dung hộp xác nhận chỉ kiểm được khi hộp xác nhận tồn tại, tách ra thì D-038 luôn N/A khi D-037 trượt. | GUI-043 |
| D-038 | Prompt 2 (Lần 2) – AI-04-05 | Nội dung xác nhận: Đọc nội dung hộp xác nhận xóa | Gộp vào D-037 | Phụ thuộc vào D-037. | GUI-043 |
| D-039 | Prompt 2 (Lần 2) – AI-04-06 | Xóa thành công: Xác nhận xóa một người dùng thử nghiệm | Giữ | Rõ ràng. | GUI-044 |
| D-040 | Prompt 2 (Lần 2) – AI-04-07 | Xóa thất bại: Tắt backend sau khi đã mở trang rồi bấm Xóa và xác nhận | Sửa | Tương tự D-035: không tắt backend (mất dữ liệu khi bật lại). Dùng DevTools chặn request DELETE. | GUI-045 |
| D-041 | Prompt 2 (Lần 2) – AI-04-08 | Bấm Xóa liên tiếp: Bấm "Xóa" hai lần liên tiếp thật nhanh trên cùng một dòng | Sửa | Kết quả 'đang xử lý hoặc chỉ gửi một yêu cầu' cho hai đáp án; chọn tiêu chí đo được: số yêu cầu trong tab Network. | GUI-046 |
| D-042 | Prompt 2 (Lần 2) – AI-04-09 | Xóa tài khoản đang đăng nhập: Thử xóa chính tài khoản admin đang đăng nhập (dùng bản sao dữ liệu để … | Sửa | Bổ sung cách khôi phục cụ thể để mục an toàn khi thực thi; chốt kết quả là chặn xóa kèm thông báo (bỏ 'chặn hoặc cảnh báo'). | GUI-047 |
| D-043 | Prompt 2 (Lần 2) – AI-04-10 | Checkbox dòng: Tick ô checkbox ở một dòng | Tách | Kết quả có hai vế 'hoặc' độc lập (phản hồi trực quan và mục đích của checkbox). Tách thành hai mục có Pass/Fail riêng. | GUI-048, GUI-049 |
| D-044 | Prompt 4 – C4-01 | Ô nhập "Tên danh mục mới": Click vào ô, gõ một ký tự rồi quan sát; so với yêu cầu có nhãn nhìn th… | Sửa | Kết quả 'nhãn cố định hoặc tên truy cập' cho hai đáp án; chốt tiêu chí nhìn thấy được: nhãn cố định, không chỉ placeholder. | GUI-052 |
| D-045 | Prompt 4 – C4-02 | Ô nhập: Mở tab Danh mục, click vào ô nhập | Giữ | Rõ ràng. | GUI-053 |
| D-046 | Prompt 4 – C4-03 | Ô nhập: Quan sát ô nhập và vùng form | Sửa | Kết quả 'dấu hiệu rõ hoặc chú thích' mơ hồ; chốt dấu * theo checklist Text Box của bài giảng. | GUI-054 |
| D-047 | Prompt 4 – C4-04 | Ô nhập + nút "Thêm mới": Để trống ô nhập rồi bấm "Thêm mới" | Gộp | Gộp với D-055 (C4-04 + C4-12): cùng thao tác 'để trống rồi bấm Thêm mới', chỉ khác điểm quan sát (thông báo và focus). | GUI-055 |
| D-048 | Prompt 4 – C4-05 | Ô nhập: Nhập chỉ vài dấu cách rồi bấm "Thêm mới" | Giữ | Rõ ràng. | GUI-056 |
| D-049 | Prompt 4 – C4-06 | Ô nhập: Nhập `<b>test</b> & "a" 'b' $#+-` rồi bấm "Thêm mới" | Sửa | C4-06: kết quả 'hoặc bị từ chối... hoặc được lưu...' khiến gần như luôn Pass. Chọn một kết quả. | GUI-057 |
| D-050 | Prompt 4 – C4-07 | Ô nhập: Nhập chuỗi rất dài (ví dụ 300 chữ "W") rồi bấm "Thêm mới" | Sửa | Kết quả có nhánh 'nếu chấp nhận thì...'. Chọn kỳ vọng cụ thể: có giới hạn độ dài. | GUI-058 |
| D-051 | Prompt 4 – C4-08 | Ô nhập: Nhập tên đã có (ví dụ "Laptop", rồi "laptop" viết thường) và bấm "Thêm… | Giữ | Rõ ràng. | GUI-059 |
| D-052 | Prompt 4 – C4-09 | Ô nhập: Nhập tên có dấu tiếng Việt và ký tự khác (ví dụ "Điện thoại di động 20… | Giữ | Rõ ràng. | GUI-060 |
| D-053 | Prompt 4 – C4-10 | Ô nhập + form: Gõ tên hợp lệ trong ô nhập rồi nhấn Enter | Giữ | Rõ ràng. | GUI-061 |
| D-054 | Prompt 4 – C4-11 | Ô nhập: Nhập " Phụ kiện mới  " (có dấu cách đầu và cuối) rồi bấm "Thêm mới" | Sửa | Kết quả 'cắt hoặc từ chối' cho hai đáp án. Chọn hành vi chuẩn là cắt khoảng trắng. | GUI-062 |
| D-055 | Prompt 4 – C4-12 | Ô nhập: Gây lỗi (để trống) rồi bấm "Thêm mới" và quan sát focus | Gộp vào D-047 | Cùng thao tác với D-047 (C4-12 với C4-04). | GUI-055 |
| D-056 | Prompt 4 – C4-13 | Nút "Thêm mới": Nhập tên hợp lệ ("Màn hình") rồi bấm "Thêm mới" | Giữ | Rõ ràng. | GUI-065 |
| D-057 | Prompt 4 – C4-14 | Nút "Thêm mới": Nhập tên hợp lệ rồi bấm "Thêm mới" hai lần liên tiếp thật nhanh | Sửa | Kết quả 'nút đang xử lý hoặc bị vô hiệu' cho hai đáp án; đo bằng số yêu cầu POST trong tab Network. | GUI-066 |
| D-058 | Prompt 4 – C4-15 | Nút "Thêm mới": Tắt backend rồi nhập tên hợp lệ và bấm "Thêm mới" | Sửa | Không tắt backend (khởi động lại sẽ seed lại DB). Dùng DevTools chặn request POST. | GUI-067 |
| D-059 | Prompt 4 – C4-16 | Nút "Xóa": Bấm "Xóa" ở một danh mục thử nghiệm | Giữ | Rõ ràng. | GUI-068 |
| D-060 | Prompt 4 – C4-17 | Nút "Xóa": Xóa một danh mục đang có sản phẩm thuộc về nó (dùng dữ liệu thử) | Sửa | Không cần tạo dữ liệu riêng: danh mục seed "Laptop" đã có sản phẩm. Ghi rõ sao lưu DB; chốt kết quả là chặn xóa kèm thông báo (bỏ 'chặn hoặc cảnh báo'). | GUI-069 |
| D-061 | Prompt 4 – C4-18 | Bảng danh mục: Xóa hết danh mục thử nghiệm (hoặc dùng cơ sở dữ liệu trống) | Bỏ | Giả lập nặng (phải xóa cả danh mục seed đang có sản phẩm) và trùng ý 'trạng thái rỗng' với mục tự thêm ở tab Đơn hàng, nơi trạng thái rỗng có sẵn. | — |
