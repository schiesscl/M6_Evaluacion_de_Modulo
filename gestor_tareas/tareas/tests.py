from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tareas import storage

class AuthenticationTests(TestCase):
    """Pruebas para el sistema de autenticación"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        # Limpiar almacenamiento
        storage.tareas_storage.clear()
        storage.contador_id = 1
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_registro_usuario(self):
        """Prueba de registro de nuevo usuario"""
        response = self.client.post(reverse('tareas:registro'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpass123456',
            'password2': 'testpass123456'
        })
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_correcto(self):
        """Prueba de inicio de sesión con credenciales correctas"""
        response = self.client.post(reverse('tareas:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_incorrecto(self):
        """Prueba de inicio de sesión con credenciales incorrectas"""
        response = self.client.post(reverse('tareas:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Se mantiene en la página
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_logout(self):
        """Prueba de cierre de sesión"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tareas:logout'))
        self.assertEqual(response.status_code, 302)  # Redirección
    
    def test_acceso_sin_autenticacion(self):
        """Prueba de acceso a vistas protegidas sin autenticación"""
        response = self.client.get(reverse('tareas:lista_tareas'))
        self.assertEqual(response.status_code, 302)  # Redirección a login
        self.assertIn('/login/', response.url)


class TareaTests(TestCase):
    """Pruebas para el sistema de gestión de tareas"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.client = Client()
        # Limpiar almacenamiento antes de cada prueba
        storage.tareas_storage.clear()
        storage.contador_id = 1
        
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
    
    def test_crear_tarea(self):
        """Prueba de creación de tarea"""
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('tareas:crear_tarea'), {
            'titulo': 'Tarea de prueba',
            'descripcion': 'Descripción de prueba'
        })
        self.assertEqual(response.status_code, 302)  # Redirección
        tareas = storage.obtener_tareas_usuario('user1')
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0]['titulo'], 'Tarea de prueba')
    
    def test_editar_tarea_propia(self):
        """Prueba de edición de tarea propia"""
        tarea = storage.agregar_tarea('Tarea original', 'Descripción original', 'user1')
        self.client.login(username='user1', password='pass123')
        
        response = self.client.post(
            reverse('tareas:editar_tarea', kwargs={'tarea_id': tarea['id']}),
            {
                'titulo': 'Tarea editada',
                'descripcion': 'Descripción editada'
            }
        )
        
        self.assertEqual(response.status_code, 302)  # Redirección
        tarea_editada = storage.obtener_tarea_por_id(tarea['id'])
        self.assertEqual(tarea_editada['titulo'], 'Tarea editada')
        self.assertEqual(tarea_editada['descripcion'], 'Descripción editada')
    
    def test_no_editar_tarea_ajena(self):
        """Prueba que no se puede editar tarea de otro usuario"""
        tarea = storage.agregar_tarea('Tarea User1', 'Descripción', 'user1')
        self.client.login(username='user2', password='pass123')
        
        response = self.client.post(
            reverse('tareas:editar_tarea', kwargs={'tarea_id': tarea['id']}),
            {
                'titulo': 'Intento de edición',
                'descripcion': 'No debería funcionar'
            }
        )
        
        self.assertEqual(response.status_code, 302)  # Redirección
        # La tarea no debe haber cambiado
        tarea_sin_cambios = storage.obtener_tarea_por_id(tarea['id'])
        self.assertEqual(tarea_sin_cambios['titulo'], 'Tarea User1')
    
    def test_lista_tareas_usuario(self):
        """Prueba que usuarios solo ven sus propias tareas"""
        # Crear tareas para diferentes usuarios
        storage.agregar_tarea('Tarea User1', 'Descripción 1', 'user1')
        storage.agregar_tarea('Tarea User2', 'Descripción 2', 'user2')
        
        # Login como user1
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('tareas:lista_tareas'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tareas']), 1)
        self.assertEqual(response.context['tareas'][0]['titulo'], 'Tarea User1')
    
    def test_ver_detalle_tarea_propia(self):
        """Prueba de ver detalle de tarea propia"""
        tarea = storage.agregar_tarea('Mi tarea', 'Mi descripción', 'user1')
        self.client.login(username='user1', password='pass123')
        response = self.client.get(
            reverse('tareas:detalle_tarea', kwargs={'tarea_id': tarea['id']})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mi tarea')
    
    def test_no_ver_detalle_tarea_ajena(self):
        """Prueba que no se puede ver tarea de otro usuario"""
        tarea = storage.agregar_tarea('Tarea User1', 'Descripción', 'user1')
        self.client.login(username='user2', password='pass123')
        response = self.client.get(
            reverse('tareas:detalle_tarea', kwargs={'tarea_id': tarea['id']})
        )
        self.assertEqual(response.status_code, 302)  # Redirección
    
    def test_eliminar_tarea_propia(self):
        """Prueba de eliminación de tarea propia"""
        tarea = storage.agregar_tarea('Tarea a eliminar', 'Descripción', 'user1')
        self.client.login(username='user1', password='pass123')
        response = self.client.post(
            reverse('tareas:eliminar_tarea', kwargs={'tarea_id': tarea['id']})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(storage.obtener_tarea_por_id(tarea['id']))
    
    def test_no_eliminar_tarea_ajena(self):
        """Prueba que no se puede eliminar tarea de otro usuario"""
        tarea = storage.agregar_tarea('Tarea User1', 'Descripción', 'user1')
        tarea_id_original = tarea['id']
        self.client.login(username='user2', password='pass123')
        response = self.client.post(
            reverse('tareas:eliminar_tarea', kwargs={'tarea_id': tarea_id_original})
        )
        self.assertEqual(response.status_code, 302)
        # La tarea debe seguir existiendo
        self.assertIsNotNone(storage.obtener_tarea_por_id(tarea_id_original))


class FormularioTests(TestCase):
    """Pruebas para los formularios"""
    
    def setUp(self):
        self.client = Client()
        # Limpiar almacenamiento
        storage.tareas_storage.clear()
        storage.contador_id = 1
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123'
        )
        self.client.login(username='testuser', password='pass123')
    
    def test_formulario_tarea_valido(self):
        """Prueba de formulario de tarea con datos válidos"""
        response = self.client.post(reverse('tareas:crear_tarea'), {
            'titulo': 'Tarea válida',
            'descripcion': 'Descripción válida'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_formulario_tarea_invalido(self):
        """Prueba de formulario de tarea con datos inválidos"""
        response = self.client.post(reverse('tareas:crear_tarea'), {
            'titulo': '',  # Campo vacío
            'descripcion': 'Descripción'
        })
        self.assertEqual(response.status_code, 200)  # Se mantiene en la página
        # Verificar que hay errores en el formulario
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('titulo', response.context['form'].errors)


class IntegrationTests(TestCase):
    """Pruebas de integración del flujo completo"""
    
    def setUp(self):
        """Limpiar almacenamiento antes de cada prueba"""
        storage.tareas_storage.clear()
        storage.contador_id = 1
    
    def test_flujo_completo_usuario(self):
        """Prueba del flujo completo: registro, login, crear, editar, ver, eliminar"""
        client = Client()
        
        # 1. Registro
        response = client.post(reverse('tareas:registro'), {
            'username': 'integrationuser',
            'email': 'integration@example.com',
            'password1': 'testpass123456',
            'password2': 'testpass123456'
        })
        self.assertEqual(response.status_code, 302)
        
        # 2. Verificar login automático después del registro
        self.assertTrue(User.objects.filter(username='integrationuser').exists())
        
        # 3. Crear tarea
        response = client.post(reverse('tareas:crear_tarea'), {
            'titulo': 'Tarea de integración',
            'descripcion': 'Descripción de integración'
        })
        self.assertEqual(response.status_code, 302)
        
        # 4. Ver lista de tareas
        response = client.get(reverse('tareas:lista_tareas'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tareas']), 1)
        
        # 5. Ver detalle de tarea
        tarea_id = response.context['tareas'][0]['id']
        response = client.get(reverse('tareas:detalle_tarea', kwargs={'tarea_id': tarea_id}))
        self.assertEqual(response.status_code, 200)
        
        # 6. Editar tarea
        response = client.post(
            reverse('tareas:editar_tarea', kwargs={'tarea_id': tarea_id}),
            {
                'titulo': 'Tarea editada',
                'descripcion': 'Descripción editada'
            }
        )
        self.assertEqual(response.status_code, 302)
        
        # 7. Verificar que se editó
        response = client.get(reverse('tareas:lista_tareas'))
        self.assertEqual(response.context['tareas'][0]['titulo'], 'Tarea editada')
        
        # 8. Eliminar tarea
        response = client.post(reverse('tareas:eliminar_tarea', kwargs={'tarea_id': tarea_id}))
        self.assertEqual(response.status_code, 302)
        
        # 9. Verificar lista vacía
        response = client.get(reverse('tareas:lista_tareas'))
        self.assertEqual(len(response.context['tareas']), 0)
        
        # 10. Logout
        response = client.get(reverse('tareas:logout'))
        self.assertEqual(response.status_code, 302)
