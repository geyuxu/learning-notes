from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Chunk:
    text: str
    start: int
    end: int

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> List[Chunk]:
    """
    Simple character-based chunker.
    chunk_size: number of characters per chunk
    overlap: overlap characters between adjacent chunks
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be in [0, chunk_size)")

    chunks: List[Chunk] = []
    step = chunk_size - overlap
    n = len(text)

    for start in range(0, n, step):
        end = min(start + chunk_size, n)
        piece = text[start:end].strip()
        if piece:
            chunks.append(Chunk(text=piece, start=start, end=end))
        if end == n:
            break
    return chunks