# 💾 EC2 Storage Ecosystem — EBS, EFS, FSx Deep Dive

> **Bộ ba storage** của EC2: **EBS** (block, 1-1), **EFS** (file, shared NFS), **FSx** (managed FS)  
> Hiểu sự khác biệt này là bắt buộc cho mọi thiết kế hạ tầng thực tế.

---

## 1. Tổng quan so sánh 3 loại Storage

```
┌─────────────────────────────────────────────────────────────────┐
│                    EC2 Storage Decision Tree                     │
│                                                                  │
│  Cần ổ đĩa gắn vào 1 EC2?                                       │
│  ├── YES → EBS (Elastic Block Store)                             │
│  │         gp3, io2, st1, sc1                                    │
│  │                                                               │
│  └── NO → Cần nhiều EC2 cùng đọc/ghi?                           │
│           ├── YES → File System dạng gì?                         │
│           │         ├── NFS (Linux) → EFS                        │
│           │         ├── SMB (Windows/AD) → FSx for Windows       │
│           │         └── High-perf HPC/ML → FSx for Lustre        │
│           │                                                       │
│           └── NO → Xem xét S3 (object storage)                   │
└─────────────────────────────────────────────────────────────────┘
```

| Tiêu chí | EBS | EFS | FSx |
|---|---|---|---|
| **Protocol** | Block (iSCSI-like) | NFS v4 | SMB / Lustre / NFS |
| **Scope** | AZ-level | Multi-AZ | Multi-AZ |
| **Gắn đồng thời** | 1 EC2* | Nhiều EC2 không giới hạn | Nhiều EC2/clients |
| **Tự co giãn** | Không (manual resize) | Có (tự động) | Không (cấp phát trước) |
| **OS** | Linux + Windows | Linux (NFS) | Windows / Linux |
| **Chi phí/GB** | ~$0.08-0.125 | ~$0.30 | ~$0.13-2.00 |
| **Backup** | Snapshot → S3 | AWS Backup | AWS Backup |

> *EBS Multi-Attach: io1/io2 có thể gắn vào tối đa 16 EC2 **cùng AZ**, dùng cho cluster DB (Ví dụ: Oracle RAC).

---

## 2. EBS — Elastic Block Store

### 2.1 Kiến trúc & Cơ chế hoạt động

```
EC2 Instance (AZ: ap-southeast-1a)
     │
     │ Kết nối qua mạng AWS nội bộ (low-latency)
     │
     ▼
┌─────────────────────────────┐
│        EBS Volume           │
│  ┌─────────────────────┐    │
│  │  Data Blocks        │    │  Replicated within AZ
│  │  (512B - 128KB/IO)  │    │  (tự động replicate nội bộ AZ)
│  └─────────────────────┘    │
└─────────────────────────────┘
     │ Snapshot (incremental)
     ▼
   Amazon S3 (cross-AZ durable storage)
```

**Key facts:**
- EBS volume và EC2 phải **cùng AZ** → muốn chuyển AZ phải snapshot → restore
- EBS **tồn tại độc lập** với EC2 (persist khi Stop, có thể detach và reattach)
- Root EBS mặc định `DeleteOnTermination=true` (có thể đổi lúc launch)

### 2.2 Volume Types — Chọn loại nào?

```
IOPS (I/O Operations Per Second)
     │
     ├── General Purpose SSD
     │   ├── gp3 ── 3,000 IOPS baseline, 125 MB/s throughput
     │   │          Tăng IOPS/throughput ĐỘC LẬP với dung lượng
     │   │          → CHỌN MẶC ĐỊNH (cost-efficient)
     │   │
     │   └── gp2 ── IOPS = 3 × GB (max 16,000)
     │              Throughput phụ thuộc dung lượng → legacy, không dùng nữa
     │
     ├── Provisioned IOPS SSD (Critical workload)
     │   ├── io2 ── Max 64,000 IOPS, 99.999% durability
     │   │          Multi-Attach support → Dùng cho: OLTP DB, Oracle, SAP
     │   │
     │   └── io1 ── Legacy của io2, tương tự nhưng 99.9% durability
     │
     ├── Throughput Optimized HDD (Sequential read/write lớn)
     │   └── st1 ── Max 500 MB/s throughput, 500 IOPS
     │              Dùng cho: Kafka, Hadoop, ETL pipelines, log processing
     │              KHÔNG dùng làm boot volume
     │
     └── Cold HDD (Archival, ít truy cập)
         └── sc1 ── Max 250 MB/s, rẻ nhất trong HDD
                    Dùng cho: backup cold data, ít access
                    KHÔNG dùng làm boot volume
```

