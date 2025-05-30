from .conexion import conectar
import pandas as pd
import matplotlib.pyplot as plt

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

def obtener_tabla_descuentos(nombre, anio, mes):
    conexion = conectar()
    if anio == None:
        anio = 2024
    try:
        cursor = conexion.cursor()
        query = """
            SELECT
                pyd.employee_id,
                em.full_name,
                SUM(CAST(REPLACE(pyd.deductions_total, ',', '.') AS DECIMAL(10, 2))) AS total_deductions_for_month,
                YEAR(py.start_date) AS payroll_year,
                MONTH(py.start_date) AS payroll_month
            FROM
                payroll_details AS pyd
            INNER JOIN
                payrolls py ON py.id = pyd.payroll_id
            INNER JOIN
                user_data usd ON usd.user_id = pyd.user_id
            INNER JOIN
                employees em ON em.id = pyd.employee_id
            WHERE
                em.full_name LIKE %s
                AND YEAR(py.start_date) = %s
                AND MONTH(py.start_date) = %s
            GROUP BY
                pyd.employee_id,
                em.full_name,
                YEAR(py.start_date),
                MONTH(py.start_date);
        """
        cursor.execute(query, (f"%{nombre}%", anio, mes))
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(resultados, columns=columnas)

        if df.empty:
            return None, "No se encontraron resultados."

        fig, ax = plt.subplots(figsize=(10, len(df)*0.5 + 1))
        ax.axis('tight')
        ax.axis('off')
        tabla = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
        tabla.scale(1, 1.5)
        ruta_imagen = "tabla_salario.png"
        plt.savefig(ruta_imagen, bbox_inches='tight')
        plt.close(fig)

        return ruta_imagen, f"Este es el resultado de las personas llamadas {nombre} y su descuento en el año {anio} y mes {mes}"
    except Exception as e:
        return None, str(e)
    finally:
        conexion.close()
   
def obtener_tabla_diasTrabajados(nombre, anio, mes):
    conexion = conectar()
    if anio == None:
        anio = 2024
    try:
        cursor = conexion.cursor()
        query = """
            SELECT
                pyd.employee_id,
                em.full_name,
                SUM(pyd.period_worked_days) AS total_period_worked_days,
                YEAR(py.start_date) AS payroll_year,
                MONTH(py.start_date) AS payroll_month
            FROM
                payroll_details AS pyd
            INNER JOIN
                payrolls py ON py.id = pyd.payroll_id
            INNER JOIN
                user_data usd ON usd.user_id = pyd.user_id
            INNER JOIN
                employees em ON em.id = pyd.employee_id
            WHERE
                em.full_name LIKE %s
                AND YEAR(py.start_date) = %s
                AND MONTH(py.start_date) = %s
            GROUP BY
                pyd.employee_id,
                em.full_name,
                YEAR(py.start_date),
                MONTH(py.start_date);
        """
        cursor.execute(query, (f"%{nombre}%", anio, mes))
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(resultados, columns=columnas)

        if df.empty:
            return None, "No se encontraron resultados."

        fig, ax = plt.subplots(figsize=(10, len(df)*0.5 + 1))
        ax.axis('tight')
        ax.axis('off')
        tabla = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
        tabla.scale(1, 1.5)
        ruta_imagen = "tabla_días.png"
        plt.savefig(ruta_imagen, bbox_inches='tight')
        plt.close(fig)

        return ruta_imagen, f"Este es el resultado de las personas llamadas {nombre} y sus días trabajados en el año {anio} y mes {mes}"
    except Exception as e:
        return None, str(e)
    finally:
        conexion.close()

def contratos_empleados(nombre):
    conexion = conectar()
    print(nombre)
    try:
        cursor = conexion.cursor()
        query = """
            SELECT
                e.full_name,
                JSON_EXTRACT(ec.type, '$.description') AS contract_type
            FROM
                employees AS e
            INNER JOIN
                employee_contracts ec ON ec.employee_id = e.id
            WHERE e.full_name LIKE %s
        """
        cursor.execute(query, (f"%{nombre}%",))
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(resultados, columns=columnas)

        if df.empty:
            return None, "No se encontraron resultados."

        fig, ax = plt.subplots(figsize=(10, len(df)*0.5 + 1))
        ax.axis('tight')
        ax.axis('off')
        tabla = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
        tabla.scale(1, 1.5)
        ruta_imagen = "tabla_días.png"
        plt.savefig(ruta_imagen, bbox_inches='tight')
        plt.close(fig)

        return ruta_imagen, f"Este es el resultado de las personas llamadas {nombre} y sus contratos."
    except Exception as e:
        return None, str(e)
    finally:
        conexion.close()

def contactos_deudores():
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
             SELECT 
                 cs.contact_id,
                 c.full_name,
                 (cs.invoices_total - cs.payments_received_total) AS pending_amount
             FROM demo_wft.contact_statements cs
             JOIN demo_wft.contacts c ON cs.contact_id = c.id
             ORDER BY pending_amount DESC
             LIMIT 10;
         """)

        resultados = cursor.fetchall()  
        columnas = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(resultados, columns=columnas)
        if df.empty:
            return None, "No se encontraron resultados de contactos con deudas."
        fig, ax = plt.subplots(figsize=(10, len(df)*0.5 + 1))
        ax.axis('tight')
        ax.axis('off')
        tabla = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
        tabla.scale(1, 1.5)
        ruta_imagen = "tabla_deudores.png"
        plt.savefig(ruta_imagen, bbox_inches='tight')
        plt.close(fig)
    
        return ruta_imagen, f"Estos son los contactos con mayores deudas"
    except mysql.connector.Error as err:
        return f"La consulta no se pudo realizar: {err}"
    finally:
        conexion.close()
        
def facturas_emitidas():
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
             SELECT 
                c.document_number,
                c.full_name,
                cs.invoices_counter
            FROM demo_wft.contact_statements cs
            JOIN demo_wft.contacts c ON cs.contact_id = c.id
            ORDER BY cs.invoices_counter DESC
            LIMIT 10;
         """)

        resultados = cursor.fetchall()  
        columnas = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(resultados, columns=columnas)
        if df.empty:
            return None, "No se encontraron resultados de contactos con facturas"
        fig, ax = plt.subplots(figsize=(10, len(df)*0.5 + 1))
        ax.axis('tight')
        ax.axis('off')
        tabla = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
        tabla.scale(1, 1.5)
        ruta_imagen = "tabla_facturas_emitidas.png"
        plt.savefig(ruta_imagen, bbox_inches='tight')
        plt.close(fig)
    
        return ruta_imagen, "Estas son los 10 contactos con mayor cantidad emitida por contacto"
    except mysql.connector.Error as err:
        return f"La consulta no se pudo realizar: {err}"
    finally:
        conexion.close()
        
def porcentaje_efectividad():
    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                ROUND(SUM(cs.payments_received_total) / SUM(cs.invoices_total) * 100, 2) AS avg_collection_rate
            FROM demo_wft.contact_statements cs
            WHERE cs.invoices_total > 0;
         """)

        resultados = cursor.fetchall()  
        if resultados :
            return f"El porcentaje de efectividad de cobranza es del {resultados[0][0]}%"
        else:
            return f"No se encontraron datos para obtener la efectividad de cobranza."
    except mysql.connector.Error as err:
        return f"La consulta no se pudo realizar: {err}"
    finally:
        conexion.close()