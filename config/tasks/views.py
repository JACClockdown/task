from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Tarea, Categoria
from .serializers import (
    UserSerializer, TareaSerializer, CategoriaSerializer,
    TareaCreateSerializer, TareaUpdateEstadoSerializer
)




class RegisterView(generics.CreateAPIView):
    """Registro de nuevos usuarios"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    """Login de usuarios - retorna tokens JWT"""
    permission_classes = (AllowAny,)


class LogoutView(views.APIView):
    """Logout - invalida el refresh token"""
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Se requiere el refresh token"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"message": "Sesión cerrada exitosamente"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Token inválido o ya expirado"},
                status=status.HTTP_400_BAD_REQUEST
            )




class CategoriaListCreateView(generics.ListCreateAPIView):
    """Listar y crear categorías"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (IsAuthenticated,)


class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Ver, actualizar y eliminar una categoría"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (IsAuthenticated,)




class TareaListCreateView(generics.ListCreateAPIView):
    """Listar todas las tareas del usuario y crear nuevas"""
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TareaCreateSerializer
        return TareaSerializer
    
    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class TareaPendientesView(generics.ListAPIView):
    """Listar solo tareas pendientes del usuario (últimas 6 con paginación)"""
    serializer_class = TareaSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Tarea.objects.filter(
            usuario=self.request.user,
            estado='pendiente'
        ).order_by('-creada_en')


class TareaFinalizadasView(generics.ListAPIView):
    """Listar solo tareas finalizadas del usuario (últimas 6 con paginación)"""
    serializer_class = TareaSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Tarea.objects.filter(
            usuario=self.request.user,
            estado='finalizada'
        ).order_by('-finalizada_en')


class TareaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Ver, actualizar y eliminar una tarea específica"""
    serializer_class = TareaSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        
        return Tarea.objects.filter(usuario=self.request.user)


class TareaUpdateEstadoView(generics.UpdateAPIView):
    """Actualizar solo el estado de una tarea (pendiente/finalizada)"""
    serializer_class = TareaUpdateEstadoSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)


class TareasPorCategoriaView(generics.ListAPIView):
    """Listar tareas filtradas por categoría"""
    serializer_class = TareaSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        categoria_id = self.kwargs.get('categoria_id')
        return Tarea.objects.filter(
            usuario=self.request.user,
            categoria_id=categoria_id
        )