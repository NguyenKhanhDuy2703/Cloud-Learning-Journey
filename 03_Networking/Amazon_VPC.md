# Amazon VPC: Configuring and Deploying with Multiple Subnets

> **Khóa học:** Configuring and Deploying VPCs with Multiple Subnets  
> **Cấp độ:** AWS Solutions Architect | **Phiên bản tài liệu:** v1.0

---

## Overview

**Amazon Virtual Private Cloud (Amazon VPC)** là dịch vụ cho phép bạn khởi chạy các tài nguyên AWS trong một mạng ảo riêng biệt, được định nghĩa logic và hoàn toàn do bạn kiểm soát.

### Vấn đề thực tế mà Amazon VPC giải quyết

Hãy tưởng tượng bạn mở một tòa nhà văn phòng trong "đám mây":
- **Không có VPC** → Mọi người đều có thể tự do đi vào tất cả các phòng.
- **Có VPC** → Bạn xây tường, đặt thẻ từ, bảo vệ từng tầng, kiểm soát chặt chẽ ai được vào phòng nào.

VPC giải quyết ba vấn đề cốt lõi:
1. **Cô lập mạng** – Tài nguyên của bạn không bị lẫn lộn với tài nguyên của người khác trên AWS.
2. **Kiểm soát truy cập** – Quyết định ai (user, service, IP) được phép đi vào/ra khỏi mạng.
3. **Kiến trúc linh hoạt** – Thiết kế nhiều tầng (tiers) bảo mật phù hợp với từng loại ứng dụng.

---

## Key Concepts & Keywords

| Từ khóa | Bản chất |
|---|---|
| **VPC** | Mạng ảo riêng biệt, hoàn toàn do bạn định nghĩa trong AWS Cloud |
| **Subnet** | Phân vùng nhỏ hơn trong VPC, gắn với một Availability Zone |
| **Public Subnet** | Subnet có route đến Internet Gateway → tài nguyên bên trong có thể tiếp cận internet |
| **Private Subnet** | Subnet KHÔNG có route đến Internet Gateway → bảo vệ database, backend |
| **Internet Gateway (IGW)** | Cổng kết nối VPC với internet công cộng |
| **Route Table** | Bảng định tuyến, quyết định traffic đi đâu từ subnet |
| **CIDR Block** | Dải địa chỉ IP của VPC (ví dụ: `172.31.0.0/16`) |
| **Network ACL** | Tường lửa ở cấp độ subnet, stateless |
| **Security Group** | Tường lửa ở cấp độ instance/ENI, stateful |
| **IAM** | Quản lý danh tính và quyền hạn – kiểm soát ai được làm gì trong AWS |
| **ELB** | Elastic Load Balancing – phân phối traffic vào nhiều instance để đạt HA |
| **Availability Zone (AZ)** | Trung tâm dữ liệu vật lý riêng biệt trong một Region – nền tảng của High Availability |
| **Multi-AZ** | Triển khai tài nguyên trên nhiều AZ để đảm bảo không bị gián đoạn |

---

## Detailed Deep Dive

### Module 1: Amazon VPC Deployment

#### 1.1 Default VPC vs Custom VPC

```
Default VPC (AWS tạo sẵn)          Custom VPC (do bạn tự tạo)
─────────────────────────           ─────────────────────────
CIDR: 172.31.0.0/16                 CIDR: tự chọn
/20 subnet mỗi AZ (4,096 IPs)       Subnet size: tự định nghĩa
Internet Gateway: ✅ có sẵn         Internet Gateway: phải tạo thủ công
Public & Private IP cho EC2: ✅     IP assignment: tự cấu hình
Default Security Group: ✅          Security: phải tự thiết lập
Default Network ACL (allow all): ✅  ACL: phải tự cấu hình
```

> **Ghi chú quan trọng:** Default VPC cho phép bắt đầu ngay lập tức, nhưng cho môi trường production, **luôn luôn sử dụng Custom VPC** để kiểm soát hoàn toàn bảo mật và kiến trúc mạng.

#### 1.2 Kiến trúc VPC cơ bản (từng bước)

