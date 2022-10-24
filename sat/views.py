from django.shortcuts import render
from django.http import HttpResponse

def prueba(request):
    return render(request,'prueba/base.html')

