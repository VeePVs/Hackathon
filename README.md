# 🤖 NeuCol_Bot – Bot de Telegram para Consultas de Nómina

NeuCol_Bot es un bot de Telegram desarrollado para automatizar consultas frecuentes relacionadas con nómina, empleados activos y otros datos laborales, usando un sistema basado en palabras clave.

Funciona con conexión a base de datos MySQL, procesamiento de archivos con pandas y generación de gráficos con matplotlib.

---

## 📦 Requisitos de instalación

Antes de iniciar, asegúrate de tener instalado Python 3.8 o superior.

### 1. Clona el repositorio

bash
git clone https://github.com/VeePVs/Hackathon.git

### 2. Crea un entorno virtual (opcional pero recomendado)

python -m venv venv
source venv/bin/activate     # En Linux/macOS
venv\Scripts\activate        # En Windows

### 3. Instala las dependencias

pip install pandas
python -m pip install -U matplotlib
pip install python-telegram-bot --upgrade
pip install mysql-connector-python

⚙️ Archivos principales
main.py: archivo principal que ejecuta el bot.

config.py: archivo para configurar el token del bot y los datos de conexión a la base de datos.

db_connection.py: gestiona la conexión y consultas a la base de datos MySQL.

handlers.py: contiene la lógica para interpretar los mensajes del usuario y responder basándose en palabras clave.

utils.py: funciones auxiliares para formatear datos, validar fechas, etc.

### Ejecución del bot
Una vez instaladas las dependencias y configurado tu config.py, simplemente ejecuta:

python main.py
El bot se conectará a Telegram y estará listo para responder mensajes según las palabras clave programadas.
