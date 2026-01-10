import FastAPI

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "files"

app = FastAPI(title="Collectorium API", version="1.0.0")