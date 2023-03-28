"""
from distutils.command.upload import upload
from apps.sat.models import Tarea, Tramite, Empleados, Personas
import datetime
"""

from django import forms
from .templatetags.poll_extras import get_verbose_name
from .models import Rol, Tipo_Documentos, Estados, Comentarios, Tipo_Archivos
#Formulario Persona
"""
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
"""

#{--------------------------------------------------------------------------------}

class Formulario_Estado(forms.ModelForm):
    nombre = forms.CharField(required=True, label=get_verbose_name(Estados, 'nombre'))

    class Meta:
        model = Estados

        fields = [
            'nombre',
        ]


class Formulario_Comentario(forms.ModelForm):
    descr = forms.CharField(required=True, label=get_verbose_name(Comentarios, 'descr'))

    class Meta:
        model = Comentarios

        fields = [
            'descr',
        ]


class Formulario_Tipo_Archivo(forms.ModelForm):
    extension = forms.CharField(required=True, label=get_verbose_name(Tipo_Archivos, 'extension'))

    class Meta:
        model = Tipo_Archivos

        fields = [
            'extension',
        ]


class Formulario_Rol(forms.ModelForm):
    Rol = forms.CharField(required=True, label=get_verbose_name(Rol, 'Rol'))

    class Meta:
        model = Rol

        fields = [
            'Rol',
        ]


class Formulario_tipoDocumento(forms.ModelForm):
    nombre = forms.CharField(required=True, label=get_verbose_name(Tipo_Documentos, 'nombre'))
    tamano_MB = forms.IntegerField(required=True, label=get_verbose_name(Tipo_Documentos, 'tamano_MB'))
    listaExtensiones = [(choice.pk, choice.extension) for choice in Tipo_Archivos.objects.all()]
    tipo_archivo = forms.ChoiceField(label="Extension del documento", required=True, choices=listaExtensiones)

    class Meta:
        model = Tipo_Documentos

        fields = [
            'nombre',
            'tamano_MB',
        ]