```
┌─────────────────────────────────────────────┐
│                  AWS Cloud                  │
│  ┌───────────────────────────────────────┐  │
│  │              Region                   │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │         VPC (CIDR Block)        │  │  │
│  │  │                                 │  │  │
│  │  │  ┌──────────────────────────┐   │  │  │
│  │  │  │   Public Subnet          │   │  │  │
│  │  │  │   [Route → IGW]          │   │  │  │
│  │  │  │   EC2 Instance           │   │  │  │
│  │  │  └──────────────────────────┘   │  │  │
│  │  │                                 │  │  │
│  │  │  ┌──────────────────────────┐   │  │  │
│  │  │  │   Private Subnet         │   │  │  │
│  │  │  │   [No Route to IGW]      │   │  │  │
│  │  │  │   Database / Backend     │   │  │  │
│  │  │  └──────────────────────────┘   │  │  │
│  │  └─────────────────────────────────┘  │  │
│  │              │                        │  │
│  │    Internet Gateway (IGW)             │  │
│  └──────────────│────────────────────────┘  │
│                 ▼                           │
│              Internet                       │
└─────────────────────────────────────────────┘
```

**Sự khác biệt duy nhất giữa Public và Private Subnet:**
> Public Subnet = Subnet có **một route trỏ đến Internet Gateway** trong Route Table. Đó là tất cả sự khác biệt.

#### 1.3 Các lưu ý bổ sung quan trọng về VPC

- **DNS:** Mặc định VPC tự xử lý DNS. Có thể dùng `Amazon Route 53` với **Private Hosted Zones** để tạo DNS tùy chỉnh bên trong VPC.
- **Traffic giữa các subnet:** Mặc định tất cả subnet trong cùng VPC có thể giao tiếp với nhau. Dùng **Network ACL** để hạn chế nếu cần.
- **Traffic nội bộ trong cùng VPC:** Được forward trực tiếp, không cần đi ra ngoài.
- **Không có ARP:** VPC sử dụng unicast, không cần Address Resolution Protocol.
- **Kết nối với On-Premises:** Dùng `AWS Direct Connect`, `AWS Site-to-Site VPN`, hoặc `AWS Client VPN`.

---

### Module 2: Securing and Configuring High Availability

#### 2.1 AWS Identity and Access Management (IAM)

IAM kiểm soát **ai** được phép **làm gì** với tài nguyên AWS – đây là lớp bảo mật đầu tiên trước khi traffic chạm vào VPC.

```
Luồng hoạt động của IAM:
─────────────────────────────────────────────
User/App → [Authenticate] → [Authorize] → AWS Resource
              ↑                 ↑
         IAM Identity      IAM Policy
         (User/Group/Role) (Allow/Deny)
```

**Các thành phần IAM:**

- **IAM Users** – Đại diện cho con người hoặc ứng dụng cần truy cập tài khoản AWS.
- **IAM Groups** – Nhóm các user có cùng chức năng (dev team, sysadmin, finance...). Gán policy cho group thay vì từng user.
- **IAM Roles** – Được AWS services sử dụng (ví dụ: EC2 instance cần đọc S3). Cũng dùng để cấp quyền cho external access.
- **IAM Policies** – Tài liệu JSON định nghĩa Allow/Deny. **Phải được gắn** vào User, Group, hoặc Role mới có hiệu lực.

> **Nguyên tắc vàng: Principle of Least Privilege**  
> Chỉ cấp quyền tối thiểu cần thiết để thực hiện công việc. Quyền thừa = rủi ro thừa.

**Root User:**
- Được tạo tự động khi lập tài khoản AWS.
- Có **toàn quyền tuyệt đối**, không thể bị hạn chế.
- **KHÔNG nên dùng** cho công việc hằng ngày. Tạo IAM User riêng cho mọi tác vụ.

#### 2.2 Security Features: Network ACL vs Security Group

Đây là hai lớp bảo mật chính trong VPC, hoạt động ở **hai cấp độ khác nhau**.

