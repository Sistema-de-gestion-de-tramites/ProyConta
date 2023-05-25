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
from tkinter import E
from django.http import HttpResponseRedirect, HttpResponse, Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required,login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied

from .forms import *   #{IMPORTA LOS METODOS DE LA CLASE FORM}
import os
from .cifrado import AES
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import SuspiciousFileOperation
from django.forms.models import model_to_dict
from apps.clientes.models import Personas, Telefonos, Direcciones
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from apps.empleados.views import obtenerEmpleadoDeCuentaUsuario, obtenerFotoPerfil
from django.contrib.auth.decorators import permission_required


class Crear_Persona(PermissionRequiredMixin,CreateView):
    permission_required = ['sat.dev_crear_empleados', 'sat.dev_crear_clientes']
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_clientes')

    def form_invalid(self, form):
        # Acceder a los errores del formulario
        errores = form.errors

        context = self.get_context_data(form=form, errores=errores)
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        registro = form.save(commit=False)
        if self.kwargs.get('pk') == '1':
            self.success_url = reverse_lazy('listar_empleados')
            try:
                tipoEmpleado = Tipo_Usuarios.objects.filter(descr__icontains="Empleado").first()
                registro.tipo_usuario_id = tipoEmpleado.pk
            except Tipo_Usuarios.DoesNotExist:
                print("Error al obtener el tipo empleado")
        return super().form_valid(form)

    # Formulario del empleado
    def get_form_emp(self, form_class=None):
        form = super().get_form(form_class)
        tipoEmpleado = get_object_or_404(Tipo_Usuarios, descr__icontains="Empleado")
        form.fields['tipo_usuario'].initial = tipoEmpleado
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('pk') == '1':
            context['esEmpleado'] = True
            context['titulo'] = 'Registrar empleado'
            context['form'] = self.get_form_emp()
        else:
            context['esEmpleado'] = False
            context['titulo'] = 'Registrar cliente'
            context['form'] = self.get_form()
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

# Listar solo los clientes
class Listar_Clientes(PermissionRequiredMixin,ListView):
    permission_required = 'sat.dev_ver_clientes'
    queryset = Personas.objects.exclude(tipo_usuario__descr="Empleado")
    template_name = 'plantilla_lista.html'
    extra_context={'titulo':'clientes',
                   'actualizar_url': 'actualizar_cliente',
                   'borrar_url':'eliminar_cliente',
                   'detalle_url':'detalle_persona'}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

@permission_required(['sat.dev_ver_clientes','sat.dev_ver_empleados']) 
def detalle_Persona(request, pk):
    objeto = Personas.objects.get(id=pk)
    lista_1 = Direcciones.objects.filter(persona_id=pk)
    lista_2 = Telefonos.objects.filter(persona_id=pk)
    lista_3 = Cuentas.objects.filter(persona_id=pk)

    context = {
        'titulo': 'CLientes',
        'obj': objeto,
        'listas_extra': [{'titulo': 'Direccion', 'lista': lista_1,  'nuevo_url': 'registrar_direccion', 'borrar_url': 'eliminar_direccion', 'actualizar_url':'actualizar_direccion',},
                         {'titulo': 'Telefonos', 'lista': lista_2,  'nuevo_url': 'registrar_telefono',  'borrar_url': 'eliminar_telefono',  'actualizar_url':'actualizar_telefono',},
                         {'titulo': 'Cuentas',   'lista': lista_3,  'nuevo_url': 'registrar_cuenta',    'borrar_url': 'eliminar_cuenta',    'actualizar_url':'actualizar_cuenta','ver_url':'autenticar'},
                         ],
        'archivos_url': 'listar_documentos',
        'editar_url': 'actualizar_cliente',
        'fotoPerfil': obtenerFotoPerfil(request),
        'clienteID': pk
    }
    if objeto.tipo_usuario == Tipo_Usuarios.objects.get(descr__icontains="Empleado"):
        context['titulo'] = 'Empleados'
        context['editar_url'] = 'actualizar_empleado'
        user = Usuario_empleado.objects.get(empleado_id = pk).usuario
        infoCuentaUsuario = [("Nombre de usuario: " + str(user.username)),
                                    ("Ultimo acceso: " + str(user.last_login)),
                                    ("Fecha de creacion: " + str(user.date_joined))]
        infoRoles = user.groups.all
        context['listas_extra'].extend([
                                {'titulo': 'Información de cuenta', 'lista': infoCuentaUsuario},
                                {'titulo': 'Mis roles', 'lista': infoRoles},
                            ])
        context['fotoPerfil'] = objeto.foto_perfil
        print(context)

    return render(request, 'plantilla_detalle.html', context)

