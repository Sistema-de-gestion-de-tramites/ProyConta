from django import forms
from apps.sat.models import Personas
import datetime

#Formulario Persona

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
            'nombre': 'Nombre(s):',
            'ap_paterno': 'Apellido paterno:',
            'ap_materno': 'Apellido materno:',
            'telefono': 'Telefono:',
            'calle': 'Calle:',
            'dir_num': 'Numero exterior:',
            'colonia': 'Colonia:',
            'delegacion': 'Delegación:',
            'cod_postal': 'Codigo postal:',
            'municipio': 'Municipio:',
            'estado': 'Estado:',
            'pais': 'Pais:',
            'correo': 'Correo electronico:',
            'estado_civil': 'Estado civil:',
            'fecha_nac': 'Fecha de nacimiento:',
            'rfc': 'RFC:',
            'curp': 'CURP:',
            'fecha_reg': 'Fecha de registro:',
        }

        widgets = {
            #'nombre': forms.TextInput(attrs={'class':'form-control'}),

        }
