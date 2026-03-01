from utils.pdf_utils import extract_text_from_pdf
from utils.text_chunker import chunk_text
from utils.prompt_template import create_qa_model, create_qa_prompt

def answer_question_from_pdf(pdf_path, question, max_chunks=3):
    """Answer a question based on PDF content."""
    # Extract text
    with open(pdf_path, 'rb') as pdf_file:
        text = extract_text_from_pdf(pdf_file)
    
    # Chunk if needed
    chunks = chunk_text(text, chunk_size=3000, chunk_overlap=200)
    
    # Use relevant chunks (for now, use first few)
    context = "\n\n".join(chunks[:max_chunks])
    
    # Create prompt and get answer
    model = create_qa_model()
    prompt = create_qa_prompt(context, question)
    
    response = model.generate_content(prompt)
    return response.text
