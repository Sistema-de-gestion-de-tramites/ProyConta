from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from apps.clientes.models import Personas, Tipo_Usuarios, Telefonos, Direcciones, Ext_Direcciones
import datetime

#formulario version 3

class ChoiceField_tipo_usuario(forms.ModelChoiceField):     # Clase para el formulario de PersonaForm
    def label_from_instance(self, obj):
        return obj.descr

class PersonaForm(forms.ModelForm):
    correo = forms.EmailField()
    fecha_nac = forms.DateField(initial=datetime.date.today)
    fecha_reg = forms.DateField(initial=datetime.date.today, disabled=True)
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
    persona = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = Telefonos

        fields = [
            'descr',
            'telefono',
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
