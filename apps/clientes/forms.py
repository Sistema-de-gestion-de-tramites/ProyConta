from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.clientes.models import Personas
import datetime

#formulario version 2

class PersonaForm(forms.ModelForm):

    correo = forms.EmailField()
    fecha_nac = forms.DateField(initial=datetime.date.today)
    fecha_reg = forms.DateField(initial=datetime.date.today, disabled=True)

    class Meta:
        model = Personas

        fields = [
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

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField()
    password1: forms.CharField(label="contraseña", max_length=50, required=True, widget=forms.PasswordInput)
    password2: forms.CharField(label="confirmar contraseña", max_length=50, required=True, widget=forms.PasswordInput)
    
    class meta:
        model = User
        fields = ['username','email','password1','password2']