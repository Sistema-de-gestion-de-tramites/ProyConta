from email.policy import default
from multiprocessing import Value
from tkinter import Widget
from tokenize import group
from django import forms

from apps.sat.models import Personas
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label="Correo electronico")
    username = forms.CharField(label="Nombre de usuario", max_length=50, required=True)
    password1 = forms.CharField(label="contraseña", max_length=50, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirmar contraseña", max_length=50, required=True, widget=forms.PasswordInput)
    roles = forms.ModelMultipleChoiceField(Group.objects.all(),widget=forms.CheckboxSelectMultiple)
    class meta:
        model = User
        fields = ['username','email','password1','password2','esAdministrador','roles']