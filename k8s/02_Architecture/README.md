# 02. Kubernetes Architecture (Kiến trúc Kubernetes)

Hiểu rõ cấu trúc và nguyên lý hoạt động của các thành phần trong Cluster giúp bạn dễ dàng debug khi gặp sự cố.

---

## 📌 Các thành phần chính của Cluster

Kubernetes cluster gồm 2 phần chính: **Control Plane (Master Node)** và **Worker Nodes**.

```mermaid
graph TD
    subgraph Control Plane (Master Node)
        API[kube-apiserver]
        ETCD[(etcd)]
        SCH[kube-scheduler]
        CM[kube-controller-manager]
    end

    subgraph Worker Node
        KLT[kubelet]
        KPX[kube-proxy]
        CRT[Container Runtime e.g. containerd]
    end

    API <--> ETCD
    API <--> SCH
    API <--> CM
    KLT <--> API
    KPX <--> API
    KLT <--> CRT
```

### 1. Control Plane (Bộ não điều khiển)
*   **kube-apiserver:** Cổng giao tiếp trung tâm của cluster. Mọi câu lệnh `kubectl` hay giao tiếp giữa các thành phần đều đi qua đây. API Server là stateless và lưu trạng thái vào etcd.
*   **etcd:** Cơ sở dữ liệu phân tán dạng Key-Value lưu trữ toàn bộ trạng thái cấu hình của cluster. Đây là "Source of Truth" duy nhất của cluster.
*   **kube-scheduler:** Lựa chọn Worker Node phù hợp nhất để chạy các Pod chưa được chỉ định node (dựa trên tài nguyên CPU/RAM yêu cầu, taints/tolerations, affinity...).
*   **kube-controller-manager:** Chạy các controller để giữ cluster ở trạng thái mong muốn (Desired State):
    *   *Node Controller:* Giám sát trạng thái các Node.
    *   *Job Controller:* Quản lý các công việc chạy 1 lần.
    *   *Endpoint Controller:* Kết nối Service và Pods.

### 2. Worker Nodes (Nơi chạy ứng dụng)
*   **kubelet:** Agent chạy trên từng Worker Node, chịu trách nhiệm nhận thông số PodSpecs từ API Server và đảm bảo các container được chạy đúng trạng thái mô tả.
*   **kube-proxy:** Quản lý cấu hình mạng trên từng Node, xử lý IP forwarding và tạo iptables/IPVS rules để điều hướng traffic đến các Pod khi gọi qua Service.
*   **Container Runtime:** Phần mềm chạy container (ví dụ: `containerd`), tải image và chạy container.

---

## 📝 Khái niệm cần phân biệt

### Imperative (Mệnh lệnh) vs. Declarative (Khai báo)
*   **Imperative:** Ra lệnh cho K8s làm gì và làm thế nào (ví dụ: `kubectl run nginx --image=nginx`). Dễ dùng cho việc test nhanh nhưng khó quản lý phiên bản.
*   **Declarative (Khuyên dùng):** Khai báo trạng thái mong muốn trong file YAML, K8s sẽ tự động tìm cách đưa cluster về trạng thái đó (ví dụ: `kubectl apply -f deployment.yaml`).

---

## 📚 Câu hỏi ôn tập tự đánh giá
1.  [ ] Chuyện gì xảy ra nếu etcd bị sập? Cluster có tiếp tục chạy ứng dụng hiện tại được không? Có scale hay deploy mới được không?
2.  [ ] Thành phần nào thực hiện hành động kéo image từ Registry về chạy? (Kubelet hay Kube-proxy hay Container Runtime?)
3.  [ ] Làm thế nào để xem logs của Control Plane components khi cài đặt cluster dạng self-managed?
