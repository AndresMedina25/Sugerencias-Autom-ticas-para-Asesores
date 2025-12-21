from typing import List  # importar list para anotar tipos (historial, respuestas)
from fastapi import FastAPI, HTTPException # Framework web ligero y manejo de excepciones HTTP
from fastapi.middleware.cors import CORSMiddleware # Middleware para manejar CORS
from app.schemas import SuggestRequest, SuggestResponse, HistoryItem, KBItem # Importar los modelos pydantic 
from app.suggest import load_kb, save_kb, best_match # Funciones para cargar, guardar y buscar coincidencias
from app.ai import generate_suggestion # Función para generar sugerencias usando IA (simulada)  

# Inicializa la aplicación FastAPI con metadatos útiles
app = FastAPI(title="Sugerencias Automáticas para Asesores", version="1.0.0")

# Configura CORS básico para permitir pruebas desde diferentes orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Ajusta en producción a dominios específicos
    allow_credentials=True,    # Permitir cookies y credenciales
    allow_methods=["*"],       # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],       # Permitir todos los encabezados
)

# Estado en memoria: historial y base de conocimiento
history: List[HistoryItem] = [] # Lista para almacenar el historial de consultas y sugerencias
kb = load_kb() # Cargar la base de conocimiento al iniciar la aplicación

@app.post("/suggest", response_model=SuggestResponse) # Endpoint principal para sugerencias
def suggest(req: SuggestRequest): # Recibe una solicitud de sugerencia
    """
    Endpoint principal:
    - Recibe una 'query' del usuario.
    - Busca la coincidencia más cercana en la base de conocimiento.
    - Si no hay coincidencia, usa IA generativa opcional para una sugerencia razonable.
    - Guarda en 'history' y retorna la 'suggestion'.
    """
    match = best_match(req.query, kb, cutoff=0.6) # Buscar la mejor coincidencia en la base de conocimiento
    if match: # Si se encuentra una coincidencia
        _, respuesta = match # Desempaquetar la tupla (pregunta, respuesta)
        suggestion = respuesta # Usar la respuesta de la base de conocimiento como sugerencia
    else: # Si no hay coincidencia
        suggestion = generate_suggestion(req.query, kb) # Generar sugerencia usando IA (simulada)
        if not suggestion: # Si la IA no genera una sugerencia
            suggestion = "No encontré una respuesta directa. Por favor, consulta nuestro Centro de Ayuda." # Respuesta por defecto
    
    # Guardar en el historial
    item = HistoryItem(query=req.query, suggestion=suggestion) # Crear un nuevo elemento de historial
    history.append(item) # Agregar al historial en memoria
    return SuggestResponse(suggestion=suggestion) # Convierte a JSON y retorna la sugerencia

@app.get("/history", response_model=List[HistoryItem]) # Endpoint para obtener el historial de consultas y sugerencias
def get_history(): # La función no recibe parámetros
    """
    Retorna la lista de consultas y sugerencias acumuladas durante la ejecución.
    (Persistencia en memoria; se reinicia al reiniciar el servidor.)
    """
    return history # Retorna el historial completo

@app.post("/kb", response_model=KBItem) # Endpoint opcional para agregar items a la base de conocimiento
def add_kb_item(item: KBItem): # Recibe un nuevo item para agregar a la base de conocimiento
    """
    Endpoint opcional:
    - Permite agregar nuevas preguntas/respuestas a la base de conocimiento.
    - Verifica duplicados por la 'pregunta' ignorando mayúsculas/minúsculas.
    """
    for existing in kb: # Verificar si la pregunta ya existe en la base de conocimiento
        if existing["pregunta"].strip().lower() == item.pregunta.strip().lower(): # Comparar sin distinguir mayúsculas/minúsculas y espacios
            raise HTTPException(status_code=409, detail="La pregunta ya existe en la base de conocimiento.") # Error 409 Conflict si ya existe
    kb.append({"pregunta": item.pregunta, "respuesta": item.respuesta}) # Agregar el nuevo item a la base de conocimiento
    save_kb(kb) # Guardar la base de conocimiento actualizada en el archivo
    return item # Retornar el item agregado como confirmación