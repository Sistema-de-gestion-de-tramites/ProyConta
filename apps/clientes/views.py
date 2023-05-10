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

from .forms import *   #{IMPORTA LOS METODOS DE LA CLASE FORM}
import os
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import SuspiciousFileOperation
from django.forms.models import model_to_dict
from apps.clientes.models import Personas, Telefonos, Direcciones
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from apps.empleados.views import obtenerEmpleadoDeCuentaUsuario, obtenerFotoPerfil

Empleado_id = 1

class Crear_Persona(PermissionRequiredMixin,CreateView):
    permission_required = 'editor.dev_crear_empleados'
    permission_required = 'editor.dev_crear_clientes'
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
            context['titulo'] = 'empleados'
            context['form'] = self.get_form_emp()
        else:
            context['esEmpleado'] = False
            context['titulo'] = 'clientes'
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
                   'telefono_url':'listar_telefonos',
                   'direccion_url':'listar_direcciones',
                   'cuentas_url':'listar_cuentas',
                   'detalle_url':'detalle_persona'}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

def detalle_Persona(request, pk):
    objeto = Personas.objects.get(id=pk)
    titulo_1 = 'Direccion'
    lista_1 = Direcciones.objects.filter(persona_id=pk)
    titulo_2 = 'Telefonos'
    lista_2 = Telefonos.objects.filter(persona_id=pk)
    titulo_3 = 'Cuentas'
    lista_3 = Cuentas.objects.filter(persona_id=pk)
    context = {
        'obj': objeto,
        'listas_extra': [{'titulo': titulo_1, 'lista': lista_1},
                         {'titulo': titulo_2, 'lista': lista_2},
                         {'titulo': titulo_3, 'lista': lista_3},
                         ],
        'editar_url': 'actualizar_cliente',
        'fotoPerfil': obtenerFotoPerfil(request),
    }
    return render(request, 'plantilla_detalle.html', context)

