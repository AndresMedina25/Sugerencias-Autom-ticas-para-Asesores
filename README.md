# Sugerencias Automáticas para Asesores

## Tecnologias Utilizadas
Python 3.12 (usado dentro del contenedor Docker)

FastAPI – Framework web ligero para crear APIs

Uvicorn – Servidor ASGI

Pytest – Pruebas automatizadas

Docker – Para ejecutar la aplicación en un entorno reproducible

## Estructura del proyecto
suggestions-assistant/
│

├── app/

│   ├── main.py              # Punto de entrada de la API

│   ├── suggest.py           # Lógica de sugerencias y similitud

│   └── knowledge_base.json  # Base de conocimiento

│
├── tests/

│   ├── test_suggest.py      # Pruebas del endpoint /suggest

│   └── test_history.py      # Pruebas del endpoint /history

│
├── Dockerfile

├── requirements.txt

├── README.md

└── .gitignore
## Instalación y Ejecución de (Docker)
### Construir la imagen
docker build -t suggestions-assistant .
### Ejercutar el contenedor
docker build -t suggestions-assistant .

#### NOTA
La API estará disponible en (docker run -p 8000:8000 suggestions-assistant)

## ENDPOINTS DISPONIBLES
### POST/suggest
Recibe una consulta del usuario y devuelve una sugerencia basada en la base de conocimiento.

**Ejemplo de entrada**

{

  "query": "¿Cómo cambio mi contraseña?"
  
}

**Ejemplo de salida**

[
  {
  
    "query": "¿Cómo cambio mi contraseña?",
    
    "suggestion": "Puedes cambiar tu contraseña en la sección de configuración de tu perfil."
    
  }]

## Logica de sugerencias
La aplicación utiliza una búsqueda básica de similitud para encontrar la respuesta más cercana dentro de la base de conocimiento, apoyándose en coincidencias textuales simples.

La base de conocimiento está almacenada en un archivo JSON y puede extenderse fácilmente agregando nuevas preguntas, ejemplos o palabras clave.

## Uso de IA generativa
La IA generativa fue utilizada como herramienta de apoyo para:

Estructurar la base de conocimiento

Optimizar la organización del código

Acelerar el desarrollo manteniendo control total sobre la lógica de negocio

La lógica principal de la aplicación fue diseñada y validada manualmente para garantizar claridad, mantenibilidad y correcto funcionamiento.

## Pruebas
El proyecto incluye pruebas básicas para cada endpoint.

Para ejecutarlas:

pytest

También es posible ejecutarlas dentro del contenedor Docker:

docker run --rm suggestions-assistant pytest

## Notas finales
El historial de consultas se almacena en memoria, según los requerimientos.

No se utiliza base de datos.

El proyecto está diseñado para ser simple, extensible y fácil de evaluar.



## Descripción
API que sugiere respuestas basadas en preguntas frecuentes mientras asesores responden consultas de usuarios...

# Autor
Andres Fernando Medina Pino
