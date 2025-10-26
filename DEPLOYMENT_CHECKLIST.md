# Checklist de Despliegue - Gestor de Tareas

## Antes del Despliegue

### Configuración

- [ ] Cambiar `DEBUG = False` en settings_prod.py
- [ ] Configurar `ALLOWED_HOSTS` con tu dominio
- [ ] Generar nueva `SECRET_KEY` para producción
- [ ] Configurar variables de entorno
- [ ] Configurar base de datos de producción (si aplica)

### Seguridad

- [ ] Activar `SESSION_COOKIE_SECURE = True`
- [ ] Activar `CSRF_COOKIE_SECURE = True`
- [ ] Activar `SECURE_SSL_REDIRECT = True`
- [ ] Configurar certificado SSL/TLS
- [ ] Revisar configuraciones HSTS

### Archivos Estáticos

- [ ] Ejecutar `python manage.py collectstatic`
- [ ] Configurar servidor web para servir archivos estáticos

### Base de Datos

- [ ] Ejecutar `python manage.py migrate`
- [ ] Crear superusuario: `python manage.py createsuperuser`
- [ ] Hacer backup de la base de datos

### Pruebas

- [ ] Ejecutar todas las pruebas: `python manage.py test`
- [ ] Probar registro de usuario
- [ ] Probar login/logout
- [ ] Probar creación de tareas
- [ ] Probar eliminación de tareas
- [ ] Verificar que usuarios no puedan ver tareas ajenas

### Monitoreo

- [ ] Configurar logging
- [ ] Configurar monitoreo de errores
- [ ] Configurar alertas

## Comandos Útiles

### Desarrollo

```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar pruebas
python manage.py test tareas

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### Producción

```bash
# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar con settings de producción
python manage.py runserver --settings=gestor_tareas.settings_prod

# Crear superusuario
python manage.py createsuperuser
```

## Verificación Post-Despliegue

- [ ] Verificar que el sitio carga correctamente
- [ ] Probar registro de nuevo usuario
- [ ] Probar login
- [ ] Crear una tarea de prueba
- [ ] Eliminar la tarea de prueba
- [ ] Verificar logs de errores
- [ ] Verificar certificado SSL
- [ ] Probar en diferentes navegadores
- [ ] Probar en dispositivos móviles
