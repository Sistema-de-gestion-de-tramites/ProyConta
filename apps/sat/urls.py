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

    path('tareas/crear_tarea/', views.Tarea_Create.as_view(), name="crear_tarea"),
    path('tareas/lista_tareas/', views.Tarea_Listar.as_view(), name="lista_tareas"),
    path('tareas/actualizar_tarea/<pk>', views.Tarea_Update.as_view(), name="actualizar_tarea"),
    path('tareas/eliminar_tarea/<pk>', views.Tarea_Delete.as_view(), name="eliminar_tarea"),

]
#{----------------------------------------------------------------------------------------------}