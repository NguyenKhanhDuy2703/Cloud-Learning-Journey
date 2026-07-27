# 🔐 IAM Role & EC2 Integration Deep Dive

> **Nguyên tắc vàng:** KHÔNG BAO GIỜ lưu AWS credentials (access key/secret) trên EC2.  
> Thay vào đó, dùng **IAM Role + Instance Profile** — credentials tự động, tự gia hạn.

---

## 1. Vấn đề & Giải pháp

### Vấn đề: Hardcoded Credentials

```bash
# ❌ TUYỆT ĐỐI KHÔNG LÀM NÀY
aws configure
# AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/...

# Hoặc hardcode trong app:
s3 = boto3.client('s3',
    aws_access_key_id='AKIAIOSFODNN7...',  # ❌
    aws_secret_access_key='wJalrX...'      # ❌
)
```

**Rủi ro:**
- Credentials lọt vào git history → bị lộ
- Không có expiration → tấn công lâu dài
- Không audit được: ai dùng credential này?
- Phải rotate thủ công ở mọi server

### Giải pháp: IAM Role + Instance Profile

```mermaid
flowchart TD
    EC2["EC2 Instance"] -->|"1. Request Credentials"| IMDS["IMDSv2 (169.254.169.254)"]
    IMDS -->|"2. Gọi STS để tạo"| STS["AWS Security Token Service (STS)"]
    STS -->|"3. Trả về Temp Credentials\n(AccessKeyId, SecretKey, SessionToken, Expiry 6h)"| EC2
    EC2 -->|"4. Sử dụng AssumeRole"| Role["IAM Role (gắn qua Instance Profile)"]
    Role -->|"5. Thừa hưởng quyền"| Policy["IAM Policy (e.g., S3 Read Only)"]
    Policy -->|"6. Truy cập an toàn"| AWSService["AWS Services (S3, DynamoDB, SSM...)"]

    style STS fill:#fff7e6,stroke:#ffa940,stroke-width:2px
    style EC2 fill:#e6f7ff,stroke:#1890ff,stroke-width:2px
    style Role fill:#f9f0ff,stroke:#722ed1,stroke-width:2px
```

---

## 2. IAM Role vs IAM User

| | IAM User | IAM Role |
|---|---|---|
| **Danh tính** | Người/application cụ thể | Tập quyền có thể assume |
| **Credential type** | Long-term (Access Key) | Short-term (STS token, 15min - 12h) |
| **MFA** | Có thể bật | Không (dùng ở assume role) |
| **Ai dùng được** | Chỉ chính User | Bất kỳ principal được phép trong Trust Policy |
| **Rotation** | Thủ công | Tự động |
| **Dùng cho EC2** | ❌ Không khuyến nghị | ✅ Best practice |

---

## 3. Instance Profile — Cơ chế gắn Role vào EC2

### 3.1 Khái niệm

```mermaid
flowchart LR
    Role["IAM Role"] -->|Chứa trong 1-to-1| Profile["Instance Profile (Wrapper Container)"]
    Profile -->|Gắn trực tiếp attach| EC2["EC2 Instance (Không cần Restart)"]

    style Role fill:#f9f0ff,stroke:#722ed1,stroke-width:2px
    style Profile fill:#fff7e6,stroke:#ffa940,stroke-width:2px
    style EC2 fill:#e6f7ff,stroke:#1890ff,stroke-width:2px
```

**Lưu ý quan trọng:**
- Khi tạo Role qua Console → Console **tự động** tạo Instance Profile cùng tên
- Khi tạo qua CLI/IaC → phải tạo Instance Profile riêng và attach Role vào đó

### 3.2 Tạo và Gắn qua CLI

```bash
# 1. Tạo IAM Role với Trust Policy cho EC2
aws iam create-role \
  --role-name EC2-S3ReadRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": { "Service": "ec2.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }]
  }'

# 2. Gắn Permission Policy vào Role
aws iam attach-role-policy \
  --role-name EC2-S3ReadRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# 3. Tạo Instance Profile
aws iam create-instance-profile \
  --instance-profile-name EC2-S3ReadProfile

# 4. Gắn Role vào Instance Profile
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2-S3ReadProfile \
  --role-name EC2-S3ReadRole

# 5. Gắn vào EC2 khi launch
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.micro \
  --iam-instance-profile Name=EC2-S3ReadProfile \
  ...

# 6. Hoặc gắn vào EC2 đang chạy (không cần restart!)
aws ec2 associate-iam-instance-profile \
  --instance-id i-1234567890abcdef0 \
  --iam-instance-profile Name=EC2-S3ReadProfile
```

