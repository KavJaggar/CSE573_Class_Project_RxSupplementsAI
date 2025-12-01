**CSE 573 Final Project - Group 21**

An intelligent AI-powered medical assistant that answers questions about supplements, herbal medicines, and natural products using Retrieval-Augmented Generation (RAG) technology.

![Demo](https://img.shields.io/badge/Status-Active-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![React](https://img.shields.io/badge/React-19.x-61DAFB) ![License](https://img.shields.io/badge/License-Academic-yellow)

---

## 📖 Overview

RxSupplementsAI is a RAG-based question-answering system designed to provide accurate, evidence-based information about dietary supplements, herbal medicines, and natural products. The system combines semantic search with large language models to deliver contextually relevant answers while citing authoritative sources.

### Key Features

- 🔍 **Hybrid Retrieval System** - Vector similarity search (FAISS) with BM25 fallback
- 🧠 **LLM-Powered Responses** - Mistral model via Ollama for natural language generation
- 📚 **Large Knowledge Base** - 30,566+ documents from authoritative sources
- 💬 **Interactive Chat Interface** - Modern React-based web application
- 📊 **Source Citations** - All answers include citations to original sources

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         React Frontend                               │
│                    (Chat Interface)                                  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTP/REST
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Flask Backend                                   │
│                                                                      │
│  ┌────────────────┐    ┌─────────────────┐    ┌──────────────────┐  │
│  │ Query Handler  │───▶│ Retrieval Engine│───▶│ Response Builder │  │
│  └────────────────┘    └─────────────────┘    └──────────────────┘  │
│           │                     │                      │             │
│           │            ┌────────┴────────┐             │             │
│           │            ▼                 ▼             │             │
│           │    ┌─────────────┐   ┌─────────────┐       │             │
│           │    │    FAISS    │   │    BM25     │       │             │
│           │    │   (Vector)  │   │  (Keyword)  │       │             │
│           │    └─────────────┘   └─────────────┘       │             │
└───────────┼─────────────────────────────────────────────┼─────────────┘
            │                                             │
            ▼                                             ▼
┌─────────────────────┐                    ┌────────────────────────┐
│  Corpus Data        │                    │  Ollama (Mistral LLM)  │
│  • FAISS Index      │                    │                        │
│  • Document Store   │                    └────────────────────────┘
│  • BM25 Index       │
└─────────────────────┘
```

---

## 📂 Project Structure

```
CSE573_Class_Project_RxSupplementsAI/
│
├── 📁 CorpusData/                    # Processed corpus and indices
│   ├── bm25_index.pkl               # BM25 retrieval index
│   ├── natmed_data.faiss            # FAISS vector index
│   └── natmed_documents.json        # Document store with metadata
│
├── 📁 Evaluation/                    # Evaluation data and results
│   ├── evaluationquestions.txt      # 50 test questions
│   ├── BM25RetrievalTest.json       # BM25 retrieval results
│   ├── RAGVectorRetrievalTest.json  # Vector retrieval results
│   └── TestResponses*.json          # LLM response evaluations
│
├── 📁 KnowledgeGraphData/            # Knowledge graph triples
│   └── KGRelationshipsA.json        # Extracted S-P-O relationships
│
├── 📁 NatMedData/                    # Raw scraped NatMed data
│   └── natmed_data[1-27].json       # Supplement monographs (A-Z)
│
├── 📁 NatMedOtherNames/              # Alternative supplement names
│   └── natmed_other_names[1-7].json
│
├── 📁 RedditData/                    # Community discussion data
│   └── reddit_supplements_data.json
│
├── 📁 Scripts/                       # Backend and utility scripts
│   ├── query_phi.py                 # Main RAG query API (Flask)
│   ├── natmedcorpus.py             # Corpus building & FAISS indexing
│   ├── BM25_corpus.py              # BM25 index generation
│   ├── web_scraper.py              # NatMed web scraper (Selenium)
│   ├── reddit_data.py              # Reddit data collection tool
│   ├── KG_relationship_generation.py # Knowledge graph extraction
│   ├── test_responses.py           # Response evaluation script
│   ├── test_RAG_retrieval.py       # Vector retrieval testing
│   └── test_BM25_retrieval.py      # BM25 retrieval testing
│
└── 📁 WebApp/my-react-app/          # Frontend application
    ├── src/
    │   ├── Chat.jsx                 # Main chat component
    │   ├── App.jsx                  # App entry point
    │   └── App.css                  # Styling
    ├── package.json
    └── vite.config.js
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core backend language |
| **Flask** | REST API server |
| **Sentence-Transformers** | Text embeddings (`all-MiniLM-L6-v2`) |
| **FAISS** | Vector similarity search |
| **rank-bm25** | BM25 keyword retrieval |
| **Ollama** | Local LLM inference (Mistral) |
| **Selenium** | Web scraping |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI framework |
| **Vite** | Build tool and dev server |
| **CSS3** | Custom styling with CSS variables |

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 18+ and npm
- [Ollama](https://ollama.ai/) installed with Mistral model

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/CSE573_Class_Project_RxSupplementsAI.git
cd CSE573_Class_Project_RxSupplementsAI
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install flask flask-cors sentence-transformers faiss-cpu rank-bm25 requests numpy

# Ensure Ollama is running with Mistral
ollama pull mistral
ollama serve
```

### 3. Frontend Setup

```bash
cd WebApp/my-react-app
npm install
```

### 4. Build Corpus (if starting fresh)

```bash
cd Scripts

# Generate FAISS vector index
python natmedcorpus.py

# Generate BM25 index
python BM25_corpus.py
```

---

## 🎮 Usage

### Starting the Application

**1. Start Ollama (if not running):**
```bash
ollama serve
```

**2. Start the Backend API:**
```bash
cd Scripts
python query_phi.py
# Server runs on http://localhost:8181
```

**3. Start the Frontend:**
```bash
cd WebApp/my-react-app
npm run dev
# App runs on http://localhost:5173
```

**4. Open your browser and navigate to `http://localhost:5173`**

### Example Queries

- *"What are the benefits of taking L-Theanine?"*
- *"Is it safe to take vitamin D during pregnancy?"*
- *"What supplements can help with anxiety?"*
- *"How does turmeric interact with blood thinners?"*

---

## 📊 Data Sources

| Source | Description | Documents |
|--------|-------------|-----------|
| **Natural Medicines NatMedPro Database** | Professional monographs on supplements, herbs, and natural products |
| **Reddit r/supplements** | Community discussions and experiences |
| **Total Corpus** | Combined indexed documents | **30,566** |

---

## 🧪 Evaluation

The system was evaluated using 50 curated test questions covering:
- Supplement benefits and uses
- Safety and side effects
- Drug interactions
- Dosage recommendations
- Special populations (pregnancy, children)
- Off-topic queries (to test refusal to answer)

### Retrieval Comparison

| Method | Pros | Cons |
|--------|------|------|
| **FAISS (Vector)** | Semantic understanding, handles paraphrasing | May retrieve tangentially related content |
| **BM25 (Keyword)** | Exact term matching | Struggles with synonyms and context |

---

## 👥 Team - Group 21

- Kavinkumaar Jaganathan
- Gourav Bhimavarapu
- Niranth Reddy Kakulavaram
- Peshal Srinivas Kanamaluru
- Sai Roshan Rao Nelavalli
- Gunakarthik Naidu Lanka

---

## ⚠️ Disclaimer

This tool is intended for **educational and informational purposes only**. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider before starting any new supplement regimen.

---

## 📝 License

This project was developed for CSE 573 at Arizona State University. All rights reserved.

---

## 🙏 Acknowledgments

- Natural Medicines Therapeutic Research database
- Ollama and the open-source LLM community
- Sentence-Transformers library
- FAISS by Meta AI
- Robert McDermott's KG Relationships Generation Tool: https://github.com/robert-mcdermott/ai-knowledge-graph

---
