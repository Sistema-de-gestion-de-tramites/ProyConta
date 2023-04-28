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
    path('registrar_persona/', views.Crear_Persona.as_view(), name="registrar_persona"),

    path('lista_clientes/', views.Listar_Clientes.as_view(), name="listar_clientes"),
    path('actualizar_cliente/<pk>', views.Cliente_Update.as_view(), name="actualizar_cliente"),
    path('eliminar_cliente/<pk>', views.Cliente_Delete.as_view(), name="eliminar_cliente"),

    path('registrar_telefono/<per_id>', views.Registrar_Telefono, name="registrar_telefono"),
    path('lista_telefono/<per_id>', views.listar_telefonos, name="listar_telefonos"),
    path('actualizar_telefono/<pk>', views.editar_Telefono, name="actualizar_telefono"),
    path('eliminar_telefono/<pk>', views.eliminar_Telefono, name="eliminar_telefono"),

    path('clientes/registrar_telefono/<per_id>', views.Registrar_Telefono, name="registrar_telefono"),
    path('clientes/lista_telefono/<per_id>', views.listar_telefonos, name="listar_telefonos"),
    path('clientes/actualizar_telefono/<pk>', views.editar_Telefono, name="actualizar_telefono"),
    path('clientes/eliminar_telefono/<pk>', views.eliminar_Telefono, name="eliminar_telefono"),

    path('clientes/directorio/', views.Directorio, name="directorio"),

    path('clientes/registrar_direccion/<per_id>', views.Registrar_Direccion, name="registrar_direccion"),
    path('clientes/lista_direcciones/<per_id>', views.listar_Direcciones, name="listar_direcciones"),
    path('clientes/actualizar_direccion/<pk>', views.editar_Direccion, name="actualizar_direccion"),
    path('clientes/eliminar_direccion/<pk>', views.eliminar_Direccion, name="eliminar_direccion"),

    path('clientes/subir_documento', views.subir_archivo.as_view(), name="subir_documento"),
    path('clientes/lista_documento/', views.listar_archivos, name="listar_todos_documentos"),
    path('clientes/lista_documento/<clie_id>', views.busqueda_archivos, name="listar_documentos"),
    path('clientes/actualizar_documento/<pk>', views.editar_archivo.as_view(), name="actualizar_documento"),
    path('clientes/eliminar_documento/<pk>', views.eliminar_archivo, name="eliminar_documento"),
    #path('files/<pk>', views.view_file, name="media"),

    path('clientes/detalles/<pk>', views.detalle_Persona, name="detalle_persona")
]
#{----------------------------------------------------------------------------------------------}