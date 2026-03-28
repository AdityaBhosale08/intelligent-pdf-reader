"""
Unit tests for PDF utility functions.

This module tests:
1. Successful PDF text extraction
2. Handling of empty PDFs
3. Handling of wrong file types
4. Text cleaning functionality
"""

import pytest
import io
from unittest.mock import Mock, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pdf_utils import extract_text_from_pdf, clean_text


class TestCleanText:
    """Tests for the clean_text function"""
    
    def test_clean_text_multiple_spaces(self):
        """Test that multiple spaces are reduced to single space"""
        text = "This    has    multiple     spaces"
        result = clean_text(text)
        assert result == "This has multiple spaces"
    
    def test_clean_text_tabs(self):
        """Test that tabs are converted to spaces"""
        text = "Hello\t\tWorld"
        result = clean_text(text)
        assert result == "Hello World"
    
    def test_clean_text_control_characters(self):
        """Test that control characters are removed"""
        text = "Hello\x00\x01\x02World"
        result = clean_text(text)
        assert "Hello" in result
        assert "World" in result
        assert "\x00" not in result
        assert "\x01" not in result
    
    def test_clean_text_empty_string(self):
        """Test that empty string returns empty string"""
        result = clean_text("")
        assert result == ""
    
    def test_clean_text_whitespace_only(self):
        """Test that whitespace-only string returns empty string"""
        result = clean_text("   \t\n   ")
        assert result == ""


class TestExtractTextFromPdf:
    """Tests for the extract_text_from_pdf function"""
    
    def test_wrong_file_type(self):
        """Test that non-PDF files return appropriate error"""
        # Create a mock file object with .txt extension
        mock_file = Mock()
        mock_file.name = "document.txt"
        
        result = extract_text_from_pdf(mock_file, show_progress=False)
        
        assert result == "Error: Please upload a valid PDF file."
    
    def test_empty_pdf(self):
        """Test that empty PDFs return appropriate error"""
        # Create a mock PDF file with no pages
        mock_file = Mock()
        mock_file.name = "document.pdf"
        
        # Mock the PdfReader to return 0 pages
        with pytest.MonkeyPatch.context() as m:
            mock_reader = MagicMock()
            mock_reader.pages = []
            
            m.setattr("PyPDF2.PdfReader", lambda x: mock_reader)
            
            result = extract_text_from_pdf(mock_file, show_progress=False)
            
            assert result == "Error: PDF is empty."
    
    def test_successful_extraction(self):
        """Test successful text extraction from PDF"""
        # Create a mock PDF file with content
        mock_file = Mock()
        mock_file.name = "document.pdf"
        
        # Mock the PdfReader and page extraction
        with pytest.MonkeyPatch.context() as m:
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "This is sample PDF text content."
            
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page]
            
            m.setattr("PyPDF2.PdfReader", lambda x: mock_reader)
            
            result = extract_text_from_pdf(mock_file, show_progress=False)
            
            assert "sample PDF text content" in result
            assert not result.startswith("Error:")
    
    def test_pdf_with_no_readable_text(self):
        """Test PDF that has pages but no extractable text"""
        mock_file = Mock()
        mock_file.name = "document.pdf"
        
        with pytest.MonkeyPatch.context() as m:
            mock_page = MagicMock()
            mock_page.extract_text.return_value = ""
            
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page]
            
            m.setattr("PyPDF2.PdfReader", lambda x: mock_reader)
            
            result = extract_text_from_pdf(mock_file, show_progress=False)
            
            assert result == "Error: No readable text found in PDF."
    
    def test_multi_page_pdf(self):
        """Test extraction from multi-page PDF"""
        mock_file = Mock()
        mock_file.name = "document.pdf"
        
        with pytest.MonkeyPatch.context() as m:
            mock_page1 = MagicMock()
            mock_page1.extract_text.return_value = "Page 1 content."
            
            mock_page2 = MagicMock()
            mock_page2.extract_text.return_value = "Page 2 content."
            
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page1, mock_page2]
            
            m.setattr("PyPDF2.PdfReader", lambda x: mock_reader)
            
            result = extract_text_from_pdf(mock_file, show_progress=False)
            
            assert "Page 1 content" in result
            assert "Page 2 content" in result


class TestIntegration:
    """Integration tests using the actual sample PDF"""
    
    def test_real_pdf_extraction(self):
        """Test extraction from the actual sample PDF file"""
        from pathlib import Path
        
        pdf_path = Path("data/A_Brief_Introduction_To_AI.pdf")
        
        if not pdf_path.exists():
            pytest.skip("Sample PDF file not found")
        
        with open(pdf_path, "rb") as pdf_file:
            result = extract_text_from_pdf(pdf_file, show_progress=False)
        
        # Verify extraction was successful
        assert not result.startswith("Error:")
        assert len(result) > 0
        assert "Artificial Intelligence" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
