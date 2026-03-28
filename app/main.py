import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Intelligent PDF Reader",
    page_icon="📄",
    layout="wide"
)

# Main title
st.title("Intelligent PDF Reader")

# Header
st.header("AI-Powered PDF Question & Answer System")

# App description using markdown
st.markdown("""
Welcome to the **Intelligent PDF Reader**! 

You can upload any PDF document and ask questions, and we will provide answers based on the content of the document

### Features:
- 📄 **PDF Upload**: Upload any PDF document
- 🔍 **Smart Reading**: AI-powered text extraction and analysis  
- 💬 **Ask Questions**: Get instant answers about your PDF document
- 📚 **Understand Faster**: Compress complex information into easy-to-understand answers

---
*Upload a PDF file in the sidebar to get started!*
""")

# Create sidebar
with st.sidebar:
    st.sidebar.title("📚 Navigation")
    st.sidebar.markdown("---")
    
    # Sidebar sections
    st.sidebar.header("Upload PDF")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload your PDF document here"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("Settings")
    
    # Model selection
    model_option = st.sidebar.selectbox(
        "Select AI Model",
        ["gemini-2.0-flash", "gemini-pro", "gemini-ultra"],
        index=0,
        help="Choose the AI model for answering questions"
    )
    
    # Chunk size option
    chunk_size = st.sidebar.slider(
        "Text Chunk Size",
        min_value=500,
        max_value=5000,
        value=1000,
        step=100,
        help="Adjust the size of text chunks for processing"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Tip: Smaller chunk sizes are faster but may miss context. Larger chunks preserve more context but take longer to process.")