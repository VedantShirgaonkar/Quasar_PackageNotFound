import torch
from sentence_transformers import SentenceTransformer, util

# Load the Sentence Transformer model for semantic sentence encoding
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_key_sentences(sentences, top_n=5):
    """
    Identifies the most important sentences from a given list.

    Args:
    - sentences (list of str): Input sentences.
    - top_n (int): Number of key sentences to extract.

    Returns:
    - list of str: Top-N most relevant sentences.
    """
    if not sentences:
        return []

    # Encode sentences into numerical embeddings
    embeddings = model.encode(sentences, convert_to_tensor=True)

    # Compute sentence centrality (importance) using cosine similarity
    scores = util.cos_sim(embeddings, embeddings).mean(dim=1)

    # Select indices of top-N most important sentences
    top_indices = scores.argsort(descending=True)[:top_n]

    return [sentences[i] for i in top_indices]