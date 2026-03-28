import PyPDF2
import re


def clean_text(text):
    """
    Clean extracted text by removing extra whitespace and handling special characters.
    
    Steps:
    1. Remove extra whitespace (multiple spaces, newlines, tabs)
    2. Handle special characters (control characters, non-printable characters)
    
    Args:
        text: Raw text extracted from PDF
        
    Returns:
        Cleaned text string
    """
    if not text:
        return text
    
    # Step 1: Remove control characters and non-printable characters
    # Keep only printable ASCII characters and common Unicode characters
    # This removes \r, \n (we'll handle them separately), tabs, and other control chars
    cleaned = ''.join(char for char in text if char.isprintable() or char in '\n\r\t')
    
    # Step 2: Normalize line endings - replace \r\n and \r with \n
    cleaned = re.sub(r'\r\n?', '\n', cleaned)
    
    # Step 3: Clean up multiple newlines - replace with double newline for paragraph separation
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
    
    # Step 4: Replace multiple spaces/tabs with single space (preserve newlines)
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    
    # Step 5: Strip leading and trailing whitespace from each line
    lines = cleaned.split('\n')
    cleaned = '\n'.join(line.strip() for line in lines)
    
    # Step 6: Remove multiple consecutive newlines (more than 2)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    
    # Step 7: Strip overall leading and trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned


def extract_text_from_pdf(pdf_file, show_progress=True):
    """
    Extract text from a PDF file with optional progress indicator.
    
    Args:
        pdf_file: File object of the PDF
        show_progress: If True, print progress messages (default: True)
        
    Returns:
        Extracted and cleaned text string
    """
    try:
        # Check file type
        if not pdf_file.name.endswith(".pdf"):
            return "Error: Please upload a valid PDF file."

        # Try reading PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Check if PDF has pages
        total_pages = len(pdf_reader.pages)
        if total_pages == 0:
            return "Error: PDF is empty."

        if show_progress:
            print(f"PDF has {total_pages} page(s)")
            print("-" * 40)

        text = ""

        # Extract text from each page with progress indicator
        for page_num, page in enumerate(pdf_reader.pages, start=1):
            if show_progress:
                print(f"Processing page {page_num} of {total_pages}...")
            
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if show_progress:
            print("-" * 40)
            print("Cleaning extracted text...")
        
        # Clean the extracted text
        text = clean_text(text)
        
        # Check if text is extracted
        if not text.strip():
            return "Error: No readable text found in PDF."

        if show_progress:
            print(f"Extraction complete! Total characters: {len(text)}")

        return text

    except Exception as e:
        return f"Error: Unable to process PDF. {str(e)}"
