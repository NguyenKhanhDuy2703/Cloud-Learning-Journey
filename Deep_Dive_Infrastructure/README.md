# 🛠️ AWS Deep Dive Infrastructure: Phân tích mối quan hệ giữa các dịch vụ

Chào mừng bạn đến với tài liệu học sâu (Deep Dive) về hạ tầng **Amazon Web Services (AWS)**. Dựa trên lộ trình chuyên nghiệp từ [roadmap.sh/aws](https://roadmap.sh/aws), tài liệu này không chỉ đi qua định nghĩa của từng dịch vụ mà tập trung phân tích **mối quan hệ tương quan, cách các dịch vụ tích hợp, bảo mật, và luồng dữ liệu chạy qua lại giữa chúng**.

---

## 🏛️ Sơ đồ kiến trúc tổng quan (Comprehensive 3-Tier Architecture)

Dưới đây là sơ đồ Mermaid thể hiện cách các dịch vụ AWS cốt lõi kết hợp với nhau trong một hệ thống Web App 3 lớp (3-Tier) an toàn, có khả năng tự động mở rộng và chịu lỗi cao:

```mermaid
graph TD
    %% Định nghĩa Client & DNS Tầng ngoài
    User[Người dùng / Clients] -->|1. Request DNS| R53[Amazon Route 53]
    User -->|2. HTTP/HTTPS Traffic| CF[Amazon CloudFront CDN]
    CF -.->|Bảo vệ WAF| WAF[AWS WAF]
    
    %% Tầng lưu trữ tĩnh & CDN
    CF -->|3a. Static Content Request| S3_Static[(Amazon S3 Private Bucket)]
    style S3_Static fill:#f9f,stroke:#333,stroke-width:2px
    
    %% Tầng mạng VPC & Load Balancer
    subgraph VPC [AWS VPC - Virtual Private Cloud]
        %% Tầng Load Balancer công cộng (Public Subnets)
        subgraph Public_Subnets [Public Subnets - Multi-AZ]
            ALB[Application Load Balancer - ALB]
            NAT[NAT Gateway]
        end
        CF -->|3b. Dynamic API/App Request| ALB
        
        %% Tầng ứng dụng (Private Subnets)
        subgraph Private_Subnets_App [Private Subnets - App Tier]
            ASG[Auto Scaling Group]
            EC2_A[EC2 Instance - AZ A]
            EC2_B[EC2 Instance - AZ B]
            ASG -.-> EC2_A
            ASG -.-> EC2_B
        end
        ALB -->|4. Forward Traffic| Private_Subnets_App
        EC2_A -->|5a. Outbound Internet| NAT
        EC2_B -->|5b. Outbound Internet| NAT
        
        %% Tầng CSDL (Private Isolated Subnets)
        subgraph Private_Subnets_DB [Private Subnets - Database Tier]
            RDS[(Amazon RDS Aurora - Multi-AZ)]
            Cache[(Amazon ElastiCache Redis)]
            Dynamo[(Amazon DynamoDB - VPC Endpoint)]
        end
        
        Private_Subnets_App -->|6. Query Cached Data| Cache
        Private_Subnets_App -->|7. Read/Write Relational| RDS
        Private_Subnets_App -->|8. NoSQL / Key-Value| Dynamo
    end
    
    %% Tầng Giám sát & Quản lý Bảo mật
    CW[Amazon CloudWatch] -.->|Thu thập metrics/logs| Private_Subnets_App
    CW -.->|Thu thập logs| RDS
    CW -.->|Kích hoạt scaling| ASG
    
    IAM[AWS IAM - Quyền & Quyền hạn] -.->|Cấp Role / Policy| Private_Subnets_App
    IAM -.->|Access Control| S3_Static
    
    %% Styles cho các thành phần chính
    style User fill:#f96,stroke:#333,stroke-width:2px
    style R53 fill:#6cf,stroke:#333,stroke-width:2px
    style CF fill:#6cf,stroke:#333,stroke-width:2px
    style VPC fill:#eee,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5
    style ALB fill:#ff9,stroke:#333,stroke-width:1px
    style RDS fill:#9cf,stroke:#333,stroke-width:2px
    style Cache fill:#9cf,stroke:#333,stroke-width:2px
    style Dynamo fill:#9cf,stroke:#333,stroke-width:2px
    style CW fill:#ff9,stroke:#333,stroke-width:1px
    style IAM fill:#f99,stroke:#333,stroke-width:2px
```

---

## 📂 Các giai đoạn phân tích chuyên sâu (Learning Phases)

Để giúp bạn tiếp thu một cách hệ thống và bám sát theo roadmap.sh/aws, kiến thức được chia làm 8 Phase cụ thể:

1. **[Phase 1: Foundations & Core Concepts (Nền tảng & Khái niệm cốt lõi)](./01_Foundations_Core_Concepts/)**
   - Tìm hiểu về các mô hình cloud, hạ tầng toàn cầu, Shared Responsibility Model và 6 trụ cột của Well-Architected Framework.
2. **[Phase 2: Core Compute, Networking & IAM (Hạ tầng Máy chủ, Mạng & Định danh)](./02_Core_Compute_Networking_IAM/)**
   - Phân tích sâu mối liên kết cốt lõi giữa `VPC`, `EC2`, và `IAM` cùng các nguyên tắc bảo mật mạng/máy chủ.
3. **[Phase 3: Storage, Content Delivery & SES (Lưu trữ, CDN & Email)](./03_Storage_ContentDelivery_SES/)**
   - Phân tích sâu luồng phân phối nội dung tĩnh/động kết hợp `S3`, `CloudFront`, `Route 53`, `SES` và giám sát qua `CloudWatch`.
4. **[Phase 4: Databases & Caching (Cơ sở dữ liệu & Bộ nhớ đệm)](./04_Databases_Caching/)**
   - Tìm hiểu cách tối ưu hóa tầng dữ liệu thông qua sự kết hợp của `RDS`, `DynamoDB`, `ElastiCache` và các mẫu thiết kế cache.
5. **[Phase 5: Containers & Serverless (Container & Điện toán Không máy chủ)](./05_Containers_Serverless/)**
   - Phân tích cơ chế hoạt động và tích hợp các dịch vụ hiện đại: `ECR`, `ECS`, `EKS`, `Fargate`, `Lambda`, và `API Gateway`.
6. **[Phase 6: Multi-Account Governance & Global Traffic (Quản trị Đa tài khoản & Điều phối Lưu lượng)](./06_MultiAccount_Governance_Global_DNS/)**
   - Phân tích tầng điều khiển: `AWS Organizations` (SCP/RCP), `IAM` (Policy Evaluation, Permissions Boundary, Identity Center) và `Route 53` (DNS tập trung, Latency Routing) trong kiến trúc multi-account.
7. **[Phase 7: Observability & Incident Response (Quan sát Hệ thống & Xử lý Sự cố)](./07_Observability_Incident_Response/)**
   - Ba trụ cột Metrics/Logs/Traces với `CloudWatch`, `X-Ray`, `CloudTrail`, `EventBridge` — và quy trình chẩn đoán sự cố trong hệ thống phân tán.
8. **[Phase 8: IaC, CI/CD & Deployment Automation (Hạ tầng dưới dạng Mã & Tự động hóa)](./08_IaC_CICD_Automation/)**
   - `CloudFormation`, `CDK`, `Terraform`, `StackSets`, `CodePipeline` và OIDC — biến toàn bộ hạ tầng Phase 1-7 thành code lặp lại được.

---

## 🎯 Cách khai thác tài liệu này hiệu quả

- **Bước 1:** Bắt đầu bằng việc đọc tài liệu tổng quan của từng nhóm để hiểu được **Why (Tại sao cần kết hợp chúng)** và **How (Chúng liên kết như thế nào)**.
- **Bước 2:** Nghiên cứu kỹ các sơ đồ kiến trúc cục bộ (Mermaid) trong mỗi thư mục để ghi nhớ luồng đi của dữ liệu.
- **Bước 3:** Áp dụng các kiến trúc này vào các dự án thực tế nằm trong thư mục [Example](../Example) để thực hành trực quan.
