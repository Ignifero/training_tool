#!user/bin/env python
"""Módulo para la gestión de la base de datos.
La aplicación utiliza SQLite3 para almacenar los datos de los usuarios y los datos de los ejercicios.
Este módulo contiene las funciones necesarias para la gestión de la base de datos,
como la creación de la base de datos, la creación de tablas, la inserción de datos,
la consulta de datos, etc."""

# Importación de módulos

import sqlite3
import os


# Funciones

def crear_bd():
    conexion = sqlite3.connect("training_tool.db")
    
    try:
        conexion.execute("""create table USUARIO (
                username text primary key,
                contrasena text not null
            )""")
        print("Tabla USUARIO creada correctamente.")
    except sqlite3.OperationalError:
        print("La tabla USUARIO ya existe.")
    
    conexion.close()
    

def validar_bd():
    if os.path.isfile("training_tool.db"):
        return True
    else:
        return False
    
    
def nuevoUsuario(username, contrasena):
    if validar_bd():       
        conexion = sqlite3.connect("training_tool.db")
        
        try:
            conexion.execute("insert into USUARIO values (?, ?)", (username, contrasena))
            print("Usuario creado correctamente.")
        except sqlite3.IntegrityError:
            print("El usuario ya existe.")
        
        conexion.commit()
        conexion.close()
    else:
        print("No se ha encontrado la base de datos.")


def validarUsuario(username, contrasena):
    if validar_bd():
        conexion = sqlite3.connect("training_tool.db")
        
        cursor = conexion.execute("select * from USUARIO where username = ? and contrasena = ?", (username, contrasena))
        resultado = cursor.fetchone()
        
        if resultado is None:
            print("\nUsuario no encontrado.")
            conexion.close()
            return False
        else:
            print("\nUsuario encontrado.")
            conexion.close()
            return True
    else:
        print("No se ha encontrado la base de datos.")
        return False
