# Amazon Athena: Dịch vụ truy vấn Serverless

Tài liệu này tóm lược Amazon Athena theo hướng ngắn gọn, sạch và dễ đọc: khái niệm cốt lõi, cách vận hành, ví dụ thực tế và các mẹo tối ưu.

---

## Overview

**Amazon Athena** là dịch vụ truy vấn tương tác serverless cho phép phân tích dữ liệu trực tiếp trên **Amazon S3** bằng **SQL** tiêu chuẩn. Athena phù hợp cho truy vấn ad-hoc trên Data Lake mà không cần nạp dữ liệu vào cơ sở dữ liệu truyền thống.

## Key Concepts & Keywords

- **Serverless**: Không cần quản lý hay mở rộng máy chủ; AWS lo phần hạ tầng tính toán.
- **Pay-per-query**: Chỉ trả tiền cho dung lượng dữ liệu mà Athena quét.
- **Glue Data Catalog**: Kho metadata tập trung giúp Athena hiểu schema của dữ liệu trên S3.
- **Schema-on-Read**: Chỉ áp dụng schema khi đọc dữ liệu, không cần định nghĩa bảng trước khi nạp.
- **Presto & Apache Spark**: Athena dùng Presto cho truy vấn SQL và hỗ trợ Spark cho xử lý nâng cao.

## Detailed Deep Dive

### 1. Cách thức vận hành

Athena tách biệt hoàn toàn giữa compute và storage:

- **Tầng lưu trữ**: Dữ liệu nằm trên **Amazon S3**, thường ở các định dạng như CSV, JSON, Parquet hoặc ORC.
- **Tầng metadata**: Dùng **AWS Glue Crawler** để quét dữ liệu trên S3 và tạo bảng trong **Glue Data Catalog**.
- **Tầng truy vấn**: Khi chạy `SELECT`, Athena quét các tệp liên quan trên S3, xử lý và trả kết quả.

### 2. Liên kết trong hệ sinh thái AWS

Athena thường đi cùng các dịch vụ khác để hoàn thiện kiến trúc dữ liệu:

- **Athena + S3**: S3 là nơi chứa dữ liệu thô.
- **Athena + AWS Glue**: Glue cung cấp metadata để Athena hiểu cấu trúc dữ liệu.
- **Athena + Amazon QuickSight**: Dùng để tạo dashboard và báo cáo trực quan.
- **Athena + Amazon Bedrock**: Có thể dùng như nguồn dữ liệu cho các ứng dụng AI tạo sinh và RAG.

## Practical Examples & Scenarios

### Ví dụ: Phân tích log hệ thống

Giả sử công ty lưu trữ hàng tỷ dòng access logs từ **Application Load Balancer (ALB)** vào S3.

Bạn cần thống kê 10 địa chỉ IP gửi nhiều lỗi 500 nhất trong 24 giờ qua:

```sql
SELECT client_ip, count(*) AS error_count
FROM alb_logs
WHERE elb_status_code = '500'
GROUP BY client_ip
ORDER BY error_count DESC
LIMIT 10;
```

Athena sẽ quét dữ liệu trực tiếp trên S3 và trả kết quả trong vài giây.

> Hãy hình dung S3 như một kho dữ liệu khổng lồ, Glue là người quản kho giữ danh mục, còn Athena là công cụ tìm kiếm thông minh đi thẳng vào kho và trả lời đúng câu hỏi bạn cần.

## Exam Essentials & Tips

### 1. Tối ưu chi phí

> Athena tính phí dựa trên dung lượng dữ liệu bị quét, khoảng $5 cho mỗi 1 TB dữ liệu quét.

- **Dùng định dạng columnar**: Ưu tiên **Parquet** hoặc **ORC** thay vì CSV.
- **Phân vùng dữ liệu**: Chia dữ liệu theo `year/month/day` và thêm điều kiện `WHERE` theo partition.
- **Nén dữ liệu**: Dùng Snappy hoặc các định dạng nén phù hợp để giảm lượng dữ liệu quét.

### 2. Bảo mật

- **IAM Policies**: Quản lý chặt quyền chạy truy vấn và quyền truy cập S3.
- **Workgroups**: Giới hạn chi phí cho từng dự án hoặc phòng ban.
- **Mã hóa**: Hỗ trợ SSE-S3, SSE-KMS và mã hóa kết quả truy vấn trên S3.

### 3. Hiệu suất

- **Tránh `SELECT *`**: Chỉ chọn cột cần thiết.
- **Tối ưu kích thước tệp**: Tránh quá nhiều file nhỏ; nên gộp file để Athena xử lý hiệu quả hơn.

---

Nếu bạn muốn, mình có thể làm tiếp một bản rút gọn theo kiểu học thi, hoặc thêm sơ đồ minh họa cho Athena + S3 + Glue.
