import sys
import os

# Get the absolute path of the project's root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sentence_transformers import SentenceTransformer, util
import torch

# Load the model (optimized for offline usage)
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_key_sentences(sentences, top_n=5):
    """Extracts the most important sentences using sentence embeddings."""
    # Convert sentences into vector embeddings
    embeddings = model.encode(sentences, convert_to_tensor=True)

    # Compute similarity scores (higher score = more important)
    scores = util.pytorch_cos_sim(embeddings, embeddings).mean(dim=1)

    # Sort sentences by importance and select the top N
    top_indices = scores.argsort(descending=True)[:top_n]
    return [sentences[i] for i in top_indices]

# Test the function
if __name__ == "__main__":
    from scripts.text_processing import process_input  # Import text processing module

    # Load and process input text
    sentences = process_input("data/Hack the Future.pdf")  # Change filename if needed

    # Extract key sentences
    key_sentences = extract_key_sentences(sentences)
    
    # Print key sentences
    print("\n🔹 Key Sentences Extracted:")
    for i, sent in enumerate(key_sentences, 1):
        print(f"{i}. {sent}")