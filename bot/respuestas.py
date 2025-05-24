from database.querys import pago_nomina_mes, empleados_activos, salarioPromedio, obtener_tabla_descuentos, obtener_tabla_diasTrabajados, contactos_deudores, facturas_emitidas, porcentaje_efectividad, contratos_empleados

meses = {
    "enero": 1, "febrero": 2, "marzo": 3,
    "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9,
    "octubre": 10, "noviembre": 11, "diciembre": 12
}

def obtener_mes_desde_texto(texto):
    for mes_texto in meses.keys():
        if f"el {mes_texto}" in texto or f"{mes_texto}" in texto:
            return meses[mes_texto]
    return None

def obtener_anio_desde_texto(texto):
    texto = texto.lower().strip()
    for i in range(2021, 2031):
        if str(i) in texto:
            return i
    return None

def responder_pregunta(texto):
    texto = texto.lower()

    if ("nomina" in texto or "nómina" in texto) and ("pague" in texto or "pagué" in texto):
        mes_numero = obtener_mes_desde_texto(texto)
        anio_numero = obtener_anio_desde_texto(texto)
        if mes_numero:
            return pago_nomina_mes(mes_numero, anio_numero)
        else:
            return "No reconocí el mes. Intenta escribirlo correctamente (ejemplo: marzo, junio)."

    elif "empleados" in texto and "activos" in texto:
        return empleados_activos()
    
    elif "salario" in texto and "promedio" in texto and "empleados":
        mes_numero = obtener_mes_desde_texto(texto)
        anio_numero = obtener_anio_desde_texto(texto)
        return salarioPromedio(mes_numero, anio_numero)

    elif "descuento" in texto and "empleado" in texto:
        nombre = texto.split("empleado")[-1].strip()
        mes = obtener_mes_desde_texto(texto)
        anio = obtener_anio_desde_texto(texto)
        return obtener_tabla_descuentos(nombre, anio, mes)
    elif ("dias" in texto or "días" in texto) and "trabajo" in texto and "empleado" in texto:
        nombre = texto.split("empleado")[-1].strip()
        mes = obtener_mes_desde_texto(texto)
        anio = obtener_anio_desde_texto(texto)
        return obtener_tabla_diasTrabajados(nombre, anio, mes)
    elif "deudores" in texto:
        return contactos_deudores()
    elif "cantidad" in texto and "facturas" in texto and "emitidas" in texto:
        return facturas_emitidas()
    elif "efectividad" in texto and "cobranza" in texto:
        return porcentaje_efectividad()
    elif "contrato" in texto and "tipo" in texto:
        nombre = texto.split("empleado")[-1].strip()
        return contratos_empleados(nombre)
    else:
        return (
            "Lo siento, no entendí tu pregunta. Asegúrate de mencionar palabras clave como 'nómina', 'empleado', 'salario', etc.\n\n"
            "Aquí tienes algunos ejemplos que puedes probar:\n"
            "- ¿Cuánto pagué en nómina el marzo pasado?\n"
            "- ¿Cuántos empleados tengo activos actualmente?\n"
            "- ¿Cuál fue el salario promedio de los empleados en julio de 2023?\n"
            "- ¿Qué descuentos en abril del 2024 tuvo el empleado Laura?\n"
            "- ¿Cuántos días trabajó en junio del 2024 el empleado Carlos?\n"
            "- ¿Quiénes son los contactos deudores?\n"
            "- ¿Qué cantidad de facturas se emitieron en abril del 2023?\n"
            "- ¿Cuál es el porcentaje de efectividad de la cobranza?\n"
            "- ¿Qué tipo de contrato tiene el empleado Andrés?"
        )