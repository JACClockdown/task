from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tarea, Categoria
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class CategoriaSerializer(serializers.ModelSerializer):
    tareas_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'creada_en', 'tareas_count']
        read_only_fields = ['creada_en']
    
    def get_tareas_count(self, obj):
        return obj.tareas.count()


class TareaSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Tarea
        fields = [
            'id', 'titulo', 'descripcion', 'categoria', 'categoria_nombre',
            'estado', 'color', 'usuario', 'usuario_nombre',
            'creada_en', 'actualizada_en', 'finalizada_en'
        ]
        read_only_fields = ['color', 'usuario', 'creada_en', 'actualizada_en', 'finalizada_en']
    
    def validate_categoria(self, value):
        """Valida que la categoría exista"""
        if not Categoria.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("La categoría no existe")
        return value


class TareaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'categoria']
    
    def create(self, validated_data):
        
        return Tarea.objects.create(**validated_data)


class TareaUpdateEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['estado']
    
    def update(self, instance, validated_data):
        nuevo_estado = validated_data.get('estado')
        
        if nuevo_estado == 'finalizada' and instance.estado != 'finalizada':
            instance.finalizada_en = timezone.now()
        elif nuevo_estado == 'pendiente':
            instance.finalizada_en = None
        
        instance.estado = nuevo_estado
        instance.save()
        return instance