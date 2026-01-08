from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView,
    CategoriaListCreateView, CategoriaDetailView,
    TareaListCreateView, TareaPendientesView, TareaFinalizadasView,
    TareaDetailView, TareaUpdateEstadoView, TareasPorCategoriaView
)

urlpatterns = [
    
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('categorias/', CategoriaListCreateView.as_view(), name='categoria-list-create'),
    path('categorias/<int:pk>/', CategoriaDetailView.as_view(), name='categoria-detail'),
    
    
    path('tareas/', TareaListCreateView.as_view(), name='tarea-list-create'),
    path('tareas/pendientes/', TareaPendientesView.as_view(), name='tareas-pendientes'),
    path('tareas/finalizadas/', TareaFinalizadasView.as_view(), name='tareas-finalizadas'),
    path('tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea-detail'),
    path('tareas/<int:pk>/estado/', TareaUpdateEstadoView.as_view(), name='tarea-update-estado'),
    path('tareas/categoria/<int:categoria_id>/', TareasPorCategoriaView.as_view(), name='tareas-por-categoria'),
]