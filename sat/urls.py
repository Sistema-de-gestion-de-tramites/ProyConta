"""
----------------------------------------------------------------------------
--          LISTA DE URLS PARA MANEJO DE ARCHIVOS HTML                    --
--              (ARCHIVO URLS DE APLICACION SAT)                          --
--               VERSION 0.1    25/10/22                                  --
--                  JOSE GERARDO LOPEZ ARROLLO                            --
----------------------------------------------------------------------------
____________________________________________________________________________
----------------------------------------------------------------------------
-- >Explicacion: CLASE PARA RENDERIZAR Y DESPLEGAR ARCHIVOS HTML EN EL SE --
-- RVIDOR MANEJANDO EL FRAMWORK DJANGO.                                   --
----------------------------------------------------------------------------
"""
from django.urls import path #{LIBRERIA URLS DE DJANGO}
from . import views #{IMPORTAR LAS CLASE DE VIEW DE LA APP SAT}

#{----------------------------------------------------------------------------------------------}

urlpatterns =[  #{LISTA DE URLS CON LOS ARCHIVOS HTML A DESPLEGAR}
    path('index/', views.index, name='index'), #{DESPLIEGUE DE INDEX.HTML (HOME PAGE)}
    path('prueba1/', views.reg_persona, name = 'prueba1'), #{HTML DE PRUEBA (BORRAR AL TERMINAR)}
    path('prueba2/', views.persona_view, name = 'prueba2'), #{HTML DE PRUEBA (BORRAR AL TERMINAR)}

]
#{----------------------------------------------------------------------------------------------}