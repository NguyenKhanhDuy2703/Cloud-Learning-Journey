Chào Duy, với tư cách là một **AWS Certified Solutions Architect**, tôi đã hệ thống lại nội dung bài học về **Amazon Kinesis Data Streams** dựa trên tài liệu và sơ đồ kiến trúc `image_cae97a.png` mà bạn cung cấp. 

Dưới đây là tài liệu học tập chuyên nghiệp dành cho bạn.

---

# Amazon Kinesis Data Streams (KDS)

## ## Overview
**Amazon Kinesis Data Streams (KDS)** là một dịch vụ truyền dữ liệu thời gian thực (real-time streaming) có khả năng mở rộng cực lớn và độ bền cao. Nó cho phép bạn liên tục thu thập hàng gigabyte dữ liệu mỗi giây từ hàng trăm nghìn nguồn khác nhau.

*   **Vấn đề thực tế giải quyết:** Các cơ sở dữ liệu truyền thống thường gặp khó khăn khi phải xử lý hàng triệu bản ghi nhỏ mỗi giây (như log web, dữ liệu cảm biến IoT). KDS đóng vai trò là một "vùng đệm" (buffer) khổng lồ, hấp thụ toàn bộ dữ liệu này trước khi chuyển đến các công cụ xử lý hoặc lưu trữ.
*   **Mục đích:** Chuyển đổi mô hình xử lý dữ liệu từ **Batch Processing** (xử lý theo lô, có độ trễ) sang **Real-time Processing** (xử lý ngay lập tức khi dữ liệu phát sinh).



---

## ## Key Concepts & Keywords
Để làm chủ KDS, bạn cần ghi nhớ các thuật ngữ nền tảng sau:

*   **Shard:** Đơn vị năng lực (Capacity Unit) cơ bản của một luồng. Một Shard cung cấp tốc độ ghi **1MB/s** (hoặc 1,000 records/s) và tốc độ đọc **2MB/s**.
*   **Producer:** Các ứng dụng hoặc dịch vụ đẩy dữ liệu vào KDS (ví dụ: KPL, SDK, CloudWatch Logs).
*   **Consumer:** Các ứng dụng đọc và xử lý dữ liệu từ KDS (ví dụ: AWS Lambda, KCL).
*   **Partition Key:** Một định danh (như `device_id`) được Producer sử dụng để nhóm dữ liệu vào các Shards cụ thể.
*   **Sequence Number:** Mã định danh duy nhất cho mỗi bản ghi dữ liệu trong một Shard, giúp đảm bảo thứ tự dữ liệu.
*   **Retention Period:** Thời gian lưu trữ dữ liệu trong luồng. Mặc định là **24 giờ**, có thể mở rộng lên đến **365 ngày**.

---

## ## Detailed Deep Dive
Dựa trên sơ đồ `image_cae97a.png`, chúng ta có thể phân tích luồng di chuyển của dữ liệu qua 5 giai đoạn chính:

### ### 1. Streaming Sources & Connectors (Giai đoạn 1, 2 & 3)
Đây là nơi dữ liệu bắt đầu. Dữ liệu từ các nguồn thực tế được đưa vào hệ thống thông qua các đầu nối:
*   **Nguồn:** Thiết bị IoT, ứng dụng doanh nghiệp, mạng xã hội, logs hệ thống.
*   **Connectors (Producers):** 
    *   **AWS IoT Core:** Kết nối trực tiếp từ các cảm biến.
    *   **Kinesis Producer Library (KPL):** Thư viện tối ưu giúp gom lô dữ liệu để tăng hiệu suất.
    *   **AWS DMS:** Di chuyển dữ liệu từ các DB truyền thống sang luồng.

### ### 2. Stream Ingestion (Giai đoạn 4)
Dữ liệu được đẩy vào **Amazon Kinesis Data Streams**. 
*   Dữ liệu tại đây được phân tán vào các **Shards**. Bạn có thể tăng/giảm số lượng Shards để đáp ứng lưu lượng truy cập (Resharding).
*   Dữ liệu trong KDS có tính chất **Immutable** (không thể thay đổi sau khi ghi) và được sao chép qua **3 Availability Zones** để đảm bảo an toàn.



### ### 3. Stream Processing & Storage (Giai đoạn 5 & 6)
Đây là bước "tiêu thụ" dữ liệu:
*   **Xử lý (Processing):** **AWS Lambda** có thể được kích hoạt ngay khi có dữ liệu mới để thực hiện tính toán. **Amazon Data Firehose** có thể nhận dữ liệu từ KDS để chuyển đổi định dạng.
*   **Lưu trữ (Storage):** Dữ liệu sau khi xử lý được đẩy vào các "hồ dữ liệu" (Data Lake) như **Amazon S3** hoặc kho dữ liệu **Amazon Redshift** để phân tích dài hạn.

### ### 4. Analytics & ML (Giai đoạn 7 & 8)
Dữ liệu cuối cùng được khai thác giá trị:
*   **Amazon Athena/QuickSight:** Chạy các câu lệnh SQL trực tiếp trên S3 để tạo báo cáo.
*   **Sử dụng thực tế:** Đưa ra quyết định thời gian thực, cảnh báo sự cố (Alerting) hoặc đưa vào các mô hình Machine Learning để dự báo.

---

## ## Practical Examples & Scenarios
**Ví dụ thực tế: Hệ thống giám sát an ninh thông minh (tương tự SpaceLens)**
1.  **Source:** Camera AI tại cửa hàng gửi dữ liệu tọa độ người dùng mỗi 100ms.
2.  **Producer:** Một script Python sử dụng **AWS SDK (Boto3)** gửi dữ liệu này vào KDS.
3.  **KDS:** Tiếp nhận hàng nghìn luồng tọa độ đồng thời từ nhiều camera.
4.  **Consumer:** Một hàm **AWS Lambda** đọc tọa độ, kiểm tra nếu có người đi vào "vùng cấm".
5.  **Output:** Nếu vi phạm, Lambda gửi thông báo đến điện thoại quản lý và lưu log vào **Amazon Redshift** để báo cáo cuối ngày.

---

## ## Exam Essentials & Tips

### ### 1. Chế độ năng lực (Capacity Modes)
Bạn cần phân biệt hai loại này để tối ưu chi phí và quản lý:
*   **On-demand mode:** AWS tự động điều chỉnh số lượng Shards. Phù hợp khi bạn không biết trước lưu lượng (Chi phí cao hơn).
*   **Provisioned mode:** Bạn tự chỉ định số lượng Shards. Phù hợp khi lưu lượng ổn định (Tiết kiệm chi phí hơn).

### ### 2. Lưu ý về Chi phí (Billing)
*   Tính theo **Shard-hour** (số lượng Shard chạy trong 1 giờ).
*   Tính theo **PUT Payload Units** (mỗi đơn vị 25KB dữ liệu được đẩy vào).
> **Tip:** Hãy gom nhiều bản ghi nhỏ thành một bản ghi lớn hơn (Batching) bằng KPL để giảm chi phí PUT.

### ### 3. Bảo mật & Hiệu suất
*   **IAM:** Sử dụng IAM Roles để kiểm soát quyền của Producer (chỉ được ghi) và Consumer (chỉ được đọc).
*   **Mã hóa:** Hỗ trợ mã hóa phía server (Server-side encryption) bằng **AWS KMS**.
*   **Lỗi ProvisionedThroughputExceeded:** Xảy ra khi Producer đẩy dữ liệu nhanh hơn năng lực của Shard. Giải pháp: Tăng số lượng Shard hoặc sử dụng cơ chế **Exponential Backoff** khi retry.

