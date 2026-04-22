import os
import subprocess
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="MemPalace API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

PALACE_DIR = os.environ.get("PALACE_DIR", "/data/palace")
API_KEY = os.environ.get("MEMPALACE_API_KEY", "changeme")


def check_auth(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


class StoreRequest(BaseModel):
    content: str
    wing: Optional[str] = "claude"
    room: Optional[str] = "general"


@app.get("/health")
def health():
    return {"status": "ok", "palace": PALACE_DIR}


@app.post("/store")
def store(req: StoreRequest, x_api_key: str = Header(...)):
    check_auth(x_api_key)
    try:
        result = subprocess.run(
            ["mempalace", "mine", "-", "--wing", req.wing, "--room", req.room],
            input=req.content,
            capture_output=True,
            text=True,
            env={**os.environ, "MEMPALACE_DIR": PALACE_DIR},
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"stored": True, "wing": req.wing, "room": req.room}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
def search(q: str, top_k: int = 5, x_api_key: str = Header(...)):
    check_auth(x_api_key)
    try:
        result = subprocess.run(
            ["mempalace", "search", q, "--top-k", str(top_k)],
            capture_output=True,
            text=True,
            env={**os.environ, "MEMPALACE_DIR": PALACE_DIR},
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"query": q, "results": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/wake")
def wake(x_api_key: str = Header(...)):
    check_auth(x_api_key)
    try:
        result = subprocess.run(
            ["mempalace", "wake-up"],
            capture_output=True,
            text=True,
            env={**os.environ, "MEMPALACE_DIR": PALACE_DIR},
        )
        return {"context": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
