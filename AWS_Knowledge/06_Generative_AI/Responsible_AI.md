#  Responsible Artificial Intelligence

Tài liệu này tóm lược Responsible AI trên AWS theo hướng thực hành: hiểu bản chất AI, nhận diện bias, và dùng các dịch vụ như SageMaker Clarify, Bedrock Guardrails, Model Cards và Model Monitor để xây dựng hệ thống AI minh bạch, an toàn, có thể kiểm soát.

---

## Key Concepts & Keywords

- **Foundation Models (FMs)**: Mô hình tiền huấn luyện quy mô lớn, là nền tảng của Generative AI.
- **Bias-Variance Trade-off**: Cân bằng giữa underfitting và overfitting.
- **Explainability**: Khả năng giải thích vì sao mô hình đưa ra một kết quả.
- **Amazon SageMaker Clarify**: Phát hiện bias và hỗ trợ giải thích mô hình.
- **Amazon Bedrock Guardrails**: Lớp kiểm soát an toàn cho AI tạo sinh.
- **Human-Centered Design (HCD)**: Thiết kế AI lấy con người làm trung tâm.

---

## Detailed Deep Dive

### 1. Traditional AI vs. Generative AI

Để xây dựng AI có trách nhiệm, trước hết cần hiểu cách chúng vận hành:

- **Traditional Machine Learning**
  - Dựa trên dữ liệu có cấu trúc do bạn cung cấp.
  - Thường được huấn luyện cho một tác vụ cụ thể như dự đoán giá nhà hoặc phân loại email rác.
  - Tìm kiếm các patterns trong dữ liệu quá khứ để dự đoán tương lai.
- **Generative AI**
  - Vận hành trên các Foundation Models lớn, được huấn luyện từ lượng dữ liệu khổng lồ.
  - Học mối quan hệ giữa các khái niệm để tạo ra nội dung mới như văn bản, ảnh hoặc code.
  - Phụ thuộc nhiều vào prompt của người dùng.

### 2. Bias-Variance Trade-off

Trách nhiệm của người xây dựng AI là tìm điểm cân bằng giữa hai loại sai số:

- **Bias**: Mô hình quá đơn giản, bỏ lỡ đặc trưng quan trọng của dữ liệu, dẫn đến underfitting.
- **Variance**: Mô hình quá nhạy với noise, học thuộc dữ liệu huấn luyện nhưng kém hiệu quả ở dữ liệu thực tế, dẫn đến overfitting.

| Kỹ thuật         | Mục tiêu xử lý                  | Cách thực hiện trên AWS              |
| ---------------- | ------------------------------- | ------------------------------------ |
| Cross Validation | Phát hiện overfitting           | Chia nhỏ tập dữ liệu trong SageMaker |
| Regularization   | Giảm độ phức tạp mô hình        | Điều chỉnh hyperparameters           |
| Increase Data    | Giúp mô hình học quy luật chung | Thu thập thêm dữ liệu vào Amazon S3  |
| Early Stopping   | Ngăn học thuộc nhiễu            | Sử dụng SageMaker Debugger           |

### 3. Hệ sinh thái dịch vụ AWS cho Responsible AI

#### A. Data Preparation

- **Amazon Macie**: Quét dữ liệu trên S3 để phát hiện và bảo vệ thông tin định danh cá nhân (PII).
- **Amazon SageMaker Ground Truth**: Kết hợp con người và AI để gắn nhãn dữ liệu khách quan hơn.

#### B. Training & Evaluation

- **Amazon SageMaker Clarify**: Phát hiện bias và cung cấp explainability cho mô hình.
- **Amazon SageMaker Model Cards**: Lưu tài liệu chuẩn hóa về mục đích, giới hạn và kết quả kiểm định của mô hình.

#### C. Inference & Monitoring

- **Amazon Bedrock Guardrails**: Chặn nội dung độc hại, chủ đề nhạy cảm và ẩn PII trong phản hồi theo thời gian thực.
- **Amazon SageMaker Model Monitor**: Theo dõi model drift và cảnh báo khi hiệu suất thực tế lệch khỏi lúc huấn luyện.

### 4. End-to-End Scenario

**Kịch bản: Xây dựng trợ lý AI cho ngân hàng số**

1. Dùng Amazon Macie để quét dữ liệu giao dịch cũ và loại bỏ thông tin cá nhân.
2. Dùng SageMaker Clarify để kiểm tra bias trong dữ liệu và mô hình.
3. Tạo Model Card để ghi rõ mục đích, phạm vi và giới hạn của mô hình.
4. Bật Bedrock Guardrails để kiểm soát nội dung phản hồi.
5. Dùng Model Monitor để phát hiện drift khi dữ liệu thực tế thay đổi.

---

## Practical Example

**Kịch bản: AI phê duyệt tín dụng ngân hàng**

1. Kỹ sư dùng Amazon Macie để loại bỏ số điện thoại và địa chỉ khỏi dữ liệu huấn luyện.
2. SageMaker Clarify phát hiện bias chống lại người trẻ tuổi, đội ngũ bổ sung thêm dữ liệu để cân bằng.
3. Khi AI từ chối cho vay, hệ thống trả về lý do rõ ràng thay vì phản hồi mơ hồ.
4. Bedrock Guardrails ngăn các yêu cầu tạo nội dung thiếu chuẩn mực hoặc gây hại.

---

## Exam Essentials & Tips

- **Low Bias + Low Variance** là trạng thái lý tưởng.
- Giảm bias bằng cách tăng độ phức tạp; giảm variance bằng cách tăng dữ liệu hoặc dùng regularization.
- Ưu tiên Amazon Macie để ẩn danh dữ liệu nhạy cảm trước khi huấn luyện.
- Dùng SHAP values trong SageMaker Clarify để tăng tính giải thích.
- Với AI tạo sinh, Guardrails là lớp kiểm soát an toàn quan trọng nhất.
- Model Cards giúp tăng tính minh bạch khi cần kiểm toán hoặc tuân thủ.

---
