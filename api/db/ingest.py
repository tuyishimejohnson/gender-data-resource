"""
PDF ingestion script: chunks PDFs, embeds with OpenAI text-embedding-3-small,
and upserts to a Pinecone index.

Usage:
    python starter-app/db/ingest.py
"""
import os
import hashlib
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

load_dotenv(Path(__file__).parents[1] / ".env")

PINECONE_KEY = os.getenv("PINECONE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

INDEX_NAME = "giz"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 512   # truncated via MRL to match existing "giz" index

CHUNK_SIZE = 2000     # characters (~500 tokens)
CHUNK_OVERLAP = 200   # characters
UPSERT_BATCH = 100    # vectors per Pinecone upsert call
EMBED_BATCH = 20      # texts per OpenAI embedding call


# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------
openai_client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_KEY)


def get_or_create_index() -> object:
    existing = [idx.name for idx in pc.list_indexes()]
    if INDEX_NAME not in existing:
        print(f"Creating Pinecone index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    return pc.Index(INDEX_NAME)


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
def chunk_text(text: str) -> list[str]:
    """Split text into overlapping character-based chunks."""
    chunks = []
    start = 0
    text = text.strip()
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------
def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = []
    for i in range(0, len(texts), EMBED_BATCH):
        batch = texts[i : i + EMBED_BATCH]
        response = openai_client.embeddings.create(input=batch, model=EMBEDDING_MODEL, dimensions=EMBEDDING_DIM)
        embeddings.extend([item.embedding for item in response.data])
    return embeddings


# ---------------------------------------------------------------------------
# Ingestion
# ---------------------------------------------------------------------------
def load_source_mapper(mapper_path: Path) -> dict[str, str]:
    """Load PDF-to-URL mapping from source_pdf_mapper.txt."""
    mapping = {}
    if not mapper_path.exists():
        return mapping

    with open(mapper_path, "r") as f:
        for line in f:
            line = line.strip()
            if " => " in line:
                pdf_name, url = line.split(" => ", 1)
                mapping[pdf_name.strip()] = url.strip()
    return mapping


def ingest_pdf(pdf_path: Path, index, source_url: str = None) -> None:
    reader = PdfReader(str(pdf_path))
    source = pdf_path.stem
    print(f"  {len(reader.pages)} pages found")

    records: list[tuple[str, str, dict]] = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if not text.strip():
            continue
        for chunk_idx, chunk in enumerate(chunk_text(text)):
            uid = hashlib.md5(f"{source}-{page_num}-{chunk_idx}".encode()).hexdigest()
            metadata = {
                "source": source,
                "page": page_num + 1,
                "chunk": chunk_idx,
                "text": chunk
            }
            if source_url:
                metadata["url"] = source_url
            records.append((uid, chunk, metadata))

    if not records:
        print("  No text extracted, skipping.")
        return

    print(f"  {len(records)} chunks to embed and upsert...")

    # Embed all chunks
    texts = [r[1] for r in records]
    embeddings = embed_texts(texts)

    # Upsert in batches
    for i in range(0, len(records), UPSERT_BATCH):
        batch = records[i : i + UPSERT_BATCH]
        vectors = [
            (batch[j][0], embeddings[i + j], batch[j][2])
            for j in range(len(batch))
        ]
        index.upsert(vectors=vectors)
        print(f"  Upserted {min(i + UPSERT_BATCH, len(records))}/{len(records)} chunks")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    index = get_or_create_index()

    db_dir = Path(__file__).parent
    pdf_dir = db_dir / "pdf"

    if not pdf_dir.exists():
        print(f"PDF directory not found: {pdf_dir}")
        return

    # Load source mapper
    mapper_path = pdf_dir / "source_pdf_mapper.txt"
    source_mapper = load_source_mapper(mapper_path)
    print(f"Loaded {len(source_mapper)} source mappings")

    pdfs = sorted(pdf_dir.glob("*.pdf"))

    if not pdfs:
        print("No PDF files found in", pdf_dir)
        return

    print(f"Found {len(pdfs)} PDF files to process\n")

    for pdf_path in pdfs:
        print(f"\nProcessing: {pdf_path.name}")
        source_url = source_mapper.get(pdf_path.name)
        if source_url:
            print(f"  Source URL: {source_url}")
        ingest_pdf(pdf_path, index, source_url)

    print("\nIngestion complete.")


if __name__ == "__main__":
    main()
