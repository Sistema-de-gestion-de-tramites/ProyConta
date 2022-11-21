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
from django.shortcuts import render, redirect #{LIBRERIA PARA DESPLEGAR(RENDER) LOS HTML}
from django.http import HttpResponse #{LIBRERIA OPERACIONES HTTP}
from django.urls import reverse_lazy

from .forms import TareaForm #{IMPORTA LOS METODOS DE LA CLASE FORM}
from apps.sat.models import Tarea, Tramite
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

#{----------------------------------------------------------------------------------------}
#{METODO PARA DEPLEGAR EL HTML INDEX (HOME)}
from apps.sat.models import Tarea


def index(request): #{METODO REQUEST DE HTTP}
    return render(request,'base/index.html') #{DEVUELVE EL HTML (REQUEST)}
#{----------------------------------------------------------------------------------------}

#{----------------------------------------------------------------------------------------}

class Tarea_Create(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'formulario_2.html'
    success_url = reverse_lazy('lista_tareas')

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