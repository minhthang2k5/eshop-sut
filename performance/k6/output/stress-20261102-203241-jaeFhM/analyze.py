import json
import re


def parse_k6_summary(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    metrics = data.get("metrics", {})

    # Xác định danh sách các phase theo thứ tự tải tăng dần
    phases = [
        "hold_200",
        "hold_400",
        "hold_600",
        "hold_800",
        "hold_1000",
        "hold_1200",
        "hold_1400",
        "hold_1600",
        "hold_1800",
        "hold_2000",
        "hold_2200",
        "hold_2400",
        "hold_2600",
        "hold_2800",
        "hold_3000",
        "recovery_1",
    ]

    # Map số VU ước lượng/quy định theo từng phase
    vu_mapping = {
        f"hold_{vus}": vus for vus in range(200, 3200, 200)
    }
    vu_mapping["recovery_1"] = 10  # Phase hạ tải/cooldown

    vu_data = [vu_mapping.get(p, 0) for p in phases]

    # 1. Tổng kết toàn hệ thống theo từng phase
    overall_p95 = []
    overall_fail = []

    for p in phases:
        dur_key = f"http_req_duration{{phase:{p}}}"
        fail_key = f"http_req_failed{{phase:{p}}}"

        p95_val = metrics.get(dur_key, {}).get("p(95)", 0.0)
        # Tỷ lệ lỗi đổi sang phần trăm (%)
        fail_val = metrics.get(fail_key, {}).get("value", 0.0) * 100

        overall_p95.append(round(p95_val, 2))
        overall_fail.append(round(fail_val, 3))

    # 2. Chi tiết theo 4 API: search, detail (details), cart, checkout
    endpoints = ["search", "detail", "cart", "checkout"]
    ep_p95 = {ep: [] for ep in endpoints}
    ep_fail = {ep: [] for ep in endpoints}

    for p in phases:
        for ep in endpoints:
            dur_key = f"http_req_duration{{phase:{p},endpoint:{ep}}}"
            fail_key = f"http_req_failed{{phase:{p},endpoint:{ep}}}"

            p95_val = metrics.get(dur_key, {}).get("p(95)", 0.0)
            fail_val = metrics.get(fail_key, {}).get("value", 0.0) * 100

            ep_p95[ep].append(round(p95_val, 2))
            ep_fail[ep].append(round(fail_val, 3))

    return {
        "phases": phases,
        "vu_data": vu_data,
        "overall_p95": overall_p95,
        "overall_fail": overall_fail,
        "ep_p95": ep_p95,
        "ep_fail": ep_fail,
    }


def generate_html_report(parsed_data: dict, output_html: str = "report.html"):
    phases_json = json.dumps(parsed_data["phases"])
    vu_json = json.dumps(parsed_data["vu_data"])
    overall_p95_json = json.dumps(parsed_data["overall_p95"])
    overall_fail_json = json.dumps(parsed_data["overall_fail"])
    ep_p95_json = json.dumps(parsed_data["ep_p95"])
    ep_fail_json = json.dumps(parsed_data["ep_fail"])

    html_template = f"""


    
    
    K6 Load Testing <xt-mark w="performance" style="color: #ff6a00 !important">Performance</xt-mark> Report
    
    
    
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0f172a;
            color: #f1f5f9;
            margin: 0;
            padding: 24px;
        }}
        h1 {{
            text-align: center;
            font-size: 24px;
            margin-bottom: 8px;
            color: #38bdf8;
        }}
        p.subtitle {{
            text-align: center;
            font-size: 14px;
            color: #94a3b8;
            margin-bottom: 32px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 24px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .card {{
            background: #1e293b;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            border: 1px solid #334155;
        }}
        .card.full-width {{
            grid-column: 1 / -1;
        }}
        .card h2 {{
            font-size: 16px;
            margin-top: 0;
            margin-bottom: 16px;
            color: #e2e8f0;
            display: flex;
            justify-content: space-between;
        }}
        .badge {{
            font-size: 12px;
            padding: 2px 8px;
            border-radius: 4px;
            background: #334155;
            color: #cbd5e1;
            font-weight: normal;
        }}
        canvas {{
            width: 100% !important;
            height: 320px !important;
        }}
    



    Báo Cáo Kết Quả Kiểm Thử Tải (K6 Load Testing)
    Tiêu chuẩn đánh giá: Response Duration P95 < 500ms | Request Failure Rate < 1%

    
        
        
            Số lượng Virtual Users (VUs) theo từng Phase Traffic Profile
            
        

        
        
            Tổng thể: Response Time P95 Threshold: < 500ms
            
        

        
        
            Tổng thể: Tỷ lệ Request Lỗi (%) Threshold: < 1%
            
        

        
        
            Chi tiết API: Response Time P95 (ms) Threshold: < 500ms
            
        

        
        
            Chi tiết API: Tỷ lệ Request Lỗi (%) Threshold: < 1%
            
        
    

    
        const phases = {phases_json};
        const vuData = {vu_json};
        const overallP95 = {overall_p95_json};
        const overallFail = {overall_fail_json};
        const epP95 = {ep_p95_json};
        const epFail = {ep_fail_json};

        const commonGridOpts = {{
            color: '#334155'
        }};

        // 1. VU Chart
        new Chart(document.getElementById('vuChart'), {{
            type: 'bar',
            data: {{
                labels: phases,
                datasets: [{{
                    label: 'VUs Target',
                    data: vuData,
                    backgroundColor: '#0ea5e9'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }} }},
                    y: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }}, title: {{ display: true, text: 'VUs', color: '#94a3b8' }} }}
                }}
            }}
        }});

        // 2. Overall Duration
        new Chart(document.getElementById('overallDurationChart'), {{
            type: 'line',
            data: {{
                labels: phases,
                datasets: [
                    {{
                        label: 'Total P95 (ms)',
                        data: overallP95,
                        borderColor: '#38bdf8',
                        backgroundColor: '#38bdf820',
                        tension: 0.2,
                        fill: true
                    }},
                    {{
                        label: 'Ngưỡng SLA (500ms)',
                        data: Array(phases.length).fill(500),
                        borderColor: '#ef4444',
                        borderDash: [6, 6],
                        pointRadius: 0,
                        borderWidth: 2
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }} }},
                    y: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }}, title: {{ display: true, text: 'ms', color: '#94a3b8' }} }}
                }}
            }}
        }});

        // 3. Overall Fail Rate
        new Chart(document.getElementById('overallFailChart'), {{
            type: 'line',
            data: {{
                labels: phases,
                datasets: [
                    {{
                        label: 'Error Rate (%)',
                        data: overallFail,
                        borderColor: '#f59e0b',
                        backgroundColor: '#f59e0b20',
                        tension: 0.2,
                        fill: true
                    }},
                    {{
                        label: 'Ngưỡng SLA (1%)',
                        data: Array(phases.length).fill(1.0),
                        borderColor: '#ef4444',
                        borderDash: [6, 6],
                        pointRadius: 0,
                        borderWidth: 2
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }} }},
                    y: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }}, title: {{ display: true, text: '%', color: '#94a3b8' }} }}
                }}
            }}
        }});

        // 4. API Endpoints Duration
        new Chart(document.getElementById('epDurationChart'), {{
            type: 'line',
            data: {{
                labels: phases,
                datasets: [
                    {{ label: 'Search', data: epP95['search'], borderColor: '#a855f7', tension: 0.2 }},
                    {{ label: 'Detail', data: epP95['detail'], borderColor: '#06b6d4', tension: 0.2 }},
                    {{ label: 'Cart', data: epP95['cart'], borderColor: '#10b981', tension: 0.2 }},
                    {{ label: 'Checkout', data: epP95['checkout'], borderColor: '#f43f5e', tension: 0.2 }},
                    {{
                        label: 'SLA (500ms)',
                        data: Array(phases.length).fill(500),
                        borderColor: '#ef4444',
                        borderDash: [6, 6],
                        pointRadius: 0,
                        borderWidth: 2
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }} }},
                    y: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }}, title: {{ display: true, text: 'ms', color: '#94a3b8' }} }}
                }}
            }}
        }});

        // 5. API Endpoints Fail Rate
        new Chart(document.getElementById('epFailChart'), {{
            type: 'line',
            data: {{
                labels: phases,
                datasets: [
                    {{ label: 'Search', data: epFail['search'], borderColor: '#a855f7', tension: 0.2 }},
                    {{ label: 'Detail', data: epFail['detail'], borderColor: '#06b6d4', tension: 0.2 }},
                    {{ label: 'Cart', data: epFail['cart'], borderColor: '#10b981', tension: 0.2 }},
                    {{ label: 'Checkout', data: epFail['checkout'], borderColor: '#f43f5e', tension: 0.2 }},
                    {{
                        label: 'SLA (1%)',
                        data: Array(phases.length).fill(1.0),
                        borderColor: '#ef4444',
                        borderDash: [6, 6],
                        pointRadius: 0,
                        borderWidth: 2
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }} }},
                    y: {{ grid: commonGridOpts, ticks: {{ color: '#94a3b8' }}, title: {{ display: true, text: '%', color: '#94a3b8' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Đã xuất file báo cáo: {output_html}")


if __name__ == "__main__":
    data = parse_k6_summary("summary.json")
    generate_html_report(data, "load_test_report.html")