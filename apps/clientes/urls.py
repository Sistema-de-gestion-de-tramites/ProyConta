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
    #path('registro/', views.registro, name="registro"),
    path('login/',LoginView.as_view(template_name='login.html')),
    path('logout/',LogoutView.as_view(template_name='base/index.html')),

    path('clientes/registrar_persona/', views.Crear_Persona.as_view(), name="registrar_persona"),

    path('clientes/lista_clientes/', views.Listar_Clientes.as_view(), name="listar_clientes"),
    path('clientes/actualizar_cliente/<pk>', views.Cliente_Update.as_view(), name="actualizar_cliente"),
    path('clientes/eliminar_cliente/<pk>', views.Cliente_Delete.as_view(), name="eliminar_cliente"),

    path('clientes/registrar_telefono/<per_id>', views.Registrar_Telefono, name="registrar_telefono"),
    path('clientes/lista_telefono/<per_id>', views.listar_telefonos, name="listar_telefonos"),
    path('clientes/actualizar_telefono/<pk>', views.editar_Telefono, name="actualizar_telefono"),
    path('clientes/eliminar_telefono/<pk>', views.eliminar_Telefono, name="eliminar_telefono"),

    path('clientes/directorio/', views.Directorio, name="directorio"),
]
#{----------------------------------------------------------------------------------------------}