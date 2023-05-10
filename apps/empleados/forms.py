from email.policy import default
from multiprocessing import Value
from tkinter import Widget
from tokenize import group
from django import forms

from apps.sat.models import Personas
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group

class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=50, required=True)
    password1 = forms.CharField(label="Contraseña", max_length=50, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", max_length=50, required=True, widget=forms.PasswordInput)
    empleado = forms.ModelChoiceField(Personas.objects.filter(tipo_usuario=1),required=True,label="Empleado Asociado")
    listaRolesDisponibles = Group.objects.all()
    roles = forms.ModelMultipleChoiceField(listaRolesDisponibles,widget=forms.CheckboxSelectMultiple)
     
    class Meta:
        model = User
        fields = ['username','password1','password2','empleado','roles']

class ActualizarUsuarioForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario", max_length=50, required=True)
    empleado = forms.ModelChoiceField(Personas.objects.filter(tipo_usuario=1),required=True,label="Empleado Asociado")
    listaRolesDisponibles = Group.objects.all()
    roles = forms.ModelMultipleChoiceField(listaRolesDisponibles,widget=forms.CheckboxSelectMultiple)
     
    class Meta:
        model = User
        fields = ['username']

class ActualizarContraseniaUsuarioForm(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=50, required=False,disabled=True)
    empleado = forms.CharField(label="Empleado propietario", max_length=50, required=False,disabled=True)
    password1 = forms.CharField(label="Contraseña", max_length=50, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", max_length=50, required=True, widget=forms.PasswordInput)
    
     
    class Meta:
        model = User
        fields = ['username','empleado','password1','password2']

class imagenPerfilForm(forms.Form):
    imagen = forms.ImageField(max_length=1000,required=True,label="Subir foto")