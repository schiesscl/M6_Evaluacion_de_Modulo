# M6_Evaluación del módulo

## Hans Schiess

### Gestor de Tareas

Sistema de gestión de tareas con autenticación de usuarios.

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```
3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```
4. Configurar variables de entorno:

   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```
5. Generar SECRET_KEY:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   # Copiar el resultado en .env
   ```
6. Ejecutar migraciones:

   ```bash
   python manage.py migrate
   ```
7. Crear superusuario (opcional):

   ```bash
   python manage.py createsuperuser
   ```
8. Ejecutar servidor:

   ```bash
   python manage.py runserver
   ```

## Ejecutar Pruebas

```bash
python manage.py test tareas
```

## Configuración de Producción

Ver archivo `DEPLOYMENT_CHECKLIST.md`
