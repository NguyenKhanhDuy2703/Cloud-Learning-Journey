# 03. Setup & Installation (Cài đặt môi trường)

Để học Kubernetes hiệu quả, việc tự tay dựng và quản trị cluster (cho dù là local hay cloud) là bước vô cùng quan trọng.

---

## 🛠️ Công cụ dòng lệnh (CLI Tools)
Trước tiên, hãy cài đặt các công cụ sau trên máy cá nhân:
1.  **kubectl:** Công cụ dòng lệnh để giao tiếp với Kubernetes API.
    *   Cấu hình autocompletion và alias (`k` thay cho `kubectl`).
2.  **kubectx & kubens:** Công cụ chuyển đổi nhanh chóng giữa các Kubernetes Clusters (context) và Namespaces.
3.  **k9s:** Giao diện terminal (TUI) rất mạnh để giám sát cluster thời gian thực.

---

## 🖥️ Các giải pháp chạy K8s Local (Dành cho việc học & phát triển)

### 1. Kind (Kubernetes in Docker)
*   Chạy các node Kubernetes dưới dạng các Docker Container.
*   **Ưu điểm:** Khởi động cực nhanh, hỗ trợ tạo multi-node cluster rất dễ dàng.
*   *Cách tạo cluster với Kind:*
    ```bash
    kind create cluster --name my-k8s-lab
    ```

### 2. Minikube
*   Giải pháp chạy Kubernetes local truyền thống, chạy trên Virtual Machine hoặc Docker.
*   *Cách chạy:* `minikube start --driver=docker`

---

## ☁️ Managed Kubernetes trên Cloud (Thực tế doanh nghiệp)

Khi đi làm, phần lớn bạn sẽ tiếp xúc với các dịch vụ Kubernetes được quản lý bởi các Cloud Providers lớn:
*   **Amazon EKS (Elastic Kubernetes Service):** Tích hợp sâu với AWS IAM, VPC, và EBS/EFS.
*   **Google GKE (Google Kubernetes Engine):** Được đánh giá là dịch vụ K8s mượt mà nhất, có tính năng auto-pilot.
*   **Azure AKS (Azure Kubernetes Service):** Dễ dàng quản trị thông qua Azure portal và tích hợp Entra ID (Azure AD).

---

## 🎯 Thực hành: Tạo Cluster đầu tiên của bạn
1.  [ ] Cài đặt `kubectl` và `kind` trên máy tính của bạn.
2.  [ ] Tạo một cluster Kind có cấu hình **1 Control Plane và 2 Worker Nodes** bằng cách tạo file `kind-config.yaml`:
    ```yaml
    kind: Cluster
    apiVersion: kind.x-k8s.io/v1alpha4
    nodes:
    - role: control-plane
    - role: worker
    - role: worker
    ```
    Sau đó chạy lệnh: `kind create cluster --config kind-config.yaml`
3.  [ ] Kiểm tra các node đang chạy bằng lệnh: `kubectl get nodes -o wide`
