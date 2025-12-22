from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

from app.suggest import load_knowledge_base, find_best_suggestion


app = FastAPI(title="Sistema de Sugerencias para Asesores")
knowledge_base = load_knowledge_base()
history = []

class SuggestRequest(BaseModel):
    query: str

    @field_validator("query")
    def not_empty(cls, v: str):
        if not v or not v.strip():
            raise ValueError("El campo 'query' no puede estar vacío")
        return v

class SuggessResponse(BaseModel):
    suggestion: str
    
@app.post("/suggest", response_model=SuggessResponse)
def suggest(req: SuggestRequest):
    suggestion = find_best_suggestion(req.query, knowledge_base)
    if not suggestion:
        suggestion = "No se encontro una respuesta adecuada para la consulta"
    
    history.append({
        "query" : req.query,
        "suggestion" : suggestion
    })
    
    return {"suggestion" : suggestion}

@app.get("/history")
def get_history():
    return history

# Manejar el estado en memoria y controlar su reinicio para pruebas
@app.on_event("startup")
def clear_history():
    history.clear()

