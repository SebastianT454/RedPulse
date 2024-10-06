from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from SecretConfig import NOTIEMAIL, NOTICONTRA

class Notificaciones:
    def __init__(self,de_email=None, contra=None):
        if None in [de_email]:
            self.de_email = NOTIEMAIL
            self.contra = NOTICONTRA
        else:
            self.de_email = de_email    
            self.contra = contra


    def notificarDonante(self, para_email, tipo_sangre):
        msj = MIMEMultipart()
        
        msj['From'] = self.from_address
        msj['To'] = para_email
        msj['Subject'] = "¡Tu ayuda es crucial! Nueva Campaña de Donación de Sangre Disponible"
        
        mensaje = f"Espero que estés bien. Nos gustaría informarte sobre una importante campaña de donación de sangre que se llevará a cabo. Esta campaña es especialmente crítica ya que estamos en necesidad urgente de sangre de tipo {tipo_sangre}. Como donante valioso, tu participación puede marcar la diferencia en la vida de muchos pacientes que dependen de transfusiones. La donación es rápida y segura, y cada gota cuenta."

        msj.attach(MIMEText(mensaje, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        server.login(self.de_email, self.contra)
        
        server.sendmail(msj['From'], msj['To'], msj.as_string())
        server.quit()
    
def notificarAdmin(self, tipo_sangre):
        msj = MIMEMultipart()
        
        msj['From'] = self.from_address
        msj['To'] = "redpulsetst@gmail.com"
        msj['Subject'] = f"Niveles de sangre {tipo_sangre} bajos"
        
        mensaje = f"Los niveles actuales de la sangre de tipo {tipo_sangre} se encuentran por debajo de lo recomendado, 
        es recomendable iniciar una campaña para retomar niveles seguros."

        msj.attach(MIMEText(mensaje, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        server.login(self.de_email, self.contra)
        
        server.sendmail(msj['From'], msj['To'], msj.as_string())
        server.quit()