# Concept 1: Khái niệm Đám mây 
1.1 Định nghĩa & Mô hình dịch vụ
- Điện toán đám mây (Cloud Computing): Cung cấp tài nguyên CNTT (tính toán, lưu trữ, DB) theo nhu cầu qua Internet với chính sách trả tiền theo mức sử dụng (Pay-as-you-go).

- Mô hình dịch vụ (Service Models):

  - IaaS (Infrastructure as a Service): Quản lý hạ tầng mạng, máy chủ ảo (vd: EC2).

  - PaaS (Platform as a Service): Quản lý ứng dụng, không cần quan tâm OS/Hạ tầng (vd: Elastic Beanstalk).

  - SaaS (Software as a Service): Sử dụng phần mềm hoàn chỉnh qua web.

  - Serverless: Mô hình không máy chủ, AWS quản lý hoàn toàn việc cấp phát tài nguyên (vd: Lambda).

1.2 Sáu lợi ích cốt lõi của Cloud Computing
  - Đổi chi phí đầu tư (CapEx) sang chi phí vận hành (OpEx): Không cần bỏ vốn lớn xây trung tâm dữ liệu.

  - Lợi thế quy mô lớn (Economies of Scale): Chi phí rẻ hơn do AWS mua tài nguyên số lượng cực lớn.

  - Ngừng phỏng đoán về dung lượng: Tự động điều chỉnh theo thực tế.

  - Tăng tốc độ và sự linh hoạt: Triển khai tài nguyên trong vài phút.

  - Tập trung vào kinh doanh: Không tốn nguồn lực vận hành máy chủ vật lý.

  - Triển khai toàn cầu trong vài phút: Mang ứng dụng đến gần người dùng khắp thế giới.

1.3 Khái niệm kiến trúc cơ bản
  - Scalability (Khả năng mở rộng): Khả năng hệ thống xử lý lượng tải lớn hơn (Vertical vs Horizontal).

  - Elasticity (Độ co giãn): Tự động tăng/giảm tài nguyên theo thời gian thực (Auto Scaling).

  - High Availability (Tính sẵn sàng cao): Hệ thống hoạt động liên tục, giảm thiểu thời gian chết.

  - Shared Responsibility Model (Mô hình trách nhiệm chia sẻ):

  - AWS: Bảo mật hạ tầng vật lý, phần mềm ảo hóa (Security of the Cloud).

  - Khách hàng: Bảo mật dữ liệu, cấu hình hệ điều hành, firewall (Security in the Cloud).
# Concept 2: Hạ tầng Toàn cầu
2.1 Cấu trúc Hạ tầng Toàn cầu AWS
  - Regions (Khu vực): Khu vực địa lý riêng biệt, chứa nhiều Availability Zones (AZs).

  - Availability Zones (AZs): Trung tâm dữ liệu vật lý riêng biệt trong cùng một Region, kết nối tốc độ cao.

  - Edge Locations: Điểm truy cập gần người dùng cuối để giảm độ trễ (vd: CloudFront).
  - Hybrid Cloud: Kết hợp giữa hạ tầng on-premises và cloud, sử dụng AWS Outposts hoặc Direct Connect để tích hợp liền mạch.