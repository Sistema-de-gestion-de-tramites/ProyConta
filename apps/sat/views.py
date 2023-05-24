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
-- ARIO, EN ESTA CLASE IRA EL BACKEND DE LA APLICACION SAT                --
----------------------------------------------------------------------------
"""
from distutils import extension
from email.policy import default
from tokenize import group

from django.db.models import Q
from functools import reduce
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from ..empleados.views import guardarPermisosDeUsuario
from apps.empleados.views import obtenerEmpleadoDeCuentaUsuario, obtenerFotoPerfil

from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.models import Permission, Group,User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required,permission_required
from django.core.mail import send_mail
"""   #Antiguas importaciones 
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect #{LIBRERIA PARA DESPLEGAR(RENDER) LOS HTML}
from django.http import HttpResponse #{LIBRERIA OPERACIONES HTTP}
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import TareaForm #{IMPORTA LOS METODOS DE LA CLASE FORM}
from apps.sat.models import Tarea, Tramite, Empleados, Emp_Clie_Asig
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
"""
#{----------------------------------------------------------------------------------------}
#{METODO PARA DEPLEGAR EL HTML INDEX (HOME)}

def index(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    return render(request,'index.html') #{DEVUELVE EL HTML (REQUEST)}


def inicio(request):  # {METODO REQUEST DE HTTP}
    
    if request.user.is_authenticated:  # valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'inicio','fotoPerfil': obtenerFotoPerfil(request)}
    return render(request, 'menu.html', contexto)  # {DEVUELVE EL HTML (REQUEST)}
def roles(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'roles','fotoPerfil': obtenerFotoPerfil(request)}
    return render(request,'menu.html',contexto) #{DEVUELVE EL HTML (REQUEST)}
def documentos(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'documentos','fotoPerfil': obtenerFotoPerfil(request)}
    return render(request, 'menu.html', contexto) #{DEVUELVE EL HTML (REQUEST)}
def archivos(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'archivos','fotoPerfil': obtenerFotoPerfil(request)}
    return render(request, 'menu.html', contexto) #{DEVUELVE EL HTML (REQUEST)}
def directorio(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'directorio','fotoPerfil': obtenerFotoPerfil(request)}
    return render(request, 'directorio.html', contexto) #{DEVUELVE EL HTML (REQUEST)}
def clientes(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'clientes','fotoPerfil': obtenerFotoPerfil(request)}
    return render(request, 'menu.html', contexto) #{DEVUELVE EL HTML (REQUEST)}
def empleados(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'empleados','fotoPerfil': obtenerFotoPerfil(request)}
    return render(request, 'menu.html', contexto) #{DEVUELVE EL HTML (REQUEST)}


# Vistas de los Estados
def crear_Estado(request):
    if request.method == 'GET':
        contexto = {
            'titulo' : 'Registrar estado o status',
            'form': Formulario_Estado,
            'fotoPerfil': obtenerFotoPerfil(request)}
        return render(request, 'formulario.html', contexto)
    else:
        nuevoRegistro = Estados(
            nombre=request.POST['nombre']
        )
        nuevoRegistro.save()
        return redirect('listar_estados')

def listar_Estados(request):
    lista = Estados.objects.all()
    return render(request, 'plantilla_lista.html', {'titulo':'estados',
                                                    'object_list': lista,
                                                    'actualizar_url': 'editar_estado',
                                                    'borrar_url':'eliminar_estado',
                                                    'fotoPerfil': obtenerFotoPerfil(request)})

class editar_Estado(UpdateView):
    model = Estados
    form_class = Formulario_Estado
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_estados')
    extra_context = {'titulo': 'Editar estado o status'}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

def eliminar_Estado(request, pk):
    registro = get_object_or_404(Estados, id=pk)
    registro.delete()
    return redirect('listar_estados')

# Vistas de los Comentarios
def crear_Comentario(request):
    if request.method == 'GET':
        contexto = {
            'titulo': 'Añadir comentario',
            'form': Formulario_Comentario,
            'fotoPerfil': obtenerFotoPerfil(request)}
        return render(request, 'formulario.html', contexto)
    else:
        nuevoRegistro = Comentarios(
            descr=request.POST['descr']
        )
        nuevoRegistro.save()
        return redirect('listar_comentarios')

def listar_Comentarios(request):
    lista = Comentarios.objects.all()
    return render(request, 'plantilla_lista.html', {'titulo':'comentarios',
                                                    'object_list': lista,
                                                    'actualizar_url': 'editar_comentario',
                                                    'borrar_url':'eliminar_comentario',
                                                    'fotoPerfil': obtenerFotoPerfil(request)})

class editar_Comentario(UpdateView):
    model = Comentarios
    form_class = Formulario_Comentario
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_comentarios')
    extra_context = {'titulo': 'Editar comentario'}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

def eliminar_Comentario(request, pk):
    registro = get_object_or_404(Comentarios, id=pk)
    registro.delete()
    return redirect('listar_comentarios')

# Vistas de los tipo-archivo
def crear_Tipo_Archivo(request):
    if request.method == 'GET':
        contexto = {'titulo':'Registrar extensión de archivos',
                    'form': Formulario_Tipo_Archivo,
                    'fotoPerfil': obtenerFotoPerfil(request)}
        return render(request,'formulario.html',contexto)
    elif request.method=='POST':
        nuevoRegistro = Tipo_Archivos(
            extension = request.POST['extension']
        )
        if(Tipo_Archivos.objects.filter(extension= request.POST['extension']).exists()):
         messages.add_message(request=request,level=messages.ERROR,message="Error el tipo de archivo ya existe",extra_tags='danger')
         return redirect('crear_tipo_archivos')
        else:
         nuevoRegistro.save()
         return redirect('listar_tipo_archivos')

def listar_Tipo_Archivos(request):
    lista = Tipo_Archivos.objects.all()
    return render(request, 'plantilla_lista.html', {'titulo': 'archivos',
                                                    'object_list': lista,
                                                    'actualizar_url': 'editar_tipo_archivo',
                                                    'borrar_url':'eliminar_tipo_archivo',
                                                    'fotoPerfil': obtenerFotoPerfil(request)})

class editar_Tipo_Archivo(UpdateView):
    model = Tipo_Archivos
    form_class = Formulario_Tipo_Archivo
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_tipo_archivos')
    extra_context = {'titulo': 'Editar extensión de archivos'}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

def eliminar_Tipo_Archivo(request, pk):
    registro = get_object_or_404(Tipo_Archivos, id=pk)
    registro.delete()
    return redirect('listar_tipo_archivos')

# Vistas de los Roles
def crear_Rol(request):
    if request.method == 'POST':
        form = Formulario_Rol(request.POST)
        if form.is_valid():
            if(Group.objects.filter(name= request.POST['nombre']).exists()):
                mensajeError="Error el rol ya existe"
                messages.add_message(request=request,level=messages.ERROR,message=mensajeError,extra_tags='danger')
                return redirect('crear_rol')
            elif(request.POST['nombre']=='Empleado'):
                mensajeError="Error no puedes crear un rol con este nombre"
                messages.add_message(request=request,level=messages.ERROR,message=mensajeError,extra_tags='danger')
                return redirect('crear_rol')
            else:
                nuevoRol = Group(name=request.POST['nombre'])
                nuevoRol.save()
                guardarPermisos(nuevoRol,request.POST)
                return redirect('listar_roles')
        else:
         mensajeErrorFormulario ="Complete correctamente el formulario"
         messages.add_message(request=request,level=messages.ERROR,message=mensajeErrorFormulario,extra_tags='danger')
         return redirect('crear_rol')
    else:
        permisosDocumentos = list(Tipo_Documentos.objects.all().values_list('nombre',flat=True))
        contexto = {'titulo': 'Añadir rol',
                    'form': Formulario_Rol,
                    'permisosDocumentos': permisosDocumentos,
                    'fotoPerfil': obtenerFotoPerfil(request)}
    if(Permission.objects.filter(codename__contains="dev_").count()==0):
        mensajeErrorFormulario= "No existen permisos registrados, por favor crearlos primero"
        messages.add_message(request=request,level=messages.WARNING,message=mensajeErrorFormulario)
        contexto.update({'listaFieldsM2M': [('permissions','permisos')]})
    return render(request,'formulario_roles.html',contexto)


def guardarPermisos(modeloGroup,post):
    rol = Group.objects.get(id=modeloGroup.id)
    permisos = []
    for campo in post:
        if(post[campo]=='1'):
            permisos.append(Permission.objects.get(codename=campo))
        elif(campo=='permisos'):
            for permisoID in post.getlist(campo, default=[]):
                permisos.append(Permission.objects.get(id=permisoID))
    rol.permissions.set(permisos)
    modeloGroup.save()

def listar_Roles(request):
    lista = Group.objects.all()
    contexto = {'titulo': 'roles',
                'object_list': lista,
                'actualizar_url': 'editar_rol',
                'borrar_url':'eliminar_rol',
                'detalle_url':'detalle_roles',
                'rol':True,
                'fotoPerfil': obtenerFotoPerfil(request)}
    return render(request, 'plantilla_lista.html', contexto)

def detalle_roles(request, pk):
    objeto = get_object_or_404(Group,id=pk)
    lista_1 = list(objeto.permissions.filter(codename__contains="dev_").values_list('name',flat=True))
    lista_2 = list(objeto.permissions.filter(codename__contains="doc_").values_list('name',flat=True))
    informacionObjecto = [
        ('Nombre',objeto.name)
    ]
    context = {
        'titulo': 'Rol',
        'obj': objeto,
        'informacionObjecto': informacionObjecto,
        'listas_extra': [{'titulo': 'Permisos', 'lista': lista_1},
                         {'titulo': 'Permisos sobre documento', 'lista': lista_2}
                        ],
        'editar_url': 'editar_rol',
        'fotoPerfil': obtenerFotoPerfil(request)
    }
    return render(request, 'plantilla_detalle.html', context)

def editar_Rol(request,pk):
    rol = Group.objects.get(id=pk)
    if request.method == 'POST':
        form = Formulario_Rol(request.POST)
        if form.is_valid():
            if(Group.objects.filter(name= request.POST['nombre']).exists() and rol.name != request.POST['nombre']):
                messages.add_message(request=request,level=messages.ERROR,message="Error el rol ya existe",extra_tags='danger')
                return redirect('editar_rol',pk)
            else:
                rol.name=request.POST['nombre']
                rol.permissions.clear()
                rol.save()
                guardarPermisos(rol,request.POST)
                editarPermisosDeRoleEnUsuarios(rol)
                return redirect('listar_roles')
        else:
         mensajeErrorFormulario ="Complete correctamente el formulario"
         messages.add_message(request=request,level=messages.ERROR,message=mensajeErrorFormulario,extra_tags='danger')
         return redirect('editar_rol',pk)
    else:
        permisos = list(rol.permissions.filter(codename__contains="dev_").values_list('pk',flat=True))
        initialValues = {'nombre':rol.name,'permisos':permisos}
        permisosDocumentos = list(Tipo_Documentos.objects.all().values_list('nombre',flat=True))
        permisosDocumentosSelecionados = list(rol.permissions.filter(codename__contains="doc_").values_list('codename',flat=True))
        contexto = {'titulo': 'Editar rol',
                    'form': Formulario_Rol(initial=initialValues),
                    'permisosDocumentos':permisosDocumentos,
                    'seleccionados':permisosDocumentosSelecionados,
                    'fotoPerfil': obtenerFotoPerfil(request)}
    if(Permission.objects.filter(codename__contains="dev_").count()==0):
        mensajeErrorFormulario= "No existen permisos registrados, por favor crearlos primero"
        messages.add_message(request=request,level=messages.WARNING,message=mensajeErrorFormulario)
        contexto.update({'listaFieldsM2M': [('permissions','permisos')]})
    return render(request,'formulario_roles.html',contexto)
    

def eliminar_Rol(request, pk):
    registro = get_object_or_404(Group, id=pk)
    if registro.name != 'Administrador':
        registro.delete()
    actualizarPermisosEnUsuarios()
    return redirect('listar_roles')

def editarPermisosDeRoleEnUsuarios(rol):
    usuarios = User.objects.filter(groups=rol)
    for usuario in usuarios:
        print(usuario.groups.all().values_list('id',flat=True))
        guardarPermisosDeUsuario(usuario,usuario.groups.all().values_list('id',flat=True))

def actualizarPermisosEnUsuarios():
    usuarios = User.objects.all()
    for usuario in usuarios:
        print(usuario.groups.all().values_list('id',flat=True))
        guardarPermisosDeUsuario(usuario,usuario.groups.all().values_list('id',flat=True))        
# vista de documento

def crearTipoDocumento(request):
    if request.method == 'POST':
        form = Formulario_tipoDocumento(request.POST)
        if form.is_valid():
            if(Tipo_Documentos.objects.filter(nombre= request.POST['nombre']).exists()):
                messages.add_message(request=request,level=messages.ERROR,message="Error el documento ya existe",extra_tags='danger')
                return redirect('crear_tipo_documento')
            else:
                nuevoTipoArchivo = form.save(commit=False)
                nuevoTipoArchivo.save()
                form.save_m2m()
                cont_type = ContentType.objects.get(id=1)
                permisoEditar = Permission(name="Edicion "+request.POST['nombre'],codename="doc_edicion_"+request.POST['nombre'],content_type=cont_type)
                permisoEditar.save()
                permisoVer = Permission(name="Ver "+request.POST['nombre'],codename="doc_ver_"+request.POST['nombre'],content_type=cont_type)
                permisoVer.save()
            return redirect('listar_tipo_documento')
        else:
         mensajeErrorFormulario ="Complete correctamente el formulario"
         messages.add_message(request=request,level=messages.ERROR,message=mensajeErrorFormulario,extra_tags='danger')
         return redirect('crear_tipo_documento')
    else:
        contexto = {'titulo': 'Registrar documento',
                    'form': Formulario_tipoDocumento,
                    'fotoPerfil': obtenerFotoPerfil(request)}
    if(Tipo_Archivos.objects.all().count()==0):
        mensajeErrorFormulario= "No existen tipos de archivos registrados, por favor crearlos primero"
        messages.add_message(request=request,level=messages.WARNING,message=mensajeErrorFormulario)
        contexto.update({'listaFieldsM2M': [('archivos','crear_tipo_archivos')]})
    return render(request,'formulario.html',contexto)

def listar_tipoDocumento(request):
   lista = Tipo_Documentos.objects.all()
   contexto =  {'object_list' : lista,
                'titulo': 'documentos',
                'actualizar_url': 'editar_tipo_documento',
                'borrar_url':'eliminar_tipo_documento',
                'detalle_url':'detalle_tipo_documento',
                'fotoPerfil': obtenerFotoPerfil(request)}

   return render(request, 'plantilla_lista.html', contexto)

def detalle_tipoDocumento(request, pk):
    objeto = Tipo_Documentos.objects.get(id=pk)
    lista_1 = objeto.archivos.all()
    context = {
        'titulo': 'Documento',
        'obj': objeto,
        'listas_extra': [{'titulo': 'Extensiones validas', 'lista': lista_1},
                        ],
        'editar_url': 'editar_tipo_documento',
        'fotoPerfil': obtenerFotoPerfil(request)
    }
    return render(request, 'plantilla_detalle.html', context)

class editar_tipoDocumento(UpdateView):
    model = Tipo_Documentos
    form_class = Formulario_tipoDocumento
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_tipo_documento')
    extra_context = {'titulo': 'Editar documento'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context
    
    def form_valid(self, form, **kwargs):
        registro = form.save(commit=False)
        try:
            nombreAntiguo =  str(Tipo_Documentos.objects.get(id=self.object.id).nombre)
        except Tipo_Documentos.DoesNotExist:
            mensajeError ="Error al obtener el objecto.Por favor vuelve a intentarlo o reporta el error"
            messages.add_message(request=self.request,level=messages.WARNING,message=mensajeError,extra_tags='danger')
            return redirect('editar_tipo_documento',self.object.id)
        try:    
            permisoEdicion = Permission.objects.get(codename='doc_edicion_' + nombreAntiguo)
        except Permission.DoesNotExist:
            mensajeError ="Error al actualizar los permisos.Por favor vuelve a intentarlo o reporta el error"
            messages.add_message(request=self.request,level=messages.WARNING,message=mensajeError,extra_tags='danger')
            return redirect('editar_tipo_documento',self.object.id)
        permisoEdicion.name = "Edicion "+ self.request.POST['nombre']
        permisoEdicion.codename = 'doc_edicion_' + self.request.POST['nombre']
        permisoEdicion.save()
        try:
            permisoVer = Permission.objects.get(codename='doc_ver_' + nombreAntiguo)
        except Permission.DoesNotExist:
            mensajeError ="Error al actualizar los permisos.Por favor vuelve a intentarlo o reporta el error"
            messages.add_message(request=self.request,level=messages.WARNING,message=mensajeError,extra_tags='danger')
            return redirect('editar_tipo_documento',self.object.id)
        permisoVer.name = "Ver " + self.request.POST['nombre']
        permisoVer.codename = 'doc_ver_' + self.request.POST['nombre']
        permisoVer.save()
        registro.save()
        return super().form_valid(form)

def eliminar_TipoDocumento(request, pk):
    registro = get_object_or_404(Tipo_Documentos, id=pk)
    registro.delete()
    nombre= registro.nombre
    permisos = Permission.objects.filter(codename__contains=nombre)
    permisos.delete()
    return redirect('listar_tipo_documento')


# Buscador
def buscar(request):
    lista = request.GET.get('q').split()

    titulo_1 = 'Documentos'
    lista_1 = Tipo_Documentos.objects.all()
    titulo_2 = 'Usuarios'
    lista_2 = Personas.objects.all()
    titulo_3 = 'Archivos'
    lista_3 = Entrega_Doc.objects.all()


    if lista:
        queries_1 = [Q(nombre__icontains=busqueda) for busqueda in lista]
        lista_1 = lista_1.filter(reduce(lambda x, y: x | y, queries_1))

        queries_2 = [Q(nombre__icontains=busqueda) for busqueda in lista]
        queries_2.extend([Q(ap_paterno__icontains=busqueda) for busqueda in lista])
        queries_2.extend([Q(ap_materno__icontains=busqueda) for busqueda in lista])
        queries_2.extend([Q(correo__icontains=busqueda) for busqueda in lista])
        queries_2.extend([Q(curp__icontains=busqueda) for busqueda in lista])
        queries_2.extend([Q(rfc__icontains=busqueda) for busqueda in lista])
        queries_2.extend([Q(correo__icontains=busqueda) for busqueda in lista])
        queries_2.extend([Q(telefonos__telefono__icontains=busqueda) for busqueda in lista])
        lista_2 = lista_2.filter(reduce(lambda x, y: x | y, queries_2))

        queries_3 = [Q(cliente__nombre__icontains=busqueda) for busqueda in lista]
        queries_3.extend([Q(empleado__nombre__icontains=busqueda) for busqueda in lista])
        queries_3.extend([Q(tipo_doc__nombre__icontains=busqueda) for busqueda in lista])
        queries_3.extend([Q(estado__nombre__icontains=busqueda) for busqueda in lista])
        lista_3 = lista_3.filter(reduce(lambda x, y: x | y, queries_3))

    contexto = [{'object_list': lista_1, 'titulo': titulo_1, 'lista_url': 'listar_documentos'},
                {'object_list': lista_2, 'titulo': titulo_2, 'lista_url': 'detalle_persona'},
                {'object_list': lista_3, 'titulo': titulo_3, 'lista_url': 'detalle_documento'},
                ]

    return render(request, 'buscador.html', {'contexto': contexto,
                                             'fotoPerfil': obtenerFotoPerfil(request)})

# VISTA: funciona para la vista de soporte tecnico
#DESCRIPCION: se utiliza el core de email de Django para enviar
# un correo de soporte con remitente: soporte.satra@gmail.com
# al correo destino: satra.itq@gmail.com
def soporteTecnico(request):
    
    if request.method == 'GET':
        form = FormularioEmail
        contexto = {'form':form,'titulo':'correo a soporte tecnico'}
        return render(request,'formulario.html',contexto)
    else:
        form = FormularioEmail(request.POST)
        if form.is_valid():
            remitente = 'REMITENTE: ' + request.POST['email'] +'\n'
            send_mail(
                'SOPORTE: '+request.POST['asunto'],
                remitente + request.POST['texto'],
                'soporte.satra@gmail.com',
                ['satra.itq@gmail.com'],
                fail_silently=False)
            mensaje ="correo enviado con exito"
            messages.add_message(request=request,level=messages.SUCCESS,message=mensaje)
        else:
            mensaje ="Error verifica que los campos solicitados esten llenados de forma correcta"
            messages.add_message(request=request,level=messages.ERROR,message=mensaje,extra_tags='danger')
        return redirect('enviar_email')