class Cliente_Delete(PermissionRequiredMixin,DeleteView):
    permission_required = 'sat.dev_eliminar_clientes'
    model = Personas    # Especificar a solo los empleados con el rol != 0
    template_name = 'borrar.html'
    success_url = reverse_lazy('listar_clientes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

class Cliente_Update(PermissionRequiredMixin,UpdateView):
    permission_required = 'sat.dev_editar_clientes'
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_clientes')
    extra_context = {'esEmpleado': False, 'titulo': 'Editar clientes'}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

class Registrar_Telefono(CreateView):
    model = Telefonos
    form_class = TelefonosForm
    template_name = 'formulario.html'
    extra_context = {'titulo': 'Añadir telefono'}
    #success_url = reverse_lazy('directorio')

    def get_success_url(self):
        obj = self.object
        success_url = reverse('detalle_persona', kwargs={'pk': obj.persona_id})
        return success_url

    def form_valid(self, form):
        registro = form.save(commit=False)
        registro.persona_id = get_object_or_404(Personas, id=self.kwargs.get('pk')).pk
        return super().form_valid(form)

    def get_form(self, form_class=None, **kwargs):
        form = super().get_form(form_class)
        nombre = get_object_or_404(Personas, id=self.kwargs.get('pk'))
        form.fields['nombre'].initial = nombre
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

# Directorio
def Directorio(request):
    lista = Telefonos.objects.all().order_by('persona')
    return render(request, 'directorio.html', {'titulo':'directorio',
                                               'object_list': lista,
                                               'fotoPerfil': obtenerFotoPerfil(request),
                                               'detalle_url': 'detalle_persona',})

def listar_telefonos(request, per_id):
    persona = get_object_or_404(Personas, pk=per_id)
    lista = Telefonos.objects.filter(persona_id=persona)
    return render(request, 'plantilla_lista.html', {'object_list': lista,
                                                    'actualizar_url': 'actualizar_telefono',
                                                    'borrar_url': 'eliminar_telefono',
                                                    'crear_url': 'registrar_telefono',
                                                    'valor_fk': per_id,
                                                    'fotoPerfil': obtenerFotoPerfil(request),})

def eliminar_Telefono(request, pk):
    registro = get_object_or_404(Telefonos, id=pk)
    per_id = registro.persona_id
    registro.delete()
    return redirect('detalle_persona', pk=per_id)

def editar_Telefono(request, pk):
    modelo = get_object_or_404(Telefonos, pk=pk)
    if request.method == 'POST':
        formulario = TelefonosForm(request.POST, instance=modelo)
        if formulario.is_valid():
            modelo = formulario.save(commit=False)
            modelo.save()
            return redirect('detalle_persona', pk=modelo.persona_id)
    else:
        formulario = TelefonosForm(instance=modelo, initial={'nombre':modelo.persona, 'persona' : modelo.persona_id})
    return render(request, 'formulario.html', {'titulo': 'Editar telefono',
                                               'form': formulario,
                                               'fotoPerfil': obtenerFotoPerfil(request)})

# Direcciones

class Registrar_Direccion(CreateView):
    model = Direcciones
    form_class = DireccionesForm
    template_name = 'formulario.html'
    extra_context = {'titulo': 'Registrar dirección'}

    def get_success_url(self):
        obj = self.object
        success_url = reverse('detalle_persona', kwargs={'pk': obj.persona_id})
        return success_url

    def form_valid(self, form):
        registro = form.save(commit=False)
        registro.persona_id = get_object_or_404(Personas, id=self.kwargs.get('pk')).pk
        return super().form_valid(form)

    def get_form(self, form_class=None, **kwargs):
        form = super().get_form(form_class)
        nombre = get_object_or_404(Personas, id=self.kwargs.get('pk'))
        form.fields['nombre'].initial = nombre
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

def listar_Direcciones(request, per_id):
    persona = get_object_or_404(Personas, pk=per_id)
    lista = Direcciones.objects.filter(persona_id=persona)
    return render(request, 'plantilla_lista.html', {'object_list': lista,
                                                    'actualizar_url': 'actualizar_direccion',
                                                    'borrar_url': 'eliminar_direccion',
                                                    'crear_url': 'registrar_direccion',
                                                    'valor_fk': per_id,
                                                    'fotoPerfil': obtenerFotoPerfil(request)})

def eliminar_Direccion(request, pk):
    registro = get_object_or_404(Direcciones, id=pk)
    per_id = registro.persona_id
    registro.delete()
    return redirect('detalle_persona', pk=per_id)

def editar_Direccion(request, pk):
    modelo = get_object_or_404(Direcciones, pk=pk)
    if request.method == 'POST':
        formulario = DireccionesForm(request.POST, instance=modelo)
        if formulario.is_valid():
            modelo = formulario.save(commit=False)
            modelo.save()
            return redirect('detalle_persona', pk=modelo.persona_id)
    else:
        formulario = DireccionesForm(instance=modelo, initial={'nombre':modelo.persona, 'persona': modelo.persona_id})
    return render(request, 'formulario.html', {'titulo': 'Editar dirección',
                                               'form': formulario,
                                               'fotoPerfil': obtenerFotoPerfil(request)})

# Cuentas de clientes

class Registrar_Cuenta(CreateView):
    permission_required = 'sat.dev_crear_cuentas'
    model = Cuentas
    form_class = CuentasForm
    template_name = 'formulario.html'
    extra_context = {'titulo': 'Registrar cuenta'}

    def get_success_url(self):
        obj = self.object
        success_url = reverse_lazy('detalle_persona', kwargs={'pk': obj.persona_id})
        return success_url

    def form_valid(self, form):
        registro = form.save(commit=False)
        registro.persona_id = get_object_or_404(Personas, id=self.kwargs.get('pk')).pk
        registro.contra = AES.encript(str.encode(registro.contra)).decode()
        return super().form_valid(form)

    def get_form(self, form_class=None, **kwargs):
        form = super().get_form(form_class)
        nombre = get_object_or_404(Personas, id=self.kwargs.get('pk'))
        form.fields['nombre'].initial = nombre
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

@permission_required('sat.dev_ver_cuentas') 
def listar_Cuentas(request, per_id):
    persona = get_object_or_404(Personas, pk=per_id)
    lista = Cuentas.objects.filter(persona_id=persona)
    return render(request, 'plantilla_lista.html', {'object_list': lista,
                                                    'actualizar_url': 'actualizar_cuenta',
                                                    'borrar_url': 'eliminar_cuenta',
                                                    'crear_url': 'registrar_cuenta',
                                                    'valor_fk': per_id,
                                                    'fotoPerfil': obtenerFotoPerfil(request)})

@permission_required('sat.dev_eliminar_cuentas')
def eliminar_Cuenta(request, pk):
    registro = get_object_or_404(Cuentas, id=pk)
    per_id = registro.persona_id
    registro.delete()
    return redirect('detalle_persona', pk=per_id)

def editar_Cuenta(request, pk):
    modelo = get_object_or_404(Cuentas, pk=pk)
    if request.method == 'POST':
        formulario = CuentasForm(request.POST, instance=modelo)
        if formulario.is_valid():
            modelo = formulario.save(commit=False)
            modelo.contra = AES.encript(str.encode(modelo.contra)).decode()
            modelo.save()
            return redirect('detalle_persona', pk=modelo.persona_id)
    else:
        binarioDeContra = str.encode(modelo.contra)
        contra = AES.decript(binarioDeContra)
        datosIniciales = {'nombre': modelo.persona,
                          'persona': modelo.persona_id,
                          'contra': contra.decode()}
        if request.resolver_match.url_name == "actualizar_cuenta":
            if  not request.user.has_perm('sat.dev_editar_cuentas'):
                raise PermissionDenied
            formulario = CuentasForm(instance=modelo, initial=datosIniciales)
            verCuenta = False
        else:
            permisoVerContrasenia = get_object_or_404(Permission,codename='auth_ver_password')
            if  not (request.user.has_perm('sat.auth_ver_password') and request.user.has_perm('sat.dev_ver_cuentas')):
                request.user.user_permissions.remove(permisoVerContrasenia)
                raise PermissionDenied
            verCuenta =True
            formulario = CuentasFormView(instance=modelo, initial=datosIniciales)
            request.user.user_permissions.remove(permisoVerContrasenia)
        
    return render(request, 'formulario.html', {'titulo': 'Editar cuenta',
                                               'form': formulario,
                                               'fotoPerfil': obtenerFotoPerfil(request),
                                               'verCuenta':verCuenta})

def autenticarParaVerPassword(request,clienteID,cuentaID):
    
    if request.method == "GET":
        form = FormularioAutenticar
        contexto = {'form':form,
                    'clienteID':clienteID,
                    'fotoPerfil': obtenerFotoPerfil(request)}
        return render(request,'autenticar.html',contexto)
    else:
        form = FormularioAutenticar(request.POST)
        if form.is_valid:
            print(request.POST['password'])
            esPasswordCorrecto = request.user.check_password(request.POST['password'])
            print(esPasswordCorrecto)
            if esPasswordCorrecto:
                permisoVerContrasenia = get_object_or_404(Permission,codename='auth_ver_password')
                request.user.user_permissions.set([permisoVerContrasenia])
                return redirect('ver_cuenta',cuentaID)
            else:
                mensaje = "Contraseña incorrecta vuelve a intentarlo. contacte al administrador si desea recuperar su contraseña"
                messages.add_message(request=request,level=messages.ERROR,message=mensaje,extra_tags='danger')
                return redirect('autenticar',clienteID,cuentaID)

# Subir documentos
class subir_archivo(CreateView):
    form_class = Formulario_Documento
    template_name = 'formulario.html'
    extra_context = {'titulo': 'Subir documento al fichero'}
    success_url = 'lista_documento'

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        try:
            emp = Usuario_empleado.objects.get(usuario=user)
            initial['empleado'] = emp.empleado
        except: #Para pruebas con el super user
            initial['empleado'] = 1
        return initial

    def form_valid(self, form):
        archivo = form.cleaned_data['direccion']
        # Prepara el nombre del archivo y lo normaliza
        base, extension = os.path.splitext(archivo.name)
        base = slugify(base)
        nombre_archivo = base + extension
        # Define el sistema de archivos para guardar el archivo
        cliente_id = self.request.POST.get('cliente')
        carpeta = str(settings.MEDIA_ROOT) + '/carp_' + str(cliente_id)
        fs = FileSystemStorage(location=carpeta)

        # Si el archivo ya existe, agrega un sufijo numérico al nombre para evitar colisiones
        i = 0
        while fs.exists(nombre_archivo):
            i += 1
            nombre_archivo = f"{base}_{i}{extension}"

        # Guarda el archivo en el sistema de archivos
        fs.save(nombre_archivo, archivo)

        # Establece el nombre del archivo en el modelo antes de guardarlo
        instancia = form.save(commit=False)
        instancia.direccion = 'carp_' + str(cliente_id) + '/' + str(nombre_archivo)
        instancia.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

def listar_archivos(request):
    lista = Entrega_Doc.objects.all().order_by("-fecha")
    cliente = request.GET.get('clie')
    doc = request.GET.get('doc')

    if cliente:
        lista = lista.filter(cliente_id=cliente)
    if doc:
        lista = lista.filter(tipo_doc_id=doc)
    listaPermisosVerDocumento = list(request.user.user_permissions.filter(codename__contains="doc_ver").values_list('codename',flat=True))
    return render(request, 'plantilla_lista.html', {'titulo': 'fichero',
                                                    'object_list': lista,
                                                    'actualizar_url': 'actualizar_documento',
                                                    'borrar_url': 'eliminar_documento',
                                                    'detalle_url':'detalle_documento',
                                                    'crear_url': 'subir_documento',
                                                    'fotoPerfil': obtenerFotoPerfil(request),
                                                    'listaPermisosVerDocumento':listaPermisosVerDocumento})

def detalle_archivo(request, pk):
    objeto = Entrega_Doc.objects.get(id=pk)
    listaPermisosVerDocumento = list(request.user.user_permissions.filter(codename__contains="doc_ver").values_list('codename',flat=True))
    context = {
        'obj': objeto,
        'editar_url': 'actualizar_documento',
        'fotoPerfil': obtenerFotoPerfil(request),
        'listaPermisosVerDocumento':listaPermisosVerDocumento
    }
    return render(request, 'plantilla_detalle.html', context)

class editar_archivo(UpdateView):
    model = Entrega_Doc
    form_class = Formulario_Documento
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_documentos')
    extra_context = {'titulo': 'Editar documento del fichero'}

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        try:
            emp = Usuario_empleado.objects.get(usuario=user)
            initial['empleado'] = emp.empleado
        except: #Para pruebas con el super user
            initial['empleado'] = 1
        return initial

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.old_value = obj.direccion
        return obj

    def form_valid(self, form):
        print(form)

        archivo = self.request.FILES.get('direccion')
        if archivo:
            # Prepara el nombre del archivo y lo normaliza
            base, extension = os.path.splitext(archivo.name)
            base = slugify(base)
            nombre_archivo = base + extension
            # Define el sistema de archivos para guardar el archivo
            cliente_id = self.request.POST.get('cliente')
            fs = FileSystemStorage()
            # Borrar archivo anterior

            file_path = os.path.join(settings.MEDIA_ROOT, str(self.old_value))
            print(file_path)
            default_storage.delete(file_path)
            fs.location = str(settings.MEDIA_ROOT) + '/carp_' + str(cliente_id)
            # Si el archivo ya existe, agrega un sufijo numérico al nombre para evitar colisiones
            i = 0
            while fs.exists(nombre_archivo):
                i += 1
                nombre_archivo = f"{base}_{i}{extension}"

            # Guarda el archivo en el sistema de archivos
            fs.save(nombre_archivo, archivo)

            # Establece el nombre del archivo en el modelo antes de guardarlo
            instancia = form.save(commit=False)
            instancia.direccion = 'carp_' + str(cliente_id) + '/' + str(nombre_archivo)
        else:
            instancia = form.save(commit=False)

        instancia.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        nombreDocumento = str(self.get_object().tipo_doc.nombre)
        if self.request.user.has_perm("admin.doc_edicion_"+nombreDocumento):
            return context
        else:
            raise PermissionDenied

def eliminar_archivo(request, pk):
    registro = get_object_or_404(Entrega_Doc, id=pk)
    nombreDocumento = str(registro.tipo_doc.nombre)
    if request.user.has_perm("admin.doc_edicion_"+nombreDocumento):
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, str(registro.direccion))
            default_storage.delete(file_path)
        except SuspiciousFileOperation:
            # Manejar la excepción de operación de archivo sospechosa
            messages.error(request, 'La ruta del archivo no es válida.')
        except OSError:
            # Manejar la excepción de sistema de archivos
            messages.error(request, 'No se pudo borrar el archivo.')

        registro.delete()
        return redirect('listar_documentos')
    else:
        raise PermissionDenied
        


