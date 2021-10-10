from django.db import models
from django.contrib.auth.models import AbstractUser




class UserProfile(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=100, default='', verbose_name="Nombres")
    last_name = models.CharField(max_length=100, default='', verbose_name="Apellidos")
    is_active = models.BooleanField(default=True)
    token = models.CharField(blank=True, max_length=50)
    email = models.EmailField(unique=True,blank=True, null=True)
    email_is_valid = models.BooleanField(default=False)
    date_joined = models.DateTimeField(blank=True)
    identification = models.CharField(db_index=True, unique=True, max_length=15, verbose_name="Cédula")
    phone = models.CharField(max_length=10, default='', verbose_name="Teléfono")
    phone_indicator = models.CharField(max_length=4, default='', verbose_name="Indicador")
    country = models.CharField(max_length=100, default='', verbose_name="País")
    state = models.CharField(max_length=100, default='', verbose_name="Departamento")
    company = models.ForeignKey('companies.Company',on_delete=models.CASCADE,verbose_name="Compañia",null=True,blank=False)
    city = models.CharField(max_length=100, default='', verbose_name="Ciudad")

    #USERNAME_FIELD = 'identification'
    #REQUIRED_FIELDS = ['password','email']

    def get_full_name(self):
        full_name = ''
        full_name += str(self.first_name) if self.first_name else ''
        full_name += " " + str(self.last_name) if self.last_name else ''
        return full_name

    def __str__(self) -> str:
        return self.get_full_name()