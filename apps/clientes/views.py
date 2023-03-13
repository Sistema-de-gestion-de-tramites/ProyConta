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
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import PersonaForm, ClienteForm, RegistroUsuarioForm #{IMPORTA LOS METODOS DE LA CLASE FORM}
from apps.clientes.models import Personas
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
