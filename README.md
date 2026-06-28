---
title: RateMyCV
emoji: 💼
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.45.0
app_file: app.py
pinned: false
---

<div align="center">

# 💼 RateMyCV

### AI-powered resume analyser — built with RAG, LLMs, and a focus on real-world job matching.

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-1c3c3c?style=flat)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-ff4b4b?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-f55036?style=flat)](https://groq.com)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-MiniLM--L6-ffd21e?style=flat&logo=huggingface&logoColor=black)](https://huggingface.co)

![RateMyCV Demo]

</div>

---

## What is RateMyCV?

RateMyCV is a portfolio project that uses **Retrieval-Augmented Generation (RAG)** to analyse a candidate's resume against any job description. Upload your CV, paste a JD, and get four AI-powered outputs in seconds — all grounded in your actual experience, no hallucinations.

This project demonstrates a production-style RAG pipeline from document ingestion through to LLM-generated outputs and a deployed web UI.

---

## Features

| Feature | Description |
|---|---|
| 📊 **Match Score** | 0–100 score with strong and weak alignment breakdown |
| ✉️ **Cover Letter** | Tailored to the role, grounded in your actual CV — downloadable |
| 🔍 **Skill Gaps** | What's missing from your resume and three concrete actions to fix it |
| 🎯 **Interview Prep** | Likely interview questions with answer frameworks based on your experience |

---

## Architecture

```
Resume (PDF/DOCX)
       │
       ▼
┌─────────────────┐
│  Document       │  pdfplumber / python-docx
│  Parser         │
└────────┬────────┘
         │ raw text
         ▼
┌─────────────────┐
│  Preprocessor   │  unicodedata normalisation + regex cleaner
│  & Chunker      │  LangChain RecursiveCharacterTextSplitter
└────────┬────────┘
         │ chunks[]
         ▼
┌─────────────────┐
│  Embedder       │  HuggingFace all-MiniLM-L6-v2 (384-dim vectors)
└────────┬────────┘
         │ vectors
         ▼
┌─────────────────┐
│  FAISS Index    │  Local vector store — similarity search
└────────┬────────┘
         │ top-k relevant chunks
         ▼
┌─────────────────┐     ┌──────────────────────┐
│  Context        │────▶│  Job Description     │
│  Builder        │     │  (user input)        │
└────────┬────────┘     └──────────────────────┘
         │ resume context + JD
         ▼
┌─────────────────┐
│  Groq LLM       │  LLaMA 3.3 70B via Groq API
│  (4 prompts)    │  Match Score · Cover Letter · Gap Analysis · Interview Prep
└────────┬────────┘
         │ structured outputs
         ▼
┌─────────────────┐
│  Streamlit UI   │  Dark/light theme · History · Download
└─────────────────┘
```

---

## Project Structure

```
ratemycv/
├── app.py                        # Streamlit entry point
├── styles.py                     # All CSS — theme-aware
├── requirements.txt
├── .env                          # API keys (gitignored)
├── README.md
│
├── src/
│   ├── ingestion/
│   │   ├── resume_parser.py      # PDF + DOCX parsing
│   │   └── jd_loader.py
│   │
│   ├── preprocessing/
│   │   ├── chunker.py            # LangChain text splitter
│   │   └── cleaner.py            # Unicode normaliser + regex
│   │
│   ├── embeddings/
│   │   ├── embedder.py           # HuggingFace all-MiniLM-L6-v2
│   │   └── vector_store.py       # FAISS index builder + searcher
│   │
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── context_builder.py
│   │
│   └── llm/
│       ├── llm_client.py         # Groq LLM client (LangChain)
│       └── prompts/
│           ├── match_scorer.py
│           ├── cover_letter.py
│           ├── gap_analyser.py
│           └── interview_prep.py
│
└── tests/
    ├── test_parser.py
    └── test_pipeline.py
```

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Document parsing | `pdfplumber`, `python-docx` | Extract text from PDF and DOCX resumes |
| Text processing | `LangChain RecursiveCharacterTextSplitter` | Chunk resume into semantically meaningful pieces |
| Embeddings | `HuggingFace all-MiniLM-L6-v2` | Convert text chunks to 384-dim vectors |
| Vector store | `FAISS` | Store and search resume embeddings locally |
| Retrieval | `LangChain RetrievalQA` | Query FAISS with JD, return top-k resume chunks |
| LLM | `Groq (LLaMA 3.3 70B)` | Generate all four outputs via structured prompts |
| Orchestration | `LangChain` | Chain retrieval + generation pipeline |
| Frontend | `Streamlit` | Web UI with dark/light theme, tabs, history |
| Deployment | `Hugging Face Spaces` | Free hosted deployment with public URL |

---

## Getting Started

### Prerequisites
- Python 3.10+
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/CY3R3N/rate-my-cv.git
cd rate-my-cv

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Run

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## How It Works

1. **Upload** your resume as a PDF or DOCX file
2. **Paste** the full job description you're applying for
3. **Click** Analyse Application
4. The RAG pipeline parses → chunks → embeds → retrieves relevant resume sections → passes context to the LLM
5. Four structured outputs are generated and displayed in tabs
6. Cover letter is downloadable; all analyses are saved in session history

---

## What I Learned

- Building a full **RAG pipeline** from scratch — ingestion, chunking, embedding, retrieval, generation
- Prompt engineering for structured, grounded LLM outputs
- Integrating **LangChain**, **FAISS**, and **HuggingFace** in a production-style codebase
- Building and deploying a **Streamlit** web app with custom theming
- Working with the **Groq API** for fast LLM inference

---

## Roadmap

- [ ] Job board integration (Seek, LinkedIn scraper)
- [ ] Multi-resume comparison
- [ ] ATS keyword optimisation suggestions
- [ ] Export full analysis as PDF report
- [ ] User authentication + persistent history

---

## Author

**Ahnaf Ar Rasheed**
Master's in Applied Artificial Intelligence — Deakin University, Melbourne

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0a66c2?style=flat&logo=linkedin)](https://www.linkedin.com/in/cyeren24/)
[![GitHub](https://img.shields.io/badge/GitHub-CY3R3N-181717?style=flat&logo=github)](https://github.com/CY3R3N)

---

<div align="center">
  <sub>Built with LangChain · FAISS · HuggingFace · Groq · Streamlit</sub>
</div>
