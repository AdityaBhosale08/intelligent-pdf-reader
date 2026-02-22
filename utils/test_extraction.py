"""
Test script for multi-page PDF text extraction
"""

from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pdf_utils import extract_text_from_pdf


def main():
    # Path to sample PDF
    pdf_path = Path("data/A_Brief_Introduction_To_AI.pdf")

    print(f"Testing PDF extraction from: {pdf_path}")
    print("=" * 60)

    # Check if file exists
    if not pdf_path.exists():
        print(f"Error: PDF file not found at {pdf_path}")
        return

    print(f"File exists: {pdf_path.exists()}")
    print(f"File size: {pdf_path.stat().st_size} bytes")
    print("-" * 60)

    # Extract text using the utility function
    with open(pdf_path, "rb") as pdf_file:
        extracted_text = extract_text_from_pdf(pdf_file, show_progress=True)

    print("\n--- EXTRACTED TEXT ---\n")
    print(extracted_text)
    print("\n--- END OF EXTRACTED TEXT ---\n")

    # Validate success
    if extracted_text and not extracted_text.startswith("Error"):
        print("SUCCESS: Multi-page text extracted successfully!")
        print(f"Total characters extracted: {len(extracted_text)}")
        print(f"Total words extracted: {len(extracted_text.split())}")
    else:
        print("FAILED: Could not extract text")
        print(f"Error message: {extracted_text}")


if __name__ == "__main__":
    main()