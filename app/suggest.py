import json # Importar modulo estandar de Json
from difflib import get_close_matches  # Comparar textos y encontrar los más parecidos 
from pathlib import Path # Manejo de rutas de archivos, evita problemas entre Windows / Linux / Mac
from typing import Optional, Tuple, List # Tipos de datos

# Ruta del archivo de base de conocimiento relativa a este módulo
KB_PATH = Path(__file__).parent / "knowledge_base.json"

def load_kb() -> List[dict]:
    """
    Carga la base de conocimiento desde kb.json.
    Retorna una lista de dicts con 'pregunta' y 'respuesta'.
    """
    with KB_PATH.open("r", encoding="utf-8") as f: # Abrir archivo en modo lectura con codificación utf-8
        return json.load(f) # Cargar y retornar el contenido JSON como lista de diccionarios

def save_kb(kb: List[dict]) -> None: 
    """
    Guarda la base de conocimiento en kb.json con formato legible.
    Útil para el endpoint opcional que agrega items dinámicamente.
    """
    with KB_PATH.open("w", encoding="utf-8") as f: # Abrir archivo en modo escritura con codificación utf-8
        json.dump(kb, f, ensure_ascii=False, indent=2) # Guardar la lista de diccionarios en formato JSON


def best_match(query: str, kb: List[dict], cutoff: float = 0.6) -> Optional[Tuple[str, str]]:
    """
    Busca la pregunta más similar a 'query' usando difflib.
    - cutoff: umbral de similitud (0 a 1). Más alto = más estricto.
    - Retorna (pregunta, respuesta) si encuentra coincidencia, o None si no.
    """
    preguntas = [item["pregunta"] for item in kb] # Extraer todas las preguntas de la base de conocimiento
    matches = get_close_matches(query, preguntas, n=1, cutoff=cutoff) # Buscar la mejor coincidencia
    if not matches: 
        return None # Si no hay coincidencias, retornar None
    pregunta = matches[0]
    # Encuentra la respuesta correspondiente a la pregunta seleccionada
    for item in kb: # Iterar sobre los items en la base de conocimiento
        if item["pregunta"] == pregunta: # Si la pregunta coincide
            return pregunta, item["respuesta"] # Retornar la pregunta y su respuesta
    return None