```
┌─────────────────────────────────────────────────────┐
│                       VPC                            │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │              Subnet                           │   │
│  │  ╔══════════════╗  ← Network ACL (Subnet)    │   │
│  │  ║              ║                             │   │
│  │  ║  ┌────────┐  ║  ← Security Group (ENI)    │   │
│  │  ║  │  EC2   │  ║                             │   │
│  │  ║  └────────┘  ║                             │   │
│  │  ║              ║                             │   │
│  │  ╚══════════════╝                             │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**So sánh chi tiết:**

| Tiêu chí | Network ACL | Security Group |
|---|---|---|
| **Cấp độ áp dụng** | Subnet boundary | Instance / ENI |
| **Stateful/Stateless** | **Stateless** – phải định nghĩa cả inbound & outbound | **Stateful** – cho phép inbound thì outbound tự động được phép |
| **Default behavior** | Allow all (default ACL) | Deny all inbound (no inbound rules mặc định) |
| **Explicit Deny** | ✅ Có thể deny rõ ràng | ❌ Không có explicit deny (chỉ allow, còn lại implicit deny) |
| **Block IP address** | ✅ Làm được | ❌ Không làm được trực tiếp |
| **Nhận biết AWS resource** | ❌ Không | ✅ Có (có thể reference Security Group khác, Instance ID) |
| **Thứ tự rule** | Có thứ tự (rule number thấp = ưu tiên cao) | Không có thứ tự, tất cả rule được evaluate |

**Ví dụ thực tế:**
- Muốn **block toàn bộ IP từ một quốc gia** → Dùng **Network ACL**.
- Muốn **cho phép EC2 trong cùng Security Group giao tiếp với nhau** → Dùng **Security Group** (self-referencing rule).
- Muốn **chặn một IP cụ thể** trước khi nó chạm vào instance → Dùng **Network ACL** (vì Security Group không có explicit deny).

> **Lưu ý:** Hai EC2 instance trong cùng subnet giao tiếp với nhau sẽ **không bị Network ACL chặn** nếu traffic không vượt qua subnet boundary.

#### 2.3 Stateless vs Stateful – Giải thích bằng ví dụ

```
STATELESS (Network ACL):
─────────────────────────────────────────────
Client → [Request IN → ALLOW] → EC2
Client ← [Response OUT → ???] ← EC2
                ↑
       Phải có rule riêng cho phép traffic OUT
       Nếu không có rule OUT → Response bị BLOCK!

STATEFUL (Security Group):
─────────────────────────────────────────────
Client → [Request IN → ALLOW] → EC2
Client ← [Response OUT → Tự động ALLOW] ← EC2
                ↑
       Security Group nhớ "đây là response của connection đã được allow"
       → Tự động cho phép ra, không cần rule riêng
```

#### 2.4 Adding High Availability với Elastic Load Balancing

**Vấn đề:** Nếu chỉ có 1 EC2 instance trong 1 AZ, khi AZ đó gặp sự cố → toàn bộ ứng dụng sập.

**Giải pháp:** Multi-AZ + Elastic Load Balancing

```
                  Internet
                     │
            ┌────────▼────────┐
            │  Load Balancer   │  ← ELB phân phối traffic
            └────────┬────────┘
              ┌──────┴──────┐
              ▼             ▼
        ┌──────────┐  ┌──────────┐
        │  AZ - A  │  │  AZ - B  │
        │ [Subnet] │  │ [Subnet] │
        │  EC2 #1  │  │  EC2 #2  │
        └──────────┘  └──────────┘
```

**Bốn loại Elastic Load Balancer:**

| Load Balancer | Khi nào dùng |
|---|---|
| **Classic Load Balancer** | Legacy only – KHÔNG khuyến nghị cho hệ thống mới |
| **Application Load Balancer (ALB)** | HTTP/HTTPS, routing theo path/host, Layer 7 – **Ưu tiên chọn** |
| **Network Load Balancer (NLB)** | TCP/UDP, cần hiệu suất cực cao, Layer 4 |
| **Gateway Load Balancer (GWLB)** | Tích hợp với third-party virtual appliances (firewall, IDS/IPS) |

> **Best Practice:** Kết hợp ELB với **AWS Auto Scaling Group** để tự động thêm/bớt EC2 instance theo tải, đạt được **High Availability + Fault Tolerance + Scalability** cùng lúc.

---

### Module 3: Multi-Tier Architecture

#### 3.1 Tại sao cần Multi-Tier Architecture?

**Single-tier (mọi thứ trong 1 subnet):**
```
Internet → [Public Subnet: Web + App + Database]
                ↑
   Nếu attacker vào được subnet → Truy cập TOÀN BỘ hệ thống
