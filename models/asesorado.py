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
        
        return f"""
    Nombre: {self.nombre.title()}
    Fecha de nacimiento: {self.fecha_nacido}
    Sexo: {self.sexo}
    Altura: {self.altura} cm
    Peso: {self.peso} kg
    Somatotipo: {"Ectomorfo" if self.somatotipo == "E" else "Mesomorfo" if self.somatotipo == "M" else "Endomorfo"}
    Porcentaje de grasa: {self.porcen_graso}%
    Gasto energético basal: {round(self.gasto, 2)} kcal
    """
    
    def ffmi(self):
        ffmi = (self.peso * ((100 - self.porcen_graso) / 100)) / ((self.altura / 100) ** 2)
        
        if self.sexo == "H":
            if ffmi < 18:
                fisico = "pobre"
            elif ffmi >= 18 and ffmi < 19:
                fisico = "regular"
            elif ffmi >= 19 and ffmi < 20:
                fisico = "normal"
            elif ffmi >= 20 and ffmi < 21:
                fisico = "bueno"
            elif ffmi >= 21 and ffmi < 22.5:
                fisico = "muy bueno"
            elif ffmi >= 22.5 and ffmi < 24:
                fisico = "excelente"
            elif ffmi >= 24 and ffmi < 26:
                fisico = "totalmente desarrollado. ¡Enhorabuena! ¡Haz alcanzado el máximo!"
            else:
                fisico = "excesivamente desarrollado. ¿Estás seguro de que no estás tomando esteroides?"
        else:
            if ffmi < 13.5:
                fisico = "pobre"
            elif ffmi >= 13.5 and ffmi < 14.5:
                fisico = "regular"
            elif ffmi >= 14.5 and ffmi < 16:
                fisico = "normal"
            elif ffmi >= 16 and ffmi < 17:
                fisico = "bueno"
            elif ffmi >= 17 and ffmi < 18.5:
                fisico = "muy bueno"
            elif ffmi >= 18.5 and ffmi < 20.5:
                fisico = "excelente"
            elif ffmi >= 20.5 and ffmi < 22:
                fisico = "totalmente desarrollado. ¡Enhorabuena! ¡Haz alcanzado el máximo!"
            else:
                fisico = "excesivamente desarrollado. ¿Estás seguro de que no estás tomando esteroides?"
        
        return round(ffmi, 1), fisico;

    def ffmi_text(self):
        """Método para calcular el índice de masa muscular libre de grasa."""
        
        ffmi = (self.peso * ((100 - self.porcen_graso) / 100)) / ((self.altura / 100) ** 2)
        
        if self.sexo == "H":
            if ffmi < 18:
                fisico = "pobre"
            elif ffmi >= 18 and ffmi < 19:
                fisico = "regular"
            elif ffmi >= 19 and ffmi < 20:
                fisico = "normal"
            elif ffmi >= 20 and ffmi < 21:
                fisico = "bueno"
            elif ffmi >= 21 and ffmi < 22.5:
                fisico = "muy bueno"
            elif ffmi >= 22.5 and ffmi < 24:
                fisico = "excelente"
            elif ffmi >= 24 and ffmi < 26:
                fisico = "totalmente desarrollado. ¡Enhorabuena! ¡Haz alcanzado el máximo!"
            else:
                fisico = "excesivamente desarrollado. ¿Estás seguro de que no estás tomando esteroides?"
        elif self.sexo == "M":
            if ffmi < 13.5:
                fisico = "pobre"
            elif ffmi >= 13.5 and ffmi < 14.5:
                fisico = "regular"
            elif ffmi >= 14.5 and ffmi < 16:
                fisico = "normal"
            elif ffmi >= 16 and ffmi < 17:
                fisico = "bueno"
            elif ffmi >= 17 and ffmi < 18.5:
                fisico = "muy bueno"
            elif ffmi >= 18.5 and ffmi < 20.5:
                fisico = "excelente"
            elif ffmi >= 20.5 and ffmi < 22:
                fisico = "totalmente desarrollado. ¡Enhorabuena! ¡Haz alcanzado el máximo!"
            else:
                fisico = "excesivamente desarrollado. ¿Estás seguro de que no estás tomando esteroides?"
        
        return f"""Nivel de desarrollo corporal:
    
    El índice de masa muscular es de {round(ffmi, 2)}. Esto indica que posee nivel físico {fisico}. Puedes
    ver la tabla de referencia abajo para saber qué significa cada nivel:
    
   --------------------------------------------------------
   |  HOMBRES   |       FORMA FÍSICA        |   MUJERES   |
   --------------------------------------------------------
   | 18 o menos |           pobre           | 13.5 o menos|
   --------------------------------------------------------
   |  18 - 19   |          regular          | 13.5 - 14.5 |
   --------------------------------------------------------
   |  19 - 20   |           normal          | 14.5 - 16   |
   --------------------------------------------------------
   |  20 - 21   |           bueno           | 16 - 17     |
   --------------------------------------------------------
   |  21 - 22.5 |         muy bueno         | 17 - 18.5   |
   --------------------------------------------------------
   |  22.5 - 24 |         excelente         | 18.5 - 20.5 |
   --------------------------------------------------------
   |  24 - 26   |           Máximo          | 20.5 - 22   |
   --------------------------------------------------------
   | más de 26  | Posible uso de esteroides | más de 22   |
   --------------------------------------------------------
    """
