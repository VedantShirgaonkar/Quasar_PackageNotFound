import sys
import os
import torch
from sentence_transformers import SentenceTransformer, util

# Ensure the script can access project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_key_sentences(sentences, top_n=5):
    """Extracts the most important sentences using embeddings and ranks them by importance."""
    if not sentences:
        return []
    
    num_sentences = len(sentences)
    if num_sentences <= top_n:
        return sentences  # Return all sentences if fewer than `top_n`

    # Convert sentences into vector embeddings
    embeddings = model.encode(sentences, convert_to_tensor=True)

    # Compute similarity scores (measuring how central each sentence is)
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)
    scores = similarity_matrix.mean(dim=1)  # Compute centrality of each sentence

    # Sort sentences by importance and select the top N
    top_indices = scores.argsort(descending=True)[:top_n]
    
    return [sentences[i] for i in top_indices]

# Test the function independently
if __name__ == "__main__":
    from scripts.text_processing import process_input  # Import text processing module

    test_file = "data/Hack the Future.pdf"  # Change to actual file path
    key_sentences = extract_key_sentences(process_input(test_file))

    print("\n🔹 Extracted Key Sentences:")
    for i, sent in enumerate(key_sentences, 1):
        print(f"{i}. {sent}")