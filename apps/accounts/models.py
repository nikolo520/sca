from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserProfile(AbstractUser):
    username = models.CharField(max_length=15, unique=True, verbose_name="Nombre de Usuario")
    first_name = models.CharField(max_length=100, default='', verbose_name="Nombres")
    last_name = models.CharField(max_length=100, default='', verbose_name="Apellidos")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    token = models.CharField(blank=True, max_length=50)
    email = models.EmailField(unique=True,blank=True, null=True,verbose_name="Correo electrónico")
    email_is_valid = models.BooleanField(default=False)
    date_joined = models.DateTimeField(blank=True)
    identification = models.CharField(db_index=True, unique=True, max_length=15, verbose_name="Cédula")
    phone = models.CharField(max_length=10, default='', verbose_name="Teléfono")
    phone_indicator = models.CharField(max_length=4, default='', verbose_name="Indicador")
    country = models.CharField(max_length=100, default='', verbose_name="País")
    state = models.CharField(max_length=100, default='', verbose_name="Departamento")
    company = models.ForeignKey('companies.Company',on_delete=models.CASCADE,verbose_name="Compañia",null=False,blank=False)
    city = models.CharField(max_length=100, default='', verbose_name="Ciudad")

    def get_full_name(self):
        full_name = ''
        full_name += str(self.first_name) if self.first_name else ''
        full_name += " " + str(self.last_name) if self.last_name else ''
        return full_name

    def send_activation_email(self):
        from django.core.mail import EmailMultiAlternatives
        from django.conf import settings
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self)
        url = "{0}validate_email?ut={1}&token={2}".format(settings.SITE_URL,self.id, token)
        html = """
            <html>
                <p>Estimado usuario, el registro de su cuenta fue exitoso.</p>
                <p>Por favor active su cuenta haciendo click <a target="_blank" href="{0}">aquí</a>.</p>
                <br>
                <p>Si por algun motivo su dispositivo no abre la ventana, copie y pegue en su navegador el siguiente link</p>
                <p>{0}</p>
            </html>
        """.format(url)
        send_mail(
            "ACTIVA TU CUENTA",
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            html_message=html,
            fail_silently=False
        )

    def create(self,args):
        return super.create(args)


    def __str__(self) -> str:
        return self.get_full_name()