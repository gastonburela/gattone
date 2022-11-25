from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Productos)
admin.site.register(Proveedores)
admin.site.register(Ventas)
admin.site.register(Avatar)