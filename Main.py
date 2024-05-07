
import os.path

from googleapiclient.errors import HttpError 
from DbConnection import create_connection
from ValidarPermisos import ConfirmarPermiso
from googleApi import enviar_correo
from googleApi import obtener_archivos

def main():
  #Conexión a la base de datos usando el archivo dbconenection.py
  db_connection = create_connection()
  if db_connection.is_connected():
    sqlconnection = db_connection.cursor()

  try:
    #serviceDrive = build("drive", "v3", credentials=creds)
    serviceDrive = obtener_archivos()

    # Llamar API de google drive para consultar los archivos
    results = (
        serviceDrive.files()
        .list(pageSize=12, fields="nextPageToken, files(id, name, mimeType, owners, modifiedTime, permissions)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    print("Files:")
    for item in items:
      print(f"{item['name']} {item['mimeType']} {item['owners'][0]['displayName']} {item['modifiedTime']} ({item['id']})")
      Id = item['id']
      Name = item['name']
      OwnerName = item['owners'][0]['displayName']
      OwnerEmail = item['owners'][0]['emailAddress']
      LastModifiedDate = item['modifiedTime']
      FileExtension = item['mimeType']
      if 'permissions' in item:
        Visibility = ConfirmarPermiso(item['permissions'])
      else:
        Visibility = 'Privado'

      sqlconnection.execute("USE AppIAM")
      queryFile = "SELECT Id FROM AppIAM.ArchivosDrive WHERE Id = %s"
      sqlconnection.execute(queryFile, (Id,))
      queryresult = sqlconnection.fetchall() #Recupera los resutados
      if not queryresult:
        print("NO FILES")
        insertitem = "INSERT INTO ArchivosDrive (Id, Name, OwnerName, OwnerEmail, LastModifiedDate, FileExtension, Visibility) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (Id, Name, OwnerName, OwnerEmail, LastModifiedDate, FileExtension, Visibility)
        sqlconnection.execute (insertitem,values)
        db_connection.commit()
      else:
        updatefile = "UPDATE ArchivosDrive SET Name = %s, OwnerName = %s, OwnerEmail = %s, LastModifiedDate = %s, FileExtension = %s, Visibility = %s Where  Id = %s"
        values = (Name, OwnerName, OwnerEmail, LastModifiedDate, FileExtension, Visibility, Id)
        sqlconnection.execute (updatefile, values)
        print ("UPDATE FILE")
        db_connection.commit()
      
      if Visibility == 'Publico':
        insertitem = "INSERT INTO HistoricoArchivosPublicos (Id, LastModifiedDate) VALUES (%s, %s)"
        values = (Id, LastModifiedDate)
        sqlconnection.execute (insertitem,values)
        db_connection.commit()
        try:
          serviceDrive.permissions().delete(fileId=id, permissionId='anyoneWithLink').execute()
        except HttpError as error:
          print(f"No tienes permisos sobre el archivo {item['name']} para cambiarlo a privado")
        # Definir los detalles del correo electrónico
        destinatario = 'dajmunozos@gmail.com'
        asunto = 'Archivo público en Google Drive'
        mensaje = f'El archivo {item['name']} tienen visibilidad publica en google drive, por favor cambiarlo a privado'
        
        # Llamar a la función para enviar el correo electrónico
        enviar_correo(destinatario, asunto, mensaje)
  
    # Cerrar el cursor y la conexión
    sqlconnection.close()
    db_connection.close()
      
  except HttpError as error:
    #TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
# [END drive_quickstart]