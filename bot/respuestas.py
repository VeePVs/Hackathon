from database.consultas import empleados_activos

def responder_pregunta(texto):
    # Aquí puedes agregar lógica para interpretar otras preguntas
    if "activo" in texto:
        return empleados_activos()
    else:
        return "No entendí tu pregunta. Intenta con algo como: ¿Cuántos empleados activos hay?"
