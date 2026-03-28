"""
Test script for comparing different chunk sizes for AI document processing.

This script tests chunk_size values of 500, 1000, and 2000 to determine
the optimal chunk size for this document QA project.

Learning objective: Understand how different chunk sizes affect:
- Number of chunks produced
- Chunk content coherence
- Suitability for AI processing
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.text_chunker import chunk_text
from utils.pdf_utils import extract_text_from_pdf


def test_chunk_sizes(text, chunk_sizes=[500, 1000, 2000], chunk_overlap=100):
    """
    Test different chunk sizes and compare results.
    
    Args:
        text: The text to chunk
        chunk_sizes: List of chunk sizes to test
        chunk_overlap: Overlap between chunks (default: 100)
    
    Returns:
        Dictionary with results for each chunk size
    """
    results = {}
    
    print("=" * 60)
    print("CHUNK SIZE COMPARISON TEST")
    print("=" * 60)
    print(f"Total text length: {len(text)} characters")
    print(f"Chunk overlap: {chunk_overlap} characters")
    print("-" * 60)
    
    for size in chunk_sizes:
        chunks = chunk_text(text, chunk_size=size, chunk_overlap=chunk_overlap)
        
        # Calculate statistics
        avg_chunk_len = sum(len(chunk) for chunk in chunks) / len(chunks) if chunks else 0
        min_chunk_len = min(len(chunk) for chunk in chunks) if chunks else 0
        max_chunk_len = max(len(chunk) for chunk in chunks) if chunks else 0
        
        results[size] = {
            'num_chunks': len(chunks),
            'avg_chunk_length': avg_chunk_len,
            'min_chunk_length': min_chunk_len,
            'max_chunk_length': max_chunk_len,
            'chunks': chunks
        }
        
        print(f"\nChunk Size: {size}")
        print(f"  Number of chunks: {len(chunks)}")
        print(f"  Average chunk length: {avg_chunk_len:.1f} characters")
        print(f"  Min chunk length: {min_chunk_len} characters")
        print(f"  Max chunk length: {max_chunk_len} characters")
    
    return results


def display_sample_chunks(results, chunk_sizes=[500, 1000, 2000]):
    """
    Display sample chunks from each chunk size for comparison.
    
    Args:
        results: Results dictionary from test_chunk_sizes
        chunk_sizes: List of chunk sizes to display samples for
    """
    print("\n" + "=" * 60)
    print("SAMPLE CHUNKS (First chunk from each size)")
    print("=" * 60)
    
    for size in chunk_sizes:
        if size in results and results[size]['chunks']:
            print(f"\n--- Chunk Size {size} - First Chunk ---")
            chunk = results[size]['chunks'][0]
            # Display first 300 chars of chunk
            display_text = chunk[:300] + "..." if len(chunk) > 300 else chunk
            print(display_text)
            print(f"[Total length: {len(chunk)} characters]")


def analyze_results(results):
    """
    Analyze and provide recommendations based on chunk size results.
    
    Args:
        results: Results dictionary from test_chunk_sizes
    
    Returns:
        Dictionary with analysis and recommendation
    """
    print("\n" + "=" * 60)
    print("ANALYSIS AND RECOMMENDATIONS")
    print("=" * 60)
    
    analysis = {}
    
    for size, data in results.items():
        num_chunks = data['num_chunks']
        avg_len = data['avg_chunk_length']
        
        # Evaluate based on AI processing considerations
        pros = []
        cons = []
        
        if size <= 500:
            pros.append("More granular chunks - better for precise retrieval")
            pros.append("Lower token count per chunk - fits easily in context windows")
            cons.append("May split important context across chunks")
            cons.append("More chunks to process - higher API costs")
            recommendation = "Good for precise Q&A but may lose context"
        elif size <= 1000:
            pros.append("Balanced chunk size for most AI models")
            pros.append("Good balance between context and granularity")
            pros.append("Fits well within typical token limits (512-1024 tokens)")
            cons.append("May still split some paragraphs")
            recommendation = "RECOMMENDED - Best balance for most use cases"
        else:  # 2000+
            pros.append("More context preserved per chunk")
            pros.append("Fewer API calls needed")
            cons.append("May exceed some model token limits")
            cons.append("Less precise retrieval possible")
            cons.append("Higher per-chunk processing cost")
            recommendation = "Good for summarization, less ideal for precise Q&A"
        
        analysis[size] = {
            'pros': pros,
            'cons': cons,
            'recommendation': recommendation
        }
        
        print(f"\nChunk Size {size}:")
        print(f"  Pros: {', '.join(pros)}")
        print(f"  Cons: {', '.join(cons)}")
        print(f"  Recommendation: {recommendation}")
    
    return analysis


def main():
    """
    Main function to run chunk size tests on the sample PDF.
    """
    # Path to the sample PDF
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            'data', 'A_Brief_Introduction_To_AI.pdf')
    
    print("Loading PDF document...")
    print(f"PDF path: {pdf_path}")
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    # Extract text from PDF
    with open(pdf_path, 'rb') as pdf_file:
        text = extract_text_from_pdf(pdf_file, show_progress=False)
    
    # Check for extraction errors
    if text.startswith("Error:"):
        print(f"Error extracting text: {text}")
        return
    
    print(f"Extracted {len(text)} characters from PDF")
    print()
    
    # Test different chunk sizes
    chunk_sizes = [500, 1000, 2000]
    results = test_chunk_sizes(text, chunk_sizes=chunk_sizes)
    
    # Display sample chunks
    display_sample_chunks(results, chunk_sizes)
    
    # Analyze and provide recommendations
    analysis = analyze_results(results)
    
    # Final recommendation
    print("\n" + "=" * 60)
    print("FINAL RECOMMENDATION FOR THIS PROJECT")
    print("=" * 60)
    print("""
Based on the analysis:

For a Document Q&A system, chunk_size=1000 is RECOMMENDED because:
1. It provides a good balance between context preservation and retrieval precision
2. It fits well within typical AI model token limits (512-1024 tokens)
3. It produces a manageable number of chunks for processing
4. It's the industry standard for RAG (Retrieval Augmented Generation) applications

However, consider these adjustments:
- Use chunk_size=500 for documents requiring very precise retrieval
- Use chunk_size=2000 for documents where broader context is more important
- Always use chunk_overlap (100-200 chars) to prevent losing context at boundaries
""")
    
    # Save results to a file for documentation
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               'data', 'chunking_results.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("CHUNK SIZE COMPARISON RESULTS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Document: A_Brief_Introduction_To_AI.pdf\n")
        f.write(f"Total characters: {len(text)}\n\n")
        
        for size in chunk_sizes:
            data = results[size]
            f.write(f"Chunk Size: {size}\n")
            f.write(f"  Number of chunks: {data['num_chunks']}\n")
            f.write(f"  Average chunk length: {data['avg_chunk_length']:.1f}\n")
            f.write(f"  Min chunk length: {data['min_chunk_length']}\n")
            f.write(f"  Max chunk length: {data['max_chunk_length']}\n")
            f.write(f"  Recommendation: {analysis[size]['recommendation']}\n\n")
    
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
