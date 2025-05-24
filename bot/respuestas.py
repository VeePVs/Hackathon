from database.querys import pago_nomina_mes, empleados_activos

meses = {
    "enero": 1, "febrero": 2, "marzo": 3,
    "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9,
    "octubre": 10, "noviembre": 11, "diciembre": 12
}

def obtener_mes_desde_texto(texto):
    for mes_texto in meses.keys():
        if f"el {mes_texto}" in texto or f"{mes_texto} pasado" in texto:
            return meses[mes_texto]
    return None

def responder_pregunta(texto):
    texto = texto.lower()

    if ("nomina" in texto or "nómina" in texto) and ("pague" in texto or "pagué" in texto):
        mes_numero = obtener_mes_desde_texto(texto)
        if mes_numero:
            return pago_nomina_mes(mes_numero)
        else:
            return "No reconocí el mes. Intenta escribirlo correctamente (ejemplo: marzo, junio)."

    elif "empleados" in texto and "activos" in texto:
        return empleados_activos()

    else:
        return "No entendí tu pregunta. Intenta con algo como:\n- ¿Cuánto pagué en nómina el marzo pasado?\n- ¿Cuántos empleados tengo activos actualmente?"
