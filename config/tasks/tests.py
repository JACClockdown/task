import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Categoria, Tarea


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(
            username=kwargs.get('username', 'testuser'),
            email=kwargs.get('email', 'test@example.com'),
            password=kwargs.get('password', 'testpass123')
        )
    return make_user


@pytest.fixture
def create_categoria(db):
    def make_categoria(**kwargs):
        return Categoria.objects.create(
            nombre=kwargs.get('nombre', 'Test Categoria')
        )
    return make_categoria


@pytest.fixture
def authenticated_client(api_client, create_user):
    user = create_user()
    response = api_client.post('/api/auth/login/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    api_client.user = user
    return api_client




@pytest.mark.django_db
class TestAuthentication:
    
    def test_register_user(self, api_client):
        """Test: Registrar un nuevo usuario"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'username' in response.data
        assert response.data['username'] == 'newuser'
    
    def test_login_user(self, api_client, create_user):
        """Test: Login de usuario existente"""
        create_user(username='loginuser', password='loginpass123')
        response = api_client.post('/api/auth/login/', {
            'username': 'loginuser',
            'password': 'loginpass123'
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalid_credentials(self, api_client):
        """Test: Login con credenciales inválidas"""
        response = api_client.post('/api/auth/login/', {
            'username': 'noexiste',
            'password': 'wrongpass'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_logout_user(self, authenticated_client):
        """Test: Logout de usuario autenticado"""
        
        response = authenticated_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        refresh_token = response.data['refresh']
        
        response = authenticated_client.post('/api/auth/logout/', {
            'refresh': refresh_token
        })
        assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
class TestCategorias:
    
    def test_list_categorias(self, authenticated_client, create_categoria):
        """Test: Listar categorías"""
        create_categoria(nombre='Trabajo')
        create_categoria(nombre='Estudio')
        
        response = authenticated_client.get('/api/categorias/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_create_categoria(self, authenticated_client):
        """Test: Crear una nueva categoría"""
        data = {'nombre': 'Nueva Categoria'}
        response = authenticated_client.post('/api/categorias/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['nombre'] == 'Nueva Categoria'
    
    def test_create_duplicate_categoria(self, authenticated_client, create_categoria):
        """Test: No permitir categorías duplicadas"""
        create_categoria(nombre='Duplicada')
        data = {'nombre': 'Duplicada'}
        response = authenticated_client.post('/api/categorias/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST




@pytest.mark.django_db
class TestTareas:
    
    def test_create_tarea(self, authenticated_client, create_categoria):
        """Test: Crear una nueva tarea"""
        categoria = create_categoria(nombre='Trabajo')
        data = {
            'titulo': 'Mi primera tarea',
            'descripcion': 'Descripción de la tarea',
            'categoria': categoria.id
        }
        response = authenticated_client.post('/api/tareas/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['titulo'] == 'Mi primera tarea'
        assert 'color' in response.data
        assert response.data['color'].startswith('#')
    
    def test_tarea_unique_color(self, authenticated_client, create_categoria):
        """Test: Cada tarea debe tener un color único"""
        categoria = create_categoria(nombre='Trabajo')
        colores = []
        
        for i in range(5):
            data = {
                'titulo': f'Tarea {i}',
                'descripcion': 'Descripción',
                'categoria': categoria.id
            }
            response = authenticated_client.post('/api/tareas/', data)
            colores.append(response.data['color'])
        
        
        assert len(colores) == len(set(colores))
    
    def test_list_tareas_pendientes(self, authenticated_client, create_categoria):
        """Test: Listar solo tareas pendientes"""
        categoria = create_categoria(nombre='Trabajo')
        
        
        for i in range(3):
            Tarea.objects.create(
                titulo=f'Tarea Pendiente {i}',
                categoria=categoria,
                usuario=authenticated_client.user,
                estado='pendiente'
            )
        
        for i in range(2):
            Tarea.objects.create(
                titulo=f'Tarea Finalizada {i}',
                categoria=categoria,
                usuario=authenticated_client.user,
                estado='finalizada'
            )
        
        response = authenticated_client.get('/api/tareas/pendientes/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
    
    def test_list_tareas_finalizadas(self, authenticated_client, create_categoria):
        """Test: Listar solo tareas finalizadas"""
        categoria = create_categoria(nombre='Trabajo')
        
        for i in range(4):
            Tarea.objects.create(
                titulo=f'Tarea Finalizada {i}',
                categoria=categoria,
                usuario=authenticated_client.user,
                estado='finalizada'
            )
        
        response = authenticated_client.get('/api/tareas/finalizadas/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 4
    
    def test_update_tarea_estado(self, authenticated_client, create_categoria):
        """Test: Actualizar estado de tarea a finalizada"""
        categoria = create_categoria(nombre='Trabajo')
        tarea = Tarea.objects.create(
            titulo='Tarea a finalizar',
            categoria=categoria,
            usuario=authenticated_client.user,
            estado='pendiente'
        )
        
        response = authenticated_client.patch(
            f'/api/tareas/{tarea.id}/estado/',
            {'estado': 'finalizada'}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['estado'] == 'finalizada'
        assert response.data['finalizada_en'] is not None
    
    def test_delete_tarea(self, authenticated_client, create_categoria):
        """Test: Eliminar una tarea"""
        categoria = create_categoria(nombre='Trabajo')
        tarea = Tarea.objects.create(
            titulo='Tarea a eliminar',
            categoria=categoria,
            usuario=authenticated_client.user
        )
        
        response = authenticated_client.delete(f'/api/tareas/{tarea.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Tarea.objects.filter(id=tarea.id).exists()
    
    def test_pagination_works(self, authenticated_client, create_categoria):
        """Test: La paginación funciona correctamente (6 por página)"""
        categoria = create_categoria(nombre='Trabajo')
        
        
        for i in range(10):
            Tarea.objects.create(
                titulo=f'Tarea {i}',
                categoria=categoria,
                usuario=authenticated_client.user
            )
        
        response = authenticated_client.get('/api/tareas/pendientes/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 6
        assert response.data['count'] == 10
    
    def test_user_can_only_see_own_tasks(self, api_client, create_user, create_categoria):
        """Test: Un usuario solo puede ver sus propias tareas"""
        user1 = create_user(username='user1', password='pass1')
        user2 = create_user(username='user2', password='pass2')
        categoria = create_categoria(nombre='Trabajo')
        
        
        Tarea.objects.create(
            titulo='Tarea de User1',
            categoria=categoria,
            usuario=user1
        )
        
        
        Tarea.objects.create(
            titulo='Tarea de User2',
            categoria=categoria,
            usuario=user2
        )
        
        
        response = api_client.post('/api/auth/login/', {
            'username': 'user1',
            'password': 'pass1'
        })
        token = response.data['access']
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        
        response = api_client.get('/api/tareas/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['titulo'] == 'Tarea de User1'