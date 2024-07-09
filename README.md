# ﻿Local Ollama RAG
Streamlit Chat Ui with local Ollama, which inculde:
- RAG with crawled data using LangChain, ChromaDB (prototype-Done, will refine when complete web-search)
- Web-search with query generation (currently using naive approach, I am considering about using LLMs but seem to make the flow using too much LLM calls)

# TODOs:
- Convert ``ChatOllama`` to another wrapper to adapt for remote ollama server
- Figure out how to keep context window in RAG flow as RAG prompt template kinda suck for context window optimization.
- Figure out how to add documents faster and retrieve better, as garbage information retrival rate is still very high
