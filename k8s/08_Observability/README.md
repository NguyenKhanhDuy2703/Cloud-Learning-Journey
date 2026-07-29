# 08. Observability (Giám sát & Khả năng quan sát)

Ứng dụng chạy trên môi trường phân tán cần được kiểm tra sức khỏe liên tục, thu thập log tập trung và giám sát các chỉ số hiệu năng (metrics).

---

## 📌 Các nội dung cốt lõi

### 1. Container Health Probes (Kiểm tra sức khỏe Pod)
Kubernetes kiểm tra container thông qua 3 cơ chế probe chính:
*   **Startup Probe:** Kiểm tra xem ứng dụng đã khởi động thành công chưa. Mọi probe khác sẽ bị tạm ngưng cho tới khi Startup Probe thành công. Rất hữu ích cho các ứng dụng legacy khởi động chậm.
*   **Liveness Probe:** Kiểm tra xem ứng dụng còn sống (hoạt động bình thường) hay không. Nếu Liveness probe fail, K8s sẽ tự động hủy (kill) container và restart lại nó.
*   **Readiness Probe:** Kiểm tra xem ứng dụng đã sẵn sàng nhận request chưa. Nếu fail, Pod sẽ bị rút ra khỏi Service endpoint (không nhận traffic từ người dùng nữa).

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 3
  periodSeconds: 3
```

### 2. Logging (Thu thập Log tập trung)
Container logs thường xuất ra `stdout` và `stderr`. Ta cần thu thập chúng về một nơi tập trung trước khi container bị xoá:
*   **Kiến trúc:** Chạy logging agent (DaemonSet) trên từng node để đọc log files của container rồi đẩy về log storage.
*   **Các stack phổ biến:**
    *   **EFK / ELK Stack:** Elasticsearch (lưu trữ/tìm kiếm), Fluentd / Logstash (thu thập), Kibana (trực quan hóa).
    *   **PLG Stack (Hiện đại):** Grafana Loki (lưu trữ nhẹ), Promtail (thu thập), Grafana (trực quan hóa).

### 3. Monitoring & Metrics (Giám sát tài nguyên)
*   **Metrics Server:** Cung cấp tài nguyên CPU/RAM tiêu thụ của Pods/Nodes cho CLI (`kubectl top`) và hỗ trợ HPA.
*   **Prometheus & Grafana:** Bộ đôi tiêu chuẩn để thu thập metrics dạng Time-Series và vẽ các dashboard giám sát tài nguyên chi tiết.

---

## 🎯 Bài tập thực hành
1.  [ ] Viết một Deployment có cấu hình `livenessProbe` và `readinessProbe` dạng HTTP endpoint `/health`.
2.  [ ] Giả lập lỗi ở endpoint `/health` (ví dụ: trả về status code 500) và quan sát xem Kubernetes có tự động restart Pod hay không.
3.  [ ] Cài đặt `Metrics Server` lên cluster local của bạn và chạy lệnh `kubectl top nodes` / `kubectl top pods`.
