"""
----------------------------------------------------------------------------
--          LISTA DE URLS PARA MANEJO DE ARCHIVOS HTML                    --
--              (ARCHIVO URLS DE APLICACION SAT)                          --
--               VERSION 0.1    31/10/22                                  --
--                  JOSE GERARDO LOPEZ ARROYO                             --
----------------------------------------------------------------------------
____________________________________________________________________________
----------------------------------------------------------------------------
-- >Explicacion: CLASE PARA RENDERIZAR Y DESPLEGAR ARCHIVOS HTML EN EL SE --
-- RVIDOR MANEJANDO EL FRAMWORK DJANGO.                                   --
----------------------------------------------------------------------------
"""
from math import perm
from django.urls import path #{LIBRERIA URLS DE DJANGO}
from . import views #{IMPORTAR LAS CLASE DE VIEW DE LA APP EMPLEADOS}

#{----------------------------------------------------------------------------------------------}

urlpatterns =[  #{LISTA DE URLS CON LOS ARCHIVOS HTML A DESPLEGAR}
    # urls CRUD empleados
    path('lista_empleados/', views.Listar_Empleados.as_view(), name="listar_empleados"),
    path('actualizar_empleado/<pk>', views.Empleado_Update.as_view(), name="actualizar_empleado"),
    path('eliminar_empleado/<pk>', views.Empleado_Delete.as_view(), name="eliminar_empleado"),
    path('lista_personas/', views.Listar_Personas.as_view(), name="listar_personas"),
    # urls CRUD usuarios
    path('registro/',views.registro,name='registro'),
    path('lista_cuentas_usuario/', views.Listar_Usuarios.as_view(), name="listar_cuentas_usuario"),
    path('eliminar_usuario/<pk>', views.Usuario_Delete.as_view(), name="eliminar_usuario"),
    path('actualizar_usuario/<pk>', views.usuario_Update.as_view(), name="actualizar_usuario"),
    path('actualizar_contrasenia_usuario/<pk>', views.usuario_contrasenia_Update.as_view(), name="actualizar_contrasenia_usuario"),

]
#{----------------------------------------------------------------------------------------------}