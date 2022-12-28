
"""Módulo principal de la aplicación en versión gráfica."""

# Importación de módulos

import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import font
from controllers import db_manager as db
from models import usuario
from models import fase_entrenamiento
from models import asesorado


# Clases y funciones

class VentanaBase:
    """Clase que representa la ventana base de la aplicación."""
    def __init__(self):
        # Creación de la ventana
        self.root = tk.Tk()
        self.root.title("Training Tool")
        self.root.geometry("400x500+500+200")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "menus.png"))
        
        # Widgets
        self.logo = tk.Label(self.root, image=logo, anchor='center')
        self.label_copy = tk.Label(self.root, text="© 2022, Training Tool, Juan Peña Giffoni", anchor='center')
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.boton_login = ttk.Button(self.root, text="Iniciar Sesión", command=self.login)
        self.boton_regsitro = ttk.Button(self.root, text="Registrarse", command=self.registrar)
        self.boton_about = ttk.Button(self.root, text="Acerca de Training Tool", command=self.sobreLaApp)
        self.boton_salir = ttk.Button(self.root, text="Salir", command=self.root.destroy)
        
        # Configuración de widgets
        self.logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.label_copy.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
        self.label_copy.config(font=("Arial", 8))
        self.separador.pack(side=tk.TOP, fill=tk.X, padx=20, expand=True)
        self.boton_login.pack(side=tk.TOP, pady=5)
        self.boton_login.config(width=30)
        self.boton_regsitro.pack(side=tk.TOP, pady=5)
        self.boton_regsitro.config(width=30)
        self.boton_about.pack(side=tk.TOP, pady=5)
        self.boton_about.config(width=30)
        self.boton_salir.pack(side=tk.BOTTOM, pady=5)
        self.boton_salir.config(width=30)
        
        # Configuración de la ventana
        self.root.mainloop()
        
    # Funciones
    def login(self):
        login = VentanaLogin(self.root)
        
    def registrar(self):
        registro = VentanaRegistroUsuario(self.root)
        
    def sobreLaApp(self):
        mensaje = msg.askyesno("Acerca de Training Tool",
                               "¿Desea saber más sobre la aplicación? Será redirigido a la página web del proyecto." + 
                            "\n\n¿Desea continuar al navegador?")
        if mensaje:
            os.system('start chrome.exe "https://github.com/Ignifero/training_tool"')
 # --- Fin de la clase VentanaBase --- #


class VentanaLogin:
    """Clase que representa la ventana de login de la aplicación."""
    def __init__(self, ventana_base):
        # Creación de la ventana
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Iniciar Sesión")
        self.root.geometry("300x400+550+250")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        self.usuario = tk.StringVar()
        self.contrasena = tk.StringVar()
        
        # Widgets
        self.logo = tk.Label(self.root, image=logo, anchor='center')
        self.titulo_logo = tk.Label(self.root, text="Inicio de Sesión")
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.lframe_registro = ttk.Labelframe(self.root, text="Ingrese sus datos")
        self.label_usuario = tk.Label(self.lframe_registro, text="Nombre de Usuario:")
        self.entry_usuario = ttk.Entry(self.lframe_registro, textvariable=self.usuario)
        self.label_contrasena = tk.Label(self.lframe_registro, text="Contraseña:")
        self.entry_contrasena = ttk.Entry(self.lframe_registro, textvariable=self.contrasena, show="*")
        self.boton_ingresar = ttk.Button(self.root, text="Ingresar", command=self.ingresar)
        self.boton_cancelar = ttk.Button(self.root, text="Cancelar", command=self.root.destroy)
        
        # Configuración de widgets
        self.logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.titulo_logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.titulo_logo.config(font=("Arial", 24))
        self.separador.pack(side=tk.TOP, fill=tk.X, padx=20, expand=True)
        self.lframe_registro.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.label_usuario.grid(row=0, column=0, padx=5, pady=5)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)
        self.label_contrasena.grid(row=1, column=0, padx=5, pady=5)
        self.entry_contrasena.grid(row=1, column=1, padx=5, pady=5)
        self.boton_ingresar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.boton_cancelar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configuración de la ventana
        self.root.transient(master=ventana_base)
        self.root.grab_set()
        self.entry_usuario.focus_set()
        self.ventana_base = ventana_base
        self.ventana_base.wait_window(self.root)
        
    def ingresar(self):
        if self.usuario.get() == "" or self.contrasena.get() == "":
            msg.showerror("Error", "Debe ingresar un nombre de usuario y una contraseña.")
        else:
            try:
                user = usuario.Usuario(self.usuario.get(), self.contrasena.get())
                if user.login():
                    msg.showinfo("Login", "Inicio de sesión exitoso.")
                    global usuario_activo
                    usuario_activo = user.username
                    self.ventana_base.withdraw()
                    menu_principal = VentanaMenuPrincipal(self.root)
                    self.ventana_base.deiconify()
                    self.root.destroy()
                else:
                    msg.showerror("Error", "Usuario o contraseña incorrectos.")
            except Exception as e:
                msg.showerror("Error", "Ha ocurrido un error inesperado. Por favor, inténtelo de nuevo.")
                print(e)
