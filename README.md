<h1 align="center">🔍 RAG from Scratch</h1>
<p align="center">
  Build your own <strong>Native Retrieval-Augmented Generation</strong> system using local models.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/pip-ready-blue?logo=pypi&logoColor=white" alt="PIP Ready" />
  <img src="https://img.shields.io/badge/NumPy-enabled-013243?logo=numpy&logoColor=white" alt="NumPy" />
  <img src=https://img.shields.io/badge/-Ollama-000000?style=flat&logo=ollama&logoColor=white alt="Ollama" />
</p>


---

## 🚀 Project Overview

<img src="https://miro.medium.com/v2/resize:fit:1100/format:webp/1*a_qVjYbKuuJrWxoBOnEAbA.png" alt="" />

This repository contains code to build a **RAG (Retrieval-Augmented Generation)** system from scratch using local models powered by [Ollama](https://ollama.com).

The system retrieves relevant content from the GitLab Handbook and uses a local LLM to answer user queries.

---

## 🛠️ Setup

### 1. Clone the repository:
```bash
git clone https://github.com/IDEAS-Incubator/LLM_Bootcamp_Native_RAG
cd LLM_Bootcamp_Native_RAG
```

### 2. Create and activate conda environment:
```bash
conda create -n rag_scratch python=3.12
conda activate rag_scratch
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Install Ollama and required models:
```bash
# Install Ollama (follow instructions for your OS)
# For Windows:
winget install ollama

# For linux:
brew install ollama
brew services start ollama

# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2
```

### 5. Configure environment variables:

```bash
copy .env.example .env
```

---

## 📦 Running the Project

### 1. Chunk the data
Split the GitLab Handbook into smaller chunks:
```bash
python chunk.py
```

### 2. Generate embeddings
Create embeddings using the local embedding model:
```bash
python embeddings.py
```

### 3. Ask your question!
Run the RAG pipeline:
```bash
python rag.py "who is ceo"
```

---

## 📚 Data Source

The knowledge base for this project is the **GitLab Handbook**, a comprehensive, real-world dataset perfect for demonstrating RAG systems.

---

## 🌐 Support & Contribution

Have questions or suggestions? Reach out or contribute!

🔗 **Project URL**: [https://github.com/IDEAS-Incubator/LLM_Bootcamp_Native_RAG](https://github.com/IDEAS-Incubator/LLM_Bootcamp_Native_RAG)

---

