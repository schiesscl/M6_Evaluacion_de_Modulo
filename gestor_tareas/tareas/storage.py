# Almacenamiento en memoria para las tareas
tareas_storage = []
contador_id = 1

def obtener_todas_tareas():
    """Retorna todas las tareas"""
    return tareas_storage

def obtener_tarea_por_id(tarea_id):
    """Obtiene una tarea específica por su ID"""
    for tarea in tareas_storage:
        if tarea['id'] == tarea_id:
            return tarea
    return None

def agregar_tarea(titulo, descripcion, usuario):
    """Agrega una nueva tarea"""
    global contador_id
    tarea = {
        'id': contador_id,
        'titulo': titulo,
        'descripcion': descripcion,
        'usuario': usuario,
        'completada': False
    }
    tareas_storage.append(tarea)
    contador_id += 1
    return tarea

def editar_tarea(tarea_id, titulo, descripcion):
    """Edita una tarea existente"""
    tarea = obtener_tarea_por_id(tarea_id)
    if tarea:
        tarea['titulo'] = titulo
        tarea['descripcion'] = descripcion
        return tarea
    return None

def eliminar_tarea(tarea_id):
    """Elimina una tarea por su ID"""
    global tareas_storage
    tareas_storage = [t for t in tareas_storage if t['id'] != tarea_id]

def obtener_tareas_usuario(username):
    """Obtiene todas las tareas de un usuario específico"""
    return [t for t in tareas_storage if t['usuario'] == username]