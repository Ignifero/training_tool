#!user/bin/env python
"""Módulo para clase Asesorado. Contiene la clase Asesorado, sus atributos y sus métodos."""

# Importación de módulos

from datetime import date
from datetime import datetime
from controllers import db_manager

# Clase

class Asesorado:
    """Clase para los asesorados de la aplicación. Este objeto se crea al iniciar sesión con un usuario.
    Contiene los atributos y métodos necesarios para la gestión de los asesorados."""
    
    def __init__(self, nombre, fecha_nacido, altura, peso, sexo, somatotipo, porcen_graso, user):
        
        # Nombre
        try:
            if len(nombre) > 11:
                if type(nombre) is str:
                    if not nombre.isspace():
                        if "0" or "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" not in nombre:
                            self.nombre = nombre
            else:
                raise ValueError
        except ValueError:
            print("El nombre debe tener al menos 12 caracteres. Escriba su nombre completo.")
            
        # Fecha de nacimiento
        try:
            _fecha = datetime.strptime(fecha_nacido, "%d/%m/%Y")
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
            if sexo.upper() == "H" or sexo.upper() == "M":
                self.sexo = sexo.upper()
            else:
                raise ValueError
        except ValueError:
            print("El sexo debe ser H para hombre o M para mujer.")
            
        # Somatotipo
        try:
            if somatotipo.upper() == "E" or somatotipo.upper() == "M" or somatotipo.upper() == "H":
                self.somatotipo = somatotipo.upper()
            else:
                raise ValueError
        except ValueError:
            print("El somatotipo debe ser E para ectomorfo, M para mesomorfo o H para endomorfo.")
            
        # Porcentaje de grasa
        try:
            if float(porcen_graso) < 60 and float(porcen_graso) > 0:
                self.porcen_graso = float(porcen_graso)
            else:
                raise ValueError
        except ValueError:
            print("El porcentaje de grasa debe ser un número entre 0 y 60.")
            
        # Gasto energético basal
        edad = date.today().year - datetime.strptime(fecha_nacido, "%d/%m/%Y").year
        
        if self.sexo == "H":
            tmb = 66.5 + 13.8 * self.peso + 5 * self.altura - 6.8 * edad
            self.gasto = tmb
        else:
            tmb = 655.1 + 9.6 * self.peso + 1.8 * self.altura - 4.7 * edad
            self.gasto = tmb
            
        # Usuario
        
        self.user = user
            
            
    def registrar(self):
        """Método para registrar un asesorado en la base de datos."""
        
        db_manager.nuevoAsesorado(self.nombre, self.fecha_nacido, self.altura, self.peso,
                                       self.sexo, self.somatotipo, self.porcen_graso, self.gasto, self.user)
       
        
    def actualizar(self, altura, peso, p_graso):
        """Método para actualizar los datos de un asesorado."""
        
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
            
        # Porcentaje de grasa
        try:
            if float(p_graso) < 60 and float(p_graso) > 0:
                self.porcen_graso = float(p_graso)
            else:
                raise ValueError
        except ValueError:
            print("El porcentaje de grasa debe ser un número entre 0 y 60.")
            
        # Gasto energético basal
        edad = date.today().year - datetime.strptime(self.fecha_nacido, "%d/%m/%Y").year
        
        if self.sexo == "H":
            tmb = 66.5 + (13.8 * peso) + (5 * altura) - (6.8 * edad)
            self.gasto = tmb
        else:
            tmb = 655.1 + (9.6 * peso) + (1.8 * altura) - (4.7 * edad)
            self.gasto = tmb
            
        db_manager.actualizarAsesorado(self.nombre, self.altura, self.peso, self.porcen_graso, self.gasto)
        
    def __str__(self):
        """Método para imprimir los datos de un asesorado."""
        
        return "Nombre: {}\nFecha de nacimiento: {}\nAltura: {}\nPeso: {}\nSexo: {}\nSomatotipo: {}\nPorcentaje de grasa: {}\nGasto energético basal: {}".format(self.nombre, self.fecha_nacido, self.altura, self.peso, self.sexo, self.somatotipo, self.porcen_graso, self.gasto)
