# AWS Deep-Dive Learning Plan — Relationship & Layer-Based Approach

> Goal: Move away from rote memorization of AWS services and instead build a mental model based on **how services relate to each other**, **which layer they belong to**, and **what their scope/boundary is**.

---

## 1. Why Rote Memorization Fails

AWS has 200+ services. Memorizing feature lists per service creates isolated facts that:
- Don't transfer to real architecture decisions
- Are forgotten quickly (no structural "hooks" in memory)
- Don't help during debugging (e.g., "why can't my Lambda reach the DB?")

The fix: learn services as **nodes in a graph**, not entries in a glossary. For every service, always resolve **relationships** and **scope** before features.

---

## 2. The Layer Model

Instead of AWS's own service categories (too broad, too flat), organize services into layers that mirror the actual path of a request through a system:

| Layer | Purpose | Example Services |
|---|---|---|
| 0 — Identity & Governance | Who can do what, everywhere | IAM, Organizations, SCP, STS |
| 1 — Network Edge | Entry point from the internet | Route 53, CloudFront, WAF, Shield |
| 2 — Network Core | How traffic moves internally | VPC, Subnets, IGW/NAT, Security Groups, NACLs, Transit Gateway |
| 3 — Compute | Where logic runs | EC2, ECS, EKS, Lambda, Fargate |
| 4 — Storage | Where data at rest lives | S3, EBS, EFS, FSx |
| 5 — Database | Structured/queryable data | RDS, Aurora, DynamoDB, ElastiCache |
| 6 — Integration & Messaging | How components talk async | SQS, SNS, EventBridge, Step Functions, API Gateway |
| 7 — Observability | How you see what's happening | CloudWatch, CloudTrail, X-Ray |
| 8 — Delivery / DevOps | How you ship changes | CodePipeline, CodeBuild, CloudFormation, CDK |

**Rule:** Before studying a service's features, first place it in a layer. The layer tells you its likely dependencies (layers below) and consumers (layers above).

---

## 3. The 4-Question Framework (Apply to Every Service)

For each new service, answer these instead of memorizing a feature list:

1. **Scope** — Is it Global, Regional, or AZ-bound? (This determines HA/DR behavior.)
2. **Depends on** — What does it require to function? (e.g., an IAM role, a VPC, a KMS key)
3. **Depended on by** — What sits on top of it / calls it?
4. **Boundary** — What does it explicitly *not* do? (This prevents "feature confusion" between similar services.)

**Worked example — S3:**
- Scope: Regional (bucket names are globally unique, but the bucket itself lives in one region)
- Depends on: IAM (bucket policy), optionally KMS (encryption)
- Depended on by: CloudFront (as origin), Lambda (event trigger), Athena, Glacier (lifecycle rules)
- Boundary: No compute, no native query engine (needs Athena/S3 Select for that)

---

## 4. Learn Through Architecture Scenarios, Not Isolated Services

Pick 3–4 reference architectures and trace every service along the request path. This is what actually builds relationship-memory.

**Scenario A — 3-Tier Web App**
```
User → Route 53 → CloudFront → WAF → ALB → EC2 (Auto Scaling Group) / ECS
     → RDS (Multi-AZ)
     → S3 (static assets)
CloudWatch collects logs/metrics across every hop
IAM Roles attached at each compute layer control access downward
```

**Scenario B — Event-Driven / Serverless**
```
Client → API Gateway → Lambda → DynamoDB
                     → SQS (buffer) → Lambda (worker) → SNS (notify)
EventBridge orchestrates cross-service events
Step Functions coordinates multi-step workflows
```

**Scenario C — Static Site + CDN**
```
Route 53 → CloudFront → S3 (origin)
ACM provides TLS certificate to CloudFront
WAF attached to CloudFront for edge protection
```

**Scenario D — Private/Internal System**
```
VPC (private subnets) → EC2/ECS (no public IP)
NAT Gateway → outbound internet only
VPC Endpoints → private access to S3/DynamoDB without NAT
Security Groups (stateful, instance-level) vs NACLs (stateless, subnet-level)
```

For each scenario: draw it, label every arrow, and explicitly note which layer each service belongs to and why it appears where it does.

---

## 5. Suggested Study Order

Foundations first — most other services depend on these two:

1. **IAM + VPC** — the backbone; almost everything else depends on identity and network.
2. **EC2 + S3 + Security Groups/NACLs** — nail down network scope early (this is where most confusion starts).
3. **RDS vs DynamoDB** — understand relational vs NoSQL tradeoffs, Multi-AZ vs Read Replicas.
4. **Lambda + API Gateway + SQS/SNS** — enter the event-driven/serverless world.
5. **CloudFront + Route 53** — edge/global layer.
6. **CloudWatch + CloudTrail + advanced IAM policies** — observability and governance.
7. **ECS/EKS + Step Functions + CI/CD (CodePipeline/CDK)** — complex, composed architectures.

---

## 6. Weekly Study Loop (Repeatable Template)

For each week/topic:

1. **Pick one service** from the current stage in Section 5.
2. **Answer the 4 questions** (Section 3) for it.
3. **Place it on the layer diagram** (Section 2) and draw its in/out arrows.
4. **Fit it into at least one scenario** (Section 4) — where does it appear, and what breaks if it's removed?
5. **Hands-on**: configure it for real (console or IaC) and deliberately break something (e.g., wrong Security Group rule) to observe the failure mode — this cements scope understanding faster than reading docs.
6. **Write a 3-line summary** in your own notes: Layer / Scope / One relationship you didn't know before.

---

## 7. Practice Resources

- [roadmap.sh/aws](https://roadmap.sh/aws) — structured topic checklist
- [roadmap.sh/aws/projects](https://roadmap.sh/aws/projects) — hands-on projects to pair with each stage above
- Build each scenario in Section 4 yourself using either the AWS Console or IaC (CloudFormation/CDK/Terraform) to reinforce the relationships physically, not just visually

---

## 8. Quick Reference — Common Scope Confusions

| Comparison | Key Difference |
|---|---|
| Security Group vs NACL | SG = stateful, instance-level, allow-only. NACL = stateless, subnet-level, allow+deny |
| S3 vs EBS vs EFS | S3 = object store, regional, no attach. EBS = block store, AZ-bound, one instance. EFS = file store, regional, multi-instance |
| SQS vs SNS vs EventBridge | SQS = queue (pull, 1 consumer per message). SNS = pub/sub (push, fan-out). EventBridge = event bus with routing rules |
| RDS vs DynamoDB | RDS = relational, vertical scaling, Multi-AZ for HA. DynamoDB = NoSQL, horizontal scaling, built-in multi-region option (Global Tables) |
| IAM Role vs IAM Policy vs IAM User | Policy = permission document. Role = identity assumed temporarily (no long-term credentials). User = long-term identity with credentials |