```

**Multi-tier (phân tầng bảo mật):**
```
Internet
   │
   ▼
[PUBLIC SUBNET - Tier 1: Web/Presentation Layer]
   │  ← Chỉ cho phép traffic từ Tier 1 xuống Tier 2
   ▼
[PRIVATE SUBNET - Tier 2: Application Layer]
   │  ← Chỉ cho phép traffic từ Tier 2 xuống Tier 3
   ▼
[PRIVATE SUBNET - Tier 3: Database Layer]
```

**Lợi ích:** Attacker phải vượt qua TỪNG lớp bảo mật. Compromise Tier 1 không có nghĩa là mất Tier 2, Tier 3.

#### 3.2 Production-Ready: Multi-Tier VPC Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud - Region                        │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Custom VPC                              │  │
│  │                                                            │  │
│  │  ┌─────────────────────┐  ┌─────────────────────────┐    │  │
│  │  │      AZ - A          │  │         AZ - B            │    │  │
│  │  │                      │  │                           │    │  │
│  │  │ [PUBLIC SUBNET]      │  │ [PUBLIC SUBNET]           │    │  │
│  │  │  Web Server / LB     │  │  Web Server / LB          │    │  │
│  │  │                      │  │                           │    │  │
│  │  │ [PRIVATE SUBNET]     │  │ [PRIVATE SUBNET]          │    │  │
│  │  │  App Server          │  │  App Server               │    │  │
│  │  │                      │  │                           │    │  │
│  │  │ [PRIVATE SUBNET]     │  │ [PRIVATE SUBNET]          │    │  │
│  │  │  Database (Primary)  │  │  Database (Standby)       │    │  │
│  │  └─────────────────────┘  └─────────────────────────┘    │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│           │                                                       │
│   Internet Gateway                                               │
└───────────│─────────────────────────────────────────────────────┘
            ▼
         Internet
```

#### 3.3 Khi nào KHÔNG cần Multi-Tier?

| Tình huống | Kiến trúc phù hợp |
|---|---|
| Blog cá nhân, website đơn giản | **Single-Tier** – đủ dùng, tiết kiệm chi phí |
| Có thể chịu downtime kéo dài | **Single-AZ** deployment |
| Chỉ một mình sử dụng | Single-tier, Single-AZ |
| Ứng dụng doanh nghiệp, có dữ liệu nhạy cảm | **Multi-Tier, Multi-AZ** |
| Cần kết nối nhiều VPC | **VPC Peering / Transit Gateway** |

---

## Practical Examples & Scenarios

### Scenario 1: E-commerce Website

**Yêu cầu:** Website bán hàng, cần bảo vệ database khách hàng, luôn phải online.

**Giải pháp:**
```
User (Internet)
      │
      ▼
Application Load Balancer (ALB)
      │
  ┌───┴───┐
  │       │
AZ-A    AZ-B
[Public Subnet: Web servers]
      │
[Private Subnet: App servers]  ← Xử lý đơn hàng, business logic
      │
[Private Subnet: RDS Database] ← Không thể access từ internet
```

**Security layers:**
1. **IAM** – chỉ DevOps team có quyền deploy
2. **Network ACL** – block tất cả IP không thuộc dải private từ truy cập App/DB subnet
3. **Security Group** – Web chỉ nhận port 443, App chỉ nhận từ Web SG, DB chỉ nhận từ App SG

---

### Scenario 2: Hiểu Network ACL Stateless

Bạn tạo rule **ALLOW inbound port 443** trên Network ACL nhưng **quên tạo outbound rule** cho response.

**Kết quả:** HTTPS request vào được EC2, nhưng response **không thể gửi về** client → Website không load được dù EC2 đang chạy bình thường.

**Sửa:** Thêm outbound rule cho **ephemeral ports** (1024–65535) để cho phép response traffic.

