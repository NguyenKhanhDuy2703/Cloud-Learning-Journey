# 05. Configuration & Secrets (Cấu hình & Bảo mật thông tin)

Mục tiêu chính là tách biệt mã nguồn (Code) khỏi cấu hình môi trường (Configuration) và thông tin nhạy cảm (Credentials).

---

## 📌 Các loại tài nguyên cấu hình

### 1. ConfigMaps
*   Lưu trữ cấu hình không nhạy cảm dưới dạng Key-Value (ví dụ: file config, biến môi trường, port, url).
*   Có thể truyền vào Pod dưới dạng **Biến môi trường (Environment Variables)** hoặc mount thành **File** bên trong container.
*   *Mẫu ConfigMap:*
    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: app-config
    data:
      APP_MODE: "production"
      DATABASE_URL: "db.example.com"
    ```

### 2. Secrets
*   Dùng để lưu thông tin nhạy cảm (Passwords, API Keys, SSL Certificates, Docker Registry credentials).
*   Mặc định giá trị được mã hóa dạng **Base64** trong manifest (Lưu ý: Base64 chỉ là encoding, không phải mã hóa bảo mật - Encryption).
*   **Các loại Secret phổ biến:**
    *   `Opaque`: Dùng chung cho Key-Value tùy biến.
    *   `kubernetes.io/dockerconfigjson`: Chứa thông tin đăng nhập registry để pull private image.
    *   `kubernetes.io/tls`: Chứa SSL/TLS certificate.
*   *Sử dụng Secret trong Pod:* Truyền qua biến môi trường (`valueFrom.secretKeyRef`) hoặc mount thành file trong thư mục an toàn.

### 3. ServiceAccounts
*   Cung cấp danh tính (identity) cho các tiến trình chạy bên trong Pod.
*   Nếu ứng dụng của bạn cần gọi API Server (ví dụ: Prometheus cần quét node, Jenkins cần tạo Pod), nó sẽ sử dụng token của ServiceAccount được gán cho Pod đó.

---

## 🔒 Lưu ý bảo mật thực tế
*   Tránh commit file YAML chứa Secret lên Git. Nên sử dụng các giải pháp quản lý secret chuyên sâu như **HashiCorp Vault**, **AWS Secrets Manager**, hoặc các công cụ mã hóa Git như **Mozilla SOPS**, **Sealed Secrets**.
*   Bật tính năng **Encryption at Rest** cho etcd để đảm bảo dữ liệu trong etcd được mã hóa vật lý.

---

## 🎯 Bài tập thực hành
1.  [ ] Tạo một `ConfigMap` chứa config của ứng dụng và mount nó vào Pod dưới dạng file `/etc/config/app.conf`. Truy cập vào Pod kiểm tra nội dung file.
2.  [ ] Tạo một `Secret` chứa password Database qua CLI:
    ```bash
    kubectl create secret generic db-secret --from-literal=password=SuperSecret123
    ```
3.  [ ] Viết Pod YAML sử dụng password này làm biến môi trường `DB_PASS`.
