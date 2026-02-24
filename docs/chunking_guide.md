# Text Chunking Guide for Document Q&A Project

## Overview

This document provides guidance on choosing optimal chunk sizes for AI document processing in our Q&A system.

## What is Text Chunking?

Text chunking is the process of splitting large documents into smaller, manageable pieces (chunks) that can be processed by AI models. This is essential because:

1. **Token Limits**: AI models have maximum token limits for input
2. **Retrieval Efficiency**: Smaller chunks allow more precise information retrieval
3. **Context Management**: Proper chunking preserves important context

## Chunk Size Comparison Results

We tested three chunk sizes on our sample document (A_Brief_Introduction_To_AI.pdf, 12,328 characters):

| Chunk Size | Number of Chunks | Avg Length | Min Length | Max Length |
|------------|------------------|------------|------------|------------|
| 500        | 31               | 494.5      | 328        | 500        |
| 1000       | 14               | 973.4      | 628        | 1000       |
| 2000       | 7                | 1846.9     | 928        | 2000       |

## Analysis by Chunk Size

### Chunk Size: 500 characters

**Pros:**
- More granular chunks - better for precise retrieval
- Lower token count per chunk - fits easily in context windows
- Better for finding specific facts or answers

**Cons:**
- May split important context across chunks
- More chunks to process - higher API costs
- Risk of losing semantic connections

**Best for:** Documents requiring very precise fact retrieval, short Q&A pairs

### Chunk Size: 1000 characters ✅ RECOMMENDED

**Pros:**
- Balanced chunk size for most AI models
- Good balance between context and granularity
- Fits well within typical token limits (512-1024 tokens)
- Industry standard for RAG applications

**Cons:**
- May still split some paragraphs
- Moderate number of API calls

**Best for:** General-purpose Document Q&A systems, RAG applications

### Chunk Size: 2000 characters

**Pros:**
- More context preserved per chunk
- Fewer API calls needed
- Better for understanding broader themes

**Cons:**
- May exceed some model token limits
- Less precise retrieval possible
- Higher per-chunk processing cost

**Best for:** Document summarization, theme analysis, broader context needs

## Recommendation for This Project

**Recommended Chunk Size: 1000 characters with 100 character overlap**

### Rationale:

1. **Balance**: Provides optimal balance between context preservation and retrieval precision
2. **Token Efficiency**: Fits well within typical AI model token limits (512-1024 tokens)
3. **Manageable Volume**: Produces reasonable number of chunks for processing
4. **Industry Standard**: Most RAG applications use similar chunk sizes

### Implementation:

```python
from utils.text_chunker import chunk_text

# Recommended configuration
chunks = chunk_text(
    text,
    chunk_size=1000,    # Optimal for Q&A
    chunk_overlap=100   # Prevents context loss at boundaries
)
```

## When to Adjust Chunk Size

### Use Smaller Chunks (500) When:
- Document contains many specific facts or data points
- Users ask very specific questions
- Precision is more important than context

### Use Larger Chunks (2000) When:
- Document has long, interconnected narratives
- Users ask broad, thematic questions
- Context is more important than precision

## Chunk Overlap Importance

Always use chunk overlap (100-200 characters) to:
- Prevent losing context at chunk boundaries
- Ensure important information isn't split awkwardly
- Improve retrieval quality

## Files Reference

- **Chunking Implementation**: [`utils/text_chunker.py`](../utils/text_chunker.py)
- **Test Script**: [`utils/test_chunking_sizes.py`](../utils/test_chunking_sizes.py)
- **Results File**: [`data/chunking_results.txt`](../data/chunking_results.txt)

## Conclusion

For this Document Q&A project, **chunk_size=1000 with chunk_overlap=100** provides the best balance for most use cases. This configuration ensures efficient processing while maintaining sufficient context for accurate question answering.
