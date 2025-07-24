import json
import os
import textwrap
import uuid
from pathlib import Path
from dotenv import load_dotenv
import re

load_dotenv()

CHUNK_SIZE = 750


METADATA_MARK = "---"

# Create chunks directory if it doesn't exist
Path("chunks").mkdir(exist_ok=True)


def gather_handbook_documents() -> list[str]:
    return [
        f"{directory}/{file}"
        for directory, subdirectory, files in os.walk("handbook")
        for file in files
        if ".md" in file
    ]


def extract_document_metadata(document_text: str) -> tuple:
    metadata_start_index = document_text.find(METADATA_MARK) + len(METADATA_MARK)
    metadata_end_index = document_text.find(METADATA_MARK, metadata_start_index)

    metadata = document_text[metadata_start_index:metadata_end_index]
    title = ""
    description = ""

    for line in metadata.split("\n"):
        if "title:" in line:
            title = line.replace("title: ", "").replace('"', "").strip()
        if "description:" in line:
            description = line.replace("description: ", "").replace('"', "").strip()

    return title, description, document_text[metadata_end_index:]


def create_file_for_each_chunk(
    title: str, description: str, document: str, chunk_index: int, chunk: str
) -> None:
    chunk_id = str(uuid.uuid4())

    # Use Path to create a safe filename
    document_path = Path(document)
    clean_path = document_path.with_suffix('').as_posix().replace('/', '_').replace('\\', '_')
    safe_filename = f"{clean_path}-{chunk_index}.json"

    # Ensure chunks directory exists
    chunks_dir = Path("chunks")
    chunks_dir.mkdir(parents=True, exist_ok=True)

    # Full path to the chunk file
    chunk_file_path = chunks_dir / safe_filename

    with chunk_file_path.open("w", encoding="utf-8") as chunk_file:
        json.dump(
            {
                "id": chunk_id,
                "title": title,
                "description": description,
                "document": document,
                "chunk_text": chunk,
                "chunk_token_count": len(chunk.split()),
            },
            chunk_file,
            indent=4,
        )

#####################################Different Chunking Strategies########################################

def naive_line_chunking(text: str) -> list[str]: 
    """Chunk line by line"""
    lines = text.split('\n')
    return [line.strip() for line in lines if line.strip()]

def fixed_token_chunking(text: str) -> list[str]:
    """Chunk by fixed character size"""
    return textwrap.wrap(text, CHUNK_SIZE)

def paragraph_chunking(text: str) -> list[str]:
    """Chunk by paragraph"""
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]

def sentence_chunking(text: str) -> list[str]:
    """Chunk by sentence"""
    # end with . ! ? or ... or \n\n
    sentences = re.split(r'[.!?]', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def sliding_window_chunking(text: str, window_size: int = 750, overlap: int = 100) -> list[str]:
    """Chunk by sliding window"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + window_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        
    return chunks

#############################################Finish Line##################################################


def chunk_documents():
    documents = gather_handbook_documents()

    for document in documents:
        with open(document, encoding="utf-8") as d:
            document_text = d.read()
            title, description, remaining_text = extract_document_metadata(
                document_text
            )

            chunks = sliding_window_chunking(remaining_text, window_size=750, overlap=100)

            for chunk_index, chunk in enumerate(chunks, start=1):
                create_file_for_each_chunk(
                    title, description, document, chunk_index, chunk
                )


chunk_documents()
