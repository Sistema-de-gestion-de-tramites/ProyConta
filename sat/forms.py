from django import forms
from sat.models import Personas
import datetime
from django.core.validators import RegexValidator

#formulario version 1
class form_reg_persona(forms.Form):
    nombre = forms.CharField(label='Nombre(s)', max_length=50)
    ap_paterno = forms.CharField(label='Apellido paterno', max_length=25)
    ap_materno = forms.CharField(label='Apellido materno', max_length=25)
    telefono = forms.CharField(label='Telefono', max_length=10)
    calle = forms.CharField(label='Calle', max_length=25)
    dir_num = forms.CharField(label='Número exterior', max_length=4)
    colonia = forms.CharField(label='Colonia', max_length=25)
    delegacion = forms.CharField(label='Delegación', max_length=25)
    cod_postal = forms.CharField(label='Codigo Postal', max_length=5)
    municipio = forms.CharField(label='Municipio', max_length=25)
    estado = forms.CharField(label='Estado', max_length=25)
    pais = forms.CharField(label='Pais', max_length=25)
    correo = forms.CharField(label='Coreo electronico', max_length=40)
    estado_civil = forms.CharField(label='Estado civil', max_length=10)
    fecha_nac = forms.DateField()
    rfc = forms.CharField(label='RFC', max_length=13)
    curp = forms.CharField(label='CURP', max_length=28)
    fecha_reg = forms.DateTimeField()


#formulario version 2

class PersonaForm(forms.ModelForm):

    correo = forms.EmailField()
    fecha_nac = forms.DateField(initial=datetime.date.today)
    fecha_reg = forms.DateField(initial=datetime.date.today, disabled=True)

    class Meta:
        model = Personas

        fields = [
            'persona_id',
            'nombre',
            'ap_paterno',
            'ap_materno',
            'telefono',
            'calle',
            'dir_num',
            'colonia',
            'delegacion',
            'cod_postal',
            'municipio',
            'estado',
            'pais',
            'correo',
            'estado_civil',
            'fecha_nac',
            'rfc',
            'curp',
            'fecha_reg',
        ]

        labels = {
            'nombre': 'Nombre(s)',
            'ap_paterno': 'Apellido paterno',
            'ap_materno': 'Apellido materno',
            'telefono': 'Telefono',
            'calle': 'Calle',
            'dir_num': 'Num. ext.',
            'colonia': 'Colonia',
            'delegacion': 'Delegación',
            'cod_postal': 'Codigo postal',
            'municipio': 'Municipio',
            'estado': 'Estado',
            'pais': 'Pais',
            'correo': 'Correo electronico',
            'estado_civil': 'Estado civil',
            'fecha_nac': 'Fecha de nacimiento',
            'rfc': 'RFC',
            'curp': 'CURP',
            'fecha_reg': 'Fecha de registro',
        }

        widgets = {
            #'nombre': forms.TextInput(attrs={'class':'form-control'}),

        }
