# ☁️ AWS & Cloud Computing Learning Journey

Chào mừng đến với kho lưu trữ kiến thức AWS của tôi! Repository này lưu trữ, tổng hợp và phân tích toàn bộ kiến thức, các ghi chú (notes) và các bài thực hành (labs) mà tôi đã và đang tìm hiểu về hệ sinh thái **Điện toán Đám mây (Cloud Computing)** và **Generative AI** trên AWS.

Từ các khái niệm nền tảng cốt lõi, thiết kế mạng, bảo mật, dịch vụ máy tính/lưu trữ cho đến các công nghệ đỉnh cao hiện tại như Serverless, Data Engineering, Analytics, và Amazon Bedrock, tất cả đều được cấu trúc rõ ràng.

---

## 📂 Cấu trúc Thư mục Hệ thống

Kho lưu trữ được chia rải đều từ các kiến thức căn bản nhất đến các dự án thực hành (Examples).

```text
Cloud-Learning-Journey/
├── AWS_Knowledge/
│   ├── 01_Cloud_Architecture_Fundamentals/ # Khái niệm & Nền tảng Đám mây
│   ├── 02_Security_Identity/               # Bảo mật, IAM, Amazon Macie
│   ├── 03_Networking/                      # Mạng (VPC, Connectivity, Edge Services)
│   ├── 04_Compute_Serverless/              # Máy chủ ảo (EC2), Container & Serverless (Lambda)
│   ├── 05_Storage_Database/                # Lưu trữ (S3) và CSDL (Aurora, DynamoDB, Neptune, ElastiCache)
│   ├── 06_Generative_AI/                   # Amazon Bedrock, GenAI, Agents, RAG
│   ├── 07_Analytics/                       # Phân tích dữ liệu (Athena, OpenSearch)
│   ├── 08_Data_Engineering/                # Xử lý & Kỹ thuật dữ liệu (Glue, EMR, Redshift, Kinesis)
│   ├── 09_AWS Customer Engagement/         # Các dịch vụ tương tác (Amazon Connect)
│   ├── 10_Cost_Optimization/               # Chiến lược tối ưu hóa chi phí AWS
│   ├── 11_Observability/                   # Giám sát và quan sát với CloudWatch
│   └── 12_Cloud_Governance/                # Quản trị cloud, SCP, tagging và cost-aware governance
├── Deep_Dive_Infrastructure/           # Học sâu hạ tầng & Sơ đồ quan hệ các dịch vụ
└── Example/                            # Các thư mục code thực hành và dự án mẫu (Labs/Workspaces)
    └── my-workspace/
        ├── lab1-study/                 # Lab 1: Tích hợp Bedrock (Study Buddy)
        ├── lab2-cert/                  # Lab 2: Luyện thi với AI CLI và Bedrock Agents
        └── lab3-kiro/                  # Lab 3: Dự án Kiro Full-stack (React/Vite + Node.js)
```

---

## 🛠️ Học sâu Hạ tầng AWS (Deep Dive Infrastructure)

Chương trình học nâng cao, tập trung phân tích sự liên kết và luồng đi của dữ liệu giữa các dịch vụ lớn trong thực tế:

*   **[Tổng quan & Sơ đồ kiến trúc 3-Tier](./Deep_Dive_Infrastructure/README.md):** Xem sơ đồ phối hợp tổng thể của hệ thống.
*   **[Phase 1: Foundations & Core Concepts](./Deep_Dive_Infrastructure/01_Foundations_Core_Concepts/README.md):** Cloud Computing, Shared Responsibility Model, và Well-Architected Framework.
*   **[Phase 2: Core Compute, Networking & IAM](./Deep_Dive_Infrastructure/02_Core_Compute_Networking_IAM/README.md):** VPC, EC2, và cơ chế bảo mật IAM.
*   **[Phase 3: Storage, Content Delivery & SES](./Deep_Dive_Infrastructure/03_Storage_ContentDelivery_SES/README.md):** S3, CloudFront, Route 53, SES và CloudWatch.
*   **[Phase 4: Databases & Caching](./Deep_Dive_Infrastructure/04_Databases_Caching/README.md):** RDS, DynamoDB, và ElastiCache.
*   **[Phase 5: Containers & Serverless](./Deep_Dive_Infrastructure/05_Containers_Serverless/README.md):** ECR, ECS, EKS, Fargate, Lambda, và API Gateway.
*   **[Phase 6: Multi-Account Governance & Global Traffic](./Deep_Dive_Infrastructure/06_MultiAccount_Governance_Global_DNS/README.md):** AWS Organizations, IAM và Route 53 trong kiến trúc multi-account.
*   **[Phase 7: Observability & Incident Response](./Deep_Dive_Infrastructure/07_Observability_Incident_Response/README.md):** CloudWatch, X-Ray, CloudTrail, EventBridge và quy trình xử lý sự cố.
*   **[Phase 8: IaC, CI/CD & Deployment Automation](./Deep_Dive_Infrastructure/08_IaC_CICD_Automation/README.md):** CloudFormation, CDK, Terraform, StackSets, CodePipeline và OIDC.

