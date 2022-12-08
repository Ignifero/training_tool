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
             |_| \___/ \___/|_____|  BY JUAN PEÑA G.
               
        TRAINING TOOL, COPYRIGHT 2022, JUAN PEÑA GIFFONI

            Para más información, escoja la opción correspondiente a "Sobre el programa"                                            
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
                print("Inicio de sesión correcto.")
                input("Pulse ENTER para continuar...")
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
                input("Pulse ENTER para continuar...")
                main()
        elif opcion == "3":
            os.system('start chrome.exe "https://github.com/Ignifero/training_tool"')
        elif opcion == "4":
            exit()
        



if __name__ == "__main__":
    main()
