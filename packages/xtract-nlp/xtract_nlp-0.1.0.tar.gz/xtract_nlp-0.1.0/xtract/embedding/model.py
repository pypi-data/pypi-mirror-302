import torch
from transformers import AutoTokenizer, AutoModel
from typing import List


class EmbeddingModel:

    def __init__(self, model_name: str = "microsoft/codebert-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()  # no training

    def generate_embeddings(self, code_chunks: List[str], batch_size: int = 8) -> torch.Tensor:
        embeddings = []
        for i in range(0, len(code_chunks), batch_size):
            batch = code_chunks[i:i+batch_size]
            inputs = self.tokenizer(
                batch, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
                # use mean pooling to reduce token embeddings to a single embedding per chunk
                batch_embeddings = outputs.last_hidden_state.mean(dim=1)
                embeddings.append(batch_embeddings)
        # concatenate batches into a single tensor
        return torch.cat(embeddings, dim=0)

    def save_embeddings(self, embeddings: torch.Tensor, file_path: str):
        torch.save(embeddings, file_path)

    def load_embeddings(self, file_path: str) -> torch.Tensor:
        return torch.load(file_path, weights_only=True)
