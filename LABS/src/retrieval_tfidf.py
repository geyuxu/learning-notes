from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple
import math
import re
import numpy as np

_TOKEN_RE = re.compile(r"[a-z0-9]+")

def tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall(text.lower())

@dataclass(frozen=True)
class SearchResult:
    doc_id: str
    score: float
    text: str

class TfidfRetriever:
    def __init__(self, docs: List[Tuple[str, str]]):
        """
        docs: list of (doc_id, text)
        """
        self.doc_ids = [d[0] for d in docs]
        self.texts = [d[1] for d in docs]
        self.vocab: Dict[str, int] = {}
        self.idf: np.ndarray | None = None
        self.doc_vectors: np.ndarray | None = None
        self._build()

    def _build(self) -> None:
        tokenized = [tokenize(t) for t in self.texts]

        # vocab
        for toks in tokenized:
            for tok in toks:
                if tok not in self.vocab:
                    self.vocab[tok] = len(self.vocab)

        V = len(self.vocab)
        N = len(tokenized)
        df = np.zeros(V, dtype=float)

        # document frequency
        for toks in tokenized:
            seen = set(toks)
            for tok in seen:
                df[self.vocab[tok]] += 1.0

        # smooth idf
        self.idf = np.log((N + 1.0) / (df + 1.0)) + 1.0

        # doc tf-idf matrix
        X = np.zeros((N, V), dtype=float)
        for i, toks in enumerate(tokenized):
            if not toks:
                continue
            tf = {}
            for tok in toks:
                tf[tok] = tf.get(tok, 0) + 1
            for tok, c in tf.items():
                j = self.vocab[tok]
                X[i, j] = (c / len(toks)) * self.idf[j]

        # l2 normalize
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.doc_vectors = X / norms

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        assert self.idf is not None and self.doc_vectors is not None

        q_toks = tokenize(query)
        V = len(self.vocab)
        q = np.zeros(V, dtype=float)

        if q_toks:
            tf = {}
            for tok in q_toks:
                if tok in self.vocab:
                    tf[tok] = tf.get(tok, 0) + 1
            for tok, c in tf.items():
                j = self.vocab[tok]
                q[j] = (c / len(q_toks)) * self.idf[j]

        q_norm = np.linalg.norm(q)
        if q_norm == 0:
            return []

        q = q / q_norm
        scores = self.doc_vectors @ q  # cosine

        idx = np.argsort(-scores)[:top_k]
        results = []
        for i in idx:
            score = float(scores[i])
            if score <= 0:
                continue
            results.append(SearchResult(self.doc_ids[i], score, self.texts[i]))
        return results