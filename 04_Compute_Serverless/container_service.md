#  Concept 4 : Amazon ECS & EKS - Container Services
## 1. Amazon ECS & EKS: Hai hướng tiếp cận điều phối container của AWS

### A. Amazon ECS (Elastic Container Service) - Deep Dive
ECS là trình điều phối "đặc sản" của AWS. Nó cực kỳ tinh gọn vì không có các thành phần Control Plane phức tạp như Kubernetes.
* **Task Definition:** Đây là file JSON mô tả ứng dụng của bạn (giống `docker-compose`). Bạn định nghĩa Image nào, bao nhiêu CPU/RAM, và các cổng (ports).
* **Task:** Là một "instance" thực thi của Task Definition. Một Task có thể chứa một hoặc nhiều container chạy cùng nhau (sidecar pattern).
* **Service:** Đảm bảo số lượng Task bạn yêu cầu luôn chạy. Nếu 1 Task "ngỏm", Service sẽ tự động hồi sinh Task mới.
* **Cluster:** Tập hợp các tài nguyên (EC2 hoặc Fargate) nơi các Task được triển khai. Bạn có thể có nhiều Cluster cho các môi trường khác nhau (dev, staging, prod).

<figure  align="center">
  <img src="./assets/ecs_task-states.gif" width="600"/>
  <figcaption align="center"><i> Hình 1 : Kiến trúc cơ bản của Amazon ECS  </i></figcaption>
</figure>

### B. Amazon EKS (Elastic Kubernetes Service) - Deep Dive
EKS là Kubernetes được AWS quản lý. Điểm mạnh nhất là **Sự tương thích tuyệt đối**.
* **Control Plane:** AWS quản lý 3 node Master trên nhiều AZ để đảm bảo cụm K8s không bao giờ sập.
* **Nodes:** Bạn có thể dùng EC2 (tự quản lý) hoặc Fargate (không máy chủ) làm Worker Nodes.
* **VPC CNI:** Mỗi Pod trong EKS nhận được một địa chỉ IP thực từ VPC, giúp kết nối mạng đạt tốc độ tối đa.


## 2. AWS Fargate: Deep Dive vào cơ chế Bảo mật & Roles


### A. Task Execution Role (Quyền thực thi - Quyền của Fargate Agent)
Đây là quyền dành cho **hạ tầng Fargate** (ngầm định bên dưới container).
* **Mục đích:** Giúp Fargate agent thực hiện các hành động "chuẩn bị" cho container.
* **Các hành động tiêu biểu:**
    * Pull Image từ **Amazon ECR**.
    * Gửi log về **Amazon CloudWatch**.
    * Lấy bí mật từ **Secrets Manager** hoặc **Parameter Store** để nạp vào biến môi trường.

### B. Task Role (Quyền của Ứng dụng - Quyền bên trong Container)
Đây là quyền dành cho **mã nguồn ứng dụng** của bạn đang chạy trong container.
* **Mục đích:** Cho phép code của bạn tương tác với các tài nguyên AWS khác.
* **Các hành động tiêu biểu:**
    * Code Python của bạn cần upload file lên **S3**.
    * Ứng dụng Node.js cần đọc/ghi dữ liệu vào **DynamoDB**.
    * Gửi tin nhắn vào hàng đợi **SQS**.

| Đặc điểm | Task Execution Role | Task Role |
| :--- | :--- | :--- |
| **Đối tượng dùng** | Fargate Infrastructure (Agent) | Ứng dụng bên trong container |
| **Thời điểm dùng** | Lúc khởi tạo (Provisioning) | Lúc đang chạy (Runtime) |
| **Ví dụ quyền** | `ecr:GetDownloadUrlForLayer` | `s3:PutObject` |

---

## 3. Amazon ECR (Elastic Container Registry) - Deep Dive
* **Repository Policy:** Giống như S3 Bucket Policy, nó quy định ai (User/Account nào) được quyền Pull/Push image.
* **Image Scanning:** Tính năng cực mạnh giúp tự động quét Image để tìm các lỗ hổng bảo mật (CVE) trong thư viện code của bạn.
* **Lifecycle Policies:** Tự động dọn dẹp các Image cũ hoặc các Image "rác" (untagged) để tiết kiệm chi phí lưu trữ.
* **Kiến thức mới:** ECR hiện hỗ trợ **Cross-Region Replication**, giúp code của bạn luôn có sẵn ở gần nơi triển khai nhất, tăng tốc độ khởi động container.

