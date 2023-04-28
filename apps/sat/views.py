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
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from ..empleados.views import guardarPermisosDeUsuario

from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.models import Permission, Group,User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required,permission_required
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
    contexto = {'titulo': 'inicio'}
    return render(request, 'menu.html', contexto)  # {DEVUELVE EL HTML (REQUEST)}
def roles(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'roles'}
    return render(request,'menu.html',contexto) #{DEVUELVE EL HTML (REQUEST)}
def documentos(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'documentos'}
    return render(request, 'menu.html', contexto) #{DEVUELVE EL HTML (REQUEST)}
def archivos(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'archivos'}
    return render(request, 'menu.html', contexto) #{DEVUELVE EL HTML (REQUEST)}
def directorio(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'directorio'}
    return render(request, 'directorio.html', contexto) #{DEVUELVE EL HTML (REQUEST)}
def clientes(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'clientes'}
    return render(request, 'menu.html', contexto) #{DEVUELVE EL HTML (REQUEST)}
def empleados(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    contexto = {'titulo': 'empleados'}
    return render(request, 'menu.html', contexto) #{DEVUELVE EL HTML (REQUEST)}

#{----------------------------------------------------------------------------------------}
# DESCRIPCION: Devuelve el id del empleado que ha iniciado sesion (no se valida que exista una sesion activa)
def id_emp_sesion(request):
    empleados = Personas.objects.all() # Empleados son el rol = 0
    usernameValue=''
    for emp in empleados:
     if emp.username == request.user.username:
        usernameValue=request.user.username
        break
    empleado= Personas.objects.get(username=usernameValue) # Empleados son el rol = 0, pero creo que aqui ya no se requiere cambiar
    id = empleado.empleado_id
    return id
#{----------------------------------------------------------------------------------------}

#{----------------------------------------------------------------------------------------}
"""
class Tarea_Create(CreateView):
    #model = Tarea
    form_class = TareaForm
    template_name = 'formulario_2.html'
    success_url = reverse_lazy('lista_tareas')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        print(request.POST)
        form = self.form_class(request.POST,request.FILES)
        form.emp_creador.to_python()
        if form.is_valid() and request.FILES['archivo']:
            form.save(commit=False)
            file = request.FILES['archivo']
            fs = FileSystemStorage()
            cliente = Emp_Clie_Asig.objects.get(id=request.POST['emp_clie']).empleado.empleado_id
            fs.location = fs.location + "\\" + str(cliente)
            print(fs.location)
            fs.save(str(file.name),file)
            uploaded_file_url = fs.location
            form.save().dir_archivo= str(uploaded_file_url)
            print(form)
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class Tarea_Listar(ListView):
    model = Tarea
    template_name = 'tables.html'

class Tarea_Update(UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'formulario_2.html'
    success_url = reverse_lazy('lista_tareas')

class Tarea_Delete(DeleteView):
    model = Tarea
    template_name = 'borrar.html'
    success_url = reverse_lazy('lista_tareas')
"""

#{----------------------------------------------------------------------------------------}

# Vistas de los Estados
def crear_Estado(request):
    if request.method == 'GET':
        contexto = {
            'titulo' : "Estados",
            'form': Formulario_Estado}
        return render(request, 'formulario.html', contexto)
    else:
        nuevoRegistro = Estados(
            nombre=request.POST['nombre']
        )
        nuevoRegistro.save()
        return redirect('listar_estados')

def listar_Estados(request):
    lista = Estados.objects.all()
    return render(request, 'plantilla_lista.html', {'titulo':'Estados', 'object_list': lista, 'actualizar_url': 'editar_estado', 'borrar_url':'eliminar_estado'})

class editar_Estado(UpdateView):
    model = Estados
    form_class = Formulario_Estado
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_estados')

def eliminar_Estado(request, pk):
    registro = get_object_or_404(Estados, id=pk)
    registro.delete()
    return redirect('listar_estados')

# Vistas de los Comentarios
def crear_Comentario(request):
    if request.method == 'GET':
        contexto = {
            'titulo':"Comentarios",
            'form': Formulario_Comentario}
        return render(request, 'formulario.html', contexto)
    else:
        nuevoRegistro = Comentarios(
            descr=request.POST['descr']
        )
        nuevoRegistro.save()
        return redirect('listar_comentarios')

def listar_Comentarios(request):
    lista = Comentarios.objects.all()
    return render(request, 'plantilla_lista.html', {'titulo':'Comentarios', 'object_list': lista, 'actualizar_url': 'editar_comentario', 'borrar_url':'eliminar_comentario'})

class editar_Comentario(UpdateView):
    model = Comentarios
    form_class = Formulario_Comentario
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_comentarios')

def eliminar_Comentario(request, pk):
    registro = get_object_or_404(Comentarios, id=pk)
    registro.delete()
    return redirect('listar_comentarios')

# Vistas de los tipo-archivo
def crear_Tipo_Archivo(request):
    if request.method=='GET':
        contexto = {'form': Formulario_Tipo_Archivo}
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
    return render(request, 'plantilla_lista.html', {'titulo': 'archivos','object_list': lista, 'actualizar_url': 'editar_tipo_archivo', 'borrar_url':'eliminar_tipo_archivo'})

class editar_Tipo_Archivo(UpdateView):
    model = Tipo_Archivos
    form_class = Formulario_Tipo_Archivo
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_tipo_archivos')

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
                messages.add_message(request=request,level=messages.ERROR,message="Error el rol ya existe",extra_tags='danger')
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
        contexto = {'form': Formulario_Rol,
                    'permisosDocumentos':permisosDocumentos}
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
                'rol':True}
    return render(request, 'plantilla_lista.html', contexto)

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
                editarPermisosDeRolesEnUsuarios(rol)
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
        contexto = {'form': Formulario_Rol(initial=initialValues),
                    'permisosDocumentos':permisosDocumentos,
                    'seleccionados':permisosDocumentosSelecionados,}
    if(Permission.objects.filter(codename__contains="dev_").count()==0):
        mensajeErrorFormulario= "No existen permisos registrados, por favor crearlos primero"
        messages.add_message(request=request,level=messages.WARNING,message=mensajeErrorFormulario)
        contexto.update({'listaFieldsM2M': [('permissions','permisos')]})
    return render(request,'formulario_roles.html',contexto)
    

