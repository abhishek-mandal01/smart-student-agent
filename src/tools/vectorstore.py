# src/tools/vectorstore.py
import os
import faiss
import numpy as np
import pickle
from typing import List, Tuple

class FaissVectorStore:
    def __init__(self, dim: int = None, path: str = "./vector_db"):
        """
        If dim is None, index will be created lazily on first upsert using the
        dimensionality of the provided vectors.
        """
        self.dim = dim
        self.path = path
        os.makedirs(path, exist_ok=True)
        self.index_file = os.path.join(path, "faiss.index")
        self.meta_file = os.path.join(path, "meta.pkl")
        self.index = None
        self.metadata = []

        # load existing index/metadata if present
        if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.meta_file, "rb") as f:
                    self.metadata = pickle.load(f)
                self.dim = self.index.d  # set dim from loaded index
            except Exception as e:
                print("Warning: failed to load existing index:", e)
                self.index = None
                self.metadata = []

    def _create_index(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)

    def upsert(self, vectors: List[List[float]], metadatas: List[dict]):
        if not vectors:
            return
        arr = np.array(vectors).astype("float32")
        # create index if missing
        if self.index is None:
            dim = arr.shape[1]
            self._create_index(dim)

        # add vectors & metadata
        self.index.add(arr)
        self.metadata.extend(metadatas)
        # persist
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "wb") as f:
            pickle.dump(self.metadata, f)

    def query(self, vector: List[float], topk: int = 5) -> List[Tuple[dict, float]]:
        if self.index is None:
            return []
        v = np.array([vector]).astype("float32")
        distances, indices = self.index.search(v, topk)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                results.append((self.metadata[idx], float(dist)))
        return results
