from django.urls import path
from . import views

urlpatterns =[
    path('index/', views.index, name='index'),
    path('prueba1/', views.reg_persona, name = 'prueba1'),
    path('prueba2/', views.persona_view, name = 'prueba2'),

]