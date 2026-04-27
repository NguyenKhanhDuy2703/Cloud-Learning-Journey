# AWS & Cloud Computing

Chào mừng đến với kho lưu trữ kiến thức AWS của tôi! Repository này lưu trữ, tổng hợp và phân tích toàn bộ kiến thức tôi đã học trong 3 tuần qua về Điện toán đám mây, từ các khái niệm nền tảng, thiết kế mạng, bảo mật cho đến các dịch vụ xu hướng như Serverless và Generative AI.

---

## Cấu trúc Thư mục

Dưới đây là sơ đồ thư mục của dự án này. Mỗi thư mục đại diện cho một trụ cột kiến thức cốt lõi.

```text
aws-cloud-mastery/
├── README.md
├── 01_Cloud_Architecture_Fundamentals/
│   ├── Cloud_Concepts.md
│   └── Global_Infrastructure.md
├── 02_Security_Identity/
│   ├── IAM_DeepDive.md
│   └── Network_Security_SG_NACL.md
├── 03_Networking/
│   ├── VPC_Subnets_Basics.md
│   ├── Gateways_RouteTables.md
│   └── API_Gateway.md
├── 04_Compute_Serverless/
│   ├── EC2_Overview.md
│   └── Lambda_Foundations.md
├── 05_Storage/
│   ├── S3_Essentials_Advanced.md
│   └── EBS_Primer.md
├── 06_Databases/
│   ├── RDS_Relational.md
│   ├── DynamoDB_NoSQL.md
│   └── Other_DBs_ElastiCache_Neptune.md
├── 07_Generative_AI/
│   ├── Bedrock_Foundation_Models.md
│   ├── RAG_Knowledge_Bases.md
│   └── Bedrock_Multi_Agents.md
└── 08_Infrastructure_As_Code/
    └── CloudFormation_Basics.md
```
## Mục lục Chi tiết 
  1. Nền tảng Đám mây & Kiến trúc
     - Khái niệm Đám mây (IaaS, PaaS, SaaS, Serverless) & 6 Lợi ích
     - Hạ tầng Toàn cầu AWS (Regions, AZs, Edge Locations)
  2. Quản lý Định danh & Bảo mật
     - Kiến trúc IAM (Users, Roles, Policies & Least Privilege)
     - Bảo mật Mạng cơ bản: Security Groups vs Network ACLs
  3. Dịch vụ Mạng (Networking)
     - Khái niệm nền tảng Amazon VPC (IPv4, IPv6, CIDR, Subnets)
     - Định tuyến & Cổng kết nối (Route Tables, IGW, NAT Gateway)
     - Tổng quan về mạng ứng dụng: Amazon API Gateway
  4. Dịch vụ Tính toán (Compute & Serverless)
     - Tổng quan về Amazon EC2 (Máy chủ ảo)
     - Nền tảng AWS Lambda & Kiến trúc Hướng sự kiện (Event-Driven)
  5. Dịch vụ Lưu trữ (Storage)
     - Amazon S3: Từ cơ bản đến nâng cao (Classes, Versioning)
     - Lưu trữ Khối: Amazon EBS (Elastic Block Store)
  6. Cơ sở dữ liệu (Databases)
     - Cơ sở dữ liệu Quan hệ: Amazon RDS Primer
     - Cơ sở dữ liệu NoSQL: Amazon DynamoDB Getting Started
     - Tổng quan các dịch vụ DB khác (Neptune, ElastiCache)
  7. Trí tuệ Nhân tạo (AI & Generative AI)
     - Amazon Bedrock & Các mô hình nền tảng (Foundation Models)
     - Xây dựng ứng dụng với MultiModal Knowledge Bases (RAG) & S3 Vectors
     - Sự hợp tác đa tác vụ: Multi-Agent Collaboration với Bedrock Agents
  8. Tự động hóa & IaC
     - Cơ bản về AWS CloudFormation (Infrastructure as Code)