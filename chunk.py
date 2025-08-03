import json
import os
import textwrap
import uuid
from pathlib import Path
from dotenv import load_dotenv
import re
import glob

load_dotenv()

CHUNK_SIZE = 750


METADATA_MARK = "---"

# Create chunks directory if it doesn't exist
Path("chunks").mkdir(exist_ok=True)

def extract_document_metadata(document_text: str) -> tuple:
    if document_text.startswith("---"):
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
    else:
        return "", "", document_text


def create_file_for_each_chunk(
    title: str, description: str, document_path: str, chunk_index: int, chunk: str, output_folder: str
) -> None:
    chunk_id = str(uuid.uuid4())

    # Use Path to create a safe filename
    document_name = Path(document_path).stem
    safe_filename = f"{document_name}-{chunk_index}.json"

    # Ensure chunks directory exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Full path to the chunk file
    chunk_file_path = os.path.join(output_folder, safe_filename)

    with open(chunk_file_path, "w", encoding="utf-8") as chunk_file:
        json.dump(
            {
                "id": chunk_id,
                "title": title,
                "description": description,
                "document": document_path,
                "chunk_text": chunk,
                "chunk_token_count": len(chunk.split()),
                "chunk_index": chunk_index

            },
            chunk_file,
            indent=4,
        )

#Different Chunking Strategies
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


def chunk_single_document(document_path: str, chunking_function=fixed_token_chunking):

    if not os.path.exists(document_path):
        print(f"Document not found: {document_path}")
        return
    print(f"Processing: {document_path}")
    
    with open(document_path, encoding="utf-8") as f:
        document_text = f.read()
    
    title, description, remaining_text = extract_document_metadata(document_text)
    document_name = Path(document_path).stem
    output_folder = f"chunks/{document_name}"

    # Clear existing chunks
    if os.path.exists(output_folder):
        for file in os.listdir(output_folder):
            if file.endswith('.json'):
                os.remove(os.path.join(output_folder, file))
    
    chunks = chunking_function(remaining_text)
    for chunk_index, chunk in enumerate(chunks, start=1):
        create_file_for_each_chunk(title, description, document_path, chunk_index, chunk, output_folder)
    
    print(f"Processed: {document_path} and created {len(chunks)} chunks")

if __name__ == "__main__":
    document_pattern = "WIKI/*.md"
    document_paths = glob.glob(document_pattern)

    if document_paths:
        for document_path in document_paths:
            print(f"Processing: {document_path}")
            chunk_single_document(document_path, fixed_token_chunking)
    else:
        print(f"No Markdown files found at: {document_pattern}")


