# 01. Prerequisites (Kiến thức tiên quyết)

Trước khi học Kubernetes, bạn cần nắm vững các nền tảng sau để tránh bị ngợp bởi các khái niệm mạng, phân quyền và lưu trữ.

---

## 📌 Các chủ đề trọng tâm

### 1. Linux & Command Line Basics
*   **Quản lý tiến trình & dịch vụ:** `systemctl`, `journalctl`, `ps`, `top`/`htop`.
*   **Phân quyền & User:** `chmod`, `chown`, `sudo`, `useradd`.
*   **Mạng cơ bản:** `ip a`, `ping`, `nslookup`, `curl`, `netstat`/`ss`, `telnet`.
*   **Xử lý văn bản & tìm kiếm:** `grep`, `awk`, `sed`, `find`, `cat`, `less`.
*   **Shell Scripting:** Các lệnh cơ bản để viết bash script phục vụ tự động hóa.

### 2. Containers & Docker (Cực kỳ quan trọng)
Kubernetes là hệ thống điều phối container, do đó bạn cần hiểu cách container hoạt động độc lập:
*   **Container Runtimes:** Hiểu về CRI (Container Runtime Interface), `containerd`, `CRI-O`.
*   **Docker Basics:**
    *   Cách build Docker Image bằng `Dockerfile` (optimize image size, multi-stage build).
    *   Quản lý Image: `docker pull`, `docker push`, `docker build`, `docker tag`.
    *   Chạy Container: `docker run`, `docker stop`, `docker ps`, `docker logs`, `docker exec`.
    *   **Docker Volumes:** Lưu trữ dữ liệu ngoài vòng đời của container.
    *   **Docker Network:** Bridge network, Host network, Overlay network.

### 3. Cú pháp YAML
Toàn bộ tài nguyên K8s được khai báo qua định dạng YAML. Bạn cần nắm:
*   Cấu trúc Key-Value.
*   Danh sách (Lists/Arrays - ký tự `-`).
*   Map (Dictionaries/Objects).
*   Thụt lề (Indentation - sử dụng khoảng trắng, tuyệt đối không dùng Tab).
*   Multi-line strings (`|` và `>`).

---

## 🛠️ Bài tập thực hành tự đánh giá
1.  [ ] Viết một `Dockerfile` multi-stage để build ứng dụng Node.js hoặc Go mini, tối ưu dung lượng image xuống dưới 50MB.
2.  [ ] Chạy container đó và mount một thư mục từ máy host vào container (Volume mounting).
3.  [ ] Tạo một file YAML mô tả thông tin cá nhân của bạn dưới dạng cấu trúc lồng nhau (nested keys) và kiểm tra tính hợp lệ của cú pháp (YAML lint).

---

## 📚 Tài liệu khuyên đọc
*   [Docker Get Started Guide](https://docs.docker.com/get-started/)
*   [Learn YAML in Y Minutes](https://learnxinyminutes.com/docs/yaml/)
