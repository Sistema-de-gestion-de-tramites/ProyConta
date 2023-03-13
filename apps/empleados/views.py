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

from apps.empleados.forms import EmpleadoForm
from apps.clientes.forms import PersonaForm, RegistroUsuarioForm
from apps.empleados.models import Personas
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

#{----------------------------------------------------------------------------------------}

def id_emp_sesion(request):
    empleados = Personas.objects.all()    # Especificar a solo los empleados con el rol = 0
    for emp in empleados:
        if emp.username == request.user.username:
            id=request.user.username
            break
    return id

class Empleado_Create(CreateView):
    #model = Clientes
    form_class = EmpleadoForm
    second_form_class = PersonaForm
    third_form_class = RegistroUsuarioForm
    template_name = 'formulario_clientes.html'
    success_url = reverse_lazy('lista_empleados')

    def get_context_data(self, **kwargs):
        context = super(Empleado_Create, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        form3 = self.third_form_class(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            solicitud = form.save(commit=False)
            form3.save()
            solicitud.empleado_id = form2.save().id
            solicitud.username = form3.save().username
            solicitud.password = request.POST['password1']
            solicitud.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2,form3=form3))

class Empleado_Listar(ListView):
    queryset = Personas.objects.raw('SELECT * FROM personas, empleados where personas.id=empleados.empleado_id')
    #model = Personas
    template_name = 'tables.html'

class Empleado_Update(UpdateView):
    model = Personas    # Especificar a solo los empleados con el rol = 0
    form_class = EmpleadoForm
    template_name = 'formulario_2.html'
    success_url = reverse_lazy('lista_empleados')

class Empleado_Delete(DeleteView):
    model = Personas    # Especificar a solo los empleados con el rol = 0
    template_name = 'borrar.html'
    success_url = reverse_lazy('lista_empleados')


#{----------------------------------------------------------------------------------------}



