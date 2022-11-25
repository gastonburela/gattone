from django.db import models
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import User

# Create your models here.  

class Cliente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.CharField(max_length=10)
    telefono = models.CharField(max_length=30)
    direccion = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Empleado(models.Model):
    legajo = models.IntegerField()
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    area = models.CharField(max_length=30)
    cargo = models.CharField(max_length=30)
    def __str__(self):
        return f'Legajo: {self.legajo} - {self.nombre} {self.apellido}'

class Proveedores(models.Model):
    numero = models.IntegerField()
    nombre = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    direccion = models.CharField(max_length=60)
    def __str__(self):
        return f'Nombre: {self.nombre} Tipo: {self.tipo}'

class Productos(models.Model):
    codigo = models.IntegerField()
    modelo = models.CharField(max_length=30)
    genero = models.CharField(max_length=30)
    medidas = models.CharField(max_length=30)
    
    def __str__(self):
        return f'Modelo: {self.modelo}'

class Ventas(models.Model):

    cliente = models.ForeignKey(Cliente,null=True,blank=True, on_delete=models.CASCADE)
    venta = models.ManyToManyField(Productos)
    fecha = models.DateField(auto_now=True)
    detalle = models.TextField(max_length=254)

#Avatares
class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.imagen}'
