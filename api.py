from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from schemas.types import FILE_DEFS


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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


def _serialize_file_def(fd):
    return {
        "key": fd.key,
        "label": fd.label,
        "id_key": fd.id_key,
        "fields": fd.fields,
        "intKeys": sorted(list(fd.int_keys)),
        "boolKeys": sorted(list(fd.bool_keys)),
    }


def _getfile_def_or_404(key: str):
    for fd in FILE_DEFS:
        if fd.key == key:
            return fd
    raise HTTPException(status_code=404, detail="File definition not found")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "Awaken"}


@app.get("/meta/files")
def list_file_meta() -> list[dict[str, Any]]:
    return [_serialize_file_def(fd) for fd in FILE_DEFS]


@app.get("/meta/files/{key}")
def read_file_meta(key: str) -> dict[str, Any]:
    fd = _getfile_def_or_404(key)
    return _serialize_file_def(fd)


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


@app.get("/files/{name}")
def read_file(name: str) -> Any:

    path = (FILES_DIR / F"{name}.json").resolve()

    if not str(path).startswith(str(FILES_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid file name")

    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error reading JSON file")
    except OSError:
        raise HTTPException(status_code=500, detail="Error reading file")

