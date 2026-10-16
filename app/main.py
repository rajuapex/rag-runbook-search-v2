import os

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

GATEWAY_URL = os.environ.get("GATEWAY_URL", "http://localhost:8080")
GATEWAY_KEY = os.environ["GATEWAY_API_KEY"]
MODEL_ALIAS = "fast"
DATA_CLASS = "internal"

app = FastAPI(title="rag-runbook-search-v2")
client = httpx.AsyncClient(timeout=httpx.Timeout(60, connect=5))


class Ask(BaseModel):
    question: str


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.post("/ask")
async def ask(req: Ask):
    r = await client.post(
        f"{GATEWAY_URL}/v1/chat",
        headers={
            "Authorization": f"Bearer {GATEWAY_KEY}",
            "X-Data-Classification": DATA_CLASS,
        },
        json={
            "model": MODEL_ALIAS,
            "messages": [{"role": "user", "content": req.question}],
            "max_tokens": 512,
        },
    )
    r.raise_for_status()
    return r.json()