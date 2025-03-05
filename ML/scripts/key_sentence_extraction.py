import sys
import os
import torch
from sentence_transformers import SentenceTransformer, util

# Ensure the script can access the project directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_key_sentences(sentences, top_n=5):
    """Ranks sentences by importance and returns the most relevant ones."""
    if not sentences:
        return []
    
    embeddings = model.encode(sentences, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(embeddings, embeddings).mean(dim=1)  # Compute centrality

    top_indices = scores.argsort(descending=True)[:top_n]
    return [sentences[i] for i in top_indices]