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
from django.urls import path #{LIBRERIA URLS DE DJANGO}
from . import views #{IMPORTAR LAS CLASE DE VIEW DE LA APP EMPLEADOS}

#{----------------------------------------------------------------------------------------------}

urlpatterns =[  #{LISTA DE URLS CON LOS ARCHIVOS HTML A DESPLEGAR}
    #path('empleados/crear_empleado/', views.Empleado_Create.as_view(), name="crear_empleado"),              #{DESPLIEGUE DE FOMULARIO PARA EMPLEADOS}
    #path('empleados/lista_empleados/', views.Empleado_Listar.as_view(), name="lista_empleados"),            #{DESPLIEGUE DE LISTA DE EMPLEADOS}
    #path('empleados/actualizar_empleado/<pk>', views.Empleado_Update.as_view(), name="actualizar_empleado"),#{DESPLIEGUE DE FOMULARIO PARA ACTUALIZAR REGISTRO DE EMPLEADO}
    #path('empleados/eliminar_empleado/<pk>', views.Empleado_Delete.as_view(), name="eliminar_empleado"),    #{PARA ELIMINAR REGISTRO DE EMPLEADO}

]
#{----------------------------------------------------------------------------------------------}