#!user/bin/env python
"""Módulo de la clase Alimento. Contiene los atributos y métodos de la clase Alimento."""

# Importación de módulos

from datetime import datetime
from datetime import date
from controllers import db_manager
from controllers import barcode_scaner

# Clase

class Alimento:
    """Esta clase permitirá la gestión de los alimentos de la aplicación. Con ella se llevará el
    control de los alimentos que se consumen, así como de sus características nutricionales."""

    def __init__(self, nombre, calorias, proteinas, grasas, carbos, gramos_envase, cm3_envase, cant_envases):
        """Constructor de la clase Alimento."""
        
        # Atributos de la clase Alimento

        # Código del alimento

        self.codigo = barcode_scaner.qr_scanner()

        # Nombre del alimento
        self.nombre = self.validar_nombre(nombre)

        # Calorías del alimento
        self.calorias = self.validar_valor_entero(calorias, "Las calorías del alimento")

        # Proteínas del alimento
        self.proteinas = self.validar_valor_entero(proteinas, "Las proteínas del alimento")

        # Grasas del alimento
        self.grasas = self.validar_valor_entero(grasas, "Las grasas del alimento")

        # Carbohidratos del alimento
        self.carbos = self.validar_valor_entero(carbos, "Los carbohidratos del alimento")

        # Gramos por envase del alimento
        self.gramos_envase = self.validar_valor_entero(gramos_envase, "Los gramos por envase del alimento")

        # Centímetros cúbicos por envase del alimento
        self.cm3_envase = self.validar_valor_entero(cm3_envase, "Los centímetros cúbicos por envase del alimento")

        # Cantidad de envases del alimento
        self.cant_envases = self.validar_valor_entero(cant_envases, "La cantidad de envases del alimento")

    def validar_nombre(self, nombre):
        try:
            if nombre == "":
                raise ValueError("El nombre del alimento no puede estar vacío.")
            elif nombre is None:
                raise ValueError("El nombre del alimento no puede ser nulo.")
            elif not isinstance(nombre, str):
                raise ValueError("El nombre del alimento debe ser una cadena de caracteres.")
            elif nombre.isnumeric():
                raise ValueError("El nombre del alimento no puede ser un número.")
            elif len(nombre) > 50:
                raise ValueError("El nombre del alimento no puede tener más de 50 caracteres.")
            elif len(nombre) < 3:
                raise ValueError("El nombre del alimento no puede tener menos de 3 caracteres.")
            else:
                return nombre
        except Exception as e:
            print(e)

    def validar_valor_entero(self, valor, mensaje):
        try:
            if valor == "":
                raise ValueError(f"{mensaje} no pueden estar vacías.")
            elif valor is None:
                raise ValueError(f"{mensaje} no pueden ser nulas.")
            elif not isinstance(valor, int):
                raise ValueError(f"{mensaje} deben ser un número entero.")
            elif valor < 0:
                raise ValueError(f"{mensaje} no pueden ser negativas.")
            else:
                return valor
        except Exception as e:
            print(e)
            
