from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import TareaForm, RegistroForm
from .storage import (
    obtener_tareas_usuario,
    obtener_tarea_por_id,
    agregar_tarea,
    editar_tarea,
    eliminar_tarea as eliminar_tarea_storage
)

# Vista de registro
def registro_view(request):
    # Si el usuario ya está autenticado, redirigir a lista de tareas
    if request.user.is_authenticated:
        return redirect('tareas:lista_tareas')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Iniciar sesión automáticamente después del registro
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}! Tu cuenta ha sido creada exitosamente.')
            return redirect('tareas:lista_tareas')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroForm()
    return render(request, 'tareas/registro.html', {'form': form})

# Vista de login
def login_view(request):
    # Si el usuario ya está autenticado, redirigir a lista de tareas
    if request.user.is_authenticated:
        return redirect('tareas:lista_tareas')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {username}!')
            # Redirigir a la página que intentaba acceder o a lista de tareas
            next_url = request.GET.get('next', 'tareas:lista_tareas')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Por favor intenta de nuevo.')
    return render(request, 'tareas/login.html')

# Vista de logout
@login_required
def logout_view(request):
    username = request.user.username
    logout(request)
    messages.success(request, f'¡Hasta luego, {username}! Has cerrado sesión exitosamente.')
    return redirect('tareas:login')

# Vista de lista de tareas
@login_required
def lista_tareas(request):
    # Obtener solo las tareas del usuario autenticado
    tareas = obtener_tareas_usuario(request.user.username)
    context = {
        'tareas': tareas,
        'total_tareas': len(tareas)
    }
    return render(request, 'tareas/lista_tareas.html', context)

# Vista de detalle de tarea
@login_required
def detalle_tarea(request, tarea_id):
    tarea = obtener_tarea_por_id(tarea_id)
    
    # Verificar que la tarea existe
    if not tarea:
        messages.error(request, 'La tarea que buscas no existe.')
        return redirect('tareas:lista_tareas')
    
    # Verificar que la tarea pertenece al usuario autenticado
    if tarea['usuario'] != request.user.username:
        messages.error(request, 'No tienes permiso para ver esta tarea.')
        return redirect('tareas:lista_tareas')
    
    return render(request, 'tareas/detalle_tarea.html', {'tarea': tarea})

# Vista para crear tarea
@login_required
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            # Asociar la tarea al usuario autenticado
            agregar_tarea(titulo, descripcion, request.user.username)
            messages.success(request, f'La tarea "{titulo}" ha sido creada exitosamente.')
            return redirect('tareas:lista_tareas')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = TareaForm()
    return render(request, 'tareas/crear_tarea.html', {'form': form})

# Vista para editar tarea
@login_required
def editar_tarea(request, tarea_id):
    tarea = obtener_tarea_por_id(tarea_id)
    
    # Verificar que la tarea existe
    if not tarea:
        messages.error(request, 'La tarea que intentas editar no existe.')
        return redirect('tareas:lista_tareas')
    
    # Verificar que la tarea pertenece al usuario autenticado
    if tarea['usuario'] != request.user.username:
        messages.error(request, 'No tienes permiso para editar esta tarea.')
        return redirect('tareas:lista_tareas')
    
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            editar_tarea(tarea_id, titulo, descripcion)
            messages.success(request, f'La tarea "{titulo}" ha sido actualizada exitosamente.')
            return redirect('tareas:detalle_tarea', tarea_id=tarea_id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # Pre-cargar el formulario con los datos existentes
        form = TareaForm(initial={
            'titulo': tarea['titulo'],
            'descripcion': tarea['descripcion']
        })
    
    return render(request, 'tareas/editar_tarea.html', {'form': form, 'tarea': tarea})

# Vista para eliminar tarea
@login_required
def eliminar_tarea(request, tarea_id):
    tarea = obtener_tarea_por_id(tarea_id)
    
    # Verificar que la tarea existe
    if not tarea:
        messages.error(request, 'La tarea que intentas eliminar no existe.')
        return redirect('tareas:lista_tareas')
    
    # Verificar que la tarea pertenece al usuario autenticado
    if tarea['usuario'] != request.user.username:
        messages.error(request, 'No tienes permiso para eliminar esta tarea.')
        return redirect('tareas:lista_tareas')
    
    if request.method == 'POST':
        titulo = tarea['titulo']
        eliminar_tarea_storage(tarea_id)
        messages.success(request, f'La tarea "{titulo}" ha sido eliminada exitosamente.')
        return redirect('tareas:lista_tareas')
    
    return render(request, 'tareas/eliminar_tarea.html', {'tarea': tarea})

# Vista de página de inicio
def home_view(request):
    """Vista de página de inicio"""
    if request.user.is_authenticated:
        return redirect('tareas:lista_tareas')
    return render(request, 'tareas/home.html')
