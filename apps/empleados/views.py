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
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import Permission, Group,User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.conf import settings
import os

#from apps.empleados.forms import EmpleadoForm
from apps.clientes.forms import PersonaForm
from apps.empleados.forms import *
from apps.empleados.models import *
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from apps.sat.models import Usuario_empleado

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
    queryset = Personas.objects.filter(tipo_usuario__descr="Empleado")
    template_name = 'plantilla_lista.html'
    extra_context={'titulo':'empleados','actualizar_url': 'actualizar_empleado', 'borrar_url':'eliminar_empleado'}

class Empleado_Delete(PermissionRequiredMixin,DeleteView):
    permission_required = 'editor.dev_eliminar_empleados'
    model = Personas
    template_name = 'borrar.html'
    success_url = reverse_lazy('listar_empleados')

class Empleado_Update(PermissionRequiredMixin,UpdateView):
    permission_required = 'editor.dev_editar_empleados'
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_empleados')
    extra_context = {'esEmpleado': True, 'titulo': 'empleados'}

    def form_valid(self, form):
        registro = form.save(commit=False)
        try:
            tipoEmpleado = Tipo_Usuarios.objects.filter(descr__icontains="Empleado").first()
            registro.tipo_usuario_id = tipoEmpleado.pk
        except Tipo_Usuarios.DoesNotExist:
            print("Error al obtener el tipo empleado")
        registro.save()
        return super().form_valid(form)

# CRUD cuentas de usuario

#crear usuario
@permission_required('auth.dev_crear_usuario')   
def registro(request):
        if request.method == 'GET':
            form = RegistroUsuarioForm
            #form.listaRolesDisponibles = Group.objects.all()
            noHayRoles = Group.objects.all().exclude(name="Administrador").exists()
            if noHayRoles:
                sinRegistros=False
            else:
                sinRegistros=True 
            return render(request,'registro.html',{'form':form,'sinResgistros':sinRegistros})
        else:
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                nuevoUsuario = form.save()
                listaRoles = request.POST.getlist('roles',default=[])
                guardarUsuarioDeEmpleado(request.POST,nuevoUsuario)
                guardarPermisosDeUsuario(nuevoUsuario,listaRoles)
                messages.add_message(request=request,level=messages.SUCCESS,message="Registro Exitoso")
                redirect('registro/')
            else:
                messages.add_message(request=request,level=messages.ERROR,message="Datos invalidos",extra_tags="danger")
                redirect('registro/')
        return render(request,'registro.html',{'form':form})

def guardarUsuarioDeEmpleado(post,usuario):
    try:
        empleado = Personas.objects.get(id=post['empleado'])
    except:
        return redirect('registro/')
    usuario.email=empleado.correo
    usuario.save()
    nuevoUsuario_Empleado = Usuario_empleado(
        empleado = empleado,
        usuario = usuario
    )
    nuevoUsuario_Empleado.save()
    

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
    usuarioModelo.groups.clear()
    usuarioModelo.groups.set(listaModeloRoles)
    usuarioModelo.save()
    listaRolesDeUsuario = usuarioModelo.groups.all()
    listaPermisos = []
    for rolDeUsuario in listaRolesDeUsuario:
        permisos = list(rolDeUsuario.permissions.all().values_list('pk',flat=True))
        listaPermisos = list(set(listaPermisos+permisos))
    usuarioModelo.user_permissions.clear()
    usuarioModelo.user_permissions.set(listaPermisos)
    usuarioModelo.save()

#listar usuarios
class Listar_Usuarios(PermissionRequiredMixin,ListView):
    permission_required = 'auth.dev_ver_usuario'
    queryset = Usuario_empleado.objects.all()
    template_name = 'plantilla_lista.html'
    extra_context={'titulo':'Cuentas de usuario','actualizar_url': 'actualizar_usuario', 'borrar_url':'eliminar_usuario'}

#eliminar usuario
class Usuario_Delete(PermissionRequiredMixin,DeleteView):
    permission_required = 'auth.dev_eliminar_usuario'
    model = User
    template_name = 'borrar.html'
    success_url = reverse_lazy('listar_cuentas_usuario')

