import torch
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from xtract.embedding import EmbeddingModel


class QueryProcessor:

    def __init__(self, model: EmbeddingModel, code_chunks: List[str], code_embeddings: torch.Tensor):
        """
        Initialize the QueryProcessor with the embedding model and precomputed code embeddings.
        """
        self.model = model
        self.code_chunks = code_chunks
        self.code_embeddings = code_embeddings

    def query(self, _input: str, count: int = 5):
        """
        Process a query and return the 'count' relevant code snippets.
        """
        # sorted by highest similarity
        query = self.model.generate_embeddings([_input])
        similarities = cosine_similarity(query, self.code_embeddings)
        indices = similarities.argsort()[0][-count:][::-1]
        snippets = [self.code_chunks[i] for i in indices]
        return snippets
