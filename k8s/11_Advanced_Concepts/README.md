# 11. Advanced Concepts (Khái niệm nâng cao)

Khi đã nắm vững các tài nguyên cơ bản, đây là những công cụ và mô hình thiết kế giúp bạn vận hành hệ thống lớn, tự động hóa toàn diện trong môi trường Production.

---

## 📌 Các chủ đề nâng cao

### 1. Helm (Package Manager cho Kubernetes)
Thay vì viết hàng tá file YAML manifest tĩnh riêng lẻ, Helm giúp đóng gói ứng dụng (Helm Charts) để dễ dàng chia sẻ, cấu hình động và quản lý phiên bản:
*   **Templates:** Sử dụng ngôn ngữ template của Go để truyền các tham số động từ file `values.yaml` vào manifest.
*   **Values.yaml:** Nơi tập trung cấu hình của Chart.
*   **Helm CLI:** `helm install`, `helm upgrade`, `helm rollback`, `helm uninstall`.

### 2. GitOps (Mô hình triển khai hiện đại)
*   Sử dụng Git làm **Single Source of Truth** duy nhất cho trạng thái mong muốn của toàn bộ hạ tầng và ứng dụng.
*   **Công cụ nổi bật:** **ArgoCD** hoặc **Flux**.
*   **Hoạt động:** Một agent chạy trong cluster sẽ liên tục kéo (pull) cấu hình YAML từ Git repo về, so sánh với trạng thái cluster hiện tại và tự động đồng bộ (reconciliation) nếu phát hiện có sự sai lệch (Configuration Drift).

### 3. CRDs & Operators (Mở rộng K8s API)
*   **Custom Resource Definition (CRD):** Cho phép bạn tự định nghĩa ra các loại tài nguyên mới của riêng mình ngoài những đối tượng mặc định như Pod, Service (ví dụ: Tạo tài nguyên loại `Database`).
*   **Operators/Controllers:** Các ứng dụng chạy ngầm liên tục giám sát CRD và thực hiện các logic nghiệp vụ phức tạp (ví dụ: Một Mysql-Operator khi thấy khai báo CRD `kind: Mysql` sẽ tự động cấp phát PV, tạo Service, thiết lập cấu hình Replication Master-Slave, và lên lịch backup tự động).

### 4. Service Mesh (Quản trị mạng nâng cao)
*   Khi có hàng trăm Microservices giao tiếp với nhau, Service Mesh được cài đặt để quản trị kết nối nội bộ lớp Application.
*   **Công cụ:** **Istio**, **Linkerd**.
*   **Tính năng chính:**
    *   **mTLS (Mutual TLS):** Tự động mã hóa lưu lượng giao tiếp giữa các Pod.
    *   **Traffic Management:** Canary deployments, Blue-Green, A/B testing, Circuit Breaking (ngắt mạch khi quá tải).
    *   **Observability:** Theo dõi luồng đi của request qua các Service (Distributed Tracing).

---

## 🎯 Bài tập thực hành nâng cao
1.  [ ] Cài đặt Helm trên máy cá nhân và deploy một cụm Redis hoặc PostgreSQL vào cluster thông qua Bitnami Helm Chart.
2.  [ ] Tự viết một Helm Chart đơn giản cho ứng dụng của bạn bằng lệnh `helm create my-app` và tùy biến file `values.yaml`.
3.  [ ] Tìm hiểu và thiết lập ArgoCD để tự động deploy một ứng dụng khi bạn push file manifest lên Git.
