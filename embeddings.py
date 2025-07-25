import json
import os
import time
from typing import List

from dotenv import load_dotenv
from ollama import Client

load_dotenv()

ollama_client = Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))

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
    "artificial_intelligence",
    "computer_vision", 
    "data_science"
]


chunk_files = gather_chunk_files(documents_to_process)

for index, chunk_file in enumerate(chunk_files, start=1):
    chunk_data = json.load(open(chunk_file))

    with open(chunk_file, "w") as c:
        response = ollama_client.embeddings(
            model=os.environ.get("EMBEDDING_MODEL", "nomic-embed-text"),
            prompt=chunk_data["chunk_text"],
        )

        embedding = response["embedding"]

        if CUSTOM_EMBEDDING_DIM > 0 and len(embedding) > CUSTOM_EMBEDDING_DIM:
            embedding = embedding[:CUSTOM_EMBEDDING_DIM]

        chunk_data["embeddings"] = response["embedding"]
        json.dump(chunk_data, c, indent=4)

    time.sleep(0.1)
    print(f"Processed chunks -> {index}/{len(chunk_files)}")