---

## 📚 Nội dung Chi tiết các Chủ đề

### 1. Nền tảng Kiến trúc Đám mây (`01_Cloud_Architecture_Fundamentals`)

- Khái niệm về Cloud (IaaS, PaaS, SaaS)
- Lợi ích của Đám mây và hạ tầng toàn cầu (Global Infrastructure).

### 2. Quản lý Định danh & Bảo mật (`02_Security_Identity`)

- **[IAM Deep Dive](./AWS_Knowledge/02_Security_Identity/IAM_DeepDive.md):** Phân tích sâu về Quản lý định danh (Users, Roles, Policies, Best Practices).
- **[IAM Deep Dive v2](./AWS_Knowledge/02_Security_Identity/IAM_DeepDive_v2.md):** Policy Evaluation Logic, Permissions Boundary, ABAC, Confused Deputy, IAM Identity Center và Access Analyzer.
- **Network Security:** Các lớp bảo vệ mạng (Security Groups vs NACL).
- **Amazon Macie:** Khám phá công cụ phân tích và bảo vệ dữ liệu nhạy cảm sử dụng Machine Learning.

### 3. Dịch vụ Mạng (`03_Networking`)

- Kế hoạch và thiết kế [Amazon VPC](./AWS_Knowledge/03_Networking/AmazonVPC.md).
- [Kết nối Mạng](./AWS_Knowledge/03_Networking/Connectivity.md) (VPN, Direct Connect, Transit Gateway).
- [Dịch vụ biên - Edge Services](./AWS_Knowledge/03_Networking/Edge_services.md) (CloudFront, Route53, WAF).
- **[Amazon Route 53 Deep Dive](./AWS_Knowledge/03_Networking/Amazon_Route53_DeepDive.md):** 7 Routing Policies, Health Check, Alias vs CNAME, Private Hosted Zone, Resolver hybrid DNS, DNSSEC và ARC.

### 4. Máy tính & Serverless (`04_Compute_Serverless`)

- **Compute:** Kiến thức về [EC2](./AWS_Knowledge/04_Compute_Serverless/EC2_Overview.md) và Elastic Beanstalk.
- **Microservices & Serverless:** [Container Services](./AWS_Knowledge/04_Compute_Serverless/container_service.md) (ECS, EKS) và Kiến trúc Event-Driven với [AWS Lambda](./AWS_Knowledge/04_Compute_Serverless/Lambda_Foundations.md).

### 5. Lưu trữ & Khai thác Dữ liệu (`05_Storage_Database`)

- **Storage:** Khái niệm [Các dịch vụ lưu trữ](./AWS_Knowledge/05_Storage_Database/storage_service.md) cốt lõi như S3, EBS, EFS.
- **Databases:** Tổng quan về [các dịch vụ cơ sở dữ liệu](./AWS_Knowledge/05_Storage_Database/database_service.md).
- Đi sâu vào thiết kế NoSQL với [DynamoDB](./AWS_Knowledge/05_Storage_Database/DynamoDB_DesignPatterns.md), GraphDB với [Neptune](./AWS_Knowledge/05_Storage_Database/Amazon_Neptun.md), và RDBMS với [Aurora](./AWS_Knowledge/05_Storage_Database/Amazon_Aurora_Getting_Started.md).

