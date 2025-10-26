from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    """
    Middleware personalizado para manejar la autenticación
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs públicas que no requieren autenticación
        public_urls = [
            reverse('tareas:login'),
            reverse('tareas:registro'),
        ]
        
        # Si el usuario no está autenticado y no está en una URL pública
        if not request.user.is_authenticated and request.path not in public_urls:
            # Verificar si está intentando acceder a una vista protegida
            if not request.path.startswith('/admin/'):
                return redirect('tareas:login')
        
        response = self.get_response(request)
        return response