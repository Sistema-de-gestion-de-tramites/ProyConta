from django import forms
from apps.sat.models import Tarea, Tramite, Empleados, Personas
import datetime

#Formulario Persona

class TareaForm(forms.ModelForm):
    emp_creador = forms.ChoiceField(choices=[(choice.pk, choice.nombre + ' ' + choice.ap_paterno) for choice in Personas.objects.raw('SELECT * FROM personas, empleados where personas.id=empleados.empleado_id')])
    tramite = forms.ChoiceField(choices=[(choice.pk, choice.tipo) for choice in Tramite.objects.all()])
    fecha_ini = forms.DateField(initial=datetime.date.today)
    fecha_lim = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = Tarea

        fields = [
            'emp_creador',
            'emp_clie',
            'tramite',
            'info_add',
            'dir_archivo',
            'estado',
            'costo',
            'fecha_ini',
            'fecha_lim',
        ]

        labels = {
            'emp_creador': 'ID creador:',
            'emp_clie': 'Empleado-Cliente:',
            'tramite': 'Tipo de tramite:',
            'info_add': 'Notas adicionales:',
            'dir_archivo': 'Dirección del archivo:',
            'estado': 'Estado del Tramite',
            'costo': 'Costo del Tramite:',
            'fecha_ini': 'Fecha de inicio:',
            'fecha_lim': 'Fecha de Limite',
        }

        widgets = {
            #'nombre': forms.TextInput(attrs={'class':'form-control'}),

        }
