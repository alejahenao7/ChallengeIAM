import mysql.connector
import getpass

def create_connection():
    # Configura la conexión con tu base de datos MySQL
    db_connection = mysql.connector.connect(
        host = "localhost",
        user = input("Ingrese el nombre de usuario: "),
        password = getpass.getpass("Ingrese la contraseña: ")
    )
    # Verifica si la conexión fue exitosa
    if db_connection.is_connected():
        print("Conexión exitosa a la base de datos")
        sqlconnection = db_connection.cursor()
        sqlconnection.execute("SHOW DATABASES") #validar que la BD exista (# Ejecutar la consulta para obtener la lista de bases de datos)
        databases = sqlconnection.fetchall() # Obtener todas las bases de datos en una lista de tuplas
        Db_appiam = "AppIAM"
        if (Db_appiam,) in databases:
            print(f"La base de datos '{Db_appiam}' existe.") # Verificar si la base de datos que estás buscando está en la lista
        else:
            print(f"La base de datos '{Db_appiam}' no existe.")
            sqlconnection.execute("CREATE DATABASE AppIAM") # Crear la base de datos
            sqlconnection.execute("USE AppIAM")
            sqlconnection.execute("CREATE TABLE IF NOT EXISTS ArchivosDrive (Id VARCHAR(60) PRIMARY KEY, Name VARCHAR(100),OwnerName VARCHAR(50), OwnerEmail VARCHAR(50), LastModifiedDate VARCHAR(26), FileExtension VARCHAR(100), Visibility VARCHAR(15) NULL)")
            sqlconnection.execute("CREATE TABLE IF NOT EXISTS HistoricoArchivosPublicos (Register INT AUTO_INCREMENT PRIMARY KEY, Id VARCHAR(60), LastModifiedDate VARCHAR(26), FOREIGN KEY (Id) REFERENCES ArchivosDrive(Id) )")
            print(f"La base de datos '{Db_appiam}' ha sido creada exitosamente")
    else:
        print("Error al conectar a la base de datos")
    return db_connection

    # Cerrar el cursor y la conexión
    #sqlconnection.close()
    #db_connection.close()