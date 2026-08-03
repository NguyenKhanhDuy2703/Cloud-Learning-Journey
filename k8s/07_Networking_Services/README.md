# 07. Networking & Services (Mạng & Điều phối traffic)

Quản lý giao tiếp mạng giữa các Pods, Services và truy cập ứng dụng từ bên ngoài vào Kubernetes Cluster.

> [!TIP]
> **Tài liệu học tập & Thực hành:**
> - [Kubernetes_Ingress_Deep_Dive.md](file:///d:/Cloud_AWS/Cloud-Learning-Journey/k8s/07_Networking_Services/Kubernetes_Ingress_Deep_Dive.md) — Kiến trúc & Nguyên lý hoạt động chi tiết của Ingress.
> - [Nginx_Ingress_Controller_Setup_Guide.md](file:///d:/Cloud_AWS/Cloud-Learning-Journey/k8s/07_Networking_Services/Nginx_Ingress_Controller_Setup_Guide.md) — Hướng dẫn Cài đặt & Triển khai thực hành Nginx Ingress Controller từ A-Z.

---

Kubernetes có mô hình mạng phẳng: Mọi Pod đều có một IP duy nhất và có thể trực tiếp giao tiếp với các Pod khác mà không cần NAT (Network Address Translation).

---

## 📌 Các thành phần mạng cốt lõi

### 1. Services (Dịch vụ định tuyến nội bộ)
Do Pod có tính chất tạm thời và IP của chúng thay đổi liên tục khi tái tạo, Service được sinh ra làm một IP ảo cố định để làm cầu nối traffic tới các Pod phía sau (qua Selector).

*   **ClusterIP (Mặc định):** Chỉ cho phép truy cập Service từ bên trong Cluster.
*   **NodePort:** Mở một cổng tĩnh (trong khoảng `30000-32767`) trên tất cả các Node. Traffic gửi tới `NodeIP:NodePort` sẽ được chuyển tới Pod.
*   **LoadBalancer:** Tích hợp với dịch vụ Load Balancer của các nhà cung cấp Cloud (ví dụ AWS NLB/ALB) để cung cấp một IP public.
*   **Headless Service:** Không tạo ClusterIP (để `clusterIP: None`). Khi query DNS, hệ thống sẽ trả về trực tiếp IP của các Pod phía sau thay vì IP của Service. Rất hữu ích cho StatefulSets.

### 2. Ingress (Cổng định tuyến HTTP/HTTPS)
*   Quản lý traffic đi từ bên ngoài vào cluster (lớp Application Layer 7).
*   Cung cấp các luật routing dựa trên host name hoặc URL path (ví dụ: `api.example.com/v1` -> `api-service`).
*   Hỗ trợ SSL/TLS Termination.
*   Yêu cầu cài đặt một **Ingress Controller** để hoạt động (phổ biến nhất là `ingress-nginx`, `Traefik`, `Emissary-ingress`).

### 3. Network Policies (Firewall cho Pod)
*   Mặc định các Pod có thể gửi nhận traffic tự do.
*   Network Policy cho phép bạn quy định Pod nào được phép kết nối với Pod nào (Ingress rules) và Pod nào được phép gửi traffic đi đâu (Egress rules) dựa trên Label selectors.
*   Yêu cầu Network Plugin (CNI) hỗ trợ (như Calico, Cilium).

### 4. CoreDNS
*   Hệ thống quản lý phân giải tên miền (DNS) mặc định trong K8s.
*   Cho phép các Pod giao tiếp qua tên service: `http://<service-name>.<namespace>.svc.cluster.local`.

---

## 🎯 Bài tập thực hành
1.  [ ] Deploy một ứng dụng web đơn giản (2 replica). Tạo một Service dạng `ClusterIP` cho ứng dụng này.
2.  [ ] Chạy một Pod tạm thời chứa tool `curl` và thử request tới IP của Service để xem kết quả load balancing.
3.  [ ] Tạo Ingress rule để map domain `myapp.local` vào Service trên (Cần cấu hình file `/etc/hosts` trên máy cá nhân để trỏ domain về IP của Ingress Controller).
4.  [ ] Tạo một `NetworkPolicy` chặn hoàn toàn kết nối từ namespace `testing` tới namespace `production`.