#actualizar usuario
class usuario_Update(PermissionRequiredMixin,UpdateView):
    permission_required = 'auth.dev_editar_usuario'
    model = User
    form_class = ActualizarUsuarioForm
    template_name = 'registro.html'
    success_url = reverse_lazy('listar_cuentas_usuario')

    def form_valid(self, form):
        cuentaUsuario = form.save(commit=False)
        usuario_empleado = get_object_or_404(Usuario_empleado, usuario=self.object)
        usuario_empleado.empleado = get_object_or_404(Personas, id=self.request.POST['empleado'])
        guardarPermisosDeUsuario(usuario_empleado.usuario,self.request.POST.getlist('roles',default=[]))
        usuario_empleado.save()
        cuentaUsuario.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        usuario_empleado = get_object_or_404(Usuario_empleado, usuario=self.object)
        roles = list(usuario_empleado.usuario.groups.all())
        form.fields['empleado'].initial = usuario_empleado.empleado
        form.fields['roles'].initial = roles
        context['empleado'] = usuario_empleado
        context['titulo'] = 'Usuarios'
        context['form'] = form
        return context

#actualizar contraseña usuario
class usuario_contrasenia_Update(PermissionRequiredMixin,UpdateView):
    permission_required = 'auth.dev_editar_usuario'
    model = User
    form_class = ActualizarContraseniaUsuarioForm
    template_name = 'registro.html'
    success_url = reverse_lazy('listar_cuentas_usuario')

    def form_valid(self, form):
        cuentaUsuario = form.save(commit=False)
        cuentaUsuario.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        usuario_empleado = get_object_or_404(Usuario_empleado, usuario=self.object)
        form.fields['empleado'].initial = usuario_empleado.empleado
        context['empleado'] = usuario_empleado
        context['titulo'] = 'Usuarios'
        context['esActualizarContrasenia'] = True
        context['form'] = form
        return context

def PerfilEmpleado(request):
    informacionEmpleado = obtenerEmpleadoDeCuentaUsuario(request.user)
    if request.method == 'GET':
        informacionCuentaUsuario = [("Nombre de usuario: " + str(request.user.username)),
                                    ("Ultimo acceso: " + str(request.user.last_login)),
                                    ("Fecha de creacion: " + str(request.user.date_joined))]
        
        informacionRoles = request.user.groups.all
        informacionPermisos = request.user.user_permissions.all().values_list('name',flat=True)
        
        if informacionEmpleado != request.user:
            formularioFoto = imagenPerfilForm()
            if str(informacionEmpleado.foto_perfil) != '':
                fotoPerfil = informacionEmpleado.foto_perfil
            else:
                fotoPerfil = False
        else:
            formularioFoto = False
        context = {
            'obj': informacionEmpleado,
            'listas_extra': [{'titulo': 'Informacion de cuenta', 'lista': informacionCuentaUsuario},
                            {'titulo': 'Mis roles', 'lista': informacionRoles},
                            {'titulo': 'Mis Permisos', 'lista': informacionPermisos}
                            ],
            'fotoPerfilForm': formularioFoto,
            'fotoPerfil': fotoPerfil
            
        }
        return render(request, 'plantilla_detalle.html', context)
    else: 
        formularioFoto = imagenPerfilForm(request.POST,request.FILES)
        if formularioFoto.is_valid():

            archivo = formularioFoto.cleaned_data['imagen']
            # Prepara el nombre del archivo y lo normaliza
            base, extension = os.path.splitext(archivo.name)
            base = slugify(base)
            nombre_archivo = base + extension
            # Define el sistema de archivos para guardar el archivo
            carpeta = str(settings.MEDIA_ROOT) + '/fotos_perfil'
            fs = FileSystemStorage(location=carpeta)

            # Si el archivo ya existe, agrega un sufijo numérico al nombre para evitar colisiones
            i = 0
            while fs.exists(nombre_archivo):
                i += 1
                nombre_archivo = f"{base}_{i}{extension}"

            # Guarda el archivo en el sistema de archivos
            fs.save(nombre_archivo, archivo)
            
            if str(informacionEmpleado.foto_perfil) != '':
                file_path = os.path.join(settings.MEDIA_ROOT, str(informacionEmpleado.foto_perfil))
                default_storage.delete(file_path)
            
            # Establece el nombre del archivo en el modelo antes de guardarlo
            informacionEmpleado.foto_perfil = 'fotos_perfil' + '/' + str(nombre_archivo)
            informacionEmpleado.save()
        else:
            print('no valido')
        return redirect('perfil')

def obtenerEmpleadoDeCuentaUsuario(cuentaUsuario):
    try:
        relacionUsuarioEmpleado = Usuario_empleado.objects.get(usuario=cuentaUsuario)
        empleado = relacionUsuarioEmpleado.empleado
    except Usuario_empleado.DoesNotExist:
        return cuentaUsuario
    
    return empleado

def obtenerFotoPerfil(request):
    empleado = obtenerEmpleadoDeCuentaUsuario(request.user)
    if empleado != request.user:
            if str(empleado.foto_perfil) != '':
                return empleado.foto_perfil
            else:
                return False
    else:
        return False