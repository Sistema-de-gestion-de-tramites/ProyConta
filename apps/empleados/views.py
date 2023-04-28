"""
----------------------------------------------------------------------------
--          LISTA DE VIEWS PARA MANEJO DE ARCHIVOS HTML                    --
--              (ARCHIVO VIEWS DE APLICACION SAT)                          --
--               VERSION 0.2    31/10/22                                  --
--                  JOSE GERARDO LOPEZ ARROYO                            --
----------------------------------------------------------------------------
____________________________________________________________________________
----------------------------------------------------------------------------
-- >Explicacion: CLASE VIEW DESARROLLA LOS METODOS QUE LE MOSTRARA AL USU --
-- ARIO, EN ESTA CLASE IRA EL BACKEND DE LA APLICACION EMPLEADOS                --
----------------------------------------------------------------------------
"""
from email.policy import default
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import PermissionDenied

#from apps.empleados.forms import EmpleadoForm
from apps.clientes.forms import PersonaForm
from apps.empleados.forms import RegistroUsuarioForm
from apps.empleados.models import Personas
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

#{----------------------------------------------------------------------------------------}

def id_emp_sesion(request):
    empleados = Personas.objects.all()    # Especificar a solo los empleados con el rol = 0
    for emp in empleados:
        if emp.username == request.user.username:
            id=request.user.username
            break
    return id

#{----------------------------------------------------------------------------------------}

# Listar todos los registros
class Listar_Personas(PermissionRequiredMixin,ListView):
    permission_required = 'editor.dev_ver_empleados'
    permission_required = 'editor.dev_ver_clientes'
    queryset = Personas.objects.all()
    template_name = 'plantilla_lista.html'

# Listar solo los empleados
class Listar_Empleados(PermissionRequiredMixin,ListView):
    permission_required = 'editor.dev_ver_empleados'
    queryset = Personas.objects.raw('SELECT * FROM `personas` WHERE `tipo_usuario_id` = 1 ')
    template_name = 'plantilla_lista.html'
    extra_context={'titulo':'empleados','actualizar_url': 'actualizar_empleado', 'borrar_url':'eliminar_empleado'}

class Empleado_Delete(PermissionRequiredMixin,UpdateView):
    permission_required = 'editor.dev_eliminar_empleados'
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_empleados')

class Empleado_Update(PermissionRequiredMixin,UpdateView):
    permission_required = 'editor.dev_editar_empleados'
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_empleados')
    
def registro(request):
    if(request.user.has_perm("editor.dev_crear_usuario")):
        if request.method == 'GET':
            form = RegistroUsuarioForm
            return render(request,'registro.html',{'form':form})
        else:
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                nuevoUsuario = form.save()
                listaRoles = request.POST.getlist('roles',default=[])
                guardarPermisosDeUsuario(nuevoUsuario,listaRoles)
                messages.add_message(request=request,level=messages.SUCCESS,message="Registro Exitoso")
                redirect('registro/')
            else:
                messages.add_message(request=request,level=messages.ERROR,message="Datos invalidos",extra_tags="danger")
                redirect('registro/')
        return render(request,'registro.html',{'form':form})
    else:
        raise PermissionDenied

def guardarPermisosDeUsuario(usuarioModelo,listaRoles):
    listaModeloRoles = []
    for rol in listaRoles:
        try:
            rolModelo = Group.objects.get(id=rol)
            if rolModelo.name == 'Administrador':
                usuarioModelo.is_staff = True
                usuarioModelo.is_superuser = True
            listaModeloRoles.append(rolModelo)
        except Group.DoesNotExist:
            print("Error rol no encontrado")
    if len(listaModeloRoles)==1:
        usuarioModelo.groups.remove(listaModeloRoles[0])
        usuarioModelo.groups.add(listaModeloRoles[0])
    else:
        usuarioModelo.groups.set(listaModeloRoles)
    usuarioModelo.save()
    listaRolesDeUsuario = usuarioModelo.groups.all()
    listaPermisos = []
    for rolDeUsuario in listaRolesDeUsuario:
        permisos = list(rolDeUsuario.permissions.all().values_list('pk',flat=True))
        listaPermisos = list(set(listaPermisos+permisos))
    usuarioModelo.user_permissions.set(listaPermisos)
    usuarioModelo.save()




