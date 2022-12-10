#!user/bin/env python
"""Módulo para clase Asesorado. Contiene la clase Asesorado, sus atributos y sus métodos."""

# Importación de módulos

from datetime import date
from controllers import db_manager

# Clase

class Asesorado:
    """Clase para los asesorados de la aplicación. Este objeto se crea al iniciar sesión con un usuario.
    Contiene los atributos y métodos necesarios para la gestión de los asesorados."""
    
    def __init__(self, nombre, fecha_nacido, altura, peso, sexo, somatotipo, gasto):
        
        # Nombre
        try:
            if len(nombre) > 11:
                if type(nombre) is str:
                    if not nombre.isspace():
                        if nombre.isalpha():
                            self.nombre = nombre
            else:
                raise ValueError
        except ValueError:
            print("El nombre debe tener al menos 12 caracteres. Escriba su nombre completo.")
            
        # Fecha de nacimiento
        try:
            _fecha = date.strftime(fecha_nacido, "%d/%m/%Y")
            self.fecha_nacido = fecha_nacido
        except ValueError:
            print("La fecha de nacimiento no es válida.")
        
        # Altura
        try:
            if int(altura) < 300:
                self.altura = int(altura)
            else:
                raise ValueError
        except ValueError:
            print("La altura debe ser un número entero. Se guardarán los centímetros, no metros.")
            
        # Peso
        try:
            if float(peso) < 200:
                self.peso = float(peso)
            else:
                raise ValueError
        except ValueError:
            print("El peso debe ser un número. Se guardarán los kilogramos menores a 200kg.")
            
        # Sexo
        try:
            if sexo == "H" or sexo == "M":
                self.sexo = sexo
            else:
                raise ValueError
        except ValueError:
            print("El sexo debe ser H para hombre o M para mujer.")
            
        # Somatotipo
        try:
            if somatotipo == "E" or somatotipo == "M" or somatotipo == "H":
                self.somatotipo = somatotipo
            else:
                raise ValueError
        except ValueError:
            print("El somatotipo debe ser E para ectomorfo, M para mesomorfo o H para endomorfo.")
            
        # Gasto energético basal
        """if sexo == "M":
        tmb = 66.5 + (13.8 * peso) + (5 * altura) - (6.8 * edad)
    else:
        tmb = 655.1 + (9.6 * peso) + (1.8 * altura) - (4.7 * edad)"""
