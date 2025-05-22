from email.message import EmailMessage
import ssl
import smtplib

# Creación de la clase que generara el objeto para construir el email
class BuildMail:

    def __init__(
        self,
        subject: str, # Asunto del correo
        sender: str, # Dirección de correo del emisor
        reciver: str, # Dirección de correo del receptor
        credentials: str, # Contraseña de la aplicación, leer mensaje del pull request para mas info
        paciente: str, # Nombre del paciente 
        fecha: str, # Fecha de realización de teleconsulta
        enlace: str # Enlace de la teleconsulta
    ):
        self.msg = EmailMessage() # Construcción del objeto EmailMessage
        self.msg['Subject'] = subject # Incicalizador de valor Subject
        self.msg['From'] = sender # Incicalizador de valor From
        self.msg['To'] = reciver # Incicalizador de valor To

        # Setear el cuerpo del correo 
        self.msg.set_content(self._build_body(
            paciente, fecha, enlace
        ))

        # Envio del correo
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender, credentials)
            smtp.sendmail(sender, reciver, self.msg.as_string())

    # Construye el mensaje en base a la templeate de abajo
    def _build_body(self, paciente, fecha, enlace):
        return f"""\
        
Estimado(a) {paciente}:

Le confirmamos su cita de telemedicina programada para:

📅 Fecha: {fecha}  
🔗 Enlace para la reunión: {enlace}

Le recomendamos conectarse 10 minutos antes del inicio, desde un lugar tranquilo y con buena conexión a internet.  
Si tiene exámenes recientes o documentos relevantes, tenga a mano sus archivos para compartirlos durante la consulta.

Saludos cordiales.
"""
