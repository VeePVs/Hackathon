from .conexion import conectar

def pago_nomina_mes(mes=7, anio=2024):
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT SUM(CAST(REPLACE(total_payment, ',', '.') AS DECIMAL(10, 2))) "
            "AS total_monthly_payment FROM payrolls WHERE MONTH(start_date) = %s AND YEAR(start_date) = %s", 
            (mes, anio)
        )
        resultados = cursor.fetchall()
        return f"En el mes {mes} del año {anio} el total de la nómina es: {resultados[0][0]}"
    except mysql.connector.Error as err:
        return f"La consulta no se pudo realizar: {err}"
    finally:
        conexion.close()

def empleados_activos(activo=1):
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) AS active_records_count FROM employees WHERE status = %s", (activo,))
        resultados = cursor.fetchall()
        return f"El total de empleados activos es: {resultados[0][0]}"
    except mysql.connector.Error as err:
        return f"La consulta no se pudo realizar: {err}"
    finally:
        conexion.close()
