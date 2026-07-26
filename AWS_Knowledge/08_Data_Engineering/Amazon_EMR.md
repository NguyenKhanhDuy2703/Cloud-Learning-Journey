# Amazon EMR (Elastic MapReduce)

Tài liệu này tóm lược kiến thức về Amazon EMR (Elastic MapReduce): từ bản chất cốt lõi, các tùy chọn triển khai, đến kiến trúc và các kỹ thuật tối ưu hóa chi phí, bảo mật, hiệu suất.

---

## Overview

**Amazon EMR** là một nền tảng xử lý Big Data hàng đầu trên AWS, cho phép xử lý và phân tích dữ liệu quy mô Petabyte bằng các khung mã nguồn mở như Apache Spark, Hive, Presto, HBase. Thay vì tự vận hành cụm Hadoop phức tạp tại chỗ, EMR biến Big Data thành một dịch vụ theo yêu cầu.

<p align="center">
  <img src="assets/overview_EMR.png" alt="Amazon EMR Overview" width="80%" />
  <br />
  <em>Hình 1: Tổng quan Amazon EMR</em>
</p>

## Key Concepts & Keywords

- **Node (Nút)**: Một thực thể điện toán (thường là EC2) trong cụm.
- **Cluster (Cụm)**: Tập hợp các Node làm việc cùng nhau xử lý dữ liệu.
- **HDFS (Hadoop Distributed File System)**: Hệ thống tệp phân tán lưu trữ dữ liệu trên ổ đĩa của các Node.
- **EMRFS (EMR File System)**: Lớp thực thi cho phép EMR sử dụng Amazon S3 như hệ thống tệp, tách biệt tính toán và lưu trữ.
- **Step (Bước)**: Đơn vị công việc (ví dụ: lệnh Spark hoặc Hive) được gửi đến cụm thực thi.
- **Worker**: Đơn vị tài nguyên (CPU/RAM) trong mô hình Serverless thực hiện tính toán.

---

## Detailed Deep Dive

### 1. Các tùy chọn triển khai (Deployment Options)

Amazon EMR cung cấp sự linh hoạt tối đa tùy thuộc vào mức độ kiểm soát mà bạn mong muốn:

| Tùy chọn            | Đặc điểm chính                                                     | Khi nào nên dùng?                                                  |
| :------------------ | :----------------------------------------------------------------- | :----------------------------------------------------------------- |
| **EMR on EC2**      | Chạy trên các máy chủ ảo EC2. Bạn có toàn quyền cấu hình instance. | Cần kiểm soát sâu về phần cứng, tùy chỉnh OS.                      |
| **EMR Serverless**  | Không cần quản lý máy chủ hay cụm. AWS tự động co giãn tài nguyên. | Muốn tập trung vào code, không muốn bận tâm hạ tầng.               |
| **EMR on EKS**      | Chạy các ứng dụng EMR trên cụm Kubernetes (EKS) có sẵn.            | Khi doanh nghiệp đã chuẩn hóa mọi thứ trên Kubernetes.             |
| **EMR on Outposts** | Triển khai EMR ngay tại trung tâm dữ liệu tại chỗ của bạn.         | Cần xử lý dữ liệu tại chỗ để đảm bảo độ trễ hoặc tuân thủ pháp lý. |

### 2. Amazon EMR Serverless: Kiến trúc và Cơ chế

Đây là tùy chọn hiện đại nhất, giúp loại bỏ gánh nặng vận hành cụm.

#### Core Concepts trong Serverless:

1. **Application**: Thực thể logic đại diện cho khung phần mềm (ví dụ: Spark Application). Cấu hình dung lượng tối đa để kiểm soát chi phí.
2. **Job**: Đơn vị xử lý cụ thể gửi vào Application.
3. **Workers**: Tài nguyên điện toán thực tế được cấp cho Job.
4. **Pre-initialized Workers**: Workers được "làm nóng" sẵn để bắt đầu Job ngay lập tức (giảm độ trễ) nhưng tính phí duy trì.

