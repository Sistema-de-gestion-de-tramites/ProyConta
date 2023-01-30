from distutils.command.upload import upload
from django import forms
from apps.sat.models import Tarea, Tramite, Empleados, Personas
import datetime

#Formulario Persona

#{--------------------------------------------------------------------------------}
#DESCRIPCION: conjunto de funciones para generar lista de duplas para usar en formulario
def listaEmpleados():
    empleados = Empleados.objects.all()
    lista=[]
    for i in empleados:
        lista.append((i.empleado_id,Personas.objects.get(id=i.empleado_id).nombre))
    return lista

def listaTramite():
    tramites = Tramite.objects.all()
    lista=[]
    for i in tramites:
        lista.append((i.id,i.tipo))
    return lista

#{--------------------------------------------------------------------------------}
class TareaForm(forms.ModelForm):
    emp_creador = forms.ChoiceField(choices=[(choice.pk, choice.nombre + ' ' + choice.ap_paterno) for choice in Personas.objects.raw('SELECT * FROM personas, empleados where personas.id=empleados.empleado_id')])
    tramite = forms.ChoiceField(choices=[(choice.pk, choice.tipo) for choice in Tramite.objects.all()])
    fecha_ini = forms.DateField(initial=datetime.date.today)
    fecha_lim = forms.DateField(initial=datetime.date.today)
    fecha_fin = forms.DateField(initial=datetime.date.today)
    archivo = forms.FileField(widget=forms.FileInput)
    dir_archivo = forms.CharField(label='',widget=forms.TextInput(attrs={'hidden' : ''}),required=False)
    class Meta:
        model = Tarea

        fields = [
            'emp_creador',
            'emp_clie',
            'tramite',
            'info_add',
            'estado',
            'costo',
            'fecha_ini',
            'fecha_lim',
            'fecha_fin',
            'archivo'
        ]

        labels = {
            'emp_creador': 'ID creador:',
            'emp_clie': 'Empleado-Cliente:',
            'tramite': 'Tipo de tramite:',
            'info_add': 'Notas adicionales:',
            'estado': 'Estado del Tramite',
            'costo': 'Costo del Tramite:',
            'fecha_ini': 'Fecha de inicio:',
            'fecha_lim': 'Fecha de Limite',
            
        }

        widgets = {
            #'emp_creador': forms.Select(choices=listaEmpleados()),
        }
