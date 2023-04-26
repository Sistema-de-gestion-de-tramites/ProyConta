"""
----------------------------------------------------------------------------
--          LISTA DE URLS PARA MANEJO DE ARCHIVOS HTML                    --
--              (ARCHIVO URLS DE APLICACION SAT)                          --
--               VERSION 0.2    31/10/22                                  --
--                  JOSE GERARDO LOPEZ ARROYO                             --
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
    path('', views.index, name='index'), #{DESPLIEGUE DE INDEX.HTML (HOME PAGE)}
    path('inicio', views.inicio, name='inicio'),  # {DESPLIEGUE DE ROLES.HTML (ROLES PAGE)}
    path('roles', views.roles, name='roles'), #{DESPLIEGUE DE ROLES.HTML (ROLES PAGE)}
    path('documentos', views.documentos, name='documentos'), #{DESPLIEGUE DE ROLES.HTML (ROLES PAGE)}
    path('archivos', views.archivos, name='archivos'),  # {DESPLIEGUE DE ROLES.HTML (ROLES PAGE)}
    path('directorio', views.directorio, name='directorio'),  # {DESPLIEGUE DE ROLES.HTML (ROLES PAGE)}
    path('clientes', views.clientes, name='clientes'),  # {DESPLIEGUE DE ROLES.HTML (ROLES PAGE)}
    path('empleados', views.empleados, name='empleados'),  # {DESPLIEGUE DE ROLES.HTML (ROLES PAGE)}

    #path('tareas/crear_tarea/', views.Tarea_Create.as_view(), name="crear_tarea"),
    #path('tareas/lista_tareas/', views.Tarea_Listar.as_view(), name="lista_tareas"),
    #path('tareas/actualizar_tarea/<pk>', views.Tarea_Update.as_view(), name="actualizar_tarea"),
    #path('tareas/eliminar_tarea/<pk>', views.Tarea_Delete.as_view(), name="eliminar_tarea"),

    # URL del modelo Estado
    path('crear-estado', views.crear_Estado, name="crear_estado"),
    path('editar-estado/<pk>', views.editar_Estado.as_view(), name="editar_estado"),
    path('listar-estados', views.listar_Estados, name="listar_estados"),
    path('eliminar-estado/<pk>', views.eliminar_Estado, name="eliminar_estado"),
    # URL del modelo Comentario
    path('crear-comentario', views.crear_Comentario, name="crear_comentario"),
    path('editar-comentario/<pk>', views.editar_Comentario.as_view(), name="editar_comentario"),
    path('listar-comentarios', views.listar_Comentarios, name="listar_comentarios"),
    path('eliminar-comentario/<pk>', views.eliminar_Comentario, name="eliminar_comentario"),
    # URL del modelo Tipo de archivo
   path('crear-tipo-archivos', views.crear_Tipo_Archivo, name="crear_tipo_archivos"),
    path('editar-tipo-archivo/<pk>', views.editar_Tipo_Archivo.as_view(), name="editar_tipo_archivo"),
    path('listar-tipo-archivos', views.listar_Tipo_Archivos, name="listar_tipo_archivos"),
    path('eliminar-tipo_archivo/<pk>', views.eliminar_Tipo_Archivo, name="eliminar_tipo_archivo"),
    # URL del modelo Rol
    path('crear-rol', views.crear_Rol, name="crear_rol"),
    path('editar-rol/<pk>', views.editar_Rol.as_view(), name="editar_rol"),
    path('listar-roles', views.listar_Roles, name="listar_roles"),
    path('eliminar-rol/<pk>', views.eliminar_Rol, name="eliminar_rol"),
    # URL del modelo tipo documento
    path('crear-documento', views.crearTipoDocumento, name="crear_tipo_documento"),
    path('listar-documentos', views.listar_tipoDocumento, name="listar_tipo_documento"),
    path('detalle-tipo-documento/<pk>', views.detalle_tipoDocumento, name="detalle_tipo_documento"),
    path('editar-tipo-documento/<pk>', views.editar_tipoDocumento.as_view(), name="editar_tipo_documento"),
    path('eliminar-documento/<pk>', views.eliminar_TipoDocumento, name="eliminar_tipo_documento"),

    path('busqueda/', views.buscar, name="busqueda"),
]
#{----------------------------------------------------------------------------------------------}
# , 'actualizar_url': '', 'borrar_url':''})