"""Test script for Google AI API integration."""
from utils.google_ai_client import safe_get_answer

if __name__ == "__main__":
    # Test 1: Simple math question
    print("Test 1: Simple math question")
    result = safe_get_answer("", "What is 2+2?")
    print(f"Answer: {result}")
    print()
    
    # Test 2: Error handling (no API key)
    print("Test 2: Error handling")
    result = safe_get_answer("", "What is Python?")
    print(f"Answer: {result}")