### 2.3 EBS Snapshots

```
Snapshot Workflow:
─────────────────
Day 1: Full Snapshot (100 GB) ──────────────── 100 GB stored in S3
Day 2: Incremental (chỉ changed blocks) ─────── +10 GB stored
Day 3: Incremental ──────────────────────────── +5 GB stored

→ Restore từ Day 3: EBS reconstruct từ Day1 + Day2 + Day3
```

**Snapshot features:**
- **Fast Snapshot Restore (FSR):** Pre-warm snapshot → volume ready ngay khi tạo (tốn phí)
- **Cross-Region Copy:** Copy snapshot sang region khác để Disaster Recovery
- **Data Lifecycle Manager (DLM):** Tự động hóa create/retain/delete snapshots theo policy
- **EBS Recycle Bin:** Khôi phục snapshot đã xóa nhầm (retention 1 ngày - 1 năm)

### 2.4 Encryption

```
EBS Encryption (KMS):
  ├── Encrypt at rest (data trên ổ đĩa)
  ├── Encrypt in-transit (data giữa EC2 và EBS)
  └── Encrypt snapshots (snapshot của encrypted volume cũng tự động encrypted)

Cách bật:
  - Bật khi tạo volume (tick "Encrypted")
  - Account-level default: EC2 Console → "EBS Encryption" → Enable by default
  - Không thể encrypt volume đang tồn tại → snapshot → copy với encryption → restore
```

---

## 3. EFS — Elastic File System

### 3.1 Kiến trúc Multi-AZ

```
                    ┌─────────────────────────────────────────┐
                    │           Amazon EFS                    │
                    │  (File system, tự co giãn, pay-per-use) │
                    └────────┬──────────────┬─────────────────┘
                             │              │
              Mount Target   │              │  Mount Target
              (AZ 1a ENI)    │              │  (AZ 1b ENI)
                             │              │
           ┌─────────────────┘              └─────────────────┐
           ▼                                                   ▼
  ┌────────────────┐                               ┌────────────────┐
  │ EC2 Instances  │                               │ EC2 Instances  │
  │ (AZ 1a)        │ ◄──── Shared /mnt/efs ───► │ (AZ 1b)        │
  │ mount via NFS  │                               │ mount via NFS  │
  └────────────────┘                               └────────────────┘
```

### 3.2 Performance Modes

| Mode | Latency | Throughput | Dùng cho |
|---|---|---|---|
| **General Purpose** (default) | < 1ms | Burst | Web serving, CMS, home dir |
| **Max I/O** | Higher | Scale to hundreds of EC2 | Big Data, media processing |

### 3.3 Throughput Modes

| Mode | Cách tính throughput | Chi phí |
|---|---|---|
| **Bursting** (default) | Proportional to file system size | Rẻ khi FS nhỏ |
| **Elastic** | Scale tự động, pay per GB transferred | Tốt cho unpredictable workload |
| **Provisioned** | Cấp phát cố định (MB/s) | Khi biết trước throughput cần |

### 3.4 Storage Classes (Lifecycle)

```
EFS Lifecycle Management (giống S3 Intelligent-Tiering):

  Files accessed recently → EFS Standard  ($0.30/GB-month)
           │ Không access trong N ngày
           ▼
       EFS Standard-IA (Infrequent Access)  ($0.025/GB-month + retrieval fee)
           │ Access lại
           ▼
       Tự động move về Standard
```

### 3.5 Mount EC2 vào EFS