### 6. Tối ưu hóa Chi phí AWS (`10_Cost_Optimization`)

- **EBS Cost Optimization:** Giảm chi phí lưu trữ block bằng cách chọn loại volume, quản lý snapshots và sử dụng Elastic Volumes.
- **S3 Cost Optimization:** Điều chỉnh lưu trữ, lifecycle policy và storage class để giảm chi phí dữ liệu đối tượng.
- **EBS Performance Optimization:** Tối ưu hiệu năng và chi phí EBS thông qua chọn volume, IOPS/throughput và thiết kế RAID phù hợp.

### 7. Trí tuệ Nhân tạo - Generative AI (`06_Generative_AI`) 🚀

- Các khái niệm nền tảng AI/ML và làm quen với **Amazon Bedrock**.
- Hiểu về Các mô hình nền tảng (Foundation Models).
- Kỹ thuật **RAG** (Retrieval-Augmented Generation) & Knowledge Bases.
- Thực hành xây dựng tác vụ thông minh với **Agents for Amazon Bedrock** và AI có trách nhiệm (Responsible AI).

### 8. Phân tích Dữ liệu (`07_Analytics`)

- Data Query & Analytics với **Amazon Athena**.
- Giải pháp tìm kiếm nâng cao với **OpenSearch**.

### 9. Kỹ thuật Dữ liệu - Data Engineering (`08_Data_Engineering`)

- Thu thập và lưu lượng dữ liệu: **Amazon Kinesis**.
- ETL (Extract, Transform, Load): **AWS Glue**.
- Xử lý dữ liệu lớn (Big Data): **Amazon EMR** & **Redshift**.

### 10. Giám sát & Quan sát (`11_Observability`)

- **Amazon CloudWatch:** [Getting Started](./AWS_Knowledge/11_Observability/Amazon_CloudWatch_Getting_Started.md) với logs, metrics, alarms và dashboard.
- Kết hợp **Synthetics / RUM** với cảnh báo để phát hiện sự cố sớm.
- Phân biệt giữa observability và monitoring.

### 11. Cloud Governance (`12_Cloud_Governance`)

- **Cloud Governance:** [Cân bằng Bảo mật và Chi phí](./AWS_Knowledge/12_Cloud_Governance/Cloud_Governance.md).
- **[AWS Organizations Deep Dive](./AWS_Knowledge/12_Cloud_Governance/AWS_Organizations_DeepDive.md):** Kiến trúc multi-account theo AWS SRA, SCP vs RCP, Delegated Administrator, Control Tower và Data Perimeter.
- **[Phân tích Tích hợp: Route 53 + IAM + Organizations](./AWS_Knowledge/12_Cloud_Governance/Route53_IAM_Organizations_Integration.md):** Ba trục WHERE / WHO / HOW USERS ARRIVE, DNS tập trung qua RAM, chống privilege escalation và quy trình xử lý sự cố.
- **Tag Policy** và **Cost Allocation Tags** để theo dõi chi phí chính xác.
- **AWS Control Tower** và **AWS Config** cho governance tự động.

---

## 💻 Thực hành & Ví dụ (Examples / Labs)

Kho code được đặt trong thư mục `Example/` bao gồm các kịch bản thực tế nhằm áp dụng sát kiến thức lý thuyết đã học:

1. **[Lab 1: AI Study Buddy](./Example/my-workspace/lab1-study/)**
   - Ứng dụng Python kết nối Amazon Bedrock hỗ trợ hỏi đáp kiến thức từ file local.

2. **[Lab 2: Certification Prep Agent](./Example/my-workspace/lab2-cert/)**
   - Nâng cấp ứng dụng dùng Bedrock Agents và framework Python để xây dựng Chatbot CLI ôn thi AWS chuyên nghiệp.

3. **[Lab 3: Kiro Project](./Example/my-workspace/lab3-kiro/)**
   - Ứng dụng Full-stack (React/Vite Frontend, Node.js Backend).
   - Chứa tài liệu thiết kế (spec documents) chi tiết cho việc phỏng vấn/huấn luyện (Interview Coach).

---

⚡ _Repository này được thiết kế và cập nhật liên tục song hành cùng quá trình học tập thực tế và chạy Lab trên AWS Cloud._
