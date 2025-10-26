# Documentación de Pruebas - Gestor de Tareas

## Ejecutar Pruebas

### Todas las pruebas
```bash
python manage.py test tareas
```

### Pruebas específicas
```bash
# Solo pruebas de autenticación
python manage.py test tareas.tests.AuthenticationTests

# Solo pruebas de tareas
python manage.py test tareas.tests.TareaTests

# Prueba específica
python manage.py test tareas.tests.AuthenticationTests.test_login_correcto
```

### Con verbosidad
```bash
python manage.py test tareas --verbosity=2
```

## Casos de Prueba

### 1. Autenticación
✅ Registro de nuevo usuario
✅ Login con credenciales correctas
✅ Login con credenciales incorrectas
✅ Logout de usuario
✅ Acceso denegado sin autenticación

### 2. Gestión de Tareas
✅ Crear tarea
✅ Ver lista de tareas propias
✅ Ver detalle de tarea propia
✅ No ver tareas de otros usuarios
✅ Eliminar tarea propia
✅ No eliminar tareas de otros usuarios

### 3. Formularios
✅ Formulario válido de tarea
✅ Formulario inválido de tarea
✅ Validación de campos requeridos

### 4. Integración
✅ Flujo completo: registro → login → crear → ver → eliminar → logout

## Pruebas Manuales

### Funcionalidad Básica
1. **Registro**
   - Ir a /registro/
   - Completar formulario con datos válidos
   - Verificar redirección a lista de tareas
   - Verificar mensaje de bienvenida

2. **Login**
   - Ir a /login/
   - Ingresar credenciales correctas
   - Verificar acceso a área privada
   - Intentar con credenciales incorrectas
   - Verificar mensaje de error

3. **Crear Tarea**
   - Click en "Nueva Tarea"
   - Completar formulario
   - Verificar que aparece en la lista
   - Verificar mensaje de confirmación

4. **Ver Detalle**
   - Click en "Ver Detalle" de una tarea
   - Verificar que muestra información completa
   - Verificar botones de acción

5. **Eliminar Tarea**
   - Click en "Eliminar"
   - Confirmar eliminación
   - Verificar que desaparece de la lista
   - Verificar mensaje de confirmación

### Seguridad
1. **Aislamiento de Usuarios**
   - Crear usuario1 y usuario2
   - Crear tarea con usuario1
   - Intentar acceder a URL de tarea con usuario2
   - Verificar acceso denegado

2. **Protección de Rutas**
   - Cerrar sesión
   - Intentar acceder a /tareas/
   - Verificar redirección a login
   - Intentar acceder a /crear/
   - Verificar redirección a login

### Responsive
1. Probar en diferentes tamaños de pantalla
2. Verificar menú en móvil
3. Verificar formularios en móvil
4. Verificar tarjetas de tareas en móvil

## Resultados Esperados

Todas las pruebas deben pasar con éxito:
- ✅ Autenticación funcional
- ✅ CRUD de tareas operativo
- ✅ Seguridad implementada
- ✅ Validaciones correctas
- ✅ Mensajes informativos
- ✅ UI responsive