### 3.3 Terraform Example

```hcl
# IAM Role
resource "aws_iam_role" "ec2_role" {
  name = "EC2-S3ReadRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# Gắn managed policy
resource "aws_iam_role_policy_attachment" "s3_read" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

# Instance Profile (Terraform tự tạo khi có role)
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "EC2-S3ReadProfile"
  role = aws_iam_role.ec2_role.name
}

# Gắn vào EC2
resource "aws_instance" "web" {
  ami                  = "ami-0abcdef1234567890"
  instance_type        = "t3.micro"
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
}
```

---

## 4. IMDSv2 — Cách EC2 đọc Credentials

### 4.1 Luồng lấy credentials

```mermaid
sequenceDiagram
    autonumber
    actor EC2 as EC2 Instance
    participant IMDS as IMDSv2<br/>(169.254.169.254)

    Note over EC2, IMDS: Step 1: Lấy Session Token (PUT Request)
    EC2->>+IMDS: PUT /latest/api/token (TTL: 21600s)
    IMDS-->>-EC2: Trả về TOKEN

    Note over EC2, IMDS: Step 2: Dùng Token để đọc credentials (GET Request)
    EC2->>+IMDS: GET /latest/meta-data/iam/security-credentials/EC2-S3ReadRole<br/>[Header: X-aws-ec2-metadata-token: TOKEN]
    IMDS-->>-EC2: Trả về Temp Credentials JSON
```

Ví dụ dữ liệu JSON trả về từ IMDSv2:
```json
{
  "Code": "Success",
  "LastUpdated": "2024-01-15T10:25:30Z",
  "Type": "AWS-HMAC",
  "AccessKeyId": "ASIAIOSFODNN7EXAMPLE",
  "SecretAccessKey": "wJalrXUtnFEMI/...",
  "Token": "AQoDYXdzEJr...",
  "Expiration": "2024-01-15T16:25:30Z"  // Tự động gia hạn trước khi hết hạn
}
```

**AWS SDK tự động làm toàn bộ quá trình này.** Bạn chỉ cần gắn Instance Profile.

### 4.2 IMDSv1 vs IMDSv2

| | IMDSv1 | IMDSv2 |
|---|---|---|
| **Authentication** | Không (ai cũng GET được) | Token-based (PUT first) |
| **SSRF vulnerable** | ✅ Có | ❌ Không (token required) |
| **Khuyến nghị** | ❌ Không dùng | ✅ Bắt buộc dùng |

```bash
# Enforce IMDSv2 khi launch (không cho dùng v1)
aws ec2 run-instances \
  --metadata-options HttpTokens=required,HttpEndpoint=enabled \
  ...

# Hoặc bật cho instance đang chạy
aws ec2 modify-instance-metadata-options \
  --instance-id i-1234567890abcdef0 \
  --http-tokens required
```

---

## 5. Trust Policy — Ai được AssumeRole?

Trust Policy quyết định **principal nào** được phép assume role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### 5.1 Các loại Principal

```json
// EC2 service
"Principal": { "Service": "ec2.amazonaws.com" }

// Lambda service
"Principal": { "Service": "lambda.amazonaws.com" }

// IAM User cụ thể (cross-account)
"Principal": { "AWS": "arn:aws:iam::123456789012:user/alice" }

// Toàn bộ account khác (cross-account role assumption)
"Principal": { "AWS": "arn:aws:iam::123456789012:root" }

// Role cụ thể (Federated/OIDC)
"Principal": {
  "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
}
```

---

## 6. Permission Policy — EC2 thường cần những gì?

### 6.1 Policy theo Principle of Least Privilege

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadFromSpecificS3Bucket",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-bucket",
        "arn:aws:s3:::my-app-bucket/*"
      ]
    },
    {
      "Sid": "WriteLogsToCloudWatch",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Sid": "ReadSSMParameters",
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParametersByPath"
      ],
      "Resource": "arn:aws:ssm:ap-southeast-1:*:parameter/myapp/*"
    }
  ]
}
```

### 6.2 Common Managed Policies cho EC2

| Policy | Dùng cho |
|---|---|
| `AmazonS3ReadOnlyAccess` | EC2 đọc từ S3 |
| `AmazonSSMManagedInstanceCore` | SSM Session Manager (không cần SSH key) |
| `CloudWatchAgentServerPolicy` | EC2 gửi metrics/logs lên CloudWatch |
| `AmazonDynamoDBReadOnlyAccess` | EC2 đọc DynamoDB |
| `SecretsManagerReadWrite` | EC2 đọc/ghi Secrets Manager |

---

## 7. IAM Role cho EC2 — Common Patterns

### 7.1 Pattern: Đọc Secrets từ Secrets Manager

```python
import boto3
import json

