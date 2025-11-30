# RAG — Overview

Last updated: 2025-11-30  
Tags: #rag #llm #retrieval

## TL;DR
- RAG = LLM + retrieval: use external documents to ground generation.
- Core knobs: chunking, embedding/retriever, reranking, prompting, and evaluation.
- Common failure modes: retrieval misses, hallucination despite evidence, outdated/low-quality sources.

## Prereqs
- Embeddings & vector search (rough idea)
- Basic prompting and LLM limitations (hallucination)

## Core
RAG pipeline (high level):
1) Ingest docs → chunk → embed → index  
2) Query → retrieve top-k chunks  
3) (Optional) rerank/filters  
4) Compose context → generate answer with citations

Key design choices:
- Chunking: size/overlap trade-off (recall vs noise)
- Retriever: BM25 vs dense vs hybrid
- Reranking: improves precision when top-k is noisy
- Context window budgeting: keep only what helps

## Pitfalls
- “Garbage in, garbage out”: poor docs / bad chunking dominates.
- Over-retrieval: too many chunks → model ignores evidence.
- Evaluation illusion: looks good on demos, fails on adversarial/long-tail queries.

## Checklist (Can I…)
- [ ] Explain why RAG reduces hallucination (but doesn’t eliminate it)
- [ ] Implement a minimal RAG loop end-to-end
- [ ] Design an evaluation set: answer accuracy + citation faithfulness

## References
- (add later) RAG survey / LangChain docs / LlamaIndex docs / relevant papers