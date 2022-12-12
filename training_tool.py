#!user/bin/env python
"""Archivo principal de la aplicación. Contiene el menú principal y el bucle principal de la aplicación."""

# Importación de módulos

import os
import cv2
import datetime
from models import usuario
from models import asesorado
from controllers import db_manager

# Funciones

def banner():
    print("""
  _____ ____      _    ___ _   _ ___ _   _  ____    
 |_   _|  _ \    / \  |_ _| \ | |_ _| \ | |/ ___|   
   | | | |_) |  / _ \  | ||  \| || ||  \| | |  _    
   | | |  _ <  / ___ \ | || |\  || || |\  | |_| |   
   |_| |_| \_\/_/ __\_\___|_|_\_|___|_| \_|\____|_  
           |_   _/ _ \ / _ \| |    
             | || | | | | | | |    
             | || |_| | |_| | |___ 
             |_| \___/ \___/|_____|  
               
        TRAINING TOOL, COPYRIGHT 2022, JUAN PEÑA GIFFONI
                                            
          """)
    
def menu():
    print("""
    1. Iniciar sesión
    2. Registrarse
    3. Sobre el programa
    4. Salir
    """)
    
def main():
    if not db_manager.validar_bd():
        db_manager.crear_bd()
    while True:
        os.system("cls")
        banner()
        menu()
        opcion = input("Elija una opción: ")
        if opcion == "1":
            try:
                while True:
                    username = input("\nNombre de usuario: ")
                    contrasena = input("Contraseña: ")
                    if len(username) > 2 and len(contrasena) > 5:
                        if username.isspace() or contrasena.isspace():
                            print("El nombre de usuario y la contraseña no pueden estar en blanco.")
                            input("Pulse ENTER para continuar...")
                        else:
                            break
                    else:
                        print("El nombre de usuario debe tener al menos 3 caracteres y la contraseña al menos 6.")
                        input("Pulse ENTER para continuar...")
                user = usuario.Usuario(username, contrasena)
            except:
                print("Inicio de sesión incorrecto. Usuario o contraseña incorrectos.")
                input("Pulse ENTER para continuar...")
                main()
            if user.login():
                global usuario_activo
                usuario_activo = username
                print("Inicio de sesión correcto.")
                input("Pulse ENTER para continuar...")
                menu_principal()
            else:
                print("Inicio de sesión incorrecto. Usuario o contraseña incorrectos.")
                input("Pulse ENTER para continuar...")
        elif opcion == "2":
            try:
                username = input("\nNombre de usuario: ")
                contrasena = input("Contraseña: ")
                user = usuario.Usuario(username, contrasena)
                user.registro()
                print("\nRegistro correcto.")
                input("Pulse ENTER para continuar...")
            except:
                print("\nRegistro incorrecto. El nombre de usuario ya existe.")
                input("Pulse ENTER para continuar...")
                main()
        elif opcion == "3":
            os.system('start chrome.exe "https://github.com/Ignifero/training_tool"')
        elif opcion == "4":
            exit()
        else:
            print("Opción incorrecta. Use los números del 1 al 4.")
            input("Pulse ENTER para continuar...")
            