<p align="center">
  <img src="assets/EMR_serverless.png" alt="EMR Serverless Architecture" width="80%" />
  <br />
  <em>Hình 2: Kiến trúc EMR Serverless</em>
</p>

#### Cách EMR Serverless hoạt động:

Khi bạn gửi một Job, EMR Serverless sẽ tự động tính toán lượng tài nguyên cần thiết, yêu cầu các **Workers**, thực thi mã nguồn và trả lại tài nguyên ngay khi hoàn thành.

### 3. Amazon EMR Cluster Architecture (Mô hình truyền thống)

Trong mô hình chạy trên EC2, cụm được chia thành 3 loại Node chính:

- **Master Node (Nút chính)**: "Bộ não" của cụm, quản lý phân phối dữ liệu, công việc và giám sát sức khỏe các nút khác.
- **Core Node (Nút lõi)**: Thực hiện tính toán và lưu trữ dữ liệu (HDFS). Cần ít nhất một nút nếu dùng HDFS.
- **Task Node (Nút tác vụ)**: Chỉ thực hiện tính toán, không lưu trữ dữ liệu. Rất thích hợp cho Spot Instances vì nếu mất, dữ liệu ở S3 hoặc Core Node vẫn an toàn.

<p align="center">
  <img src="assets/EMR_cluster.png" alt="EMR Cluster Architecture" width="80%" />
  <br />
  <em>Hình 3: Kiến trúc Cluster EMR trên EC2</em>
</p>

### 4. Lưu trữ dữ liệu: HDFS vs EMRFS

- **HDFS**: Dữ liệu nằm trên ổ đĩa của các Node. Tốc độ truy cập rất nhanh nhưng nếu tắt cụm, dữ liệu mất (trừ khi sao lưu).
- **EMRFS**: Dữ liệu nằm trên Amazon S3
  - **Ưu điểm**: Độ bền 99.999999999%, tắt cụm vẫn giữ dữ liệu.
  - **Tính năng**: Cho phép nhiều cụm EMR cùng truy cập một Data Lake trên S3.

## Practical Examples & Scenarios

**Kịch bản 1: Pipeline ETL tự động với EMR Serverless**

1. Dữ liệu thô đổ vào S3-Bucket-Raw.
2. AWS Lambda phát hiện tệp mới và gọi StartJobRun tới EMR Serverless Spark Application.
3. Spark xử lý, làm sạch dữ liệu và ghi kết quả vào S3-Bucket-Cleaned.
4. Dữ liệu được lưu dưới dạng Parquet để Amazon Athena truy vấn hiệu quả.

**Kịch bản 2: Phân tích log quy mô lớn định kỳ**

Doanh nghiệp sử dụng EMR Cluster với Task Nodes chạy Spot Instances vào 2 giờ sáng mỗi ngày để xử lý hàng Terabyte log, sau đó tự động tắt cụm để tiết kiệm 70-90% chi phí.

## Exam Essentials & Tips

**1. Tối ưu chi phí (Billing)**

- **EMR Serverless**: Trả tiền theo CPU, bộ nhớ, lưu trữ thực sự sử dụng (tính theo giây).
- **Spot Instances**: Dùng cho Task Nodes để tối ưu ngân sách.
- **S3 (EMRFS)**: Sử dụng S3 thay HDFS để tắt cụm khi không cần mà không lo mất dữ liệu.

**2. Bảo mật (Security & IAM)**

- **IAM Roles**: EMR cần Service Role để quản lý AWS resources và Instance Profile cho Node truy cập S3/KMS.
- **Encryption**: Bật mã hóa at-rest (S3, ổ đĩa) và in-transit (giữa Node).

**3. Hiệu suất (Performance)**

- Nếu Job có tải không ổn định, chọn EMR Serverless.
- Nếu cần truy vấn phức tạp với tinh chỉnh sâu JVM parameters, EMR on EC2 tốt hơn.

---
