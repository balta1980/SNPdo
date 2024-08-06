# este modulo no tiene uso, se podría borrar, está deprecado por el de google
import smtplib
import email.message, leew

def enviar_corre0(correo_destino,mensaje,asunto):

    server = smtplib.SMTP('smtp.gmail.com:587')

    email_content = mensaje

    msg = email.message.Message()
    msg['Subject'] = asunto

    msg['From'] = leew.consulta_gen('worker.db','dir_correo','correo','status', ' "Vigente"')
    msg['To'] = correo_destino
    password = leew.consulta_gen('worker.db','clave_correo','correo','status', ' "Vigente"')
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    # Login Credentials for sending the mail
    s.login(msg['From'], password)

    s.sendmail(msg['From'], [msg['To']], msg.as_string())

#enviar_corre0('baltazar.diaz@gmail.com','dddd','wwww')