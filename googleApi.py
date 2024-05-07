import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage
from googleapiclient.errors import HttpError 
from email.mime.text import MIMEText
import base64

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    
]
def enviar_correo(destinatario, asunto, mensaje):
    creds = None
    # Generación del token.json, despues de que el usaurio autoriza los permisos en el navegador
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # Si no existe un token, se pide la autenticación del usuario en google
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        # guarda las credenciales para una proxima ejecución
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Construir el servicio de Gmail
    try: 
        ServiceGmail = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()

        message.set_content(mensaje)

        message["To"] = destinatario
        message["From"] = "alejahenao7@gmail.com"
        message["Subject"] = asunto

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            ServiceGmail.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None

#Función para obtener los arhcivos del google Drive
def obtener_archivos():
    creds = None
    # Generación del token.json, despues de que el usaurio autoriza los permisos en el navegador
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # Si no existe un token, se pide la autenticación del usuario en google
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        # guarda las credenciales para una proxima ejecución
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        serviceDrive = build("drive", "v3", credentials=creds)
        return serviceDrive
    except:
        print(f"Error al obtener archivos de google drive.")