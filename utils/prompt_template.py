import google.generativeai as genai
from utils.config import get_google_api_key

QA_SYSTEM_INSTRUCTION = """You are a helpful assistant that answers questions about documents. 
Provide clear, accurate answers based only on the document content provided.
If the answer is not in the document, say so politely."""

def create_qa_prompt(document_text, question):
    """Create a QA prompt for document-based questions."""
    return f"""Document content:
{document_text}

Question: {question}

Please provide a detailed answer based on the document above. If the information is not in the document, say so."""

def create_qa_model():
    """Create a Gemini model with system instruction."""
    api_key = get_google_api_key()
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not configured")
    
    genai.configure(api_key=api_key)
    
    return genai.GenerativeModel(
        'gemini-2.5-flash-lite',
        system_instruction=QA_SYSTEM_INSTRUCTION
    )
