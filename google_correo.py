#  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from __future__ import print_function

import base64
import mimetypes
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

#import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class manejo_gmail:
    def __init__(self,dir_correo, titulo,texto, archivo_anexo = '' ) -> None:
        self.dir_correo = dir_correo
        self.titulo = titulo
        self.archivo_anexo = archivo_anexo
        self.texto = texto

        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.readonly']
        # 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'

        self.login_gmail()
        '''if conexion == True: # para mandar correo solo despues de haberse conectado realmente
            self.gmail_create_draft_with_attachment()'''''
        #send_message = self.draft.send

    def login_gmail(self):
        
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            self.service = build('gmail', 'v1', credentials=creds, static_discovery=False)
            results = self.service.users().getProfile(userId='me').execute()

            return results['emailAddress']  # se conectó


        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred e555555: {error}')
            return False # no se conectó

    def gmail_create_draft_with_attachment(self):
        

        try:
            # create gmail api client
            
            self.mime_message = EmailMessage()

            # headers
            self.mime_message['To'] = self.dir_correo
            self.mime_message['Subject'] = self.titulo

            # text
            self.mime_message.set_content(self.texto)

            # attachment
            if self.archivo_anexo != '': # por si acaso no hay adjunto
                '''attachment_filename = self.archivo_anexo
                # guessing the MIME type
                type_subtype, _ = mimetypes.guess_type(attachment_filename)
                maintype, subtype = type_subtype.split('/')

                with open(attachment_filename, 'rb') as fp:
                    attachment_data = fp.read()
                self.mime_message.add_attachment(attachment_data, maintype, subtype)'''
                self.mime_message.add_attachment(self.build_file_part(self.archivo_anexo))

            encoded_message = base64.urlsafe_b64encode(self.mime_message.as_bytes()).decode()

            create_draft_request_body = {
                
                    'raw': encoded_message
                
            }
            # pylint: disable=E1101
            self.draft = self.service.users().messages().send(userId="me",
                                                    body=create_draft_request_body)\
                .execute()
            #print(F'Draft id: {self.draft["id"]}\nDraft message: {self.draft["message"]}')
            
        except HttpError as error:
            print(F'An error222222222 occurred: {error}')
            self.draft = None
        return self.draft

    def build_file_part(self, file):
        """Creates a MIME part for a file.

        Args:
        file: The path to the file to be attached.

        Returns:
        A MIME part that can be attached to a message.
        """
        with open(file, 'rb') as fp:
            attachment_data = fp.read()
        
        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            with open(file, 'r') as fp:
                attachment_data = fp.read()
                msg = MIMEText(attachment_data, _subtype=sub_type)
        elif main_type == 'image':
            with open(file, 'rb'):
                msg = MIMEImage(attachment_data, _subtype=sub_type)
        elif main_type == 'audio':
            with open(file, 'rb'):
                msg = MIMEAudio(attachment_data, _subtype=sub_type)
        else:
            with open(file, 'rb'):
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(file.read())
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        return msg

if __name__ == '__main__':
    #envio = manejo_gmail('baltazar.diaz@gmail.com',"hola 7hghg878787",'kdkdkdkdkdk','1.html')
    envio = manejo_gmail('baltazar.diaz@gmail.com', "hola 7hghg878787", 'kdkdkdkdkdk',)
    envio.gmail_create_draft_with_attachment()