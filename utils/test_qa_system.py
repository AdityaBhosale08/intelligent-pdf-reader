"""Test script for the full QA system."""
from utils.qa_system import answer_question_from_pdf

if __name__ == "__main__":
    pdf_path = "data/A_Brief_Introduction_To_AI.pdf"
    
    questions = [
        "What is AI?",
        "What are the types of AI?",
        "What is machine learning?"
    ]
    
    for question in questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")
        try:
            answer = answer_question_from_pdf(pdf_path, question)
            print(f"Answer: {answer}")
        except Exception as e:
            print(f"Error: {e}")
