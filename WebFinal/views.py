from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.test import Client
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from collections import namedtuple
from django.utils.decorators import method_decorator

from django.core.exceptions import FieldError
from django.db import DEFAULT_DB_ALIAS, DatabaseError
from django.db.models.constants import LOOKUP_SEP

from django.core.mail import send_mail
from django.conf import settings

from django.utils import tree
from WebFinal.forms import Formulario_cliente
from WebFinal.models import *
from WebFinal.forms import *
# Create your views here.

class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

def inicio(request):
    try:
        avatar = Avatar.objects.get(user=request.user)
        return render(request, 'inicio2.html', {'url': avatar.imagen.url})
    except:
       return render(request, 'inicio2.html')

# def form_cliente(request):

#     #CREATE
    
#     if request.method == 'POST':

#         add_cliente = Formulario_cliente(request.POST)
        
#         if add_cliente.is_valid():

#             datos = add_cliente.cleaned_data
#             nuevo_cliente = Cliente(nombre=datos['nombre'], apellido=datos['apellido'], telefono=datos['telefono'], direccion=datos['direccion'])
#             nuevo_cliente.save()
#             return render(request, 'cliente_creado.html', {'mensaje':'Cliente creado con exito.'})
        
#     else:
#         add_cliente = Formulario_cliente()

#     return render(request, 'form_cliente.html', {'add_cliente': add_cliente})



# POSIBLE CLASE PARA EL MIXIN DE STAFF MEMBER.
# class StaffRequiredMixin(object):
#     """
#     View mixin which requires that the authenticated user is a staff member
#     (i.e. `is_staff` is True).
#     """

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_staff:
#             messages.error(
#                 request,
#                 'You do not have the permission required to perform the '
#                 'requested operation.')
#             return redirect(settings.LOGIN_URL)
#         return super(StaffRequiredMixin, self).dispatch(request,
#             *args, **kwargs)


class CrearCliente(LoginRequiredMixin, CreateView):

    model = Cliente
    form_class = Formulario_cliente
    template_name = 'form_cliente.html'
    success_url = '/WebFinal/crear_exito/'


    #READ
# def lista_clientes(request):

#     clientes = Cliente.objects.all()

#     return render(request, "lista_clientes.html", {"clientes": clientes})

def creado_con_exito(request):
    avatar = Avatar.objects.get(user=request.user) 

    return render(request,'crear_exito.html' ,{'url': avatar.imagen.url})

class Mostrar_clientes(LoginRequiredMixin, ListView):

    model = Cliente
    template_name = "lista_clientes.html"
    context_object_name = "clientes"
    #EDIT

# def borracliente(request, id):

#     if request.method == 'POST':

#         cliente = Cliente.objects.get(id=id)
#         cliente.delete()

#         clientes = Cliente.objects.all()

#         return render(request, "lista_clientes.html", {"clientes": clientes})  

class Detalle_cliente(LoginRequiredMixin, DetailView):

    model = Cliente
    template_name = "detalle_cliente.html"
    context_object_name = "cliente"

class EditarCliente(LoginRequiredMixin, UpdateView):

    model = Cliente
    template_name = "cliente_update.html"
    fields = ('__all__')
    success_url = '/WebFinal/exito_update/'

def cliente_actualizado(request):
    avatar = Avatar.objects.get(user=request.user)
    return render(request,'exito_update.html', {'url': avatar.imagen.url})

class Borracliente(LoginRequiredMixin, DeleteView):

        model = Cliente
        template_name = 'borrarcliente.html'
        success_url = '/WebFinal/lista_clientes'
#BUSQUEDA
def busqueda_cliente(request):
    avatar = Avatar.objects.get(user=request.user)
    return render(request, 'busqueda_cliente.html', {'url': avatar.imagen.url})

