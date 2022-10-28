from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import form_reg_persona, PersonaForm

def index(request):
    return render(request,'base/index.html')

def reg_persona(request):
    #if request.method == 'GET':
    return render(request, 'formulario.html', {
        'forms': form_reg_persona()
    })






def persona_view(request):
    form = PersonaForm()
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'formulario.html', {
                'forms': form
            })
    return render(request, 'formulario.html', {
        'forms': form
    })