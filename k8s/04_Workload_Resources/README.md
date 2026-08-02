# 04. Workload Resources (Tài nguyên chạy ứng dụng)

Đây là những đối tượng cốt lõi giúp bạn deploy, cập nhật và quản lý các ứng dụng container hóa trên Kubernetes.

---

## 📦 Các loại Workload chính

### 1. Pods
*   Đơn vị nhỏ nhất và cơ bản nhất trong Kubernetes.
*   Một Pod chứa một hoặc nhiều container chia sẻ chung Network Namespace (IP, Port) và Storage Volumes.
*   **Init Containers:** Chạy trước container chính (thường dùng để check DB, tải file cấu hình...).
*   👉 **Tài liệu chuyên sâu:** Xem hướng dẫn thực hành và chẩn đoán lỗi tại [Pod_Deep_Dive.md](./Pod_Deep_Dive.md).

### 2. ReplicaSets
*   Đảm bảo duy trì một số lượng bản sao (replicas) của Pod nhất định luôn hoạt động.
*   Thường không tạo trực tiếp mà được quản lý thông qua **Deployment**.

### 3. Deployments (Dành cho Stateless Application)
*   Quản lý việc triển khai ứng dụng, tự động tạo ReplicaSet.
*   Hỗ trợ **Rolling Update** (cập nhật ứng dụng không gián đoạn) và **Rollback** (quay lại phiên bản cũ).
*   *Mẫu Deployment cơ bản:*
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web-app
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: web
      template:
        metadata:
          labels:
            app: web
        spec:
          containers:
          - name: nginx
            image: nginx:1.25.1
            ports:
            - containerPort: 80
    ```

### 4. StatefulSets (Dành cho Stateful Application)
*   Thích hợp cho Database (MySQL, PostgreSQL, MongoDB), Cache (Redis cluster).
*   Mỗi Pod được gán một định danh mạng duy nhất và cố định (ví dụ: `db-0`, `db-1`).
*   Yêu cầu kết hợp với **Headless Service** để định danh mạng cho từng Pod.

### 5. DaemonSets
*   Đảm bảo chạy duy nhất một bản sao của Pod trên mỗi Node trong cluster (hoặc một số Node chỉ định).
*   Thường dùng cho: Log collector (Fluentd, Promtail), Monitoring agent (Prometheus Node Exporter), Network plugin (Calico).

### 6. Jobs & CronJobs
*   **Job:** Chạy một hoặc nhiều Pod để hoàn thành một nhiệm vụ cụ thể rồi kết thúc (ví dụ: backup database, chạy migration).
*   **CronJob:** Chạy các Job định kỳ dựa trên cấu hình cron syntax (ví dụ: `*/5 * * * *`).

---

## 🎯 Bài tập thực hành
1.  [ ] Viết một YAML file cho một `Deployment` chạy Nginx 3 bản sao. Deploy nó vào cluster.
2.  [ ] Thực hiện cập nhật image từ `nginx:1.25.1` lên `nginx:1.25.2` bằng lệnh `kubectl set image`. Giám sát quá trình rolling update.
3.  [ ] Rollback deployment đó về phiên bản cũ và kiểm tra trạng thái.
4.  [ ] Tạo một `CronJob` in ra dòng chữ "Hello Kubernetes" mỗi phút một lần.
