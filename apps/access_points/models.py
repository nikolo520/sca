from django.db import models
from django.db.models.base import Model
from django.db.models.fields import EmailField

class AccessPoint(Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre",blank=True,null=True,max_length=150,help_text='Ej. Sucursal Norte')
    address = models.CharField(verbose_name="Dirección",blank=True,null=True,max_length=50)
    email = models.EmailField(verbose_name="Correo Electrónico",max_length=50,null=True,blank=True)
    latitude = models.DecimalField(verbose_name="Latitud",decimal_places=4,max_digits=4,null=True,blank=True,help_text='-45.1207')
    longitude = models.DecimalField(verbose_name="Longitud",decimal_places=4,max_digits=4,null=True,blank=True,help_text='150.0001')
    company = models.ForeignKey('companies.Company',on_delete=models.CASCADE,verbose_name="Compañia",null=True,blank=False)
    is_active = models.BooleanField(verbose_name="Activo",default=True)

    def __str__(self) -> str:
        return str(self.name) if self.name else 'Nombre indefinido'