```bash
# Cài EFS mount helper
sudo yum install -y amazon-efs-utils

# Mount (dùng TLS encryption)
sudo mount -t efs -o tls fs-0123456789abcdef0:/ /mnt/efs

# Auto-mount khi reboot (thêm vào /etc/fstab)
fs-0123456789abcdef0:/ /mnt/efs efs defaults,_netdev,tls 0 0
```

---

## 4. FSx — Managed File Systems

### 4.1 FSx for Windows File Server

```
Use Case: Windows workloads cần SMB protocol + Active Directory integration

Architecture:
  Windows EC2 / On-premises Windows 
       │
       │ SMB protocol (port 445)
       ▼
  ┌──────────────────────────────┐
  │    FSx for Windows Server    │
  │  ├── Active Directory Auth   │
  │  ├── DFS Namespaces          │
  │  ├── Windows ACLs            │
  │  └── Shadow Copies (VSS)     │
  └──────────────────────────────┘
       │ Multi-AZ deployment
       └── Standby file server (automatic failover)
```

**Key specs:**
- Storage: SSD (32 GB - 65,536 GB) hoặc HDD
- Throughput: 8 MB/s đến 2,048 MB/s
- IOPS: Up to 350,000
- Tích hợp: AWS Managed Microsoft AD hoặc Self-managed AD

### 4.2 FSx for Lustre

```
Use Case: High-Performance Computing, ML Training, Financial Modeling

Architecture:
  S3 Bucket (data source)
       │ Lazy loading / pre-loading
       ▼
  ┌────────────────────────────┐
  │      FSx for Lustre        │
  │  POSIX-compliant parallel  │
  │  file system               │
  │  ├── Sub-millisecond lat.  │
  │  └── GB/s throughput       │
  └────────────────────────────┘
       │ POSIX / Lustre client
       ▼
  EC2 (GPU instances p3/p4/g5)
  SageMaker Training Jobs
```

**Key specs:**
- Throughput: 50/100/200 MB/s per TB
- IOPS: Millions
- Storage: SSD (persistent) hoặc HDD
- Deployment: Single-AZ hoặc Multi-AZ (Persistent tier)

**Tích hợp S3:**
```bash
# Lazy load: chỉ load file khi cần (mặc định)
# Pre-load toàn bộ data từ S3:
aws s3 cp s3://my-bucket/training-data/ /mnt/fsx/ --recursive

# Export kết quả về S3 sau khi xong
aws s3 sync /mnt/fsx/results/ s3://my-bucket/results/
```

### 4.3 FSx for NetApp ONTAP & OpenZFS

| | FSx for NetApp ONTAP | FSx for OpenZFS |
|---|---|---|
| Protocol | NFS, SMB, iSCSI | NFS |
| Clone | Instant (zero-copy) | Instant (zero-copy) |
| Dedup/Compression | Có | Có |
| Dùng cho | Enterprise multi-protocol | Linux apps cần ZFS features |

---

## 5. Storage Decision Matrix

| Scenario | Giải pháp |
|---|---|
| Database OS disk | EBS gp3 |
| High-IOPS OLTP Database (Oracle, MySQL) | EBS io2 |
| Log aggregation, Kafka | EBS st1 |
| Cold archive ít truy cập | EBS sc1 hoặc S3 Glacier |
| Shared web content (CMS, WordPress uploads) | EFS |
| Shared home directories cho nhiều EC2 Linux | EFS |
| Docker containers shared data | EFS |
| Windows file server on AWS | FSx for Windows |
| ML Training với dữ liệu từ S3 | FSx for Lustre |
| HPC workloads (CFD, genomics) | FSx for Lustre |
| Lift-and-shift NetApp storage | FSx for NetApp ONTAP |

---

## 6. Quick Reference

```
EBS Limits:
  Max volume size:    16 TB (gp3/io2), 64 TB (io2 Block Express)
  Max IOPS/volume:    16,000 (gp3), 256,000 (io2 Block Express)
  Max throughput:     1,000 MB/s (gp3), 4,000 MB/s (io2 BE)

EFS Limits:
  Max file system size: Petabyte scale
  Max throughput:       10+ GB/s
  Max IOPS:             Millions (Max I/O mode)

FSx for Lustre Limits:
  Max throughput:       100's GB/s
  Storage per FS:       Up to 100s PB
```
