import json
import os
import time
from typing import List

from sentence_transformers import SentenceTransformer

# Load embedding model (this downloads and caches it)
embedding_model_name = os.environ.get("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
model = SentenceTransformer(embedding_model_name)

CUSTOM_EMBEDDING_DIM = 768

def gather_chunk_files(document_folders: list[str]) -> list[str]:
    chunk_files = []
    for document_folder in document_folders:
        folder_path = f"chunks/{document_folder}"
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".json"):
                    chunk_files.append(f"{folder_path}/{file}")
    return chunk_files

# 指定要处理的多个文档文件夹
documents_to_process = [
    "deep_learning"
]

chunk_files = gather_chunk_files(documents_to_process)

for index, chunk_file in enumerate(chunk_files, start=1):
    print(f"⏳ Processing file: {chunk_file}")   # Add this line

    with open(chunk_file) as f:
        chunk_data = json.load(f)

    text = chunk_data["chunk_text"]
    embedding = model.encode(text).tolist()

    if CUSTOM_EMBEDDING_DIM > 0 and len(embedding) > CUSTOM_EMBEDDING_DIM:
        embedding = embedding[:CUSTOM_EMBEDDING_DIM]

    chunk_data["embeddings"] = embedding

    with open(chunk_file, "w") as f:
        json.dump(chunk_data, f, indent=4)

    time.sleep(0.1)
    print(f"Processed chunks -> {index}/{len(chunk_files)}")
