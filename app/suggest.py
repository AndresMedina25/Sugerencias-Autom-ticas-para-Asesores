import json # Importar modulo estandar de Json
from difflib import SequenceMatcher # Para medir similitud entre textos
from pathlib import Path # Manejo de rutas de archivos, evita problemas entre Windows / Linux / Mac
from typing import Optional, List # Tipos de datos

# Ruta del archivo de base de conocimiento
BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "knowledge_base.json"

def load_knowledge_base() -> List[dict]:
    with open(KB_PATH, encoding="utf-8") as f:
        return json.load(f)

def normalize(text: str) -> str:
    return text.lower().strip()

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def find_best_suggestion(
    query: str,
    kb: List[dict],
    threshold: float = 0.6
) -> Optional[str]:
    query_norm = normalize(query)
    best_score = 0.0
    best_answer = None

    for item in kb:
        # Comparar contra ejemplos
        for example in item["examples"]:
            score = similarity(query_norm, normalize(example))
            if score > best_score:
                best_score = score
                best_answer = item["answer"]

        #Busqueda por keywords
        keyword_hits = sum(
            1 for kw in item["keywords"]
            if kw in query_norm
        )
        if keyword_hits:
            best_score += 0.05 * keyword_hits

    if best_score >= threshold:
        return best_answer

    return None
