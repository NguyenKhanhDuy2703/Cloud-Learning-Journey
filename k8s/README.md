# ☸️ Kubernetes Learning Roadmap

Chào mừng bạn đến với lộ trình học tập **Kubernetes**! Thư mục này được thiết kế để lưu trữ các tài liệu, ghi chép học tập, các file cấu hình mẫu (manifests) và các bài thực hành dựa trên lộ trình chuẩn của [roadmap.sh/kubernetes](https://roadmap.sh/kubernetes).

---

## 🗺️ Lộ trình học tập (Table of Contents)

Dưới đây là các phần học được chia theo thứ tự từ cơ bản đến nâng cao. Mỗi thư mục đều đi kèm với tài liệu hướng dẫn chi tiết và các ví dụ thực tế.

| Thứ tự | Chủ đề học tập | Trạng thái | Ghi chú & Thực hành |
| :---: | :--- | :---: | :--- |
| 01 | [**Prerequisites** (Kiến thức tiên quyết)](./01_Prerequisites/README.md) | ⏳ Chưa bắt đầu | Tìm hiểu Linux, Docker, Mạng cơ bản |
| 02 | [**Architecture** (Kiến trúc K8s)](./02_Architecture/README.md) | ⏳ Chưa bắt đầu | Control Plane, Worker Nodes, etcd, API Server... |
| 03 | [**Setup & Installation** (Cài đặt môi trường)](./03_Setup_Installation/README.md) | ⏳ Chưa bắt đầu | Minikube, Kind, Kubeadm, EKS/GKE/AKS |
| 04 | [**Workload Resources** (Tài nguyên chạy ứng dụng)](./04_Workload_Resources/README.md) | ⏳ Chưa bắt đầu | Pod, Deployment, StatefulSet, DaemonSet, Job |
| 05 | [**Configuration & Secrets** (Cấu hình & Bảo mật)](./05_Configuration_Secrets/README.md) | ⏳ Chưa bắt đầu | ConfigMap, Secret, ServiceAccount |
| 06 | [**Storage** (Lưu trữ dữ liệu)](./06_Storage/README.md) | ⏳ Chưa bắt đầu | PV, PVC, StorageClass, CSI Drivers |
| 07 | [**Networking & Services** (Mạng & Dịch vụ)](./07_Networking_Services/README.md) | ⏳ Chưa bắt đầu | Services, Ingress, NetworkPolicies, CoreDNS |
| 08 | [**Observability** (Khả năng quan sát)](./08_Observability/README.md) | ⏳ Chưa bắt đầu | Probes, Logging, Monitoring (Prometheus & Grafana) |
| 09 | [**Autoscaling** (Tự động co giãn)](./09_Autoscaling/README.md) | ⏳ Chưa bắt đầu | HPA, VPA, Cluster Autoscaler |
| 10 | [**Security & Governance** (Bảo mật & Quản trị)](./10_Security/README.md) | ⏳ Chưa bắt đầu | RBAC, SecurityContext, Quotas & Limits |
| 11 | [**Advanced Concepts** (Khái niệm nâng cao)](./11_Advanced_Concepts/README.md) | ⏳ Chưa bắt đầu | Helm, GitOps (ArgoCD/Flux), CRDs & Operators |

---

## 🛠️ Công cụ hỗ trợ khuyên dùng

*   **CLI Tools:** `kubectl`, `kubectx` / `kubens` (chuyển nhanh context/namespace), `k9s` (giao diện terminal rất trực quan).
*   **IDE Extensions:** Extension Kubernetes cho VS Code (hỗ trợ tự động gợi ý cú pháp YAML).
*   **Local Cluster:** `Kind` hoặc `Minikube`.

## 📚 Tài liệu tham khảo chính thống

1.  **Kubernetes Documentation:** [kubernetes.io/docs](https://kubernetes.io/docs/)
2.  **Interactive Roadmap:** [roadmap.sh/kubernetes](https://roadmap.sh/kubernetes)
3.  **Kubernetes Academy (Free):** [kubernetes.academy](https://kubernetes.academy/)
