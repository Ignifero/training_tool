#!user/bin/env python
"""Carpeta para los controladores de la aplicación. Contiene los controladores de la aplicación,
así como algunas funciones auxiliares para la gestión de la base de datos."""

# Importación de módulos

import os

# Funciones

def cls():
    """Función para limpiar la pantalla. Se usa para mejorar la experiencia de usuario."""
    os.system("cls" if os.name == "nt" else "clear")
