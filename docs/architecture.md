User Question
     ↓
LangChain Agent
     ↓
Tool (your function)
     ↓
DuckDB / PostgreSQL query
     ↓
Structured result
     ↓
LLM formats answer


```md
             ┌───────────────┐
             │   User Query  │
             └──────┬────────┘
                    ↓
           LangChain Agent
           /             \
          ↓               ↓
   Data Tool         Vector Search
(Postgres/DuckDB)    (FAISS/Pinecone)
          ↓               ↓
     Structured Data     Text Context
           \             /
            ↓           ↓
             Final LLM Answer
```