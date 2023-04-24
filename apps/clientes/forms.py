from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from apps.sat.templatetags.poll_extras import get_verbose_name
from apps.clientes.models import *
import datetime
from django.db.models import Q

#formulario version 3

class ChoiceField_tipo_usuario(forms.ModelChoiceField):     # Clase para el formulario de PersonaForm
    def label_from_instance(self, obj):
        return obj.descr

class PersonaForm(forms.ModelForm):
    correo = forms.EmailField()
    fecha_nac = forms.DateField(initial=datetime.date.today, label="Fecha de nacimiento")
    fecha_reg = forms.DateField(initial=datetime.date.today, label="Fecha de registro", disabled=True)
    tipo_usuario = ChoiceField_tipo_usuario(queryset=Tipo_Usuarios.objects.all())

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



class TelefonosForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    persona = forms.HiddenInput()

    class Meta:
        model = Telefonos

        fields = [
            'nombre',
            'descr',
            'telefono',
        ]

class DireccionesForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    persona = forms.HiddenInput()

    class Meta:
        model = Direcciones

        fields = [
            'nombre',
            'num_ext',
            'calle',
            'colonia',
            'cod_postal',
            'municipio',
            'estado',
        ]

class Formulario_Documento(forms.ModelForm):
    empleado = forms.HiddenInput()
    fecha = forms.DateField(disabled=True, initial=datetime.date.today)

    class Meta:
        model = Entrega_Doc

        fields = [
            'cliente',
            'empleado',
            'tipo_doc',
            'estado',
            'comentario',
            'fecha',
            'direccion',
        ]

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

