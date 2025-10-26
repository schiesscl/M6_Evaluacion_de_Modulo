from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    # Página principal
    path('', views.home_view, name='home'),
    
    # Lista de tareas
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    
    # Gestión de tareas
    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/detalle/<int:tarea_id>/', views.detalle_tarea, name='detalle_tarea'),
]
