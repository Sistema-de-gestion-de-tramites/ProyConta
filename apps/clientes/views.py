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
from django.urls import reverse_lazy
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

def id_emp_sesion(request):
    empleados = Personas.objects.all() # Especificar a solo los empleados con el rol = 0
    usernameValue=''
    for emp in empleados:
     if emp.username == request.user.username:
        usernameValue=request.user.username
        break
    empleado= Personas.objects.get(username=usernameValue)
    id = empleado.empleado_id
    return id

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
        return context

# Listar solo los clientes
class Listar_Clientes(PermissionRequiredMixin,ListView):
    permission_required = 'editor.dev_ver_clientes'
    queryset = Personas.objects.exclude(tipo_usuario__descr="Empleado")
    template_name = 'plantilla_lista.html'
    extra_context={'titulo':'clientes', 'actualizar_url': 'actualizar_cliente', 'borrar_url':'eliminar_cliente', 'telefono_url':'listar_telefonos', 'direccion_url':'listar_direcciones', 'detalle_url':'detalle_persona'}

def detalle_Persona(request, pk):
    objeto = Personas.objects.get(id=pk)
    titulo_1 = 'Direccion'
    lista_1 = Direcciones.objects.filter(persona_id=pk)
    titulo_2 = 'Telefonos'
    lista_2 = Telefonos.objects.filter(persona_id=pk)

    context = {
        'obj': objeto,
        'listas_extra': [{'titulo': titulo_1, 'lista': lista_1},
                         {'titulo': titulo_2, 'lista': lista_2},
                        ],
        'editar_url': 'editar_tipo_documento',
    }
    return render(request, 'plantilla_detalle.html', context)

class Cliente_Delete(PermissionRequiredMixin,DeleteView):
    permission_required = 'editor.dev_eliminar_clientes'
    model = Personas    # Especificar a solo los empleados con el rol != 0
    template_name = 'borrar.html'
    success_url = reverse_lazy('listar_clientes')

class Cliente_Update(PermissionRequiredMixin,UpdateView):
    permission_required = 'editor.dev_editar_clientes'
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_clientes')
    extra_context = {'esEmpleado': False, 'titulo': 'clientes'}

def Registrar_Telefono(request, per_id):
    persona = get_object_or_404(Personas, pk = per_id)
    if request.method == 'POST':
        form = TelefonosForm(request.POST)
        if form.is_valid():
            tel = form.save(commit = False)
            tel.persona_id = persona.pk
            tel.save()
            return redirect('listar_telefonos', per_id=per_id)
    else:
        contexto = {'form': TelefonosForm(initial={'nombre':persona , 'persona' : per_id})}
        return render(request, 'formulario.html', contexto)

# Directorio
def Directorio(request):
    lista = Personas.objects.all()
    return render(request, 'directorio.html', {'object_list': lista})

def listar_telefonos(request, per_id):
    persona = get_object_or_404(Personas, pk=per_id)
    lista = Telefonos.objects.filter(persona_id=persona)
    return render(request, 'plantilla_lista.html', {'object_list': lista, 'actualizar_url': 'actualizar_telefono', 'borrar_url': 'eliminar_telefono', 'crear_url': 'registrar_telefono', 'valor_fk': per_id})

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
    return render(request, 'formulario.html', {'form': formulario})

# Direcciones
def Registrar_Direccion(request, per_id):
    persona = get_object_or_404(Personas, pk = per_id)
    if request.method == 'POST':
        form = DireccionesForm(request.POST)
        if form.is_valid():
            dir = form.save(commit = False)
            dir.persona_id = persona.pk
            dir.save()
            return redirect('listar_direcciones', per_id=per_id)
    else:
        contexto = {'form': DireccionesForm(initial={'nombre':persona, 'persona' : per_id})}
        return render(request, 'formulario.html', contexto)

def listar_Direcciones(request, per_id):
    persona = get_object_or_404(Personas, pk=per_id)
    lista = Direcciones.objects.filter(persona_id=persona)
    return render(request, 'plantilla_lista.html', {'object_list': lista, 'actualizar_url': 'actualizar_direccion', 'borrar_url': 'eliminar_direccion', 'crear_url': 'registrar_direccion', 'valor_fk': per_id})

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
    return render(request, 'formulario.html', {'form': formulario})

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

def busqueda_archivos(request, clie_id):
    lista = Entrega_Doc.objects.filter(cliente_id=clie_id)
    return render(request, 'plantilla_lista.html',{'object_list': lista})

def listar_archivos(request):
    lista = Entrega_Doc.objects.all()
    return render(request, 'plantilla_lista.html', {'object_list': lista, 'actualizar_url': 'actualizar_documento', 'borrar_url': 'eliminar_documento', 'crear_url': 'subir_documento'})

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


"""
#{----------------------------------------------------------------------------------------}
def registro(request):
    if request.method == 'GET':
        print(request.user.username)
        emp = id_emp_sesion(request)
        print(emp)
        form = RegistroUsuarioForm
        return render(request,'registro.html',{'form':form})
    else:
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            print(request.POST)
            redirect('index/')
        else:
            redirect('registro/')
    return render(request,'registro.html',{'form':form})

    #{DEVUELVE EL HTML (REQUEST) CREAR DICCIONARIO CON VALORES DEVUELTOS DE FUNCION PERSONAFORM()}
#{----------------------------------------------------------------------------------------}

class Cliente_Create(CreateView):
    #model = Clientes
    form_class = ClienteForm
    second_form_class = PersonaForm
    template_name = 'formulario_clientes.html'
    success_url = reverse_lazy('lista_clientes')

    def get_context_data(self, **kwargs):
        context = super(Cliente_Create, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            solicitud = form.save(commit=False)
            solicitud.cliente_id = form2.save().id
            solicitud.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class Cliente_Listar(ListView):
    queryset = Personas.objects.raw('SELECT * FROM personas')   # Especificar a solo los clientes con el rol != 0
    #model = Personas
    template_name = 'tables.html'
    dic = {'nombre':'hola'}

class Cliente_Update(UpdateView):
    model = Personas    # Especificar a solo los clientes con el rol != 0
    form_class = ClienteForm
    template_name = 'formulario_2.html'
    success_url = reverse_lazy('lista_clientes')

class Cliente_Delete(DeleteView):
    model = Personas    # Especificar a solo los empleados con el rol != 0
    template_name = 'borrar.html'
    success_url = reverse_lazy('lista_clientes')
"""