def eliminar_Rol(request, pk):
    registro = get_object_or_404(Group, id=pk)
    if registro.name != 'Administrador':
        registro.delete()
    return redirect('listar_roles')

def editarPermisosDeRolesEnUsuarios(rol):
    usuarios = User.objects.filter(groups=rol)
    for usuario in usuarios:
        usuario.groups.remove(rol)
        guardarPermisosDeUsuario(usuario,[rol.id])
        
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
        contexto = {'form': Formulario_tipoDocumento}
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
                'detalle_url':'detalle_tipo_documento'}

   return render(request, 'plantilla_lista.html', contexto)

def detalle_tipoDocumento(request, pk):
    objeto = Tipo_Documentos.objects.get(id=pk)
    lista_1 = objeto.archivos.all()
    context = {
        'obj': objeto,
        'listas_extra': [{'titulo': 'Extensiones validas', 'lista': lista_1},
                        ],
        'editar_url': 'editar_tipo_documento',
    }
    return render(request, 'plantilla_detalle.html', context)

class editar_tipoDocumento(UpdateView):
    model = Tipo_Documentos
    form_class = Formulario_tipoDocumento
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_tipo_documento')

def eliminar_TipoDocumento(request, pk):
    registro = get_object_or_404(Tipo_Documentos, id=pk)
    registro.delete()
    nombre= registro.nombre
    permisos = Permission.objects.filter(codename__contains=nombre)
    permisos.delete()
    return redirect('listar_tipo_documento')


# Buscador
def buscar(request):
    busqueda = request.GET.get('q')

    titulo_1 = 'Documentos'
    lista_1 = Tipo_Documentos.objects.all()
    titulo_2 = 'Usuarios'
    lista_2 = Personas.objects.all()
    lista_3 = Telefonos.objects.all()


    if busqueda:
        lista_1 = Tipo_Documentos.objects.filter(nombre__icontains=busqueda)
        lista_2 = Personas.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(ap_paterno__icontains=busqueda) |
            Q(ap_materno__icontains=busqueda)
        )
        lista_3 = Telefonos.objects.filter(
            Q(descr__icontains=busqueda) |
            Q(telefono__icontains=busqueda)
        )

    contexto = [{'object_list': lista_1, 'titulo': titulo_1},
                {'object_list': lista_2, 'titulo': titulo_2},
                {'object_list': lista_3, 'titulo': 'telefonos'},
                ]

    return render(request, 'buscador.html', {'contexto': contexto})
