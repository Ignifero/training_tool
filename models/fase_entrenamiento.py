#!user/bin/env python
"""Módulo para clase FaseEntrenamiento. Contiene la clase FaseEntrenamiento, sus atributos y sus métodos."""

# Importación de módulos

from datetime import date
from datetime import datetime
from controllers import db_manager

# Clase

class FaseEntrenamiento:
    """Clase para las fases de entrenamiento de los asesorados. Este objeto se crea al fijar un objetivo de entrenamiento."""
    
    # Atributos
    def __init__(self, tipo, fecha_i, gasto_t, asesorado, proteinas, grasas, carbohidratos, comidas, fecha_fin = ""):
        
        # Tipo
        try:
            tipo = str(tipo)
            if tipo.lower() == "mantenimiento" or tipo.lower() == "definicion" or tipo.lower() == "volumen":
                self.tipo = tipo.lower()
            else:
                raise ValueError
        except ValueError:
            print("El tipo de fase de entrenamiento no es válido.")
        
        # Fecha de inicio
        try:
            if fecha_i == "":
                self.fecha_inicio = date.today().strftime("%d/%m/%Y")
            else:
                _fecha = datetime.strptime(fecha_i, "%d/%m/%Y")
                self.fecha_inicio = fecha_i
        except ValueError:
            print("La fecha de inicio no es válida.")
        
        # Fecha de finalización
        self.fecha_fin = fecha_fin
        
        # Gasto total
        try:
            self.gasto_t = float(gasto_t)
        except ValueError:
            print("El gasto total debe ser un número.")
            
        # Proteínas
        try:
            self.proteinas = float(proteinas)
        except ValueError:
            print("Las proteínas deben ser un número.")
            
        # Grasas
        try:
            self.grasas = float(grasas)
        except ValueError:
            print("Las grasas deben ser un número.")
            
        # Carbohidratos
        try:
            self.carbohidratos = float(carbohidratos)
        except ValueError:
            print("Los carbohidratos deben ser un número.")
            
        # Comidas
        if type(comidas) is int:
            if comidas > 1 and comidas < 6:
                self.comidas = comidas
            else:
                print("El número de comidas debe estar entre 2 y 5.")
        else:
            print("El número de comidas debe ser un número entero entre 2 y 5.")
            
        # Asesorado
        try:
            if len(asesorado) > 11:
                if type(asesorado) is str:
                    if not asesorado.isspace():
                        if "0" or "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" not in asesorado:
                            self.asesorado = asesorado
            else:
                raise ValueError
        except ValueError:
            print("El nombre debe tener al menos 12 caracteres. Escriba su nombre completo.")
            
    
    # Métodos
    def iniciarFase(self):
        """Método para iniciar una fase de entrenamiento. Guarda la fecha de inicio de la fase en la base de datos."""
        
        # Guardar fecha de inicio en la base de datos
        try:
            db_manager.nuevaFase(self.tipo, self.fecha_inicio, self.gasto_t, self.proteinas, self.grasas, self.carbohidratos, self.comidas, self.asesorado)
        except:
            print("No se ha podido guardar la fecha de inicio en la base de datos.")
            
    def finalizarFase(self):
        """Método para finalizar una fase de entrenamiento. Guarda la fecha de finalización de la fase en la base de datos."""
        
        self.fecha_fin = date.today().strftime("%d/%m/%Y")
        
        # Guardar fecha de finalización en la base de datos
        try:
            db_manager.actualizarFase(self.fecha_fin, self.asesorado)
        except:
            print("No se ha podido guardar la fecha de finalización en la base de datos.")
            
    def __str__(self):
        """Método para imprimir el objeto."""
        
        return f"""OBJETIVO ACTUAL:
    
    Nombre: {self.asesorado.title()}
    Tipo: {self.tipo}
    Inicio: {self.fecha_inicio}
    Gasto Objetivo: {round(self.gasto_t, 2)} kcal
    Comidas por día: {self.comidas}
    Proteínas por día: {round(self.proteinas, 2)} gr ({round(self.proteinas / self.comidas, 2)} gr por comida)
    Grasas por día: {round(self.grasas, 2)} gr ({round(self.grasas / self.comidas, 2)} gr por comida)
    Carbohidratos por día: {round(self.carbohidratos, 2)} gr ({round(self.carbohidratos / self.comidas, 2)} gr por comida)
    Finalización: {'No finalizada' if self.fecha_fin == None else self.fecha_fin}"""
    