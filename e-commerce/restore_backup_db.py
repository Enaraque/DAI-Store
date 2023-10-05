import subprocess
from rich import print
import os

# Configuración de la conexión MongoDB
host = 'mongo'
port = 27017
database_name = 'tienda'
backup_dir = './backup'


# Función para obtener la fecha de modificación de un archivo
def obtener_fecha_modificacion(dir):
    return os.path.getmtime(os.path.join(backup_dir, dir))


# Funcion para obtener el backup mas reciente
def backup_reciente():
    num_buckups = [dir for dir in os.listdir(backup_dir)
                   if os.path.isdir(os.path.join(backup_dir, dir))]

    max_backup = max(num_buckups, key=obtener_fecha_modificacion)
    database_name = os.listdir(f"{backup_dir}/{max_backup}")[0]

    return f"{max_backup}/{database_name}"


def restore_backup():
    # Obtiene el backup mas reciente
    backup = backup_reciente()

    # Comando mongorestore a ejecutar
    mongorestore_cmd = [
        'mongorestore',
        '--host', host,
        '--port', str(port),
        '--db', database_name,
        f"{backup_dir}/{backup}"
    ]

    # Ejecuta el comando de mongorestore
    subprocess.run(mongorestore_cmd)

    print("[green]Restauración completada[/green]")


def main():
    restore_backup()


if __name__ == "__main__":
    main()
