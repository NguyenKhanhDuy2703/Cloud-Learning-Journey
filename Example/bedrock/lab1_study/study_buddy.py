import streamlit as st
import os
from dotenv import load_dotenv
# Import hàm từ file tiện ích đã tạo ở bước trước
from bedrock_utils import invoke_nova_model, get_embedding, retrieve_from_knowledge_base

load_dotenv()

st.set_page_config(page_title="StudyBuddy AI", page_icon="🎓")
st.title("🎓 StudyBuddy AI Assistant")

# --- CẤU HÌNH THÔNG SỐ (Exercise 1.2) ---
response_style = "Detailed" 
temperature = 0.1
top_p = 0.5

# --- GIAO DIỆN TABS (Exercise 2: Local RAG) ---
tab1, tab2 = st.tabs(["💬 Chat", "📁 Local Documents"])
knowledge_base_id = os.environ.get("KNOWLEDGE_BASE_ID", "BZHFPFMANP")

with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hỏi StudyBuddy về bài học của bạn..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Gọi hàm xử lý đã sửa cho Nova Pro
            response = invoke_nova_model(prompt, temperature, top_p, response_style)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.header("Tải tài liệu học tập")
    st.caption(f"Knowledge Base đang dùng: {knowledge_base_id}")
    kb_question = st.text_input("Hỏi Knowledge Base", placeholder="Nhập câu hỏi để tra cứu tài liệu...")
    if st.button("Tra cứu Knowledge Base") and kb_question.strip():
        answer, citations = retrieve_from_knowledge_base(kb_question.strip(), knowledge_base_id)
        st.markdown(answer)
        if citations:
            st.write(f"Đã tìm thấy {len(citations)} nguồn tham chiếu.")

    uploaded_file = st.file_uploader("Chọn file .txt", type=("txt"))
    
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.success("Đã tải tài liệu thành công!")
        
        # Thử nghiệm tạo Embedding (Exercise 2)
        if st.button("Phân tích tài liệu với Titan Embedding"):
            vector = get_embedding(content[:500]) # Thử nghiệm với 500 ký tự đầu
            if vector:
                st.info(f"Đã tạo Vector thành công! Độ dài vector: {len(vector)}")
                st.write("Sẵn sàng cho việc truy xuất thông tin (RAG).")