def menu_principal():
    consulta = db_manager.obtenerAsesorado(str(usuario_activo))
    if consulta == None:
        print("\nNo hay asesorados registrados.")
        input("Pulse ENTER para continuar...")
        os.system("cls")
        print("REGISTRO DE ASESORADO\n")
        while True:
            nombre = input("\nIngrese nombre completo: ")
            if len(nombre) >= 15:
                if not nombre.isspace():
                    if "0" or "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" not in nombre:
                        if nombre.count(" ") < 5:
                            break
            else:
                print("El nombre debe tener al menos 15 caracteres, no puede estar en blanco y no puede contener números.")
        while True:
            fecha = str(input("Ingrese fecha de nacimiento (dd/mm/aaaa). Ej: (30/07/2001): "))
            if len(fecha) == 10:
                if fecha[2] == "/" and fecha[5] == "/":
                    try:
                        _fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y")
                        break
                    except:
                        print("Fecha incorrecta. Use el formato dd/mm/aaaa.")
                else:
                    print("Fecha incorrecta. Use el formato dd/mm/aaaa.")
        while True:
            try:
                altura = int(input("Ingrese altura (cm): "))
                if altura >= 100 and altura < 300:
                    break
                else:
                    print("Altura incorrecta. Use un número entre 100 y 300.")
            except:
                print("Altura incorrecta. Use un número entre 100 y 300.")
        while True:
            try:
                peso = float(input("Ingrese peso (kg): "))
                if peso >= 20 and peso < 200:
                    break
                else:
                    print("Peso incorrecto. Use un número entre 20 y 200.")
            except:
                print("Peso incorrecto. Use un número entre 20 y 200.")
        while True:
            sexo = input("Ingrese sexo (H para hombre o M para mujer): ")
            if sexo.upper() == "H" or sexo.upper() == "M":
                break
            else:
                print("Opción incorrecta. Use H o M.")
                input("Pulse ENTER para continuar...")
        while True:
            somatotipo = input("Ingrese somatotipo (E para Ectomorfo, M para Mesomorfo o H para Endomorfo): ")
            if somatotipo.upper() == "E" or somatotipo.upper() == "M" or somatotipo.upper() == "H":
                break
            else:
                print("Opción incorrecta. Use E, M o H.")
                input("Pulse ENTER para continuar...")
        while True:
            foto = input("\nSabe su porcentaje de grasa corporal? (Si/No): ")
            if foto.upper() == "SI" or foto.upper() == "S" or foto.upper() == "SÍ":
                break
            elif foto.upper() == "N" or foto.upper() == "NO":
                print("""
Se le va a mostrar una tabla comparativa de porcentajes de grasa corporal 
para que pueda estimar su porcentaje de grasa corporal. Vea la imagen y con honestidad compárese con ella.
Escoja el porcentaje de grasa corporal que más se asemeje a usted.
""")
                input("Pulse ENTER para continuar...")
                imagen = cv2.imread(os.path.join(os.path.dirname(__file__), "assets", "estimado_graso.png"))
                cv2.imshow("Tabla Comparativa de Porcentaje Graso", imagen)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
            else:
                print("Opción incorrecta. Use S o N.")
                input("Pulse ENTER para continuar...")
        while True:
            p_graso = input("Ingrese porcentaje de grasa corporal, sin el % (decimales con ','): ")
            if p_graso.isnumeric():
                break
            else:
                print("Opción incorrecta. Use números.")
                input("Pulse ENTER para continuar...")
        print("\nProcesando...")
        try:
            global asesorado_activo
            asesorado_activo = asesorado.Asesorado(nombre, fecha, altura, peso, sexo, somatotipo,
                                                p_graso, usuario_activo)
            asesorado_activo.registrar()
            print("\nRegistro de asesorado correcto.")
            input("Pulse ENTER para continuar...")
            menu_principal()
        except:
            print("\nError al crear asesorado.")
            input("Pulse ENTER para continuar...")
            menu_principal()
    else:
        asesorado_activo = asesorado.Asesorado(consulta[0], consulta[1], consulta[2], consulta[3], consulta[4],
                                            consulta[5], consulta[6], consulta[7])
    while True:
        os.system("cls")
        banner()
        print(f"""   Bienvenido, {usuario_activo.capitalize()}
            
            1. Gasto Energético
            2. Macronutrientes
            3. Progreso de {usuario_activo.capitalize()}
            4. Comida
            5. Cerrar sesión
            """)
        opcion = input("Elija una opción: ")
        if opcion == "1":
            print("\nGasto energético")
            input("Pulse ENTER para continuar...")
        elif opcion == "2":
            print("\nMacronutrientes")
            input("Pulse ENTER para continuar...")
        elif opcion == "3":
            print("\nProgreso de", usuario_activo)
            print("\n", asesorado_activo)
            input("Pulse ENTER para continuar...")
        elif opcion == "4":
            print("\nComida")
            input("Pulse ENTER para continuar...")
        elif opcion == "5":
            print("\nCerrando sesión...")
            input("Pulse ENTER para continuar...")
            del asesorado_activo
            main()
        else:
            print("Opción incorrecta. Use los números del 1 al 5.")
            input("Pulse ENTER para continuar...")
        



if __name__ == "__main__":
    main()
