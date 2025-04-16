
<h1 align="center">🔍 RAG from Scratch</h1>
<p align="center">
  Build your own <strong>Native Retrieval-Augmented Generation</strong> system using local models.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/pip-ready-blue?logo=pypi" alt="PIP" />
</p>

---

## 🚀 Project Overview

This repository contains code to build a **RAG (Retrieval-Augmented Generation)** system from scratch using local models powered by [Ollama](https://ollama.com).

The system retrieves relevant content from the GitLab Handbook and uses a local LLM to answer user queries.

---

## 🛠️ Setup

### 1. Create and activate conda environment:
```bash
conda create -n rag_scratch python=3.12
conda activate rag_scratch
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Install Ollama and required models:
```bash
# Install Ollama (follow instructions for your OS)
# For Windows:
winget install ollama

# Pull required models
ollama pull nomic-embed-text
ollama pull llama3:2
```

### 4. Configure environment variables:

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

🔗 **Project URL**: [https://github.com/yourusername/rag-from-scratch](https://github.com/yourusername/rag-from-scratch)

---

<p align="center">
  Made with ❤️ using local LLMs
</p>
