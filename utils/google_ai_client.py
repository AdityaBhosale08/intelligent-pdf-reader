from google import genai
import time
from .config import get_google_api_key

# Create the client instance
api_key = get_google_api_key()
client = None
if api_key:
    client = genai.Client(api_key=api_key)

# Model name
MODEL_NAME = 'gemini-2.5-flash-lite'

def get_answer(context, question):
    """Get AI answer based on document context."""
    prompt = f"""Based on this document, answer the question.

Document:
{context}

Question: {question}

Please provide a detailed answer based only on the document content above."""
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            'temperature': 0.3,
            'max_output_tokens': 1024,
        }
    )
    
    return response.text

def get_answer_with_retry(context, question, max_retries=3):
    """Get AI answer with retry logic."""
    for attempt in range(max_retries):
        try:
            return get_answer(context, question)
        except Exception as e:
            error_message = str(e).lower()
            # Check for rate limiting or resource exhausted errors
            if any(keyword in error_message for keyword in ['rate limit', 'resource exhausted', '429', 'quota']):
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise Exception("API rate limit exceeded. Please try again later.")
            else:
                raise Exception(f"API error: {str(e)}")

def safe_get_answer(context, question):
    """Get answer with full error handling."""
    if not get_google_api_key():
        return "Error: Google API key not configured. Please set GOOGLE_API_KEY in .env file."
    
    if not client:
        return "Error: Failed to initialize Google AI client. Check your API key."
    
    try:
        return get_answer_with_retry(context, question)
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg and "not found" in error_msg.lower():
            return (
                "Error: Model not found (404). This usually means:\n"
                "1. The Generative Language API is not enabled in your Google Cloud project\n"
                "2. Your API key doesn't have access to Gemini models\n"
                "3. Your Google Cloud project doesn't have billing enabled\n\n"
                "To fix this:\n"
                "1. Go to https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com\n"
                "2. Enable the Generative Language API\n"
                "3. Ensure your API key has the necessary permissions\n\n"
                f"Original error: {error_msg}"
            )
        return f"Error getting answer: {error_msg}"
