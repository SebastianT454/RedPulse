from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from secret_config import NOTIEMAIL, NOTICONTRA, ADMINEMAIL


class Notificaciones:
    def __init__(self,de_email=None, contra=None, admin_email=ADMINEMAIL):
        self.admin_email = admin_email
        if None in [de_email]:
            self.de_email = NOTIEMAIL
            self.contra = NOTICONTRA
        else:
            self.de_email = de_email    
            self.contra = contra


    def enviar_notificacion(self, para_email, asunto, mensaje):
        msj = MIMEMultipart()
        msj['From'] = self.de_email
        msj['To'] = para_email
        msj['Subject'] = asunto
        
        msj.attach(MIMEText(mensaje, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.de_email, self.contra)
        
        server.sendmail(msj['From'], msj['To'], msj.as_string())
        server.quit()
    
    def parametros_notificacion_donante(self, para_email, tipo_sangre):
            asunto = "¡Tu ayuda es crucial! Nueva Campaña de Donación de Sangre Disponible"
            mensaje = (
                f"Espero que estés bien. Nos gustaría informarte sobre una importante campaña de donación de sangre que se llevará a cabo. "
                f"Esta campaña es especialmente crítica ya que estamos en necesidad urgente de sangre de tipo {tipo_sangre}. "
                f"Como donante valioso, tu participación puede marcar la diferencia en la vida de muchos pacientes que dependen de transfusiones. "
                f"La donación es rápida y segura, y cada gota cuenta."
            )
            self.enviar_notificacion(para_email, asunto, mensaje)

    def parametros_notificacion_admin(self, tipo_sangre):
        asunto = f"Niveles de sangre {tipo_sangre} bajos"
        mensaje = (
            f"Los niveles actuales de la sangre de tipo {tipo_sangre} se encuentran por debajo de lo recomendado, "
            "es recomendable iniciar una campaña para retomar niveles seguros."
        )
        self.enviar_notificacion(self.admin_email, asunto, mensaje)

    def recuperar_contra_notificacion(self, para_email, token):
        reset_url = f"http://tuservidor.com/reset-password?token={token}" #cambiar cuando tengamos el deploy
        asunto = "Recuperación de Contraseña"
        mensaje = (
            f"Has solicitado restablecer tu contraseña. Para continuar, haz clic en el siguiente enlace:\n\n"
            f"{reset_url}\n\n"
            "Este enlace es válido solo por un tiempo limitado. Si no solicitaste este cambio, puedes ignorar este mensaje."
        )
        self.enviar_notificacion(para_email, asunto, mensaje)

         
