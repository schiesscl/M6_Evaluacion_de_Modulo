#!/usr/bin/env python
"""Script para ejecutar todas las pruebas"""
import os
import sys
import django

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_tareas.settings')
    django.setup()
    
    from django.core.management import call_command
    from django.test.utils import get_runner
    from django.conf import settings
    
    print("=" * 70)
    print("EJECUTANDO PRUEBAS DEL GESTOR DE TAREAS")
    print("=" * 70)
    
    # Ejecutar pruebas
    call_command('test', 'tareas', verbosity=2)
    
    print("\n" + "=" * 70)
    print("PRUEBAS COMPLETADAS")
    print("=" * 70)