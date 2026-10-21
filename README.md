# music-therapy-rag

A local RAG system for answering questions about a set of clinical studies on music therapy in the ICU. You ask a question, it finds the relevant passages across the papers, and a local LLM writes an answer that cites which study each claim came from.

Everything runs on your own machine with Ollama, so there's no API cost and the papers never leave your computer.

> The papers aren't included in this repo for copyright reasons. The scripts rebuild everything from your own copies.

## How it works

1. **Download** (`download_papers.py`): reads the PDF links from an Excel sheet with openpyxl and downloads them from Google Drive with gdown.
2. **Extract** (`extract.py`, `extract_pdf.py`): pulls text from each PDF with PyMuPDF, uses Tesseract OCR for scanned pages, and cleans up headers, page numbers, hyphenation, and the reference list.
3. **Chunk** (`chunk.py`, `chunk_papers.py`): splits each paper into overlapping chunks of about 1,200 characters and tags each one with its study's title and year.
4. **Embed** (`embedding.py`): turns each chunk into a vector with Qwen3-Embedding and stores them in a ChromaDB vector database.
5. **Ask** (`rag.py`): embeds your question, pulls the closest chunks from ChromaDB, and has Qwen3.5 9B answer from them with citations.

## Setup

```bash
brew install tesseract
ollama pull qwen3-embedding:0.6b
ollama pull qwen3.5:9b
pip install -r requirements.txt
```

## Usage

```bash
python download_papers.py "path/to/sheet.xlsx"
mkdir -p paper-text && python extract.py
python chunk.py
python embedding.py
python rag.py
```

You only need to run `embedding.py` again if you change how papers are extracted or chunked. Because the script uses `upsert`, rerunning is safe and will not create duplicates.

## Next steps

- Stop one paper from taking up most of the search results
- Build a test set of questions with known answers to measure accuracy
- Speed up response time
