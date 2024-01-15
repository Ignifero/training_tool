#!user/bin/env python
"""Módulo para clase Asesorado. Contiene la clase Asesorado, sus atributos y sus métodos."""

# Importación de módulos

from datetime import date
from datetime import datetime
from controllers import db_manager

# Constantes

DATE_FORMAT = "%d/%m/%Y"

# Clase

class Asesorado:
    """Clase para los asesorados de la aplicación. Este objeto se crea al iniciar sesión con un usuario.
    Contiene los atributos y métodos necesarios para la gestión de los asesorados."""
    
    def __init__(self, nombre, fecha_nacido, altura, peso, sexo, somatotipo, porcen_graso, user):
        self.nombre = self.validar_nombre(nombre)
        self.fecha_nacido = self.validar_fecha_nacimiento(fecha_nacido)
        self.altura = self.validar_altura(altura)
        self.peso = self.validar_peso(peso)
        self.sexo = self.validar_sexo(sexo)
        self.somatotipo = self.validar_somatotipo(somatotipo)
        self.porcen_graso = self.validar_porcentaje_grasa(porcen_graso)
        self.gasto = self.calcular_gasto_energetico(fecha_nacido, sexo, peso, altura)
        self.user = user

    def validar_nombre(self, nombre):
        if len(nombre) > 11 and isinstance(nombre, str) and not nombre.isspace() and not any(char.isdigit() for char in nombre):
            return nombre
        else:
            raise ValueError("El nombre debe tener al menos 12 caracteres. Escriba su nombre completo.")

    def validar_fecha_nacimiento(self, fecha_nacido):
        try:
            return datetime.strptime(fecha_nacido, DATE_FORMAT)
        except ValueError:
            raise ValueError("La fecha de nacimiento no es válida.")

    def validar_altura(self, altura):
        try:
            if int(altura) < 300:
                return int(altura)
            else:
                raise ValueError
        except ValueError:
            raise ValueError("La altura debe ser un número entero. Se guardarán los centímetros, no metros.")

    def validar_peso(self, peso):
        try:
            if float(peso) < 200:
                return float(peso)
            else:
                raise ValueError
        except ValueError:
            raise ValueError("El peso debe ser un número. Se guardarán los kilogramos menores a 200kg.")

    def validar_sexo(self, sexo):
        if sexo.upper() == "H" or sexo.upper() == "M":
            return sexo.upper()
        else:
            raise ValueError("El sexo debe ser H para hombre o M para mujer.")

    def validar_somatotipo(self, somatotipo):
        if somatotipo.upper() == "E" or somatotipo.upper() == "M" or somatotipo.upper() == "H":
            return somatotipo.upper()
        else:
            raise ValueError("El somatotipo debe ser E para ectomorfo, M para mesomorfo o H para endomorfo.")

    def validar_porcentaje_grasa(self, porcen_graso):
        try:
            if float(porcen_graso) < 60 and float(porcen_graso) > 0:
                return float(porcen_graso)
            else:
                raise ValueError
        except ValueError:
            raise ValueError("El porcentaje de grasa debe ser un número entre 0 y 60.")

    def calcular_gasto_energetico(self, fecha_nacido, sexo, peso, altura):
        edad = date.today().year - datetime.strptime(fecha_nacido, DATE_FORMAT).year
        if sexo == "H":
            return 66.5 + 13.8 * peso + 5 * altura - 6.8 * edad
        else:
            return 655.1 + 9.6 * peso + 1.8 * altura - 4.7 * edad
            
            
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
        edad = date.today().year - datetime.strptime(self.fecha_nacido, DATE_FORMAT).year
        
        if self.sexo == "H":
            tmb = 66.5 + (13.8 * peso) + (5 * altura) - (6.8 * edad)
            self.gasto = tmb
        else:
            tmb = 655.1 + (9.6 * peso) + (1.8 * altura) - (4.7 * edad)
            self.gasto = tmb
            
        db_manager.actualizarAsesorado(self.nombre, self.altura, self.peso, self.porcen_graso, self.gasto)
        
    def __str__(self):
        """Método para imprimir los datos de un asesorado."""
        
        somatotipo_str = ""
        if self.somatotipo == "E":
            somatotipo_str = "Ectomorfo"
        elif self.somatotipo == "M":
            somatotipo_str = "Mesomorfo"
        else:
            somatotipo_str = "Endomorfo"
        
        return f"""
    Nombre: {self.nombre.title()}
    Fecha de nacimiento: {self.fecha_nacido}
    Sexo: {self.sexo}
    Altura: {self.altura} cm
    Peso: {self.peso} kg
    Somatotipo: {somatotipo_str}
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
