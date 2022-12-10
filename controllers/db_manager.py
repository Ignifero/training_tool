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
    print("Creando base de datos...")
    
    # Creación de la tabla USUARIO
    try:
        conexion.execute("""create table USUARIO(
                username text primary key,
                contrasena text not null
            );""")
        print("Tabla USUARIO creada correctamente.")
        input("Pulse ENTER para continuar...")
    except sqlite3.OperationalError:
        print("La tabla USUARIO ya existe.")
        input("Pulse ENTER para continuar...")
    
    # Creación de la tabla ASESORADO
    try:
        conexion.execute("""create table ASESORADO(
                nombre_completo text primary key,
                fecha_nacimiento text not null,
                altura integer not null,
                peso real not null,
                sexo text not null,
                somatotipo text not null,
                porcen_graso real not null,
                gasto_energetico real not null,
                username text references USUARIO(username)
            );""")
        print("Tabla ASESORADO creada correctamente.")
        input("Pulse ENTER para continuar...")
    except sqlite3.OperationalError:
        print("La tabla ASESORADO ya existe.")
        input("Pulse ENTER para continuar...")
        
    # Creación de la tabla ALIMENTO
    try:
        conexion.execute("""create table ALIMENTO(
                id_alimento integer primary key,
                nombre_alimento text not null,
                calorias float not null,
                proteinas float not null,
                grasas float not null,
                carbohidratos float not null,
                cantidad_gr float not null
            );""")
        print("Tabla ALIMENTO creada correctamente.")
        input("Pulse ENTER para continuar...")
    except sqlite3.OperationalError:
        print("La tabla ALIMENTO ya existe.")
        input("Pulse ENTER para continuar...")
    
    # Creación índice unico para la tabla ALIMENTO
    try:
        conexion.execute("""create unique index idx_alimento on ALIMENTO(nombre_alimento);""")
        print("Índice único creado correctamente.")
        input("Pulse ENTER para continuar...")
    except sqlite3.OperationalError:
        print("El índice único ya existe.")
        input("Pulse ENTER para continuar...")
        
    # Creación de la tabla FASE_ENTRENAMIENTO
    try:
        conexion.execute("""create table FASE_ENTRENAMIENTO(
                id_fase integer primary key autoincrement,
                tipo_fase text not null,
                inicio_fase text not null,
                fin_fase text,
                nombre_asesorado text references ASESORADO(nombre_completo)
            );""")
        print("Tabla FASE_ENTRENAMIENTO creada correctamente.")
        input("Pulse ENTER para continuar...")
    except sqlite3.OperationalError:
        print("La tabla FASE_ENTRENAMIENTO ya existe.")
        input("Pulse ENTER para continuar...")
        
    # Creación de la tabla MENU
    try:
        conexion.execute("""create table MENU(
                id_menu integer primary key autoincrement,
                fecha_creacion text not null,
                racion_alimento real not null,
                nombre_asesorado text references ASESORADO(nombre_completo),
                id_alimento integer references ALIMENTO(id_alimento)
            );""")
        print("Tabla MENU creada correctamente.")
        print("\nBase de datos creada.")
        input("Pulse ENTER para continuar...")
    except sqlite3.OperationalError:
        print("La tabla MENU ya existe.")
        print("\nBase de datos creada.")
        input("Pulse ENTER para continuar...")
    
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
