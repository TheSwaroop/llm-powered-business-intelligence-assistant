# LLM-Powered Business Intelligence Assistant

A portfolio-ready Retrieval-Augmented Generation (RAG) demo with a polished Streamlit analytics dashboard that combines business documents, SQL records, vector similarity search, and a local LLM.

## Features

- **Document ingestion:** reads Markdown and TXT files, splits them into overlapping chunks.
- **Vector search:** creates semantic embeddings with Sentence Transformers and ranks chunks using cosine similarity.
- **SQL analytics:** stores sample sales records in SQLite and uses an LLM to plan read-only SQL queries.
- **Grounded responses:** supplies retrieved document passages and SQL results to the LLM, with instructions not to invent unsupported facts.
- **Streamlit interface:** ask questions, inspect retrieved passages, and review database records.
- **Local-first LLM:** uses Ollama, so no hosted API key is required.

## Architecture

```text
User question
    |
    +--> Document retrieval --> Sentence Transformer embeddings --> Top-k passages
    |
    +--> SQL planner (Ollama) --> Read-only SQLite query --> Business records
    |
    +--> RAG prompt (question + evidence)
                    |
                Ollama LLM
                    |
             Grounded answer
```

## Requirements

- Python 3.10+
- Ollama installed and running
- Internet connection for the first download of the embedding model and Python packages

## Setup (Windows / VS Code)

1. Extract the ZIP and open the project folder in VS Code.
2. Open the VS Code terminal.
3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Install Ollama from https://ollama.com and download the default model:

   ```powershell
   ollama pull llama3.2
   ```

6. Copy `.env.example` to `.env` if you want to customize settings.
7. Run the app:

   ```powershell
   streamlit run app.py
   ```

The browser should open the Streamlit app. On first launch, the app creates the SQLite database, downloads the embedding model, and builds the document index.

## Example questions

- Which region generated the highest revenue?
- Compare revenue by product.
- What happened during Q2 2026?
- Which customer segment is associated with laptop purchases?
- What is gross profit for each region? (Gross profit = revenue - cost.)

## Add your own data

- Add `.md` or `.txt` files to `documents/`.
- Replace or extend the seed rows in `src/database.py` to load your own authorized business records.
- Click **Rebuild document index** in the sidebar after changing documents.

Do not commit confidential company documents, customer data, credentials, `.env`, database files, or generated embedding indexes.

## Tests

```powershell
pytest
```

## GitHub

Create a new empty GitHub repository, then run:

```powershell
git init
git add .
git commit -m "Build RAG business intelligence assistant"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/llm-business-intelligence-assistant.git
git push -u origin main
```

## Current limitations and next improvements

This is a demonstration project using synthetic data. The SQL planner depends on the local Ollama model and should be reviewed before use with production data. For a production deployment, add stronger SQL parsing/allow-listing, authentication, role-based access, query timeouts, audit logs, evaluation datasets, and a managed vector database.
