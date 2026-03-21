import os
from pathlib import Path

from dotenv import load_dotenv

# Get the api directory path
API_DIR = Path(__file__).parent

# Load env from api/.env
load_dotenv(API_DIR / ".env")

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
PINECONE_KEY: str = os.getenv("PINECONE_KEY", "")
TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

PINECONE_INDEX = "giz"
CHAT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 512
TOP_K = 5

PARQUET = {
    "lfs2022": str(API_DIR / "db" / "parquets" / "RW_LFS2022_reduced.parquet"),
    "lfs2023": str(API_DIR / "db" / "parquets" / "RW_LFS2023_reduced.parquet"),
    "lfs2024": str(API_DIR / "db" / "parquets" / "RW_LFS2024_reduced.parquet"),
}

VARIABLES_CSV = str(API_DIR / "db" / "parquets" / "Variables_description_RW_LFS2023.csv")
