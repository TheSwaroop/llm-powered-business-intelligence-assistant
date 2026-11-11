from pathlib import Path
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import DOCS_DIR, INDEX_PATH, EMBEDDING_MODEL

def split_text(text, chunk_size=700, overlap=100):
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        chunk = " ".join(words[start:start + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        start += max(1, chunk_size - overlap)
    return chunks

class DocumentRetriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.chunks, self.vectors, self.sources = [], None, []

    def rebuild(self):
        self.chunks, self.sources = [], []
        for path in sorted(DOCS_DIR.glob("*.md")) + sorted(DOCS_DIR.glob("*.txt")):
            for chunk in split_text(path.read_text(encoding="utf-8")):
                self.chunks.append(chunk)
                self.sources.append(path.name)
        if self.chunks:
            self.vectors = self.model.encode(self.chunks, normalize_embeddings=True)
        else:
            self.vectors = np.empty((0, 384))
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        with INDEX_PATH.open("wb") as f:
            pickle.dump((self.chunks, self.sources, self.vectors), f)

    def load_or_build(self):
        if INDEX_PATH.exists():
            try:
                with INDEX_PATH.open("rb") as f:
                    self.chunks, self.sources, self.vectors = pickle.load(f)
                return
            except Exception:
                pass
        self.rebuild()

    def search(self, query, top_k=4):
        if self.vectors is None:
            self.load_or_build()
        if not self.chunks:
            return []
        q = self.model.encode([query], normalize_embeddings=True)[0]
        scores = np.asarray(self.vectors) @ q
        indexes = np.argsort(scores)[::-1][:top_k]
        return [{"text": self.chunks[i], "source": self.sources[i], "score": float(scores[i])} for i in indexes]