class BuscaCliente(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "busqueda_cliente.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("dni")
        if query=="":
            response = 'Cliente no encontrado'
            HttpResponseRedirect('/WebFinal/inicio2', {'response':response})
        else:    
            object_list = Cliente.objects.filter(Q(dni__icontains=query))       
            return (object_list)
        
# def editar_cliente(request, id):

#     print('method:', request.method)
#     print('post: ', request.POST)

#     cliente = Cliente.objects.get(id=id)

#     if request.method == 'POST':

#         cliente_edit = Formulario_cliente(request.POST)

#         if cliente_edit.is_valid():

#             datos = cliente_edit.cleaned_data

#             cliente.nombre = datos["nombre"]
#             cliente.apellido = datos["apellido"]
#             cliente.telefono = datos["telefono"]
#             cliente.direccion = datos["direccion"]

#             cliente.save()

#             return HttpResponseRedirect('/WebFinal/lista_clientes/')
    
#     else:

#         cliente_edit = Formulario_cliente(initial={
#             "nombre": cliente.nombre,
#             "apellido": cliente.apellido,
#             "telefono": cliente.telefono,
#             "direccion": cliente.direccion,
#         })

#         return render(request, "editarcliente.html", {"cliente_edit": cliente_edit, "id": cliente.id})


# def form_empleado(request):
#     #cuerpo 
#     return render(request, 'form_empleado')


class Empleados(StaffRequiredMixin, CreateView):

    model = Empleado
    form_class = Formulario_empleado
    template_name = 'crea_empleado.html'
    success_url = '/WebFinal/exito_empleado/'
    


def empleado_creado(request):
    avatar = Avatar.objects.get(user=request.user) 
    return render(request, 'exito_empleado.html' ,{'url': avatar.imagen.url})

class MostrarEmpleados(StaffRequiredMixin, ListView):

    model = Empleado
    form_class = Formulario_empleado
    template_name = 'lista_empleados.html'
    context_object_name = "empleados"

class Detalle_Empleado(StaffRequiredMixin, DetailView):

    model = Empleado
    template_name = "detalle_empleado.html"
    context_object_name = "empleado"

class BorraEmpleado(StaffRequiredMixin, DeleteView):

        model = Empleado
        template_name = 'borrarempleado.html'
        success_url = '/WebFinal/lista_empleados'

class EditarEmpleado(StaffRequiredMixin, UpdateView):

    model = Empleado
    template_name = "empleado_update.html"
    fields = ('__all__')
    success_url = '/WebFinal/exito_update_empleado/'

def empleado_actualizado(request):
    avatar = Avatar.objects.get(user=request.user) 
    return render(request, 'exito_update_empleado.html',{'url': avatar.imagen.url})

#BUSQUEDA
def busqueda_empleado(request):
    avatar = Avatar.objects.get(user=request.user) 
    return render(request, 'busqueda_empleado.html', {'url': avatar.imagen.url})

class BuscarEmpleado(StaffRequiredMixin, ListView):
    model = Empleado
    template_name = "busqueda_empleado.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("apellido")
        
        if query=='':
            response = 'Empleado no encontrado'
            HttpResponseRedirect('/WebFinal/resultado_empleado/', {'response':response})
        else:    
            object_list = Empleado.objects.filter(Q(apellido__icontains=query))       
            return (object_list)
# PRODUCTOS

class CrearProducto(LoginRequiredMixin, CreateView):

    model = Productos
    form_class = Formulario_productos
    template_name = 'crea_producto.html'
    success_url = '/WebFinal/exito_producto/'

def productocreado(request):
    avatar = Avatar.objects.get(user=request.user)
    return render(request, 'exito_producto.html', {'url': avatar.imagen.url})

class ListaProductos(ListView):
    
    model = Productos
    form_class = Formulario_productos
    template_name = 'lista_productos.html'
    context_object_name = "productos"

class Detalle_Producto(DetailView):

    model = Productos
    template_name = "detalle_producto.html"
    context_object_name = "producto"

class BorraProducto(LoginRequiredMixin, DeleteView):

        model = Productos
        template_name = 'borrarproducto.html'
        success_url = '/WebFinal/lista_productos'

class EditarProducto(LoginRequiredMixin, UpdateView):

    model = Productos
    template_name = "producto_update.html"
    fields = ('__all__')
    success_url = '/WebFinal/exito_update_producto/'

def producto_actualizado(request):
    avatar = Avatar.objects.get(user=request.user)
    return render(request, 'exito_update_producto.html', {'url': avatar.imagen.url})

#BUSQUEDA
def busqueda_producto(request):
    avatar = Avatar.objects.get(user=request.user) 
    return render(request, 'busqueda_producto.html', {'url': avatar.imagen.url})

class BuscarProducto(ListView):
    model = Productos
    template_name = "busqueda_producto.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("modelo")
        if query=="":
            response = 'Producto no encontrado'
            HttpResponseRedirect('/WebFinal/', {'response':response})
        else:    
            object_list = Productos.objects.filter(Q(modelo__icontains=query))       
            return (object_list)
# def form_productos(request):
#     #cuerpo 

#     return render(request, 'form_productos')

# PROVEEDORES

class CrearProveedor(LoginRequiredMixin, CreateView):

    model = Proveedores
    form_class = Formulario_proveedores
    template_name = 'crea_proveedor.html'
    success_url = '/WebFinal/exito_proveedor/'

def proveedorcreado(request):
    avatar = Avatar.objects.get(user=request.user)
    return render(request, 'exito_proveedor.html', {'url': avatar.imagen.url})

class ListaProveedores(LoginRequiredMixin, ListView):
     

    model = Proveedores
    form_class = Formulario_proveedores
    template_name = 'lista_proveedores.html'
    context_object_name = "proveedores"

    

class Detalle_Proveedor(LoginRequiredMixin, DetailView):

    model = Proveedores
    template_name = "detalle_proveedor.html"
    context_object_name = "proveedor"

class BorraProveedor(LoginRequiredMixin, DeleteView):

        model = Proveedores
        template_name = 'borrarproveedor.html'
        success_url = '/WebFinal/lista_proveedores'

class EditarProveedor(LoginRequiredMixin, UpdateView):

    model = Proveedores
    template_name = "proveedor_update.html"
    fields = ('__all__')
    success_url = '/WebFinal/exito_update_proveedor/'

def proveedor_actualizado(request):
    avatar = Avatar.objects.get(user=request.user) 
    return render(request, 'exito_update_proveedor.html', {'url': avatar.imagen.url})


#BUSQUEDA
def busqueda_proveedor(request):
    avatar = Avatar.objects.get(user=request.user) 
    return render(request, 'busqueda_proveedor.html', {'url': avatar.imagen.url})

class BuscarProveedor(LoginRequiredMixin, ListView):
    model = Proveedores
    template_name = "busqueda_proveedor.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("nombre")
        if query=="":
            response = 'Proveedor no encontrado'
            HttpResponseRedirect('/WebFinal/', {'response':response})
        else:    
            object_list = Proveedores.objects.filter(Q(nombre__icontains=query))       
            return (object_list)

# def form_proveedores(request):
#    #cuerpo 

#     return render(request, 'form_proveedores')

def userlogin(request):

    if request.method=='POST':

        formulario = AuthenticationForm(request, data=request.POST)

        if formulario.is_valid():

            datos = formulario.cleaned_data

            usuario = datos['username']
            psw = datos['password']

            user = authenticate(username=usuario, password=psw)

            if user:

                login(request, user)

                return render(request, 'inicio2.html', {'mensaje': f'Bienvenido {user}'})
            
            else:

                return render(request, 'inicio2.html', {'mensaje': f'Usuario o contraseña incorrectos.'})

        else:

            return render(request, 'inicio2.html', {'mensaje': f'Datos Incorrectos.'})

    else:

        formulario = AuthenticationForm()

        return render(request, 'login.html', {'formulario': formulario})

@method_decorator(staff_member_required)    
def registrar_user(request):

    if request.method == 'POST':
        
        formulario = UserCreationForm(request.POST)

        if formulario.is_valid():

            username = formulario.cleaned_data['username']
            formulario.save()
            return render(request, 'inicio2.html', {'mensaje': f'Usuario "{username}" creado correctamente.'})
        
        else:
            return render(request, 'inicio2.html', {'mensaje': f'Error al crear Usuario. Por favor verifique los datos ingresados.'})
    
    else:

        formulario = UserCreationForm()

        return render(request, 'registro_usuario.html', {'formulario': formulario})

def registro_ventas(request):
    avatar = Avatar.objects.get(user=request.user)
    return render(request, 'registrar_venta.html', {'url': avatar.imagen.url})

def exitoventas(request):
    avatar = Avatar.objects.get(user=request.user) 
    return render(request, 'exito_venta.html', {'url': avatar.imagen.url})

# class Ingreso_venta(LoginRequiredMixin, CreateView):

#     model = Ventas
#     fields = ('venta','detalle')
#     template_name = 'nueva_venta.html'
#     success_url = '/WebFinal/exito_venta/'

class BuscaClienteVenta(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "registrar_venta.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("dni")
        if query=="":
            response = 'Cliente no encontrado'
            HttpResponseRedirect('/WebFinal/inicio2', {'response':response})
        else:

            object_list = Cliente.objects.filter(Q(dni__icontains=query))
        
            return (object_list)

def ingreso_venta(request, pk):
   
    cliente = Cliente.objects.get(pk=pk)

    if request.method == 'POST':

        form = Formulario_ventas(request.POST)

        if form.is_valid():

            datos = form.cleaned_data
            venta = Ventas(cliente_id=pk,detalle=datos['detalle'])
            venta.save()
            venta.venta.set(datos['venta'])
            venta.save()
            return render(request, 'exito_venta.html', {'venta':venta})
        
        return render(request,'nueva_venta.html',{'form':form,'mensaje':"Formulario invalido.",'pk':pk,'cliente':cliente})
    
    else:
        form = Formulario_ventas()
        return render(request, 'nueva_venta.html',{'form':form,'pk':pk, 'cliente':cliente})

        
def form_contacto(request):
    

    if request.method == 'POST':

        asunto = request.POST['asunto']
        mensaje = request.POST['mensaje'] + request.POST['email']
        email_from = settings.EMAIL_HOST_USER
        destinatario = ['consultas_gattone@smallproyecciones.com.ar']

        send_mail(asunto, mensaje, email_from, destinatario)

        return render(request, 'exito_contacto.html')#, {'url': avatar.imagen.url})
    
    return render(request, 'formulario_contacto.html')#, {'url': avatar.imagen.url})

def nosotros(request):
    try:
        avatar = Avatar.objects.get(user=request.user)
        return render(request, 'nosotros.html', {'url': avatar.imagen.url})
    except:
       return render(request, 'nosotros.html')


