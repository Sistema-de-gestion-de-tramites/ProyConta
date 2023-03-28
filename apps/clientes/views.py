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
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *

from .forms import PersonaForm, TelefonosForm #{IMPORTA LOS METODOS DE LA CLASE FORM}
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



class Crear_Persona(CreateView):
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_personas')

# Listar solo los clientes
class Listar_Clientes(ListView):
    queryset = Personas.objects.raw('SELECT * FROM `personas` WHERE `tipo_usuario_id` != 1 ')
    template_name = 'plantilla_lista.html'
    extra_context={'actualizar_url': 'actualizar_cliente', 'borrar_url':'eliminar_cliente', 'telefono_url':'listar_telefonos'}

class Cliente_Delete(DeleteView):
    model = Personas    # Especificar a solo los empleados con el rol != 0
    template_name = 'borrar.html'
    success_url = reverse_lazy('listar_clientes')

class Cliente_Update(UpdateView):
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_clientes')

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
        contexto = {'form': TelefonosForm(initial={'persona' : persona})}
        return render(request, 'formulario.html', contexto)

# Directorio
def Directorio(request):
    lista = Telefonos.objects.all()
    return render(request, 'plantilla_lista.html', {'object_list': lista, 'actualizar_url': 'actualizar_telefono'})

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
        formulario = TelefonosForm(instance=modelo, initial={'persona' : modelo.persona_id})
    return render(request, 'formulario.html', {'form': formulario})


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