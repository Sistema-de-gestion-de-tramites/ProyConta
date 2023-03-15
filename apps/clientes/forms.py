from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from apps.clientes.models import Personas, Tipo_Usuarios, Telefonos, Direcciones, Ext_Direcciones
import datetime

#formulario version 3

opciones_usuario = [(choice.id, choice.descr) for choice in Tipo_Usuarios.objects.all()]

class PersonaForm(forms.ModelForm):
    correo = forms.EmailField()
    fecha_nac = forms.DateField(initial=datetime.date.today)
    fecha_reg = forms.DateField(initial=datetime.date.today, disabled=True)
    tipo_usuario = forms.ModelChoiceField(queryset=Tipo_Usuarios.objects.all()) #forms.ChoiceField(required=True, choices=opciones_usuario)

    class Meta:
        model = Personas

        fields = [
            'nombre',
            'ap_paterno',
            'ap_materno',
            'estado_civil',
            'correo',
            'fecha_nac',
            'rfc',
            'curp',
            'fecha_reg',
            'tipo_usuario',
        ]

        labels = {
        }

        widgets = {
        }


"""
class ClienteForm(forms.ModelForm):
    tipo_clie_id = forms.ChoiceField(choices=[(choice.pk, choice.tipo_c) for choice in TipoClie.objects.all()])
                #forms.ModelChoiceField(queryset=TipoClie.objects.all())

    class Meta:
        model = Clientes

        fields = [
            'tipo_clie_id',
        ]

        labels = {
            'tipo_clie_id': 'Tipo de cliente',
        }

ClienteInlineFormSet = inlineformset_factory(Personas, Clientes, form=ClienteForm, can_delete=False)
"""


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(label="username", max_length=50, required=True)
    password1 = forms.CharField(label="contraseña", max_length=50, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirmar contraseña", max_length=50, required=True, widget=forms.PasswordInput)

    class meta:
        model = User
        fields = ['username','email','password1','password2']

