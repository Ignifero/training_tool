#!user/bin/env python
"""Módulo para clase Usuario. Contiene la clase Usuario y sus métodos."""

# Importación de módulos

import hashlib
from controllers import db_manager

# Clase

class Usuario:
    """Clase para los usuarios de la aplicación. 
    Contiene los atributos y métodos necesarios para la gestión de los usuarios."""
    
    def __init__(self, username, contrasena):
        # Atributos
        
        # Nombre de usuario
        try:
            if len(username) > 2:
                if type(username) is str:
                    if username.isalnum():
                        if not username.isspace():
                            self.username = username
            else:
                raise ValueError
        except ValueError:
            print("El nombre de usuario debe tener al menos 3 caracteres.")
    
        # Contraseña
        try:
            if len(contrasena) > 5:
                if type(contrasena) is str:
                    if not contrasena.isspace():
                        self.contrasena = hashlib.sha256(contrasena.encode()).hexdigest()
            else:
                raise ValueError
        except ValueError:
            print("La contraseña debe tener al menos 6 caracteres.")
            
    # Métodos
    
    def login(self):
        """Método para iniciar sesión."""
        
        if db_manager.validarUsuario(self.username, self.contrasena):
            return True
        else:
            return False
        
    def registro(self):
        """Método para registrar un nuevo usuario."""
        
        db_manager.nuevoUsuario(self.username, self.contrasena)
        
    def __str__(self):
        return f"Usuario: {self.username}"
    
    
    
    
if __name__ == "__main__":
    print("Este módulo no puede ser ejecutado directamente.")
    input("Pulse una tecla para continuar...")
