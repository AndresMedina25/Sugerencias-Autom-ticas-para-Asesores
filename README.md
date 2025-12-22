# Sugerencias Automáticas para Asesores

Este proyecto implementa una API RESTful que permite a asesores recibir sugerencias automáticas basadas en una base de conocimiento de preguntas frecuentes, mientras atienden consultas de usuarios.

La solución fue desarrollada como parte de una prueba técnica, priorizando claridad, simplicidad, buenas prácticas y facilidad de validación.

## Tecnologias Utilizadas
Python 3.12+

FastAPI – Framework web

Uvicorn – Servidor ASGI

Pytest – Pruebas automatizadas

Docker – Contenerización

HTML + CSS + JavaScript – Interfaz gráfica mínima

## Estructura del proyecto
suggestions-assistant/

│

├── app/

│   ├── main.py               # Punto de entrada de la API

│   ├── suggest.py            # Lógica de sugerencias y similitud

│   ├── schemas.py            # Esquemas de validación (Pydantic)

│   ├── knowledge_base.json   # Base de conocimiento

│   └── __init__.py

│

├── tests/

│   ├── test_suggest.py       # Pruebas del endpoint /suggest

│   ├── test_history.py       # Pruebas del endpoint /history

│   └── __init__.py

│

├── ui/

│   ├── index.html            # Interfaz gráfica

│   └── styles.css

│

├── Dockerfile

├── requirements.txt

├── README.md

└── .gitignore

## Endpoints Disponibles
  ## POST /suggest

Recibe una consulta y devuelve una sugerencia basada en la base de conocimiento.

Entrada

{
  "query": "¿Cómo cambio mi contraseña?"
}


Salida

{
  "suggestion": "Puedes cambiar tu contraseña en la sección de configuración de tu perfil."
}

  ## GET /history

Devuelve el historial de consultas realizadas y sus sugerencias.

Salida

[

  {
  
    "query": "¿Cómo cambio mi contraseña?",
    
    "suggestion": "Puedes cambiar tu contraseña en la sección de configuración de tu perfil."
    
  }
  
]

### POST /knowledge (Opcional)

Permite agregar nuevas preguntas y respuestas a la base de conocimiento.

### Entrada

{

  "question": "¿Dónde están ubicados?",
  
  "answer": "Estamos ubicados en la ciudad de Popayán."
  
}


### Salida

{

  "message": "Pregunta agregada correctamente"
  
}

## Lógica de Sugerencias

Se utiliza una búsqueda básica de similitud textual

Se compara la consulta del usuario con las preguntas almacenadas

Se devuelve la respuesta más cercana

Si no hay coincidencias suficientes, se devuelve un mensaje informativo

La base de conocimiento está almacenada en un archivo JSON y puede extenderse fácilmente.

## Pruebas

El proyecto incluye pruebas automatizadas para cada endpoint.

### Ejecutar pruebas localmente

pytest

### Ejecutar pruebas con Docker

docker run --rm suggestions-assistant pytest

## Ejecución con Docker
### Construir la imagen
docker build -t suggestions-assistant .

### Ejecutar el contenedor
docker run -p 8000:8000 suggestions-assistant

### Acceder a la API

API: http://localhost:8000

Documentación Swagger: http://localhost:8000/docs

## Ejecución Local (Sin Docker)
### Crear entorno virtual
python -m venv .venv

### Activar entorno virtual

Windows

.venv\Scripts\activate

### Instalar dependencias
pip install -r requirements.txt

### Ejecutar la aplicación
uvicorn app.main:app --reload

### Validar funcionamiento

http://localhost:8000/docs

Probar /suggest, /history y /knowledge

### NOTA
Para que el EndPoint knowledge funcione de manera correcta, se recomienda ejecutar el proyecto de manera local

## Interfaz Gráfica

La aplicación incluye una UI mínima desarrollada con HTML, CSS y JavaScript, separada en tres secciones:

Consulta de sugerencias

Visualización del historial

Formulario para agregar nuevas preguntas

Esta interfaz facilita la validación funcional sin necesidad de herramientas externas.

## Notas Finales

El historial se almacena en memoria

No se utiliza base de datos

La solución es simple, extensible y fácil de evaluar

La arquitectura permite futuras mejoras como:

Integración con IA generativa

Persistencia en base de datos

Mejora visual de la interfaz

## Autor
**Andres Fernando Medina Pino**