> So sánh: Với Security Group, tạo inbound rule port 443 là đủ – response tự động được phép ra.

---

## Exam Essentials & Tips

### 🔑 Điểm mấu chốt cần nhớ

1. **Public vs Private Subnet** – Sự khác biệt DUY NHẤT là route table có trỏ đến Internet Gateway hay không.

2. **Network ACL = Stateless** → Cần tạo CÙNG LÚC inbound AND outbound rules. Quên một bên → traffic bị drop.

3. **Security Group = Stateful** → Allow inbound thì response outbound tự động được phép. **Không có explicit deny** – muốn block IP → phải dùng Network ACL.

4. **IAM Principle of Least Privilege** – Chỉ cấp quyền tối thiểu cần thiết. Root account = không dùng cho daily tasks.

5. **High Availability = Multi-AZ** – ELB + Auto Scaling Group trải đều trên nhiều AZ. Một AZ sập, AZ kia tiếp quản.

6. **ALB over Classic Load Balancer** – Luôn ưu tiên ALB cho ứng dụng mới.

### ⚠️ Các bẫy thường gặp

| Bẫy | Sự thật |
|---|---|
| "Default VPC có sẵn, dùng cho production được" | ❌ KHÔNG. Default VPC thiếu kiểm soát bảo mật cho production |
| "Security Group có thể block IP cụ thể" | ❌ KHÔNG. Phải dùng Network ACL để explicit deny |
| "Hai EC2 trong cùng Security Group tự giao tiếp được" | ❌ KHÔNG. Phải có self-referencing rule hoặc security group rule cho phép |
| "Subnet trong cùng VPC mặc định không giao tiếp được" | ❌ SAI. Mặc định tất cả subnet trong VPC ĐỀU giao tiếp được với nhau |
| "Network ACL chỉ cần rule inbound là đủ" | ❌ KHÔNG. ACL stateless → phải có cả outbound rule |

### 💰 Chi phí (Billing)

- **VPC, Subnet, Route Table, Network ACL, Security Group:** Miễn phí.
- **Internet Gateway:** Miễn phí tạo, **tính phí theo lượng data transfer** ra internet.
- **Elastic Load Balancer:** Tính phí theo giờ + lượng data xử lý.
- **NAT Gateway** (cho private subnet access internet): Tính phí theo giờ + data transfer.

### 🔒 Security Best Practices

- Dùng **multiple AZ deployments** cho High Availability.
- Dùng **Amazon CloudWatch** để monitor VPC components.
- Bật **VPC Flow Logs** để capture và phân tích traffic.
- **Chain security groups** – Security Group của App Layer chỉ accept từ Security Group của Web Layer.
- Tham khảo: [VPC Security Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)

### 🔗 Tài nguyên Compliance

| Tài nguyên | Mục đích |
|---|---|
| [AWS Compliance](https://aws.amazon.com/compliance/) | Tổng hợp các tiêu chuẩn compliance AWS hỗ trợ |
| [AWS Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html) | Trung tâm quản lý bảo mật tập trung |
| [Security Quick Starts](http://aws.amazon.com/quickstart/?awsf.quickstart-homepage-filter=categories%23security-identity-compliance) | Templates nhanh cho security & compliance |

---

## Tóm tắt Luồng Kiến Thức (Knowledge Flow)

```
[IAM] → Kiểm soát ai được cấu hình VPC
   ↓
[VPC + Subnets] → Định nghĩa mạng ảo, phân vùng Public/Private
   ↓
[Internet Gateway + Route Tables] → Điều hướng traffic vào/ra
   ↓
[Network ACL] → Lọc traffic tại subnet boundary (stateless)
   ↓
[Security Group] → Lọc traffic tại instance boundary (stateful)
   ↓
[ELB + Multi-AZ] → Phân phối tải, đạt High Availability
   ↓
[Multi-Tier Architecture] → Phân tầng bảo mật, giảm exposure
```

> **Triết lý cốt lõi:** Bảo mật là **trách nhiệm của bạn** bên trong VPC (Shared Responsibility Model). AWS cung cấp công cụ, bạn phải tự cấu hình đúng.