# --- Fin de la clase VentanaLogin --- #

    
class VentanaRegistroUsuario:
    """Clase que representa la ventana de registro de la aplicación."""
    def __init__(self, ventana_base):
        # Creación de la ventana
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Nuevo Usuario")
        self.root.geometry("400x500+550+250")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        self.usuario = tk.StringVar()
        self.contrasena = tk.StringVar()
        self.contrasena.trace("w", self.confirmarContrasena)
        self.pswd_confirmado = tk.StringVar()
        self.pswd_confirmado.trace("w", self.confirmarContrasena)
        self.confirmado = tk.StringVar()
        
        # Widgets
        self.logo = tk.Label(self.root, image=logo, anchor='center')
        self.titulo_logo = tk.Label(self.root, text="Registro de Nuevo Usuario")
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.lframe_registro = ttk.Labelframe(self.root, text="Datos de Registro")
        self.label_usuario = tk.Label(self.lframe_registro, text="Nombre de Usuario:")
        self.entry_usuario = ttk.Entry(self.lframe_registro, textvariable=self.usuario)
        self.label_contrasena = tk.Label(self.lframe_registro, text="Contraseña:")
        self.entry_contrasena = ttk.Entry(self.lframe_registro, textvariable=self.contrasena, show="*")
        self.label_pswd_confirmado = tk.Label(self.lframe_registro, text="Confirmar Contraseña:")
        self.entry_pswd_confirmado = ttk.Entry(self.lframe_registro, textvariable=self.pswd_confirmado, show="*")
        self.label_pswd_correcto = tk.Label(self.lframe_registro, textvariable=self.confirmado) 
        self.boton_registrar = ttk.Button(self.root, text="Registrar", command=self.registrar)
        self.boton_cancelar = ttk.Button(self.root, text="Cancelar", command=self.root.destroy)
        
        # Configuración de widgets
        self.logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.titulo_logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.titulo_logo.config(font=("Arial", 24))
        self.separador.pack(side=tk.TOP, fill=tk.X, padx=20, expand=True)
        self.lframe_registro.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.label_usuario.grid(row=0, column=0, padx=5, pady=5)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)
        self.label_contrasena.grid(row=1, column=0, padx=5, pady=5)
        self.entry_contrasena.grid(row=1, column=1, padx=5, pady=5)
        self.label_pswd_confirmado.grid(row=2, column=0, padx=5, pady=5)
        self.entry_pswd_confirmado.grid(row=2, column=1, padx=5, pady=5)
        self.label_pswd_correcto.grid(row=3, column=1, padx=5, pady=5)
        self.boton_registrar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.boton_cancelar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configuración de la ventana
        self.root.transient(master=ventana_base)
        self.root.grab_set()
        ventana_base.wait_window(self.root)
         
    # Funciones
    def confirmarContrasena(self, *args):
        if self.contrasena.get() == self.pswd_confirmado.get():
            self.confirmado.set("Las contraseñas coinciden")
        else:
            self.confirmado.set("Las contraseñas no coinciden")
    
    def registrar(self):
        if self.usuario.get() == "" or self.contrasena.get() == "" or self.pswd_confirmado.get() == "":
            msg.showerror(title="Error", message="Debe completar todos los campos")
        elif self.contrasena.get() != self.pswd_confirmado.get():
            msg.showerror(title="Error", message="Las contraseñas no coinciden")
        elif len(self.contrasena.get()) < 6 or len(self.usuario.get()) < 3:
            msg.showerror(title="Error", message="El nombre de usuario debe tener al menos 3 caracteres y la contraseña al menos 6")
        else:
            try:
                user = usuario.Usuario(self.usuario.get(), self.contrasena.get())
                if db.validarUsuario(user.username, user.contrasena):
                    msg.showerror(title="Error", message="El nombre de usuario ya existe")
                else:
                    user.registro()
                    msg.showinfo(title="Éxito", message="El usuario ha sido registrado exitosamente")
                    self.root.destroy()
            except db.sqlite3.IntegrityError:
                msg.showerror(title="Error", message="El nombre de usuario ya existe")
            except Exception as e:
                msg.showerror(title="Error", message="Ha ocurrido un error inesperado: {}".format(e))
