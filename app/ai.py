from typing import Optional, List

def generate_suggestion(query: str, kb_items: List[dict]) -> Optional[str]:
    """
    Genera una sugerencia simple basada en palabras clave.
    En producción, aquí integrarías un modelo generativo externo (IA),
    usando prompts y 'grounding' con el contenido de kb_items.
    """
    query_lower = query.lower()
    # Heuristicas simples por tema
    if "contraseña" in query_lower:
        return "Si necesitas cambiar tu contraseña, revisa la sección de configuración de tu perfil."
    if "horario" in query_lower or "tiempo" in query_lower or "atención" in query_lower:
        return "Nuestro horario de atención es de lunes a viernes, de 9am a 6pm."
    if "correo" in query_lower or "email" in query_lower:
        return "Puedes actualizar tu correo desde tu perfil, en 'Información de contacto'."
    # Respuesta genérica si no se detecta un tema claro
    return "¿Podrías darme un poco más de contexto? Mientras tanto, revisa el Centro de Ayuda para pasos detallados."