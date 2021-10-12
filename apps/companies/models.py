from typing import ClassVar
from django.db import models
from django.db.models.base import Model
from rest_framework.validators import UniqueValidator

class Company(Model):
    id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=100, default='', verbose_name="Nombre de la empresa")
    trade_name = models.CharField(max_length=100, default='', verbose_name="Nombre comercial")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    email = models.EmailField(blank=True, null=True, verbose_name="Correo eletrónico")
    email_is_valid = models.BooleanField(default=False)
    nit = models.CharField(db_index=True, unique=True, max_length=15, verbose_name="Nit")
    phone = models.CharField(max_length=10, verbose_name="Teléfono",null=True, blank=True)
    phone_indicator = models.CharField(max_length=4, default='57', verbose_name="Indicador",null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name="País", null=True, blank=True)
    state = models.CharField(max_length=100, verbose_name="Departamento", null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name="Ciudad", null=True, blank=True)
    web_page = models.CharField(max_length=100, verbose_name="Página Web",help_text="https://...",null=True, blank=True)

    def __str__(self) -> str:
        return self.business_name if self.business_name else 'No definido'
