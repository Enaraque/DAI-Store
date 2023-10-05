import subprocess
from datetime import datetime
from rich import print

# Configuración de la conexión MongoDB
host = 'mongo'
port = 27017
database_name = 'tienda'

# Directorio de salida para la copia de seguridad
backup_dir = './backup'

# Nombre del archivo de copia de seguridad con marca de tiempo
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
backup_file = f"{timestamp}_backup"

# Comando mongodump a ejecutar
mongodump_cmd = [
    'mongodump',
    '--host', host,
    '--port', str(port),
    '--db', database_name,
    '--out', f"{backup_dir}/{backup_file}"
]

# Ejecuta el comando de mongodump
subprocess.run(mongodump_cmd)

print("[green]Copia de seguridad completada en " +
      f"{backup_dir}/{backup_file}[/green]")
