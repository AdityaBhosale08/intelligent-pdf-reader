"""
Test script for progress indicator in PDF extraction
"""

from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pdf_utils import extract_text_from_pdf


def test_progress_indicator():
    """Test the progress indicator with PDF extraction"""
    
    pdf_path = Path("data/A_Brief_Introduction_To_AI.pdf")
    
    print("=" * 60)
    print("TESTING PROGRESS INDICATOR")
    print("=" * 60)
    
    if not pdf_path.exists():
        print(f"ERROR: PDF file not found at {pdf_path}")
        return
    
    print(f"\nExtracting text from: {pdf_path}")
    print()
    
    # Test WITH progress indicator
    print("--- WITH PROGRESS INDICATOR ---")
    with open(pdf_path, "rb") as pdf_file:
        text = extract_text_from_pdf(pdf_file, show_progress=True)
    
    print()
    print(f"Extracted text length: {len(text)} characters")
    print()
    
    # Show sample of extracted text
    print("--- SAMPLE OF EXTRACTED TEXT (first 300 chars) ---")
    print(text[:300])
    print("...")
    
    print()
    print("=" * 60)
    print("PROGRESS INDICATOR TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_progress_indicator()