# Không cần credentials! SDK tự đọc từ Instance Profile
client = boto3.client('secretsmanager', region_name='ap-southeast-1')

response = client.get_secret_value(SecretId='myapp/database/password')
secret = json.loads(response['SecretString'])

db_password = secret['password']
```

**Role cần policy:**
```json
{
  "Effect": "Allow",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": "arn:aws:secretsmanager:ap-southeast-1:*:secret:myapp/*"
}
```

### 7.2 Pattern: EC2 đọc config từ SSM Parameter Store

```bash
# Trên EC2 (không cần credentials)
DB_HOST=$(aws ssm get-parameter \
  --name "/myapp/prod/db-host" \
  --with-decryption \
  --query "Parameter.Value" \
  --output text)

echo "Database host: $DB_HOST"
```

### 7.3 Pattern: SSM Session Manager (thay SSH)

```
Truyền thống (SSH):
  Máy tính → Port 22 → EC2
  Cần: Key pair, Security Group mở port 22, IP whitelist

SSM Session Manager:
  Máy tính → AWS API → SSM Agent (trên EC2) → Shell
  Cần: IAM permission, EC2 có AmazonSSMManagedInstanceCore policy
  Không cần: Key pair, port 22 mở, public IP!
  
  Audit: Mọi session được log vào CloudWatch / S3
```

**Role cần:**
```json
"arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
```

**Kết nối:**
```bash
aws ssm start-session --target i-1234567890abcdef0
```

---

## 8. Cross-Account Role Assumption

```mermaid
flowchart TD
    subgraph Account_A [Account A - Production]
        EC2["EC2 Instance with Role A\n(Trust: ec2.amazonaws.com)\n(Permission: sts:AssumeRole)"]
    end

    subgraph Account_B [Account B - Development]
        Role_B["Role B\n(Trust: Account A)\n(Permission: s3:GetObject)"]
        S3_B[("S3 Bucket (Restricted)\n(Bucket Policy: Allow Role B)")]
    end

    STS["AWS Security Token Service (STS)"]

    EC2 -->|"1. Gọi sts:AssumeRole (Role B)"| STS
    STS -->|"2. Trả về Temp Credentials của Role B"| EC2
    EC2 -->|"3. Dùng Temp Credentials truy cập"| S3_B
    Role_B -->|"Ủy quyền truy cập"| S3_B

    style EC2 fill:#e6f7ff,stroke:#1890ff,stroke-width:2px
    style Role_B fill:#f9f0ff,stroke:#722ed1,stroke-width:2px
    style S3_B fill:#fff7e6,stroke:#ffa940,stroke-width:2px
    style STS fill:#f5f5f5,stroke:#d9d9d9,stroke-width:2px
```

Flow:
1. EC2 (Account A) → STS AssumeRole(Role B in Account B)
2. STS trả về temp credentials của Role B
3. EC2 dùng credentials đó để truy cập S3 Account B

---

## 9. Security Best Practices Checklist

- [ ] **Không bao giờ** lưu credentials trong code, environment variables, hoặc file config trên EC2
- [ ] Luôn dùng **IAM Role + Instance Profile**
- [ ] Enforce **IMDSv2** (`HttpTokens=required`) trên tất cả EC2
- [ ] Áp dụng **Least Privilege**: chỉ grant quyền tối thiểu cần thiết
- [ ] Dùng **Resource ARN cụ thể** thay vì `*` trong policy
- [ ] Enable **CloudTrail** để audit tất cả API calls từ EC2
- [ ] Dùng **Conditions** trong policy (ví dụ: chỉ cho phép từ VPC endpoint)
- [ ] **Không dùng root account** cho bất kỳ tác vụ nào
- [ ] Dùng **SSM Session Manager** thay SSH (không cần mở port 22)
- [ ] Lưu secrets trong **Secrets Manager** hoặc **SSM Parameter Store** (SecureString), không trong User Data hoặc environment variables plaintext

---

## 10. Quick Reference

```
Token types:
  - AccessKey AKIA...: Long-term (IAM User)
  - AccessKey ASIA...: Short-term (STS/Role)

STS Token lifetime:
  - EC2 Instance Profile: Tự động renew, thường 6 giờ
  - Manual AssumeRole: 15 phút - 12 giờ (default 1 giờ)
  - Role chaining: Tối đa 1 giờ (không thể extend)

Instance Profile limits:
  - 1 Instance Profile per EC2
  - 1 Role per Instance Profile  
  - 10 Instance Profiles per Role (default)
```
