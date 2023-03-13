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

    #path('tareas/crear_tarea/', views.Tarea_Create.as_view(), name="crear_tarea"),
    #path('tareas/lista_tareas/', views.Tarea_Listar.as_view(), name="lista_tareas"),
    #path('tareas/actualizar_tarea/<pk>', views.Tarea_Update.as_view(), name="actualizar_tarea"),
    #path('tareas/eliminar_tarea/<pk>', views.Tarea_Delete.as_view(), name="eliminar_tarea"),

    path('crear-tramite', views.crearTipoTramite, name = 'crear_tramite'),
    path('lista-tramites', views.listarTipoDeTramites, name = 'listar_tramites'),
    path('editar-tramite/<pk>',views.editar_tipoTramite.as_view(),name='editar_tramite'),
    path('eliminar-tipoTramite/<pk>', views.eliminar_TipoTramite, name="eliminar_tipoTramite"),
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
    path('crear-tipo-archivo', views.crear_Tipo_Archivo, name="crear_tipo_archivo"),
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
    path('editar-tipo-documento/<pk>', views.editar_TipoDocumento.as_view(), name="editar_tipo_documento"),
    path('eliminar-documento/<pk>', views.eliminar_tipoDocumento, name="eliminar_documento"),
]
#{----------------------------------------------------------------------------------------------}