class Cliente_Delete(PermissionRequiredMixin,DeleteView):
    permission_required = 'editor.dev_eliminar_clientes'
    model = Personas    # Especificar a solo los empleados con el rol != 0
    template_name = 'borrar.html'
    success_url = reverse_lazy('listar_clientes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

class Cliente_Update(PermissionRequiredMixin,UpdateView):
    permission_required = 'editor.dev_editar_clientes'
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_clientes')
    extra_context = {'esEmpleado': False, 'titulo': 'clientes'}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fotoPerfil'] = obtenerFotoPerfil(self.request)
        return context

class Registrar_Telefono(CreateView):
    model = Telefonos
    form_class = TelefonosForm
    template_name = 'formulario.html'
    #success_url = reverse_lazy('directorio')

    def get_success_url(self):
        obj = self.object
        success_url = reverse('listar_telefonos', kwargs={'per_id': obj.persona_id})
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
    lista = Personas.objects.all()
    return render(request, 'directorio.html', {'titulo':'directorio',
                                               'object_list': lista,
                                               'fotoPerfil': obtenerFotoPerfil(request),})

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
    return redirect('listar_telefonos', per_id=per_id)

def editar_Telefono(request, pk):
    modelo = get_object_or_404(Telefonos, pk=pk)
    if request.method == 'POST':
        formulario = TelefonosForm(request.POST, instance=modelo)
        if formulario.is_valid():
            modelo = formulario.save(commit=False)
            modelo.save()
            return redirect('listar_telefonos', per_id=modelo.persona_id)
    else:
        formulario = TelefonosForm(instance=modelo, initial={'nombre':modelo.persona, 'persona' : modelo.persona_id})
    return render(request, 'formulario.html', {'form': formulario,
                                               'fotoPerfil': obtenerFotoPerfil(request),})

# Direcciones

class Registrar_Direccion(CreateView):
    model = Direcciones
    form_class = DireccionesForm
    template_name = 'formulario.html'

    def get_success_url(self):
        obj = self.object
        success_url = reverse('listar_direcciones', kwargs={'per_id': obj.persona_id})
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
    return redirect('listar_direcciones', per_id=per_id)

def editar_Direccion(request, pk):
    modelo = get_object_or_404(Direcciones, pk=pk)
    if request.method == 'POST':
        formulario = DireccionesForm(request.POST, instance=modelo)
        if formulario.is_valid():
            modelo = formulario.save(commit=False)
            modelo.save()
            return redirect('listar_direcciones', per_id=modelo.persona_id)
    else:
        formulario = DireccionesForm(instance=modelo, initial={'nombre':modelo.persona, 'persona': modelo.persona_id})
    return render(request, 'formulario.html', {'form': formulario,
                                               'fotoPerfil': obtenerFotoPerfil(request)})

# Cuentas de clientes

class Registrar_Cuenta(CreateView):
    model = Cuentas
    form_class = CuentasForm
    template_name = 'formulario.html'

    def get_success_url(self):
        obj = self.object
        success_url = reverse('listar_cuentas', kwargs={'per_id': obj.persona_id})
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

def listar_Cuentas(request, per_id):
    persona = get_object_or_404(Personas, pk=per_id)
    lista = Cuentas.objects.filter(persona_id=persona)
    return render(request, 'plantilla_lista.html', {'object_list': lista,
                                                    'actualizar_url': 'actualizar_cuenta',
                                                    'borrar_url': 'eliminar_cuenta',
                                                    'crear_url': 'registrar_cuenta',
                                                    'valor_fk': per_id,
                                                    'fotoPerfil': obtenerFotoPerfil(request)})

def eliminar_Cuenta(request, pk):
    registro = get_object_or_404(Cuentas, id=pk)
    per_id = registro.persona_id
    registro.delete()
    return redirect('listar_cuentas', per_id=per_id)

def editar_Cuenta(request, pk):
    modelo = get_object_or_404(Cuentas, pk=pk)
    if request.method == 'POST':
        formulario = CuentasForm(request.POST, instance=modelo)
        if formulario.is_valid():
            modelo = formulario.save(commit=False)
            modelo.save()
            return redirect('listar_cuentas', per_id=modelo.persona_id)
    else:
        formulario = CuentasForm(instance=modelo, initial={'nombre': modelo.persona, 'persona': modelo.persona_id})
    return render(request, 'formulario.html', {'form': formulario,
                                               'fotoPerfil': obtenerFotoPerfil(request)})

# Subir documentos
class subir_archivo(CreateView):
    form_class = Formulario_Documento
    template_name = 'formulario.html'
    success_url = 'lista_documento'

    def get_initial(self):
        initial = super().get_initial()
        initial['empleado'] = Empleado_id
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

def busqueda_archivos(request, clie_id):
    lista = Entrega_Doc.objects.filter(cliente_id=clie_id)
    return render(request, 'plantilla_lista.html',{'object_list': lista,
                                                   'fotoPerfil': obtenerFotoPerfil(request)})

def listar_archivos(request):
    lista = Entrega_Doc.objects.all()
    return render(request, 'plantilla_lista.html', {'titulo': 'fichero',
                                                    'object_list': lista, 
                                                    'actualizar_url': 'actualizar_documento', 
                                                    'borrar_url': 'eliminar_documento', 
                                                    'crear_url': 'subir_documento',
                                                    'fotoPerfil': obtenerFotoPerfil(request)})

class editar_archivo(UpdateView):
    model = Entrega_Doc
    form_class = Formulario_Documento
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_todos_documentos')

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
        return context

# def view_file(request, pk):
#     registro = get_object_or_404(Entrega_Doc, id=pk)
#     file_path = os.path.join(settings.MEDIA_ROOT, 'carp_' + str(registro.cliente_id) + '/' + str(registro.direccion))
#     if os.path.exists(file_path):
#         return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
#     raise Http404

def eliminar_archivo(request, pk):
    registro = get_object_or_404(Entrega_Doc, id=pk)
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
    return redirect('listar_todos_documentos')
