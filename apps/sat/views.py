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
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect #{LIBRERIA PARA DESPLEGAR(RENDER) LOS HTML}
from django.http import HttpResponse #{LIBRERIA OPERACIONES HTTP}
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import TareaForm #{IMPORTA LOS METODOS DE LA CLASE FORM}
from apps.sat.models import Tarea, Tramite, Empleados, Emp_Clie_Asig
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

#{----------------------------------------------------------------------------------------}
#{METODO PARA DEPLEGAR EL HTML INDEX (HOME)}



def index(request): #{METODO REQUEST DE HTTP}
    if request.user.is_authenticated: #valida si existe una sesion activa
        print(request.user.username)
    return render(request,'base/index.html') #{DEVUELVE EL HTML (REQUEST)}
#{----------------------------------------------------------------------------------------}
# DESCRIPCION: Devuelve el id del empleado que ha iniciado sesion (no se valida que exista una sesion activa)
def id_emp_sesion(request):
    empleados = Empleados.objects.all()
    usernameValue=''
    for emp in empleados:
     if emp.username == request.user.username:
        usernameValue=request.user.username
        break
    empleado= Empleados.objects.get(username=usernameValue)
    id = empleado.empleado_id
    return id
#{----------------------------------------------------------------------------------------}
#{----------------------------------------------------------------------------------------}

#{----------------------------------------------------------------------------------------}

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