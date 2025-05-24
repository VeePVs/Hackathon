from .conexion import conectar

def pago_nomina_mes(mes=7, anio=2024):
    conexion = conectar()
    if anio == None:
        anio = 2024
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT SUM(CAST(REPLACE(total_payment, ',', '.') AS DECIMAL(10, 2))) "
            "AS total_monthly_payment FROM payrolls WHERE MONTH(start_date) = %s AND YEAR(start_date) = %s", 
            (mes, anio)
        )
        resultados = cursor.fetchall()
        return f"En el mes {mes} del año {anio} el total de la nómina es: {'{:,.2f}'.format(resultados[0][0])}"
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
def salarioPromedio(anio=2024, mes=7):
    conexion = conectar()
    if anio == None:
        anio = 2024
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                YEAR(created_at) AS payroll_year, 
                MONTH(created_at) AS payroll_month, 
                AVG(CAST(REPLACE(total, ',', '.') AS DECIMAL(10, 2))) AS average_salary 
            FROM payroll_details 
            WHERE YEAR(created_at) = %s AND MONTH(created_at) = %s
        """, (mes,anio,))
        resultados = cursor.fetchall()

        if resultados and resultados[0][2] is not None:
            return f"El salario promedio para para {mes}/{anio} es: {'{:,.2f}'.format(resultados[0][2])}"
        else:
            return f"No se encontraron registros de nómina para {mes}/{anio}."
    except mysql.connector.Error as err:
        return f"La consulta no se pudo realizar: {err}"
    finally:
        conexion.close()
