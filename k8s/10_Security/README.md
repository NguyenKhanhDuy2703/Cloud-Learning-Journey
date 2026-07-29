# 10. Security & Governance (Bảo mật & Quản trị)

Bảo mật Kubernetes đòi hỏi cách tiếp cận đa lớp (Defense in Depth) từ tầng hệ thống, mạng, phân quyền đến cấu hình runtime của container.

---

## 📌 Các chủ đề bảo mật trọng tâm

### 1. RBAC (Role-Based Access Control)
Phân quyền truy cập tài nguyên Kubernetes API dựa trên vai trò người dùng hoặc ServiceAccount.
*   **Role & ClusterRole:** Định nghĩa quyền hạn được làm gì (ví dụ: `get`, `list`, `watch`, `create`, `delete` đối với `pods`, `services`).
    *   *Role:* Giới hạn trong một Namespace cụ thể.
    *   *ClusterRole:* Có giá trị trên toàn bộ Cluster (hoặc cho các tài nguyên không thuộc namespace như Nodes, Namespaces).
*   **RoleBinding & ClusterRoleBinding:** Gán Role/ClusterRole đã định nghĩa ở trên cho đối tượng cụ thể (User, Group, hoặc ServiceAccount).

### 2. Security Contexts (Cấu hình bảo mật Container)
Định nghĩa các thiết lập bảo mật chạy trên mức Pod hoặc Container:
*   `runAsUser` / `runAsGroup`: Chạy container bằng user non-root (ví dụ UID 1000) thay vì root.
*   `allowPrivilegeEscalation`: Chặn container nâng quyền hạn.
*   `readOnlyRootFilesystem`: Đặt toàn bộ filesystem của container ở chế độ chỉ đọc để tránh hacker cài cắm backdoor.
*   `capabilities`: Bật/tắt các quyền hệ thống cấp kernel chi tiết (như `NET_ADMIN`, `SYS_TIME`).

### 3. Resource Quotas & Limit Ranges
*   **ResourceQuota:** Đặt giới hạn tối đa tổng tài nguyên (ví dụ: tối đa 4 CPU, 8Gi RAM, 10 Services) được phép tạo trong một Namespace.
*   **LimitRange:** Thiết lập giá trị mặc định, tối thiểu, và tối đa cho CPU/RAM `requests` và `limits` của mỗi Pod được tạo ra trong namespace đó.

### 4. Network Security (đã nhắc ở phần 07)
Chỉ cho phép những traffic cần thiết đi qua Network Policies.

---

## 🎯 Bài tập thực hành
1.  [ ] Tạo một Namespace `dev-team`.
2.  [ ] Tạo một `Role` trong namespace đó chỉ cho phép đọc (`get`, `list`) các Pods.
3.  [ ] Tạo một `ServiceAccount` tên `reader-sa`.
4.  [ ] Dùng `RoleBinding` gán Role trên cho `ServiceAccount` `reader-sa`.
5.  [ ] Sử dụng lệnh sau để kiểm tra quyền hạn của ServiceAccount:
    ```bash
    kubectl auth can-i create pods --as=system:serviceaccount:dev-team:reader-sa
    # Lệnh trên phải trả về "no"
    ```
6.  [ ] Viết Pod YAML cấu hình `securityContext` để chạy dưới user non-root (UID `1000`) và kiểm tra.
