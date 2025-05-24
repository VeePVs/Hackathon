import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="demo_wft", 
        port=3308
    )

def verificar_conexion(conexion):
    if conexion.is_connected():
        print("Conexión exitosa a la base de datos")

def desconectar(conexion):
    conexion.close()
