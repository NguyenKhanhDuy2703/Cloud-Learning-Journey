import streamlit as st
from bedrock_utils import BedrockClient, SimpleRAG
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="Study Buddy AI",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 Study Buddy AI")
    st.markdown("Analyze your study notes with AI - powered by RAG when you have multiple documents!")
    
    # Initialize clients
    if 'bedrock_client' not in st.session_state:
        st.session_state.bedrock_client = BedrockClient()
    
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = SimpleRAG(st.session_state.bedrock_client)
    
    # Initialize Knowledge Base session state
    if 'connected_kb' not in st.session_state:
        st.session_state.connected_kb = None
    if 'kb_name' not in st.session_state:
        st.session_state.kb_name = None
    
    # TODO: Excercise 1.2 - Students add system prompt
    system_prompt = "You are an experienced biology tutor specializing in helping college students master complex scientific concepts. When explaining topics, break them down into digestible steps, use relatable analogies, provide clear examples, and check for understanding. Your goal is to make difficult concepts accessible while maintaining scientific accuracy. Always encourage questions and adapt your explanations to the student's level of understanding."  # TODO: Write an appropriate system prompt for StudyBuddy AI
    
    # TODO: Excercise 1.1 - Students set default response style index (Brief, Detailed, or Comprehensive)
    response_style = "Detailed"  # TODO: What index should be default?
        
    # TODO: Excercise 1.2 - Students set temperature for analytical tasks
    temperature = 0.5  # TODO: What temperature is best for study analysis? (0.0-1.0)
    
    # TODO: Excercise 1.2 - Students set top_p for focused responses  
    top_p = 0.  # TODO: What top_p gives focused analytical responses? (0.0-1.0)
    
    # TODO: Excercise 3 - Students add their Knowledge Base ID from web scraping KB
    knowledge_base_id = "BZHFPFMANP"  # TODO: Add your web scraping Knowledge Base ID here
    
    # Create layout with empty right column (for compatibility)
    col1, col2 = st.columns([1, 0.001])  # Make col2 very narrow
    
    # MAIN CONTENT: Analysis Interface
    with col1:
        st.header("📊 Analysis")
        
        # Analysis tabs
        tab1, tab2, tab3 = st.tabs(["📄 Local Documents", "🧠 Knowledge Base", "🔍 Multi-Modal Query"])
        
        # Tab 1: Local Documents (Local Embeddings)
        with tab1:
            st.subheader("📄 Local Documents")
            
            # Initialize session state for uploaded documents
            if 'uploaded_documents' not in st.session_state:
                st.session_state.uploaded_documents = []
            if 'processed_files' not in st.session_state:
                st.session_state.processed_files = set()
            
            # Show uploaded documents
            if st.session_state.uploaded_documents:
                st.markdown("**📚 Uploaded Documents:**")
                for i, doc in enumerate(st.session_state.uploaded_documents):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        file_type_emoji = "📕" if doc['type'] == "application/pdf" else "📄"
                        word_count = len(doc['content'].split())
                        st.write(f"{file_type_emoji} **{doc['name']}** ({word_count} words)")
                    with col2:
                        if st.button("🗑️", key=f"delete_{i}", help="Delete document"):
                            # Remove from both lists
                            removed_doc = st.session_state.uploaded_documents.pop(i)
                            st.session_state.processed_files.discard(f"{removed_doc['name']}_{hash(removed_doc['content'])}")
                            st.rerun()
                
                st.divider()
            
            # File upload for documents
            uploaded_file = st.file_uploader(
                "Upload a study document:" if not st.session_state.uploaded_documents else "Upload additional document:",
                type=['txt', 'md', 'pdf'],
                help="Upload documents for analysis (text, markdown, or PDF)",
                key="doc_uploader"
            )
            
            if uploaded_file:
                # Read and process the uploaded file
                if uploaded_file.type == "application/pdf":
                    text_content = st.session_state.rag_system.doc_processor.extract_text_from_pdf(uploaded_file)
                else:
                    text_content = uploaded_file.read().decode('utf-8')
                
                if text_content:
                    # Create unique identifier for this file (name + content hash)
                    file_id = f"{uploaded_file.name}_{hash(text_content)}"
                    
                    # Check if this exact file (name + content) has been processed
                    if file_id not in st.session_state.processed_files:
                        st.session_state.uploaded_documents.append({
                            'name': uploaded_file.name,
                            'content': text_content,
                            'type': uploaded_file.type
                        })
                        st.session_state.processed_files.add(file_id)
                        st.success(f"✅ Document '{uploaded_file.name}' uploaded successfully!")
                        st.rerun()
                    # If same filename but different content, allow it with a note
                    elif any(doc['name'] == uploaded_file.name for doc in st.session_state.uploaded_documents):
                        existing_doc = next(doc for doc in st.session_state.uploaded_documents if doc['name'] == uploaded_file.name)
                        if hash(existing_doc['content']) != hash(text_content):
                            # Same name, different content - ask user what to do
                            st.warning(f"A file named '{uploaded_file.name}' already exists but with different content.")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Replace existing", key="replace_file"):
                                    # Remove old version
                                    old_file_id = f"{uploaded_file.name}_{hash(existing_doc['content'])}"
                                    st.session_state.processed_files.discard(old_file_id)
                                    st.session_state.uploaded_documents = [doc for doc in st.session_state.uploaded_documents if doc['name'] != uploaded_file.name]
                                    
                                    # Add new version
                                    st.session_state.uploaded_documents.append({
                                        'name': uploaded_file.name,
                                        'content': text_content,
                                        'type': uploaded_file.type
                                    })
                                    st.session_state.processed_files.add(file_id)
                                    st.success(f"✅ Replaced '{uploaded_file.name}' with new version!")
                                    st.rerun()
                            with col2:
                                if st.button("Keep both", key="keep_both"):
                                    # Add with modified name
                                    new_name = f"{uploaded_file.name.rsplit('.', 1)[0]}_v2.{uploaded_file.name.rsplit('.', 1)[1]}"
                                    st.session_state.uploaded_documents.append({
                                        'name': new_name,
                                        'content': text_content,
                                        'type': uploaded_file.type
                                    })
                                    new_file_id = f"{new_name}_{hash(text_content)}"
                                    st.session_state.processed_files.add(new_file_id)
                                    st.success(f"✅ Added as '{new_name}'!")
                                    st.rerun()
                        # Same name, same content - already processed
                        else:
                            pass  # Don't show warning for exact duplicates, just ignore silently
                else:
                    st.error("Could not extract text from the uploaded file. Please try a different file.")
            
            # Query interface (only show if documents are uploaded)
            if st.session_state.uploaded_documents:
                st.markdown("**💬 Query Your Documents**")
                user_query = st.text_area(
                    "Ask a question about your documents:",
                    height=100,
                    placeholder="What are the main concepts in my study materials?",
                    key="doc_query"
                )
                
                if st.button("Query Documents", type="primary", key="query_docs"):
                    if user_query:
                        # Combine all document content
                        all_content = "\n\n".join([
                            f"Document: {doc['name']}\nContent: {doc['content']}"
                            for doc in st.session_state.uploaded_documents
                        ])
                        
                        style_instruction = get_style_instruction(response_style)
                        prompt = f"{style_instruction} Based on the following study documents, please answer this question: {user_query}\n\nDocuments:\n{all_content}"
                        
                        with st.spinner("Analyzing documents..."):
                            response = st.session_state.bedrock_client.invoke_nova_pro(
                                prompt=prompt,
                                system_prompt=system_prompt,
                                max_tokens=1500,
                                temperature=temperature,
                                top_p=top_p
                            )
                            
                            if response:
                                st.subheader("📋 Response:")
                                st.write(response)
                            else:
                                st.error("No response received. Please try again.")
                    else:
                        st.warning("Please enter a question.")
        
        # Tab 2: Knowledge Base
        with tab2:
            st.subheader("🧠 Knowledge Base Query")
            
            # Show Knowledge Base status
            if knowledge_base_id != "___" and knowledge_base_id != "EXAMPLE123":
                st.success(f"✅ Connected to Knowledge Base: `{knowledge_base_id}`")
                st.caption("Web scraping Knowledge Base configured in code")
                
                # User prompt for knowledge base
                st.markdown("**💬 Ask Questions About Your Knowledge Base**")
                kb_query = st.text_area(
                    "Enter your question or prompt:",
                    height=100,
                    placeholder="What information is available in my Knowledge Base?",
                    key="kb_query"
                )
                
                if st.button("Query Knowledge Base", type="primary", key="query_kb"):
                    if kb_query:
                        with st.spinner("Querying Knowledge Base..."):
                            kb_response = st.session_state.bedrock_client.query_knowledge_base(
                                knowledge_base_id, 
                                kb_query
                            )
                        
                        if kb_response['response']:
                            st.subheader("🎯 Knowledge Base Response:")
                            st.write(kb_response['response'])
                            
                            # Show citations if available
                            if kb_response['citations']:
                                with st.expander("📋 Source Citations", expanded=False):
                                    for i, citation in enumerate(kb_response['citations']):
                                        st.write(f"**Citation {i+1}:**")
                                        
                                        # Extract citation details
                                        retrieved_refs = citation.get('retrievedReferences', [])
                                        for ref in retrieved_refs:
                                            location = ref.get('location', {})
                                            s3_location = location.get('s3Location', {})
                                            
                                            if s3_location:
                                                st.write(f"📄 Source: {s3_location.get('uri', 'Unknown')}")
                                            
                                            content = ref.get('content', {})
                                            text = content.get('text', '')
                                            if text:
                                                st.write(f"📝 Content: {text[:200]}...")
                                        
                                        st.divider()
                            else:
                                st.info("No source citations available for this response.")
                        else:
                            st.error("No response received from Knowledge Base.")
                    else:
                        st.warning("Please enter a question.")
            else:
                st.warning("🔗 Knowledge Base not configured")
                st.info("Enter your Knowledge Base ID in the code:")
                st.code('File: study_buddy.py\nLine: ~47\nknowledge_base_id = "your-kb-id-here"', language="text")
        
        # Tab 3: Multi-Modal Query (Both Documents and KB)
        with tab3:
            st.subheader("🔍 Multi-Modal Query")
            st.markdown("Query both your local documents and Knowledge Base simultaneously")
            
            # Check if both sources are available
            has_local_docs = len(st.session_state.rag_system.documents) > 0
            has_kb = knowledge_base_id != "___" and knowledge_base_id != "EXAMPLE123"
            
            # Check if both sources are available
            has_local_docs = len(st.session_state.uploaded_documents) > 0
            has_kb = knowledge_base_id != "___" and knowledge_base_id != "EXAMPLE123"
            
            if has_local_docs and has_kb:
                st.success(f"✅ Ready to query {len(st.session_state.uploaded_documents)} local documents + Knowledge Base")
                
                # User prompt for multi-modal query
                st.markdown("**💬 Ask Questions Across All Sources**")
                multi_query = st.text_area(
                    "Enter your question or prompt:",
                    height=100,
                    placeholder="Compare information from my documents with the Knowledge Base...",
                    key="multi_query"
                )
                
                if st.button("Query All Sources", type="primary", key="query_multi"):
                    if multi_query:
                        col_local, col_kb = st.columns([1, 1])
                        
                        # Query local documents
                        with col_local:
                            st.markdown("**📄 Local Documents Response:**")
                            
                            # Combine all document content for simple querying
                            all_content = "\n\n".join([
                                f"Document: {doc['name']}\nContent: {doc['content']}"
                                for doc in st.session_state.uploaded_documents
                            ])
                            
                            style_instruction = get_style_instruction(response_style)
                            prompt = f"{style_instruction} Based on the following documents, {multi_query}\n\nDocuments:\n{all_content}"
                            
                            with st.spinner("Analyzing local documents..."):
                                local_response = st.session_state.bedrock_client.invoke_nova_pro(
                                    prompt=prompt,
                                    system_prompt=system_prompt,
                                    max_tokens=1500,
                                    temperature=temperature,
                                    top_p=top_p
                                )
                            
                            if local_response:
                                st.write(local_response)
                            else:
                                st.error("No response from local documents")
                        
                        # Query Knowledge Base
                        with col_kb:
                            st.markdown("**🧠 Knowledge Base Response:**")
                            with st.spinner("Querying Knowledge Base..."):
                                kb_response = st.session_state.bedrock_client.query_knowledge_base(
                                    knowledge_base_id, 
                                    multi_query
                                )
                            
                            if kb_response['response']:
                                st.write(kb_response['response'])
                            else:
                                st.error("No response from Knowledge Base")
                    else:
                        st.warning("Please enter a question.")
            
            elif has_local_docs and not has_kb:
                st.warning("🔗 Knowledge Base not configured. Only local documents available.")
                st.info("Complete the Part 3 Knowledge Base TODO to enable multi-modal querying.")
            
            elif not has_local_docs and has_kb:
                st.warning("📚 No local documents uploaded. Only Knowledge Base available.")
                st.info("Upload documents in the Local Documents tab to enable multi-modal querying.")
            
            else:
                st.warning("⚠️ Neither local documents nor Knowledge Base are available.")
                st.info("Upload documents and configure Knowledge Base to use multi-modal querying.")
    # Empty right column
    with col2:
        pass

def get_style_instruction(response_style):
    """Get style instruction based on response style"""
    return {
        "Brief": "Keep your response concise and to the point.",
        "Detailed": "Provide a thorough but well-organized response.",
        "Comprehensive": "Give a complete, in-depth analysis with examples and context."
    }[response_style]

if __name__ == "__main__":
    main()
