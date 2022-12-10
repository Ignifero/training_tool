#!user/bin/env python
"""Archivo principal de la aplicación. Contiene el menú principal y el bucle principal de la aplicación."""

# Importación de módulos

import os
from models import usuario
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
            username = input("Nombre de usuario: ")
            contrasena = input("Contraseña: ")
            user = usuario.Usuario(username, contrasena)
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
    while True:
        os.system("cls")
        banner()
        print(f"""   Bienvenido, {usuario_activo}
            
            1. Gasto Energético
            2. Macronutrientes
            3. Progreso de {usuario_activo}
            4. Comida
            5. Salir
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
            input("Pulse ENTER para continuar...")
        elif opcion == "4":
            print("\nComida")
            input("Pulse ENTER para continuar...")
        elif opcion == "5":
            exit()
        else:
            print("Opción incorrecta. Use los números del 1 al 5.")
            input("Pulse ENTER para continuar...")
        



if __name__ == "__main__":
    main()
