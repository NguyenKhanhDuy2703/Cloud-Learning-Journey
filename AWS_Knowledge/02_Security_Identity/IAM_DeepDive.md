#  Concept 1: AWS IAM - Chi tiết chuyên sâu

## 1. AWS IAM là gì?
**AWS Identity and Access Management (IAM)** là một dịch vụ web giúp bạn kiểm soát quyền truy cập vào các tài nguyên của AWS một cách an toàn. Về cơ bản, IAM giúp bạn trả lời câu hỏi: **"Ai (Who) có thể truy cập vào cái gì (What) và bằng cách nào (How) trong tài khoản AWS của bạn?"**

---

## 2. Các thực thể định danh trong IAM (IAM Entities)

Để quản lý "Ai", IAM cung cấp các thành phần sau:

### 2.1 Root User (Người dùng gốc)
- **Bản chất:** Là tài khoản được tạo ra khi bạn lần đầu đăng ký AWS (sử dụng email).
- **Quyền hạn:** Có quyền tối cao, truy cập được mọi ngóc ngách và không thể bị hạn chế bởi bất kỳ policy nào.
- **Best Practice:** Không bao giờ sử dụng Root User cho các công việc quản trị hàng ngày. Chỉ dùng để tạo IAM User đầu tiên có quyền Admin, sau đó "cất" thông tin Root đi.

### 2.2 IAM User
- **Bản chất:** Đại diện cho một con người hoặc một ứng dụng cụ thể trong tổ chức của bạn.
- **Thông tin xác thực:** Bao gồm Password (để đăng nhập Console) và Access Keys (để truy cập qua CLI/SDK).

### 2.3 IAM Group (Nhóm)
- **Bản chất:** Là một tập hợp các IAM User.
- **Mục đích:** Thay vì gán quyền cho từng người, bạn gán quyền cho Nhóm. Mọi User trong nhóm sẽ tự động thừa hưởng các quyền đó.
- **Ví dụ:** Nhóm `Admins`, `Developers`, `Testers`.

### 2.4 IAM Role (Vai trò)
- **Bản chất:** Giống như một User nhưng **không có mật khẩu hoặc access key cố định**.
- **Cơ chế:** Role cung cấp các quyền hạn tạm thời thông qua việc "đảm nhận" (Assume Role).
- **Đối tượng sử dụng:**
    - Các dịch vụ AWS (vd: Cho phép EC2 truy cập S3).
    - Người dùng từ tài khoản AWS khác.
    - Người dùng đăng nhập qua các hệ thống bên ngoài (SSO, Google, Facebook).



---

## 3. Xác thực và Ủy quyền (Authentication & Authorization)

Đây là quy trình 2 bước khi bất kỳ ai thực hiện một hành động trên AWS:

### 3.1 Authentication (Xác thực - Bạn là ai?)
Hệ thống kiểm tra danh tính của bạn thông qua:
- **Mật khẩu:** Đăng nhập giao diện web (Console).
- **Access Keys:** Sử dụng dòng lệnh (CLI) hoặc lập trình (SDK).
- **MFA (Multi-Factor Authentication):** Lớp bảo mật thứ 2 (App điện thoại hoặc thiết bị vật lý). **Bắt buộc phải bật MFA cho Root và các tài khoản quản trị.**

### 3.2 Authorization (Ủy quyền - Bạn được làm gì?)
Sau khi biết bạn là ai, AWS sẽ kiểm tra các **Policies** (Chính sách) gắn liền với bạn để quyết định cho phép (Allow) hay từ chối (Deny) hành động đó.



---

## 4. IAM Policies (Chính sách quyền hạn)

Policy là các tài liệu định dạng **JSON** mô tả quyền hạn.

### 4.1 Cấu trúc một Policy JSON cơ bản:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::example-bucket"
    }
  ]
}
```
- **Effect:** Allow (Cho phép) hoặc Deny (Từ chối).
- **Action:** Các hành động cụ thể (vd: `ec2:RunInstances`, `s3:GetObject`).
- **Resource:** Tài nguyên cụ thể áp dụng quyền (định danh bằng ARN).

### 4.2 Phân loại Policy
1. **Identity-based Policies:** Gán vào User, Group hoặc Role.
2. **Resource-based Policies:** Gán trực tiếp vào tài nguyên (vd: S3 Bucket Policy, KMS Key Policy).

---

## 5. Nguyên tắc vàng trong IAM

1. **Least Privilege (Đặc quyền tối thiểu):** Chỉ cấp đúng những gì cần thiết. Nếu nhân viên chỉ cần đọc file, đừng cấp quyền xóa hay sửa.
2. **Sử dụng IAM Groups:** Giúp quản lý quyền hạn nhất quán và dễ dàng thay đổi quy mô.
3. **Sử dụng Roles cho Dịch vụ:** Không bao giờ lưu Access Key của IAM User bên trong mã nguồn chạy trên EC2/Lambda. Hãy sử dụng **IAM Roles for EC2/Lambda**.
4. **Luôn bật MFA:** Bảo vệ tài khoản khỏi việc bị lộ mật khẩu.
5. **Xoay vòng Access Keys:** Định kỳ thay đổi khóa truy cập để giảm rủi ro bảo mật.
