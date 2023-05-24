from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from apps.sat.templatetags.poll_extras import get_verbose_name
from apps.clientes.models import *
import datetime
from django.db.models import Q

#formulario version 3

# Charfield que pasa el contenido en mayusculas
class UpperField(forms.CharField):
    def to_python(self, value):
        return value.upper()

class ChoiceField_tipo_usuario(forms.ModelChoiceField):     # Clase para el formulario de PersonaForm
    def label_from_instance(self, obj):
        return obj.descr

class PersonaForm(forms.ModelForm):
    #correo = forms.EmailField()
    rfc = UpperField(label="RFC")
    curp = UpperField(label="CURP")
    fecha_nac = forms.DateField(initial=datetime.date.today, label="Fecha de nacimiento")
    fecha_reg = forms.DateField(initial=datetime.date.today, label="Fecha de registro", disabled=True)
    queryTipoUsuario = Tipo_Usuarios.objects.exclude(descr__icontains="Empleado")
    tipo_usuario = forms.ModelChoiceField(queryTipoUsuario,required=False,initial=queryTipoUsuario[0])

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
            'tipo_usuario'
        ]

        labels = {
            'tipo_usuario':'Tipo de cliente'
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

class CuentasForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    persona = forms.HiddenInput()

    class Meta:
        model = Cuentas

        fields = [
            'nombre',
            'cuenta',
            'contra',
        ]

class CuentasFormView(forms.ModelForm):
    nombre = forms.CharField(label='Nombre cliente', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    persona = forms.HiddenInput()
    contra = forms.CharField(label='Contraseña', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    cuenta = forms.CharField(label='Cuenta', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Cuentas

        fields = [
            'nombre',
            'cuenta',
            'contra',
        ]

class Formulario_Documento(forms.ModelForm):
    #empleado = forms.HiddenInput()
    fecha = forms.DateField(disabled=True, initial=datetime.date.today)
    queryClientes = Personas.objects.all().exclude(tipo_usuario__id='1')
    cliente = forms.ModelChoiceField(queryClientes)
    queryEmpleado = Personas.objects.filter(tipo_usuario__id='1')
    empleado = forms.ModelChoiceField(queryEmpleado)
    
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

class FormularioAutenticar (forms.Form):
    password = forms.CharField(label="Escribe tu contraseña",widget=forms.PasswordInput, required=True)

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
