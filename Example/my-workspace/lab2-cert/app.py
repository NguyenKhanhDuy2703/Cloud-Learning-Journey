"""
AWS Cloud Practitioner Certification Prep Application
"""

import streamlit as st
import json
from dotenv import load_dotenv
from cert_prep_agent import create_agent, generate_question
from agentcore_study_guide import generate_study_guide_via_agentcore

load_dotenv()

st.set_page_config(
    page_title="AWS Cloud Practitioner Cert Prep",
    page_icon="📚",
    layout="wide"
)

def practice_questions_tab():
    """Practice Questions Tab Content"""
    st.header("🎯 Practice Questions")
    st.markdown("Practice with realistic AWS Cloud Practitioner exam questions!")

    # Session state for questions
    if "question" not in st.session_state:
        st.session_state.question = None

    if "user_answer" not in st.session_state:
        st.session_state.user_answer = None

    # Generate question
    if st.button("🎯 Generate New Question", type="primary"):
        with st.spinner("Generating question..."):
            try:
                raw_response = generate_question(st.session_state.agent)
                st.session_state.question = raw_response
                st.session_state.user_answer = None
                st.rerun()
            except Exception as e:
                st.error(f"Failed to generate question: {e}")

    # Display question
    if st.session_state.question:
        q = st.session_state.question

        st.markdown("---")
        st.markdown("### 📝 Question")
        st.markdown(f"**{q['question']}**")

        st.markdown("### 🔤 Choose your answer")

        options = q["options"]

        choice = st.radio(
            "Select one:",
            list(options.keys()),
            format_func=lambda k: f"{k}. {options[k]}"
        )

        if st.button("Submit Answer"):
            st.session_state.user_answer = choice

        if st.session_state.user_answer:
            correct = q["correct_answer"]

            st.markdown("---")
            if st.session_state.user_answer == correct:
                st.success(f"✅ Correct! ({correct})")
            else:
                st.error(
                    f"❌ Incorrect. You chose {st.session_state.user_answer}, "
                    f"correct answer is {correct}."
                )

            # Show explanation if available
            if 'explanation' in q:
                st.markdown("### 💡 Explanation")
                st.info(q["explanation"])

    else:
        st.markdown("""
        ---
        ### Welcome 👋
        Click **Generate New Question** to start practicing for the
        AWS Certified Cloud Practitioner exam.
        """)

def study_guide_tab():
    """Study Guide Tab Content - Uses AgentCore hosted agent"""
    st.header("📖 Study Guide Generator")
    st.markdown("Generate incredibly detailed study guides for AWS topics using our enhanced AI agent!")
    
    # Show AgentCore status
    st.info("🚀 **Powered by AgentCore** - Enhanced AI agent with real-time AWS documentation access")

    # Session state for study guides
    if "study_guide" not in st.session_state:
        st.session_state.study_guide = None

    # Topic input
    topic = st.text_input(
        "What AWS topic would you like to study?",
        placeholder="e.g., I want to learn more about S3 Glacier, Lambda functions, IAM roles",
        help="Enter any AWS service, concept, or feature you want to learn about"
    )

    # Generate study guide
    if st.button("📚 Generate Comprehensive Study Guide", type="primary"):
        with st.spinner(f"🤖 Generating incredibly detailed study guide for {topic}... This may take up to 2 minutes for comprehensive content."):
            try:
                # Call AgentCore hosted agent
                study_guide_content = generate_study_guide_via_agentcore(topic)
                st.session_state.study_guide = {
                    "topic": topic,
                    "content": study_guide_content
                }
                st.success("✅ Study guide generated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to generate study guide: {e}")
                st.info("💡 Make sure your AgentCore credentials are configured in the .env file")

    # Display study guide
    if st.session_state.study_guide:
        st.markdown("---")
        
        # Add download button for the study guide
        study_guide_text = f"# Study Guide: {st.session_state.study_guide['topic']}\n\n{st.session_state.study_guide['content']}"
        st.download_button(
            label="📥 Download Study Guide",
            data=study_guide_text,
            file_name=f"aws_study_guide_{st.session_state.study_guide['topic'].replace(' ', '_').lower()}.md",
            mime="text/markdown"
        )
        
        st.markdown(f"## 📖 Study Guide: {st.session_state.study_guide['topic']}")
        st.markdown(st.session_state.study_guide['content'])
    else:
        st.markdown("""
        ---
        ### How to use 💡
        
        **Our enhanced AgentCore agent creates incredibly detailed study guides with:**
        - 📋 Executive summaries and learning objectives
        - 🏗️ Detailed architecture and technical concepts
        - 💰 Comprehensive pricing analysis
        - 🎯 Real-world use cases and examples
        - 🔒 Security and compliance information
        - 📚 Exam-focused content for AWS Cloud Practitioner
        - 📖 Current AWS documentation links
        - 🎓 Best practices and common pitfalls
        
        **Example topics:**
        - **Services**: "Amazon S3", "AWS Lambda", "Amazon EC2"
        - **Concepts**: "IAM roles and policies", "VPC networking"
        - **Pricing**: "EC2 pricing models", "S3 storage classes"
        - **Security**: "AWS security best practices", "CloudTrail"
        
        Just type what you want to learn about and get a comprehensive guide!
        """)

def main():
    st.title("📚 AWS Cloud Practitioner Certification Prep")
    
    # Initialize local agent (only for practice questions)
    if "agent" not in st.session_state:
        with st.spinner("Initializing practice question agent..."):
            st.session_state.agent = create_agent()

    # Create tabs
    tab1, tab2 = st.tabs(["🎯 Practice Questions", "📖 Study Guides"])
    
    with tab1:
        practice_questions_tab()
    
    with tab2:
        study_guide_tab()

if __name__ == "__main__":
    main()
