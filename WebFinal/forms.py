from django import forms
from .models import *

class Formulario_cliente(forms.ModelForm):

    # nombre = forms.CharField(max_length=30)
    # apellido = forms.CharField(max_length=30)
    # telefono = forms.CharField(max_length=30)
    # direccion = forms.CharField(max_length=60)
    class Meta:
        model = Cliente 
        fields = ("nombre","apellido", "dni", "telefono", "direccion")


class Formulario_empleado(forms.ModelForm):
    # nombre = forms.CharField(max_length=30)
    # apellida = forms.CharField(max_length=30)
    # area = forms.CharField(max_length=30)
    # cargo = forms.CharField(max_length=30)
    class Meta:
        model = Empleado
        fields = ("nombre","apellido","area","cargo")


class Formulario_proveedores(forms.ModelForm):
    # nombre = forms.CharField(max_length=30)
    # tipo = forms.CharField(max_length=30)
    # telefono = forms.CharField(max_length=30)
    # direccion = forms.CharField(max_length=60)

    class Meta:
        model = Proveedores
        fields = ("numero","nombre","tipo","telefono","direccion")

class Formulario_productos(forms.ModelForm):
    # modelo = forms.CharField(max_length=30)
    # genero = forms.CharField(max_length=30)
    # medidas = forms.CharField(max_length=30)
    class Meta:
        model = Productos
        fields = ("modelo","genero","medidas")

class Formulario_ventas(forms.ModelForm):

    class Meta:
        model = Ventas
        fields = ("venta","detalle")