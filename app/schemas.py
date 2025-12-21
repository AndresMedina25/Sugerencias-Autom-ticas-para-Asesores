# Base model para crear modelos de datos
#Validar campos especificos
from pydantic import BaseModel, field_validator


class SuggestRequest(BaseModel): # Definir modelo de datos para la solicitud de sugerencia
    """
    Modelo de entrada para POST /suggest
    - 'query': texto de la consulta del usuario
    """
    query: str # Texto de la consulta del usuario

    @field_validator("query") # Validar que 'query' no esté vacío
    def query_not_empty(cls, v: str):
        # Valida que 'query' tenga contenido útil
        if not v or not v.strip(): # Detectar que el campo no esté vacío o solo tenga espacios
            raise ValueError("El campo 'query' no puede estar vacío.") # Lanzar error si está vacío
        return v.strip() # Retornar el valor limpio (sin espacios al inicio o final)

class SuggestResponse(BaseModel):
    """
    Modelo de salida para POST /suggest
    - 'suggestion': texto de la sugerencia de respuesta
    """
    suggestion: str # Texto de la sugerencia de respuesta

# Historial de consultas y sugerencias
class HistoryItem(BaseModel):
    """
    Elemento del historial
    - 'query': consulta original
    - 'suggestion': respuesta sugerida
    """
    query: str # Consulta original del usuario
    suggestion: str # Respuesta sugerida por el sistema

class KBItem(BaseModel): # Definir modelo de datos para un item de la base de conocimiento
    """
    Elemento de la base de conocimiento para el endpoint opcional /kb
    - 'pregunta' y 'respuesta'
    """
    pregunta: str
    respuesta: str

    @field_validator("pregunta", "respuesta") # Validar que 'pregunta' y 'respuesta' no estén vacíos
    def not_empty(cls, v: str): # Validar que el campo no esté vacío
        if not v or not v.strip(): # Detectar que el campo no esté vacío o solo tenga espacios
            raise ValueError("Los campos 'pregunta' y 'respuesta' no pueden estar vacíos.")
        return v.strip() # Retornar el valor limpio (sin espacios al inicio o final)