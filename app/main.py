from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from app.suggest import load_knowledge_base, find_best_suggestion, knowledge_base, save_knowledge
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from app.schemas import KnowledgeItem


app = FastAPI(title="Sistema de Sugerencias para Asesores")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

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

@app.get("/")
def serve_home():
    return FileResponse("app/static/index.html")

@app.get("/view-history")
def serve_history_page():
    return FileResponse("app/static/history.html")

@app.get("/view-add-knowledge")
def serve_add_page():
    return FileResponse("app/static/add_knowledge.html")

@app.post("/knowledge")
def add_knowledge(item: KnowledgeItem):
    new_item = {
        "id": f"custom_{len(knowledge_base) + 1}", # Un ID string para seguir tu formato
        "title": item.question,
        "keywords": [], # Agregamos esto para que no rompa el buscador después
        "examples": [item.question],
        "answer": item.answer
    }
    knowledge_base.append(new_item)
    save_knowledge()
    return {"message": "Pregunta agregada correctamente"}