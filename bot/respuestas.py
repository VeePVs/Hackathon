import re
from database.querys import pago_nomina_mes

meses = {
    "enero": 1, "febrero": 2, "marzo": 3,
    "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9,
    "octubre": 10, "noviembre": 11, "diciembre": 12
}

def responder_pregunta(texto):
    texto = texto.lower()
    
    coincidencia = re.search(r"nómina.*el\s+(\w+)\s+pasado", texto)

    if coincidencia:
        mes_texto = coincidencia.group(1)
        mes_numero = meses.get(mes_texto)
        
        if mes_numero:
            return pago_nomina_mes(mes_numero)
        else:
            return "No reconocí el mes. Intenta escribirlo correctamente (ejemplo: marzo, junio)."
    else:
        return "No entendí tu pregunta. Intenta con algo como: ¿Cuánto pagué en nómina el marzo pasado?"
