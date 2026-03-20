import os
from pathlib import Path

from dotenv import load_dotenv

# Load env from starter-app/.env
load_dotenv(Path(__file__).parents[1] / "starter-app" / ".env")

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
PINECONE_KEY: str = os.getenv("PINECONE_KEY", "")
TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

PINECONE_INDEX = "giz"
CHAT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 512
TOP_K = 5

DATASETS_DIR = Path(__file__).parents[1] / "starter-app" / "data" / "datasets"

PARQUET = {
    "lfs2022": DATASETS_DIR / "RW_LFS2022_reduced.parquet",
    "lfs2023": DATASETS_DIR / "RW_LFS2023_reduced.parquet",
    "lfs2024": DATASETS_DIR / "RW_LFS2024_reduced.parquet",
}

VARIABLES_CSV = DATASETS_DIR / "Variables_description_RW_LFS2023.csv"
