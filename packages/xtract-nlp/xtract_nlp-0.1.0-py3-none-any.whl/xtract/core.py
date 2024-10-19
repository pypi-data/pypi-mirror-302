import torch
from xtract.embedding import EmbeddingModel
from xtract.codebase import CodebaseProcessor
from xtract.query import QueryProcessor
from typing import List

EMBEDDINGS_FILE = "code_embeddings.pt"


def process_codebase(codebase_path: str) -> int:
    """
    Process the codebase into chunks of code and save them.
    """
    processor = CodebaseProcessor(codebase_path)
    processor.load_codebase()
    code_chunks = processor.get_code_chunks()
    torch.save(code_chunks, "code_chunks.pt")
    return len(code_chunks)


def generate_embeddings(model_name: str = "microsoft/codebert-base") -> int:
    """
    Generate embeddings for the codebase and save them.
    """
    chunks = torch.load("code_chunks.pt")
    model = EmbeddingModel(model_name)
    embeddings = model.generate_embeddings(chunks)
    model.save_embeddings(embeddings, EMBEDDINGS_FILE)
    return len(embeddings)


def query_codebase(query: str, count: int = 5) -> List[str]:
    """
    Query the codebase and return the top 'count' most relevant code snippets.
    """
    # load precomputed embeddings and code chunks
    embedding_model = EmbeddingModel()
    embeddings = embedding_model.load_embeddings(EMBEDDINGS_FILE)
    chunks = torch.load("code_chunks.pt")
    # initialize the query processor
    processor = QueryProcessor(
        embedding_model, chunks, embeddings)
    results = processor.query(query, count)
    return results
