import json
import os
import textwrap
import uuid
from pathlib import Path
from dotenv import load_dotenv

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
    safe_filename = f"{document_path.with_suffix('').as_posix().replace('/', '_').replace('\\', '_')}-{chunk_index}.json"

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


def chunk_documents():
    documents = gather_handbook_documents()

    for document in documents:
        with open(document, encoding="utf-8") as d:
            document_text = d.read()
            title, description, remaining_text = extract_document_metadata(
                document_text
            )

            for chunk_index, chunk in enumerate(
                textwrap.wrap(remaining_text, CHUNK_SIZE), start=1
            ):
                create_file_for_each_chunk(
                    title, description, document, chunk_index, chunk
                )


chunk_documents()
