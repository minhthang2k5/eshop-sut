export const rubric = {
  id: 'k6-ai-audit-v1',
  version: '1.0',
  title: 'Rubric Audit — AI-generated k6 Scripts',
  maxScore: 10,
  criteria: [
    { id: 1, title: 'Endpoint tồn tại thật', hint: 'Chỉ dùng login, products search/detail, checkout của EShop.' },
    { id: 2, title: 'Method và body đúng', hint: 'POST JSON cho login/checkout, có trường bắt buộc.' },
    { id: 3, title: 'Thứ tự flow hợp lý', hint: 'Login trước checkout và không checkout khi token rỗng.' },
    { id: 4, title: 'Correlation token đúng', hint: 'Lấy token JSON và gửi Bearer token cho checkout.' },
    { id: 5, title: 'Think-time hợp lý', hint: 'sleep ngẫu nhiên theo các khoảng yêu cầu.' },
    { id: 6, title: 'Workload đúng', hint: 'Search/detail/checkout gần 55%/25%/20%.' },
    { id: 7, title: 'Dữ liệu được parameterize', hint: 'Keyword và product ID được chọn ngẫu nhiên.' },
    { id: 8, title: 'Có checks cần thiết', hint: 'Check status 200, token và orderId.' },
    { id: 9, title: 'Có thresholds SLO', hint: 'p95 < 500ms và checks >= 0.99.' },
    { id: 10, title: 'Chạy được', hint: 'k6 smoke hoàn tất không lỗi script hoặc request do script tạo.' }
  ]
};
