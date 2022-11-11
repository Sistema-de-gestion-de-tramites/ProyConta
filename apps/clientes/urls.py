"""
----------------------------------------------------------------------------
--          LISTA DE URLS PARA MANEJO DE ARCHIVOS HTML                    --
--              (ARCHIVO URLS DE APLICACION SAT)                          --
--               VERSION 0.2    31/10/22                                  --
--                  JOSE GERARDO LOPEZ ARROYO                            --
----------------------------------------------------------------------------
____________________________________________________________________________
----------------------------------------------------------------------------
-- >Explicacion: CLASE PARA RENDERIZAR Y DESPLEGAR ARCHIVOS HTML EN EL SE --
-- RVIDOR MANEJANDO EL FRAMWORK DJANGO.                                   --
----------------------------------------------------------------------------
"""
from django.urls import path #{LIBRERIA URLS DE DJANGO}
from django.contrib.auth.views import LoginView, LogoutView
from . import views #{IMPORTAR LAS CLASE DE VIEW DE LA APP CLIENTES}

#{----------------------------------------------------------------------------------------------}

urlpatterns =[  #{LISTA DE URLS CON LOS ARCHIVOS HTML A DESPLEGAR}
    path('reg_persona/', views.persona_view, name ='reg_persona'), #{DESPLIEGUE DE FOMULARIO PARA PERSONAS}
    path('registro/',views.registro,name="registro"),
    path('login/',LoginView.as_view(template_name='startbootstrap-sb-admin-2-gh-pages/login.html')),
     path('logout/',LogoutView.as_view(template_name='base/index.html'))
]
#{----------------------------------------------------------------------------------------------}