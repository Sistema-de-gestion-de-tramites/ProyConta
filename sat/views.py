"""
----------------------------------------------------------------------------
--          LISTA DE VIEWS PARA MANEJO DE ARCHIVOS HTML                    --
--              (ARCHIVO VIEWS DE APLICACION SAT)                          --
--               VERSION 0.1    25/10/22                                  --
--                  JOSE GERARDO LOPEZ ARROLLO                            --
----------------------------------------------------------------------------
____________________________________________________________________________
----------------------------------------------------------------------------
-- >Explicacion: CLASE VIEW DESARROLLA LOS METODOS QUE LE MOSTRARA AL USU --
-- ARIO, EN ESTA CLASE IRA EL BACKEND DE LA APLICACION SAT                --
----------------------------------------------------------------------------
"""
from django.shortcuts import render, redirect #{LIBRERIA PARA DESPLEGAR(RENDER) LOS HTML}
from django.http import HttpResponse #{LIBRERIA OPERACIONES HTTP}
from .forms import form_reg_persona, PersonaForm #{IMPORTA LOS METODOS DE LA CLASE FORM}

#{----------------------------------------------------------------------------------------}
#{METODO PARA DEPLEGAR EL HTML INDEX (HOME)}
def index(request): #{METODO REQUEST DE HTTP}
    return render(request,'base/index.html') #{DEVUELVE EL HTML (REQUEST)}
#{----------------------------------------------------------------------------------------}

#{----------------------------------------------------------------------------------------}
#{METODO PARA DESPLEGUAR UN FORMULARIO}
def reg_persona(request): #{METODO REQUEST DE HTTP}
    #if request.method == 'GET':
    return render(request, 'formulario.html', {
        'forms': form_reg_persona()
    })
#{DEVUELVE EL HTML (REQUEST) CREAR DICCIONARIO CON VALORES DEVUELTOS DE FUNCION FORM_REG_PEROSNA()}

#{----------------------------------------------------------------------------------------}



#{----------------------------------------------------------------------------------------}
def persona_view(request): #{METODO REQUEST DE HTTP}
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
    #{DEVUELVE EL HTML (REQUEST) CREAR DICCIONARIO CON VALORES DEVUELTOS DE FUNCION PERSONAFORM()}
#{----------------------------------------------------------------------------------------}