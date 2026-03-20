"""
FastAPI entry point.uvi

Run:
    corn api.main:app --reload

Endpoints:
    POST /chat          — send a message, get an AI response
    DELETE /chat/{sid}  — clear a session's history
    GET  /health        — liveness check
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from api.agent import run_agent

MAX_HISTORY = 20  # messages kept per session (each turn = 2 entries)

# In-memory session store: session_id -> list[{"role": str, "content": str}]
_sessions: dict[str, list[dict]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up: pre-build the system prompt (loads variable descriptions CSV once)
    from api.agent import _system_prompt
    _system_prompt()
    yield


app = FastAPI(
    title="Gender Data AI API",
    description="AI-powered Q&A over Rwanda gender reports and LFS microdata.",
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    session_id: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    history = _sessions.setdefault(req.session_id, [])

    try:
        answer = run_agent(req.message, history)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    # Persist turn
    history.append({"role": "user", "content": req.message})
    history.append({"role": "assistant", "content": answer})
    if len(history) > MAX_HISTORY:
        _sessions[req.session_id] = history[-MAX_HISTORY:]

    return ChatResponse(answer=answer, session_id=req.session_id)


@app.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    _sessions.pop(session_id, None)
    return {"message": f"Session '{session_id}' cleared."}


@app.get("/health")
async def health():
    return {"status": "ok"}
