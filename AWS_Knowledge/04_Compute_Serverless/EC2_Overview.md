# Concept 1 : Amazon EC2

## 1. Tổng quan về Amazon EC2 (Elastic Compute Cloud)
Amazon EC2 là nền tảng điện toán đám mây cung cấp năng lực tính toán dưới dạng các máy chủ ảo (instances), được thiết kế để có quy mô linh hoạt và bảo mật cao cho hầu hết mọi khối lượng công việc.

* **Bản chất:** Thay vì sở hữu và bảo trì phần cứng vật lý, bạn có thể tiếp cận năng lượng điện toán theo nhu cầu thông qua Internet.
* **Sự đa dạng:** Cung cấp hơn **750 loại phiên bản** (instance types) với nhiều tùy chọn về bộ xử lý (Intel, AMD, Arm/Graviton), dung lượng lưu trữ, kết nối mạng và hệ điều hành.
  
* **Mô hình thanh toán:** Linh hoạt với các hình thức như :
  *  On-Demand (trả theo mức sử dụng), 
  *  Savings Plans (tiết kiệm khi cam kết sử dụng), 
  *  Spot Instances (tận dụng dung lượng dư thừa với giá rẻ).


---

## 2. Phân tích chi tiết các thành phần chính

### A. Amazon EC2 Auto Scaling (Tự động điều chỉnh quy mô)
Đây là dịch vụ giúp duy trì tính sẵn sàng của ứng dụng bằng cách tự động thêm hoặc bớt các phiên bản EC2 dựa trên các chính sách đã định trước.

* **Cơ chế hoạt động:**
    * **Dynamic Scaling (Động):** Phản ứng theo nhu cầu thực tế (ví dụ: CPU vượt ngưỡng 70% thì thêm máy chủ).
    * **Predictive Scaling (Dự đoán):** Sử dụng công nghệ máy học (Machine Learning) để dự báo nhu cầu lưu lượng và lên lịch số lượng phiên bản phù hợp trước khi tải tăng cao.
* **Lợi ích cốt lõi:**
    * **Tối ưu chi phí:** Chỉ chạy số lượng máy chủ thực sự cần thiết, giảm việc cung cấp thừa (over-provisioning).
    * **Khả năng chịu lỗi:** Tự động phát hiện và thay thế các instance bị lỗi để duy trì hoạt động ổn định.

### B. Elastic Load Balancing - ELB (Cân bằng tải linh hoạt)
ELB đóng vai trò là "người điều phối", tự động phân phối lưu lượng truy cập đến vào nhiều mục tiêu (như các phiên bản EC2, containers, địa chỉ IP).

* **Các tính năng nổi bật:**
    * **Bảo mật:** Hỗ trợ kết thúc SSL/TLS (SSL termination) để giảm tải cho máy chủ backend và tích hợp với AWS WAF để bảo vệ tầng ứng dụng.
    * **Health Checks:** Liên tục kiểm tra tình trạng sức khỏe của các instance; chỉ gửi lưu lượng đến các instance đang hoạt động tốt.
* **Mối liên hệ với Auto Scaling:** ELB và Auto Scaling thường kết hợp với nhau để tạo ra một hệ thống có khả năng tự động mở rộng theo cả chiều ngang (thêm máy chủ) và chiều sâu (phân phối tải đồng đều).


---


## 4. Các dịch vụ đi kèm quan trọng (Ecosystem)
Để EC2 hoạt động hoàn chỉnh, nó cần sự hỗ trợ từ các dịch vụ vệ tinh sau:

1.  **Amazon EBS (Elastic Block Store):** Cung cấp ổ đĩa lưu trữ dạng khối (block storage) hiệu suất cao, có thể gắn vào EC2 như ổ cứng vật lý.
2.  **AWS IAM (Identity and Access Management):** Quản lý quyền truy cập bảo mật, quy định ai hoặc dịch vụ nào được quyền thao tác trên các instance.
3.  **Amazon VPC (Virtual Private Cloud):** Tạo môi trường mạng ảo cô lập để chạy EC2, giúp kiểm soát địa chỉ IP, subnets và bảng định tuyến[cite: 167].
4.  **Amazon CloudWatch:** Giám sát các chỉ số (metrics) như CPU, Network I/O để kích hoạt các kịch bản Auto Scaling.

