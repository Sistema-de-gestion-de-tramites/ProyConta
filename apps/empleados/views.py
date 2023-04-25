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
from django.contrib import messages

#from apps.empleados.forms import EmpleadoForm
from apps.clientes.forms import PersonaForm
from apps.empleados.forms import RegistroUsuarioForm
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

#{----------------------------------------------------------------------------------------}

# Listar todos los registros
class Listar_Personas(ListView):
    queryset = Personas.objects.all()
    template_name = 'plantilla_lista.html'

# Listar solo los empleados
class Listar_Empleados(ListView):
    queryset = Personas.objects.raw('SELECT * FROM `personas` WHERE `tipo_usuario_id` = 1 ')
    template_name = 'plantilla_lista.html'
    extra_context={'titulo':'empleados','actualizar_url': 'actualizar_empleado', 'borrar_url':'eliminar_empleado'}

class Empleado_Delete(UpdateView):
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_empleados')

class Empleado_Update(UpdateView):
    model = Personas
    form_class = PersonaForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('listar_empleados')
    
def registro(request):
    if request.method == 'GET':
        form = RegistroUsuarioForm
        return render(request,'formulario.html',{'form':form})
    else:
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            print(request.POST)
            messages.add_message(request=request,level=messages.SUCCESS,message="Registro Exitoso")
            redirect('registro/')
        else:
            messages.add_message(request=request,level=messages.SUCCESS,message="Datos invalidos")
            redirect('registro/')
    return render(request,'formulario.html',{'form':form})



