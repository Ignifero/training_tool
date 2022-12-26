#!user/bin/env python
"""Módulo para la gestión de la base de datos.
La aplicación utiliza SQLite3 para almacenar los datos de los usuarios y los datos de los ejercicios.
Este módulo contiene las funciones necesarias para la gestión de la base de datos,
como la creación de la base de datos, la creación de tablas, la inserción de datos,
la consulta de datos, etc."""

# Importación de módulos

import sqlite3
import os
import time
from controllers import cls


# Funciones
APPDATA = os.environ["APPDATA"]
if not os.path.exists(os.path.join(APPDATA, "training_tool")):
    os.mkdir(os.path.join(APPDATA, "training_tool"))
    

def crear_bd():
    CONEXION = sqlite3.connect(os.path.join(APPDATA, "training_tool", "training_tool.db"))
    cls()
    print("Creando base de datos...")
    
    # Creación de la tabla USUARIO
    try:
        CONEXION.execute("""create table USUARIO(
                username text primary key,
                contrasena text not null
            );""")
        print("Tabla USUARIO creada correctamente.")
    except sqlite3.OperationalError:
        print("La tabla USUARIO ya existe.")
    
    # Creación de la tabla ASESORADO
    try:
        CONEXION.execute("""create table ASESORADO(
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
    except sqlite3.OperationalError:
        print("La tabla ASESORADO ya existe.")
        
    # Creación de la tabla ALIMENTO
    try:
        CONEXION.execute("""create table ALIMENTO(
                id_alimento integer primary key,
                nombre_alimento text not null,
                calorias float not null,
                proteinas float not null,
                grasas float not null,
                carbohidratos float not null,
                cantidad_gr float not null
            );""")
        print("Tabla ALIMENTO creada correctamente.")
    except sqlite3.OperationalError:
        print("La tabla ALIMENTO ya existe.")
    
    # Creación índice unico para la tabla ALIMENTO
    try:
        CONEXION.execute("""create unique index idx_alimento on ALIMENTO(nombre_alimento);""")
        print("Índice único creado correctamente.")
    except sqlite3.OperationalError:
        print("El índice único ya existe.")
        
    # Creación de la tabla FASE_ENTRENAMIENTO
    try:
        CONEXION.execute("""create table FASE_ENTRENAMIENTO(
                id_fase integer primary key autoincrement,
                tipo_fase text not null,
                inicio_fase text not null,
                fin_fase text,
                gasto_calorico_objetivo real not null,
                proteinas_gr_dia real not null,
                grasas_gr_dia real not null,
                carbohidratos_gr_dia real not null,
                nro_comidas_dia integer not null,
                nombre_asesorado text references ASESORADO(nombre_completo)
            );""")
        print("Tabla FASE_ENTRENAMIENTO creada correctamente.")
    except sqlite3.OperationalError:
        print("La tabla FASE_ENTRENAMIENTO ya existe.")
        
    # Creación de la tabla TIPO_MENU
    try:
        CONEXION.execute("""create table TIPO_MENU(
                    id_tipo integer primary key autoincrement,
                    nombre_tipo text not null
                );""")
        print("Tabla TIPO_MENU creada correctamente.")
    except sqlite3.OperationalError:
        print("La tabla TIPO_MENU ya existe.")
        
    # Creación de la tabla MENU
    try:
        CONEXION.execute("""create table MENU(
                    id_menu integer primary key autoincrement,
                    fecha_creacion text not null,
                    id_tipo integer references TIPO_MENU(id_tipo),
                    nombre_asesorado text references ASESORADO(nombre_completo),
                    id_fase integer references FASE_ENTRENAMIENTO(id_fase)
                );""")
        print("Tabla MENU creada correctamente.")
    except sqlite3.OperationalError:
        print("La tabla MENU ya existe.")
        print("\nBase de datos creada.")
        
    # Creación de la tabla INGREDIENTE
    try:
        CONEXION.execute("""create table INGREDIENTE(
                nro_ingrediente integer primary key autoincrement,
                id_alimento integer references ALIMENTO(id_alimento),
                id_menu integer references MENU(id_menu),
                cantidad_gr float not null
            );""")
        print("Tabla INGREDIENTE creada correctamente.")
    except sqlite3.OperationalError:
        print("La tabla INGREDIENTE ya existe.")
        
    # Insert de datos unicos en tipo_menus
    try:
        CONEXION.execute("""insert into TIPO_MENU(nombre_tipo) values ('Desayuno');""")
        CONEXION.execute("""insert into TIPO_MENU(nombre_tipo) values ('Almuerzo');""")
        CONEXION.execute("""insert into TIPO_MENU(nombre_tipo) values ('Snack');""")
        CONEXION.execute("""insert into TIPO_MENU(nombre_tipo) values ('Merienda');""")
        CONEXION.execute("""insert into TIPO_MENU(nombre_tipo) values ('Cena');""")
        print("Datos insertados en la tabla TIPO_MENU correctamente.")
    except sqlite3.IntegrityError:
        print("Los datos ya existen en la tabla TIPO_MENU.")
        
    
    CONEXION.close()
    

def validar_bd():
    if os.path.isfile(os.path.join(APPDATA, "training_tool", "training_tool.db")):
        return True
    else:
        return False
    
    
def nuevoUsuario(username, contrasena):
    if validar_bd():       
        CONEXION = sqlite3.connect(os.path.join(APPDATA, "training_tool", "training_tool.db"))
        
        try:
            CONEXION.execute("insert into USUARIO values (?, ?)", (username, contrasena))
            print("Usuario creado correctamente.")
        except sqlite3.IntegrityError:
            print("El usuario ya existe.")
        
        CONEXION.commit()
        CONEXION.close()
    else:
        print("No se ha encontrado la base de datos.")


def validarUsuario(username, contrasena):
    if validar_bd():
        CONEXION = sqlite3.connect(os.path.join(APPDATA, "training_tool", "training_tool.db"))
        
        cursor = CONEXION.execute("select * from USUARIO where username = ? and contrasena = ?", (username, contrasena))
        resultado = cursor.fetchone()
        
        if resultado is None:
            print("\nUsuario no encontrado.")
            CONEXION.close()
            return False
        else:
            print("\nUsuario encontrado.")
            CONEXION.close()
            return True
    else:
        print("No se ha encontrado la base de datos.")
        return False
 
    
def nuevoAsesorado(nombre, fecha_n, altura, peso, sexo, somatotipo, p_graso, gasto_e, username):
    if validar_bd():
        CONEXION = sqlite3.connect(os.path.join(APPDATA, "training_tool", "training_tool.db")) 
        
        try:
            CONEXION.execute("insert into ASESORADO values (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                             (nombre, fecha_n, altura, peso, sexo, somatotipo, p_graso, gasto_e, username))
            
            print("Asesorado creado correctamente.")
        except sqlite3.IntegrityError:
            print("El asesorado ya existe.")
            
        CONEXION.commit()
        CONEXION.close()
    else:
        print("No se ha encontrado la base de datos.")
        
        
def obtenerAsesorado(username):
    if validar_bd():
        CONEXION = sqlite3.connect(os.path.join(APPDATA, "training_tool", "training_tool.db")) 
        
        try:
            cursor = CONEXION.execute("select * from ASESORADO where username = ?", (username, ))
            resultado = cursor.fetchone()
            
            if resultado is None:
                print("No se ha encontrado el asesorado.")
                CONEXION.close()
                return None
            else:
                print("Asesorado encontrado.")
                CONEXION.close()
                return resultado
        except sqlite3.OperationalError:
            print("No se ha encontrado el asesorado.")
            CONEXION.close()
            return None
        except sqlite3.IntegrityError:
            print("No se ha encontrado el asesorado.")
            CONEXION.close()
            return None
        except sqlite3.ProgrammingError:
            print("No se ha encontrado el asesorado.")
            CONEXION.close()
            return None
        

def actualizarAsesorado(nombre, altura, peso, p_graso, gasto_e):
    if validar_bd():
        CONEXION = sqlite3.connect(os.path.join(APPDATA, "training_tool", "training_tool.db"))
        
        try:
            CONEXION.execute("update ASESORADO set altura = ?, peso = ?, p_graso = ?, gasto_e = ? where nombre_completo = ?", 
                             (altura, peso, p_graso, gasto_e, nombre))
            print("Asesorado actualizado correctamente.")
            CONEXION.commit()
            CONEXION.close()
        except sqlite3.OperationalError:
            print("No se ha encontrado el asesorado.")
            CONEXION.close()
            

def nuevaFase(tipo, fecha_inicio, gasto_total, protes, grasas, carbos, comidas, asesorado):
    if validar_bd():
        CONEXION = sqlite3.connect(os.path.join(APPDATA, "training_tool", "training_tool.db"))
        
        try:
            CONEXION.execute("""insert into FASE_ENTRENAMIENTO(tipo_fase,
                             inicio_fase, gasto_calorico_objetivo, proteinas_gr_dia, grasas_gr_dia,
                             carbohidratos_gr_dia, nro_comidas_dia, nombre_asesorado) values (?, ?, ?, ?, ?, ?, ?, ?);""",
                             (tipo, fecha_inicio, gasto_total, protes, grasas, carbos, comidas, asesorado))
            print("Fase creada correctamente.")
            CONEXION.commit()
            CONEXION.close()
        except sqlite3.IntegrityError:
            print("El asesorado ya existe.")
            CONEXION.close()
        
            
def obtenerFase(asesorado):
    if validar_bd():
        CONEXION = sqlite3.connect(os.path.join(APPDATA, "training_tool", "training_tool.db"))
        
        try:
            cursor = CONEXION.execute("""select tipo_fase, inicio_fase, gasto_calorico_objetivo, fin_fase, 
                                        proteinas_gr_dia, grasas_gr_dia, carbohidratos_gr_dia, nro_comidas_dia
                                        from FASE_ENTRENAMIENTO
                                        where nombre_asesorado = ?;""",
                                        (asesorado, ))
            buscar = cursor.fetchall()
            resultado = buscar[len(buscar) - 1]
            
            if resultado is None:
                print("No se ha encontrado la fase.")
                CONEXION.close()
                return None
            else:
                print("Fase encontrada.")
                CONEXION.close()
                return resultado
        except sqlite3.OperationalError:
            print("No se ha encontrado la fase.")
            CONEXION.close()
            return None
        except sqlite3.IntegrityError:
            print("No se ha encontrado la fase.")
            CONEXION.close()
            return None
        except sqlite3.ProgrammingError:
            print("No se ha encontrado la fase.")
            CONEXION.close()
            return None
    

def actualizarFase(fecha_fin, asesorado):
    CONEXION = sqlite3.connect(os.path.join(APPDATA, "training_tool", "training_tool.db"))
    
    try:
        CONEXION.execute("""update FASE_ENTRENAMIENTO set fin_fase = ? where nombre_asesorado = ? and fin_fase is null""",
                         (fecha_fin, asesorado))
        print("Fase actualizada correctamente.")
        CONEXION.commit()
        CONEXION.close()
    except sqlite3.OperationalError:
        print("No se ha encontrado la fase.")
        CONEXION.close()
