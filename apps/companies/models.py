from django.db import models
from django.db.models.base import Model

class Company(Model):
    id = models.CharField(primary_key=True, blank=True, max_length=40)
    business_name = models.CharField(max_length=100, default='', verbose_name="Nombre de la empresa")
    trade_name = models.CharField(max_length=100, default='', verbose_name="Nombre comercial")
    is_active = models.BooleanField(default=True)
    email = models.EmailField(blank=True, null=True)
    email_is_valid = models.BooleanField(default=False)
    nit = models.CharField(db_index=True, unique=True, max_length=15, verbose_name="Nit")
    phone = models.CharField(max_length=10, default='', verbose_name="Teléfono")
    phone_indicator = models.CharField(max_length=4, default='', verbose_name="Indicador")
    country = models.CharField(max_length=100, default='', verbose_name="País")
    state = models.CharField(max_length=100, default='', verbose_name="Departamento")
    city = models.CharField(max_length=100, default='', verbose_name="Ciudad")
    web_page = models.CharField(max_length=100, default='', verbose_name="Página Web")

    def __str__(self) -> str:
        return self.business_name if self.business_name else 'No definido'