# --- Fin de la clase VentanaRegistroUsuario --- #


class VentanaMenuPrincipal:
    """Clase que representa la ventana del menú principal del programa."""
    def __init__(self, ventana_base):
        # Creación de la ventana
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Menú Principal")
        self.root.geometry("400x500+500+200")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "menus.png"))
        
        # Widgets
        self.logo = tk.Label(self.root, image=logo, anchor='center')
        self.label_bienvenida = tk.Label(self.root, text=f"Bienvenido, {usuario_activo.title()}", anchor='w')
        self.label_copy = tk.Label(self.root, text="© 2022, Training Tool, Juan Peña Giffoni", anchor='center')
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.boton_objetivos = ttk.Button(self.root, text="Gasto Energéticos y Objetivos")
        self.boton_progreso = ttk.Button(self.root, text=f"Progreso de {usuario_activo.title()}")
        self.boton_dieta = ttk.Button(self.root, text="Alimentación y Dieta")
        self.boton_ejercicios = ttk.Button(self.root, text="Rutinas de Ejercicios")
        self.boton_logout = ttk.Button(self.root, text="Cerrar Sesión", command=self.logout)
        
        # Configuración de los widgets
        self.logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.separador.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=10)
        self.label_bienvenida.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.label_bienvenida.configure(font=("Arial", 16))
        self.boton_objetivos.pack(side=tk.TOP, padx=5, pady=5)
        self.boton_objetivos.configure(width=30)
        self.boton_progreso.pack(side=tk.TOP, padx=5, pady=5)
        self.boton_progreso.configure(width=30)
        self.boton_dieta.pack(side=tk.TOP, padx=5, pady=5)
        self.boton_dieta.configure(width=30)
        self.boton_ejercicios.pack(side=tk.TOP, padx=5, pady=5)
        self.boton_ejercicios.configure(width=30)
        self.boton_logout.pack(side=tk.TOP, padx=5, pady=5)
        self.boton_logout.configure(width=30)
        self.label_copy.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.label_copy.configure(font=("Arial", 8))
        
        # Configuración de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.logout)
        self.root.grab_set()
        ventana_base.withdraw()
        ventana_base.wait_window(self.root)
        
    def logout(self):
        """Función que cierra la sesión del usuario."""
        usuario_activo = None
        self.root.destroy()
# --- Fin de la clase VentanaMenuPrincipal --- #


def main():
    """Función principal del módulo."""
    app = VentanaBase()
    return 0

if __name__ == "__main__":
    if db.validar_bd():
        sys.exit(main())
    else:
        db.crear_bd()
        main()
