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
from . import views #{IMPORTAR LAS CLASE DE VIEW DE LA APP CLIENTES}

#{----------------------------------------------------------------------------------------------}

urlpatterns =[  #{LISTA DE URLS CON LOS ARCHIVOS HTML A DESPLEGAR}
    #path('registro/', views.registro, name="registro"),
    path('registrar_persona/<pk>', views.Crear_Persona.as_view(), name="registrar_persona"),

    path('lista_clientes/', views.Listar_Clientes.as_view(), name="listar_clientes"),
    path('actualizar_cliente/<pk>', views.Cliente_Update.as_view(), name="actualizar_cliente"),
    path('eliminar_cliente/<pk>', views.Cliente_Delete.as_view(), name="eliminar_cliente"),

    path('registrar_telefono/<pk>', views.Registrar_Telefono.as_view(), name="registrar_telefono"),
    path('lista_telefono/<per_id>', views.listar_telefonos, name="listar_telefonos"),
    path('actualizar_telefono/<pk>', views.editar_Telefono, name="actualizar_telefono"),
    path('eliminar_telefono/<pk>', views.eliminar_Telefono, name="eliminar_telefono"),

    path('directorio/', views.Directorio, name="directorio"),

    path('registrar_direccion/<pk>', views.Registrar_Direccion.as_view(), name="registrar_direccion"),
    path('lista_direcciones/<per_id>', views.listar_Direcciones, name="listar_direcciones"),
    path('actualizar_direccion/<pk>', views.editar_Direccion, name="actualizar_direccion"),
    path('eliminar_direccion/<pk>', views.eliminar_Direccion, name="eliminar_direccion"),

    path('registrar_cuenta/<pk>', views.Registrar_Cuenta.as_view(), name="registrar_cuenta"),
    path('lista_cuenta/<per_id>', views.listar_Cuentas, name="listar_cuentas"),
    path('actualizar_cuenta/<pk>', views.editar_Cuenta, name="actualizar_cuenta"),
    path('eliminar_cuenta/<pk>', views.eliminar_Cuenta, name="eliminar_cuenta"),

    path('subir_documento', views.subir_archivo.as_view(), name="subir_documento"),
    path('lista_documento/', views.listar_archivos, name="listar_todos_documentos"),
    path('lista_documento/<clie_id>', views.busqueda_archivos, name="listar_documentos"),
    path('actualizar_documento/<pk>', views.editar_archivo.as_view(), name="actualizar_documento"),
    path('eliminar_documento/<pk>', views.eliminar_archivo, name="eliminar_documento"),

    path('detalles/<pk>', views.detalle_Persona, name="detalle_persona")
]
#{----------------------------------------------------------------------------------------------}