# 💊 Medical Document Q&A Assistant (RAG Pipeline)

A privacy-first, locally hosted **Retrieval-Augmented Generation (RAG)** application designed to extract, process, and securely query complex medical PDF documents (such as drug prescribing information).

This project ensures strict data privacy by processing all documents locally and isolates user data via dynamic session tagging. It prevents AI hallucinations by grounding all answers strictly in the retrieved text and provides inline page citations for medical accuracy verification.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-1C3C3C)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-6E56CF)
![Ollama](https://img.shields.io/badge/LLM-Llama%203%20(Ollama)-000000)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **Layout-Aware Ingestion** — Parses multi-column medical PDFs without scrambling dosage tables or warnings.
- **Privacy-First Multi-Tenancy** — Dynamically assigns hidden IDs to user sessions so multiple users can upload personal documents simultaneously without cross-contamination.
- **Strictly Grounded Answers** — The LLM is forced to answer *only* using the provided documents. If the answer isn't in the PDF, the bot declines to answer.
- **Inline Citations** — Automatically attaches exact PDF page numbers to generated medical claims (e.g., *"...nausea and headache (Page 14)."*).
- **Conversational Memory** — Retains chat history within the session so users can ask natural follow-up questions.
- **Live Text Streaming** — Generates responses word-by-word (like ChatGPT) for a fast, responsive user experience.

---

## 🏗️ System Architecture

The system is broken into distinct microservices using the **Separation of Concerns** principle:

| Layer | File | Responsibility |
|---|---|---|
| **Frontend (UI)** | `app.py` | Streamlit interface that handles file uploads, renders the chat, and manages hidden cryptographic user/session IDs. |
| **Backend (API)** | `main.py` | FastAPI traffic controller that exposes network endpoints (`/upload` and `/chat`) and streams LLM responses back to the UI. |
| **Knowledge Base** | `database.py` | Handles the ingestion pipeline — chunks PDFs, converts text to vectors using a local HuggingFace embedding model (`BGE-small`), and stores them in **ChromaDB**. |
| **The Brain** | `pipeline.py` | Uses **LangChain** to orchestrate retrieval — fetches filtered context, manages chat memory, and passes the strict grounding prompt to **Llama 3** (running locally via Ollama). |

---

## 🚀 Getting Started

### Prerequisites

Because this project runs 100% locally to protect medical data, you'll need the following installed on your machine:

- **Python 3.12+**
- **[Ollama](https://ollama.com/)** — for running the local LLM
- **Llama 3 model** — download it by running:

  ```bash
  ollama run llama3.2
  ```

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/medical-rag-chatbot.git
   cd medical-rag-chatbot
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 How to Run the Application

You'll need two separate terminal windows to run the backend and frontend simultaneously.

**Terminal 1 — Start the FastAPI backend**

```bash
uvicorn main:app --reload
```

The backend is now listening at `http://127.0.0.1:8000`

**Terminal 2 — Start the Streamlit frontend**

```bash
streamlit run app.py
```

The chat interface will automatically open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
medical-chatbot-backend/
│
├── chroma_db/             # Local vector database (auto-generated)
│
├── main.py                # FastAPI server and route endpoints
├── pipeline.py             # LangChain conversational RAG logic
├── database.py             # PDF parsing, chunking, and embedding logic
├── app.py                  # Streamlit frontend user interface
│
├── requirements.txt        # Python dependencies
└── README.md                # Project documentation
```

---

## 🛠️ Tech Stack

- **UI Framework:** [Streamlit](https://streamlit.io/)
- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **LLM Orchestration:** [LangChain](https://www.langchain.com/)
- **Vector Database:** [ChromaDB](https://www.trychroma.com/)
- **Embeddings:** HuggingFace `bge-small-en-v1.5` (via `sentence-transformers`)
- **Local LLM Engine:** [Ollama](https://ollama.com/) (Llama 3)
- **PDF Extraction:** `pypdf`

---

## ⚠️ Disclaimer

This application is intended for informational and research purposes only. It does not provide medical advice, diagnosis, or treatment, and should not be used as a substitute for professional medical guidance. Always consult a qualified healthcare provider for medical decisions.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
