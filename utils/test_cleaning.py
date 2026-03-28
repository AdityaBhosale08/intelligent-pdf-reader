"""
Test script for text cleaning function
Demonstrates before/after comparison for text cleaning
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pdf_utils import clean_text, extract_text_from_pdf


def test_clean_text():
    """Test the clean_text function with various test cases"""
    
    print("=" * 60)
    print("TEXT CLEANING FUNCTION TESTS")
    print("=" * 60)
    
    # Test case 1: Multiple spaces
    test1 = "This    has    multiple     spaces"
    print("\n--- Test 1: Multiple spaces ---")
    print(f"BEFORE: '{test1}'")
    print(f"AFTER:  '{clean_text(test1)}'")
    
    # Test case 2: Multiple newlines
    test2 = "Line1\n\n\nLine2\n\n\nLine3"
    print("\n--- Test 2: Multiple newlines ---")
    print(f"BEFORE: '{test2}'")
    print(f"AFTER:  '{clean_text(test2)}'")
    
    # Test case 3: Special characters (control characters)
    test3 = "Hello\x00\x01\x02World\x07\x08\x09!"
    print("\n--- Test 3: Special/control characters ---")
    print(f"BEFORE (repr): {repr(test3)}")
    print(f"AFTER:  '{clean_text(test3)}'")
    
    # Test case 4: Mixed whitespace
    test4 = "  Hello   \n\n   World  \t\t  !  "
    print("\n--- Test 4: Mixed whitespace ---")
    print(f"BEFORE: '{test4}'")
    print(f"AFTER:  '{clean_text(test4)}'")
    
    # Test case 5: Tabs
    test5 = "Hello\t\tWorld"
    print("\n--- Test 5: Tabs ---")
    print(f"BEFORE: '{test5}'")
    print(f"AFTER:  '{clean_text(test5)}'")
    
    # Test case 6: Empty string
    test6 = ""
    print("\n--- Test 6: Empty string ---")
    print(f"BEFORE: '{test6}'")
    print(f"AFTER:  '{clean_text(test6)}'")
    
    print("\n" + "=" * 60)
    print("ALL TEXT CLEANING TESTS COMPLETED")
    print("=" * 60)


def test_pdf_extraction_with_cleaning():
    """Test PDF extraction with cleaning"""
    from pathlib import Path
    
    print("\n" + "=" * 60)
    print("PDF EXTRACTION WITH CLEANING TEST")
    print("=" * 60)
    
    pdf_path = Path("data/A_Brief_Introduction_To_AI.pdf")
    
    if not pdf_path.exists():
        print(f"ERROR: PDF file not found at {pdf_path}")
        return
    
    # Open and extract using the function
    with open(pdf_path, "rb") as pdf_file:
        # Extract first 500 chars to show before/after
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        raw_text = ""
        for page in pdf_reader.pages[:2]:  # First 2 pages
            page_text = page.extract_text()
            if page_text:
                raw_text += page_text + "\n"
        
        print(f"\n--- Sample of raw extracted text (first 500 chars) ---")
        print(raw_text[:500])
        print("...")
        
        cleaned = clean_text(raw_text)
        
        print(f"\n--- Sample of cleaned text (first 500 chars) ---")
        print(cleaned[:500])
        print("...")
        
        print(f"\n--- Statistics ---")
        print(f"Raw text length: {len(raw_text)} chars")
        print(f"Cleaned text length: {len(cleaned)} chars")
        print(f"Reduction: {len(raw_text) - len(cleaned)} chars ({((len(raw_text) - len(cleaned)) / len(raw_text) * 100):.1f}%)")
        
    print("\n" + "=" * 60)
    print("PDF EXTRACTION TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    test_clean_text()
    test_pdf_extraction_with_cleaning()
