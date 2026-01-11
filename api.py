from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "files"

app = FastAPI(title="Collectorium API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/files")
def list_json_files() -> list[str]:

    if not FILES_DIR.exists():
        return []

    result: list[str] = []
    for p in FILES_DIR.iterdir():
        if p.is_file() and p.suffix.lower() == ".json":
            result.append(p.stem)

    result.sort(key=lambda x: x.lower())
    return result

@app.get("/files/{file_name}")
def read_file(name: str) -> Any:

    path = (FILES_DIR / F"{name}.json").resolve()