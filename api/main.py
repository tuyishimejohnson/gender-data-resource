"""
FastAPI entry point.uvi

Run:
    corn api.main:app --reload

Endpoints:
    POST /api           — send a message, get an AI response
    DELETE /chat/{sid}  — clear a session's history
    GET  /health        — liveness check
"""
from contextlib import asynccontextmanager

import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from api.agent import run_agent, stream_agent
from api.routers.dashboard import router as dashboard_router

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)


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


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    history = _sessions.setdefault(req.session_id, [])
    collected: list[str] = []

    async def generate():
        try:
            async for item in stream_agent(req.message, history):
                if item.startswith("STATUS:"):
                    yield f"data: {json.dumps({'status': item[7:]})}\n\n"
                else:
                    collected.append(item)
                    yield f"data: {json.dumps({'t': item})}\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"
        finally:
            # Persist the full turn to session history
            full_answer = "".join(collected)
            if full_answer:
                history.append({"role": "user", "content": req.message})
                history.append({"role": "assistant", "content": full_answer})
                if len(history) > MAX_HISTORY:
                    _sessions[req.session_id] = history[-MAX_HISTORY:]
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    _sessions.pop(session_id, None)
    return {"message": f"Session '{session_id}' cleared."}


@app.get("/health")
async def health():
    return {"status": "ok"}
