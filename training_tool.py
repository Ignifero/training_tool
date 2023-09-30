
"""Módulo principal de la aplicación en versión gráfica."""

# Importación de módulos

import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from datetime import date
from datetime import datetime
from controllers import db_manager as db
from controllers import barcode_scaner as scan
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
                if not " " in self.usuario.get():
                    user = usuario.Usuario(self.usuario.get(), self.contrasena.get())
                    if db.validarUsuario(user.username, user.contrasena):
                        msg.showerror(title="Error", message="El nombre de usuario ya existe")
                    else:
                        user.registro()
                        msg.showinfo(title="Éxito", message="El usuario ha sido registrado exitosamente")
                        self.root.destroy()
                else:
                    msg.showerror(title="Error", message="El nombre de usuario no puede contener espacios")
            except db.sqlite3.IntegrityError:
                msg.showerror(title="Error", message="El nombre de usuario ya existe")
            except Exception as e:
                msg.showerror(title="Error", message="Ha ocurrido un error inesperado: {}".format(e))
# --- Fin de la clase VentanaRegistroUsuario --- #


class VentanaMenuPrincipal:
    """Clase que representa la ventana del menú principal del programa."""
    def __init__(self, ventana_base):
        global asesorado_activo
        global objetivo
        if db.validarAsesorado(usuario_activo):
            consulta = db.obtenerAsesorado(usuario_activo)
            asesorado_activo = asesorado.Asesorado(consulta[0], consulta[1], consulta[2], consulta[3], consulta[4],
                                            consulta[5], consulta[6], consulta[7])
            f_objetivo = db.obtenerFase(asesorado_activo.nombre)
            objetivo = fase_entrenamiento.FaseEntrenamiento(f_objetivo[0], f_objetivo[1], f_objetivo[2],
                                                                 asesorado_activo.nombre, f_objetivo[4],
                                                                 f_objetivo[5], f_objetivo[6], f_objetivo[7], f_objetivo[3])
            hoy = date.today()
            fecha_objetivo = datetime.strptime(objetivo.fecha_inicio, "%d/%m/%Y")
            fecha_objetivo = fecha_objetivo.date()
            dias = hoy - fecha_objetivo
            if dias.days > 6:
                msg.showwarning(title="Advertencia", message="Hace más de una semana que no actualizas tus datos.")
                actualizacion = VentanaActualizarDatos(ventana_base)

        # Creación de la ventana
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Menú Principal")
        self.root.geometry("500x600+500+200")
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
        self.boton_objetivos = ttk.Button(self.root, text="Gasto Energéticos y Objetivos", command=self.objetivos)
        self.boton_progreso = ttk.Button(self.root, text=f"Progreso de {usuario_activo.title()}", command=self.progreso)
        self.boton_dieta = ttk.Button(self.root, text="Alimentación y Dieta", command=self.alimentacion)
        self.boton_ejercicios = ttk.Button(self.root, text="Rutinas de Ejercicios", command=self.rutinas)
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
        
    def objetivos(self):
        """Función que abre la ventana de registro de objetivos."""
        if not db.validarAsesorado(usuario_activo):
            msg.showwarning(title="Advertencia - Asesorado no encontrado", message="Para acceder a esta sección debe registrar sus datos.")
            registoAsesorado = VentanaRegistroAsesorado(self.root, True)
        else:
            objetivo = MenuObjetivos(self.root)

    def progreso(self):
        """Función que abre la ventana de progreso del usuario."""
        if not db.validarAsesorado(usuario_activo):
            msg.showwarning(title="Advertencia - Asesorado no encontrado", message="Para acceder a esta sección debe registrar sus datos.")
            progreso = VentanaRegistroAsesorado(self.root, True)
        else:
            progreso = VentanaProgresoAsesorado(self.root)

    def alimentacion(self):
        """Función que abre la ventana de alimentación."""
        if not db.validarAsesorado(usuario_activo):
            msg.showwarning(title="Advertencia - Asesorado no encontrado", message="Para acceder a esta sección debe registrar sus datos.")
            alimentacion = VentanaRegistroAsesorado(self.root, True)
        else:
            alimentacion = MenuAlimentos(self.root)

    def rutinas(self):
        """Función que abre la ventana de rutinas de ejercicios."""
        if not db.validarAsesorado(usuario_activo):
            msg.showwarning(title="Advertencia - Asesorado no encontrado", message="Para acceder a esta sección debe registrar sus datos.")
            rutinas = VentanaRegistroAsesorado(self.root, True)
        else:
            msg.showinfo(title="Rutinas de Ejercicios", message="En construcción")
        
    def logout(self):
        """Función que cierra la sesión del usuario."""
        usuario_activo = None
        self.root.destroy()
# --- Fin de la clase VentanaMenuPrincipal --- #


class MenuObjetivos:
    """Clase que representa el menú de objetivos del asesorado."""
    def __init__(self, ventana_base):
        # Creación de la ventana
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Objetivos")
        self.root.geometry("400x600+500+200")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        self.ventana_base = ventana_base
        
        # Widgets de la ventana
        self.logo = tk.Label(self.root, image=logo)
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.label_objetivos = tk.Label(self.root, text="Objetivos")
        self.label_objetivos.configure(font=("Arial", 16))
        self.boton_ver_objetivo_actual = ttk.Button(self.root, text="Ver Objetivo Actual", command=self.objetivoActual)
        self.boton_nuevo_objetivo = ttk.Button(self.root, text="Nuevo Objetivo", command=self.nuevObjetivo)
        self.boton_volver = ttk.Button(self.root, text="Volver", command=self.volver)
        self.label_copy = tk.Label(self.root, text="© 2020 Training Tool. Todos los derechos reservados.")

        # Posicionamiento de los widgets
        self.logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.label_objetivos.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.separador.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=10)
        self.boton_ver_objetivo_actual.pack(side=tk.TOP, padx=5, pady=5)
        self.boton_ver_objetivo_actual.configure(width=30)
        self.boton_nuevo_objetivo.pack(side=tk.TOP, padx=5, pady=5)
        self.boton_nuevo_objetivo.configure(width=30)
        self.boton_volver.pack(side=tk.TOP, padx=5, pady=5)
        self.boton_volver.configure(width=30)
        self.label_copy.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configuración de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.volver)
        self.root.grab_set()
        self.ventana_base.withdraw()
        self.ventana_base.wait_window(self.root)

    def objetivoActual(self):
        """Función que abre la ventana para ver el objetivo actual del usuario."""
        objetivo_actual = VentanaVerObjetivo(self.root)

    def nuevObjetivo(self):
        """Función que abre la ventana para crear un nuevo objetivo."""
        nuevo_objetivo = VentanaRegistrObjetivo(self.root, False)

    def volver(self):
        """Función que vuelve a la ventana anterior."""
        self.root.destroy()
        self.ventana_base.deiconify()

class VentanaRegistroAsesorado:
    """Clase que representa la ventana de registro de un asesorado."""
    def __init__(self, ventana_base, nuevo_usuario: bool):
        # Creación de la ventana
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Registro de Asesorado")
        self.root.geometry("400x500+500+200")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        self.nombre = tk.StringVar()
        self.dia = tk.StringVar()
        self.mes = tk.StringVar()
        meses = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", 
                 "Noviembre", "Diciembre")
        self.dic_meses = {mes: i for i, mes in enumerate(meses)}
        self.año = tk.StringVar()
        self.altura = tk.StringVar()
        self.peso = tk.StringVar()
        self.sexo = tk.StringVar()
        sexos = ("Masculino", "Femenino")
        self.dic_sexos = {"Masculino": "H", "Femenino": "M"}
        self.somatotipo = tk.StringVar()
        somatotipos = ("Ectomorfo", "Mesomorfo", "Endomorfo")
        self.dic_somatotipos = {"Ectomorfo": "E", "Mesomorfo": "M", "Endomorfo": "H"}
        self.porcen_grasa = tk.StringVar()
        self.nuevo_usuario = nuevo_usuario
        
        # Widgets
        self.logo = tk.Label(self.root, image=logo, anchor='center')
        self.titulo_logo = tk.Label(self.root, text="Registro de Asesorado")
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.frame_datos_personales = tk.Frame(self.root)
        self.label_nombre = tk.Label(self.frame_datos_personales, text="Nombre Completo:")
        self.entry_nombre = ttk.Entry(self.frame_datos_personales, textvariable=self.nombre, width=30)
        self.label_fecha_nacimiento = tk.Label(self.frame_datos_personales, text="Fecha de Nacimiento:")
        self.spinbox_dia = ttk.Spinbox(self.frame_datos_personales, from_=1, to=31, textvariable=self.dia, width=10, state="readonly")
        self.combobox_mes = ttk.Combobox(self.frame_datos_personales, values=meses, textvariable=self.mes, width=10, state="readonly")
        self.spinbox_año = ttk.Spinbox(self.frame_datos_personales, from_=1960, to=2020, textvariable=self.año, width=10, state="readonly")
        self.frame_datos_antropometricos = tk.Frame(self.root)
        self.label_altura = tk.Label(self.frame_datos_antropometricos, text="Altura (cm):")
        self.entry_altura = ttk.Entry(self.frame_datos_antropometricos, textvariable=self.altura)
        self.label_peso = tk.Label(self.frame_datos_antropometricos, text="Peso (kg):")
        self.entry_peso = ttk.Entry(self.frame_datos_antropometricos, textvariable=self.peso)
        self.label_sexo = tk.Label(self.frame_datos_antropometricos, text="Sexo:")
        self.combobox_sexo = ttk.Combobox(self.frame_datos_antropometricos, values=sexos, textvariable=self.sexo, width=17, state="readonly")
        self.frame_datos_corporales = tk.Frame(self.root)
        self.label_somatotipo = tk.Label(self.frame_datos_corporales, text="Somatotipo:")
        self.combobox_somatotipo = ttk.Combobox(self.frame_datos_corporales, values=somatotipos, textvariable=self.somatotipo, width=17,
         state="readonly")
        self.boton_foto_somattpo = ttk.Button(self.frame_datos_corporales, text="Ver Somatotipos", command=self.verFotoSttpo)
        self.label_porcen_grasa = tk.Label(self.frame_datos_corporales, text="% Grasa:")
        self.entry_porcen_grasa = ttk.Entry(self.frame_datos_corporales, textvariable=self.porcen_grasa)
        self.boton_registrar = ttk.Button(self.root, text="Registrar", command=self.registrar)
        self.boton_foto_grasa = ttk.Button(self.frame_datos_corporales, text="Ver Porcentajes de Grasa", command=self.verFoto)
        self.boton_cancelar = ttk.Button(self.root, text="Cancelar", command=self.cancelar)
        
        # Configuración de widgets
        self.logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.titulo_logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.titulo_logo.config(font=("Arial", 24))
        self.separador.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10)
        self.frame_datos_personales.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=0)
        self.label_nombre.grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        self.label_fecha_nacimiento.grid(row=1, column=0, padx=5, pady=5)
        self.spinbox_dia.grid(row=2, column=0,padx=10, pady=5, sticky=tk.E)
        self.spinbox_dia.set("Día")
        self.combobox_mes.grid(row=2, column=1, pady=5)
        self.combobox_mes.set("Mes")
        self.spinbox_año.grid(row=2, column=2, pady=5)
        self.spinbox_año.set("Año")
        self.frame_datos_antropometricos.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=0)
        self.label_altura.grid(row=0, column=0, padx=5, pady=5)
        self.entry_altura.grid(row=0, column=1, padx=5, pady=5)
        self.label_peso.grid(row=1, column=0, padx=5, pady=5)
        self.entry_peso.grid(row=1, column=1, padx=5, pady=5)
        self.label_sexo.grid(row=2, column=0, padx=5, pady=5)
        self.combobox_sexo.grid(row=2, column=1, padx=5, pady=5)
        self.combobox_sexo.set("Indique su Sexo")
        self.frame_datos_corporales.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=0)
        self.label_somatotipo.grid(row=0, column=0, padx=5, pady=5)
        self.combobox_somatotipo.grid(row=0, column=1, padx=5, pady=5)
        self.combobox_somatotipo.set("Elija su Somatotipo")
        self.boton_foto_somattpo.grid(row=0, column=2, padx=5, pady=5)
        self.label_porcen_grasa.grid(row=1, column=0, padx=5, pady=5)
        self.entry_porcen_grasa.grid(row=1, column=1, padx=5, pady=5)
        self.boton_foto_grasa.grid(row=1, column=2, padx=5, pady=5)
        self.boton_registrar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.boton_cancelar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configuración de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.cancelar)
        self.root.grab_set()
        self.ventana_base = ventana_base
        self.ventana_base.withdraw()
        self.ventana_base.wait_window(self.root)
        
    def registrar(self):
        variables_correctas = 7
        if self.entry_nombre.get() == "":
            msg.showerror("Error", "Debe ingresar un nombre")
            variables_correctas -= 1
        elif len(str(self.nombre.get())) < 10:
            msg.showerror("Error", "El nombre ingresado no es válido. Debe tener al menos 10 caracteres")
            variables_correctas -= 1
        elif self.nombre.get().replace(" ", "").isalpha() == False:
            msg.showerror("Error", "El nombre ingresado no es válido. Debe contener solo letras.")
            variables_correctas -= 1
        elif not " " in self.nombre.get():
            msg.showerror("Error", "El nombre ingresado no es válido. Debe contener al menos un apellido.")
            variables_correctas -= 1
        if self.spinbox_dia.get() == "Día" or self.combobox_mes.get() == "Mes" or self.spinbox_año.get() == "Año":
            msg.showerror("Error", "Debe ingresar una fecha de nacimiento")
        else:
            try:
                fecha_bruta = f"{self.spinbox_dia.get()}/{self.combobox_mes.current() + 1}/{self.spinbox_año.get()}"
                fecha_nacimiento = datetime.strptime(fecha_bruta, "%d/%m/%Y")
            except ValueError:
                msg.showerror("Error", "La fecha ingresada no es válida")
                variables_correctas -= 1
        try:
            if str(self.altura.get()) == "":
                msg.showerror("Error", "Debe ingresar una altura")
                variables_correctas -= 1
            elif int(self.entry_altura.get()) > 250 or int(self.entry_altura.get()) < 100:
                msg.showerror("Error", "La altura ingresada no es válida. Debe estar entre 100 y 250 cm.")
                variables_correctas -= 1
            if self.peso.get() == "":
                msg.showerror("Error", "Debe ingresar un peso")
                variables_correctas -= 1
            elif float(self.entry_peso.get()) > 150 or float(self.entry_peso.get()) < 30:
                msg.showerror("Error", "El peso ingresado no es válido. Debe estar entre 30 y 150 kg.")
                variables_correctas -= 1
        except ValueError:
            msg.showerror("Error", "La altura y el peso ingresados no son válidos. Deben ser números.")
            variables_correctas -= 1
        if self.combobox_sexo.get() == "Indique su Sexo":
            msg.showerror("Error", "Debe ingresar un sexo")
            variables_correctas -= 1
        if self.combobox_somatotipo.get() == "Elija su Somatotipo":
            msg.showerror("Error", "Debe ingresar un somatotipo")
            variables_correctas -= 1
        try:
            if self.entry_porcen_grasa.get() == "":
                msg.showerror("Error", "Debe ingresar un porcentaje de grasa")
                variables_correctas -= 1
            elif float(self.entry_porcen_grasa.get()) > 60 or float(self.entry_porcen_grasa.get()) < 3:
                msg.showerror("Error", "El porcentaje de grasa ingresado no es válido. Debe estar entre 3 y 60.")
                variables_correctas -= 1
        except ValueError:
            msg.showerror("Error", "El porcentaje de grasa ingresado no es válido. Debe ser un número.")
            variables_correctas -= 1
        if variables_correctas == 7:
            try:
                msg.showinfo("Éxito", "El registro se ha realizado con éxito")
                if self.nuevo_usuario:
                    global asesorado_activo
                    asesorado_activo = asesorado.Asesorado(self.nombre.get(), fecha_bruta, int(self.altura.get()),
                                                            float(self.peso.get()), self.dic_sexos[self.combobox_sexo.get()],
                                                            self.dic_somatotipos[self.combobox_somatotipo.get()],
                                                            float(self.porcen_grasa.get()), usuario_activo)
                    asesorado_activo.registrar()
                    nuevo_objetivo = VentanaRegistrObjetivo(self.root, self.nuevo_usuario)
                    self.ventana_base.deiconify()
                    self.root.destroy()
                else:
                    self.ventana_base.deiconify()
                    self.root.destroy()
            except:
                msg.showerror("Error", "Ha ocurrido un error al registrar los datos")
        
    
    def verFoto(self):
        foto_grasa = tk.PhotoImage(file=os.path.join("assets", "estimado_graso.png"))
        ventanaFoto = tk.Toplevel(self.root)
        ventanaFoto.title("Training Tool - Porcentajes de Grasa Corporal")
        ventanaFoto.geometry("679x500")
        ventanaFoto.resizable(True, True)
        ventanaFoto.grab_set()
        ventanaFoto.protocol("WM_DELETE_WINDOW", ventanaFoto.destroy)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        ventanaFoto.iconphoto(True, ico)
        foto = tk.Label(ventanaFoto, image=foto_grasa, anchor=tk.CENTER)
        foto.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        boton = ttk.Button(ventanaFoto, text="Cerrar", command=ventanaFoto.destroy)
        boton.pack(side=tk.BOTTOM, pady=10)
        boton.config(width=30)
        self.root.wait_window(ventanaFoto)

    def verFotoSttpo(self):
        foto_sttpo = tk.PhotoImage(file=os.path.join("assets", "tipo-de-cuerpo.png"))
        ventanaFoto = tk.Toplevel(self.root)
        ventanaFoto.title("Training Tool - Somatotipos")
        ventanaFoto.geometry("729x800")
        ventanaFoto.resizable(True, True)
        ventanaFoto.grab_set()
        ventanaFoto.protocol("WM_DELETE_WINDOW", ventanaFoto.destroy)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        ventanaFoto.iconphoto(True, ico)
        foto = tk.Label(ventanaFoto, image=foto_sttpo, anchor=tk.CENTER)
        foto.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        boton = ttk.Button(ventanaFoto, text="Cerrar", command=ventanaFoto.destroy)
        boton.pack(side=tk.BOTTOM, pady=10)
        boton.config(width=30)
        self.root.wait_window(ventanaFoto)
    
    def cancelar(self):
        if not self.nuevo_usuario:
            self.ventana_base.deiconify()
            self.root.destroy()
        else:
            msg.showerror("Error", "Debe completar el registro para poder continuar")
# --- Fin de la clase VentanaRegistroAsesorado --- #

class VentanaActualizarDatos:
    """ Clase que representa la ventana de actualización de datos de un asesorado. """
    def __init__(self, ventana_base):
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Actualizar datos")
        self.root.geometry("500x500+500+200")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        self.peso_nuevo = tk.StringVar()
        self.altura_nueva = tk.StringVar()
        self.porcen_grasa_nuevo = tk.StringVar()

        # Creación de los widgets
        self.logo = tk.Label(self.root, image=logo, anchor='center')
        self.titulo_logo = tk.Label(self.root, text="Actualización de Datos", font=("Arial", 20))
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.lframe_datos = ttk.LabelFrame(self.root, text="Ingresa los nuevos datos")
        self.label_peso = tk.Label(self.lframe_datos, text="Peso (kg):")
        self.entry_peso = ttk.Entry(self.lframe_datos, textvariable=self.peso_nuevo)
        self.label_altura = tk.Label(self.lframe_datos, text="Altura (cm):")
        self.entry_altura = ttk.Entry(self.lframe_datos, textvariable=self.altura_nueva)
        self.label_porcen_grasa = tk.Label(self.lframe_datos, text="Porcentaje de grasa corporal (%):")
        self.entry_porcen_grasa = ttk.Entry(self.lframe_datos, textvariable=self.porcen_grasa_nuevo)
        self.boton_foto_grasa = ttk.Button(self.lframe_datos, text="Ver porcentajes de grasa", command=self.verFoto)
        self.boton_actualizar = ttk.Button(self.root, text="Actualizar", command=self.actualizar)

        # Posicionamiento de los widgets
        self.logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.titulo_logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.separador.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10)
        self.lframe_datos.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.label_peso.grid(row=0, column=0, padx=5, pady=5)
        self.entry_peso.grid(row=0, column=1, padx=5, pady=5)
        self.label_altura.grid(row=1, column=0, padx=5, pady=5)
        self.entry_altura.grid(row=1, column=1, padx=5, pady=5)
        self.label_porcen_grasa.grid(row=2, column=0, padx=5, pady=5)
        self.entry_porcen_grasa.grid(row=2, column=1, padx=5, pady=5)
        self.boton_foto_grasa.grid(row=2, column=3, padx=5, pady=5)
        self.boton_actualizar.pack(side=tk.BOTTOM, padx=10, pady=10)
        self.boton_actualizar.config(width=30)

        # Configuración de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.cancelar)
        self.root.grab_set()
        self.ventana_base = ventana_base
        self.ventana_base.withdraw()
        self.ventana_base.wait_window(self.root)
    
    def verFoto(self):
        foto_grasa = tk.PhotoImage(file=os.path.join("assets", "estimado_graso.png"))
        ventanaFoto = tk.Toplevel(self.root)
        ventanaFoto.title("Training Tool - Porcentajes de Grasa Corporal")
        ventanaFoto.geometry("679x500")
        ventanaFoto.resizable(True, True)
        ventanaFoto.grab_set()
        ventanaFoto.protocol("WM_DELETE_WINDOW", ventanaFoto.destroy)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        ventanaFoto.iconphoto(True, ico)
        foto = tk.Label(ventanaFoto, image=foto_grasa, anchor=tk.CENTER)
        foto.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        boton = ttk.Button(ventanaFoto, text="Cerrar", command=ventanaFoto.destroy)
        boton.pack(side=tk.BOTTOM, pady=10)
        boton.config(width=30)
        self.root.wait_window(ventanaFoto)

    def actualizar(self):
        variables_correctas = 3
        try:
            if str(self.altura_nueva.get()) == "":
                msg.showerror("Error", "Debe ingresar una altura")
                variables_correctas -= 1
            elif int(self.entry_altura.get()) > 250 or int(self.entry_altura.get()) < 100:
                msg.showerror("Error", "La altura ingresada no es válida. Debe estar entre 100 y 250 cm.")
                variables_correctas -= 1
            if self.peso_nuevo.get() == "":
                msg.showerror("Error", "Debe ingresar un peso")
                variables_correctas -= 1
            elif float(self.entry_peso.get()) > 150 or float(self.entry_peso.get()) < 30:
                msg.showerror("Error", "El peso ingresado no es válido. Debe estar entre 30 y 150 kg.")
                variables_correctas -= 1
        except ValueError:
            msg.showerror("Error", "La altura y el peso ingresados no son válidos. Deben ser números.")
            variables_correctas -= 1
        try:
            if self.porcen_grasa_nuevo.get() == "":
                msg.showerror("Error", "Debe ingresar un porcentaje de grasa")
                variables_correctas -= 1
            elif float(self.porcen_grasa_nuevo.get()) > 60 or float(self.porcen_grasa_nuevo.get()) < 3:
                msg.showerror("Error", "El porcentaje de grasa ingresado no es válido. Debe estar entre 3 y 60.")
                variables_correctas -= 1
        except ValueError:
            msg.showerror("Error", "El porcentaje de grasa ingresado no es válido. Debe ser un número.")
            variables_correctas -= 1
        if variables_correctas == 3:
            try:
                altura = int(self.entry_altura.get())
                peso = float(self.entry_peso.get())
                porcen_graso = float(self.entry_porcen_grasa.get())
                asesorado_activo.altura = altura
                asesorado_activo.peso = peso
                asesorado_activo.porcen_graso = porcen_graso
                asesorado_activo.actualizar(altura, peso, porcen_graso)
                msg.showinfo("Éxito", "Los datos se actualizaron correctamente.")
                nuevo_objetivo = VentanaRegistrObjetivo(self.root, True)
                self.ventana_base.deiconify()
                self.root.destroy()
            except Exception as e:
                msg.showerror("Error", "No se pudieron actualizar los datos. Intente nuevamente.")
                print(e)

    def cancelar(self):
        msg.showwarning("Advertencia", "No se actualizaron los datos.")

# --- Fin de la clase VentanaActualizarDatos --- #


class VentanaRegistrObjetivo:
    """Clase que representa la ventana de registro de objetivos de un asesorado."""
    def __init__(self, ventana_base, nuevo_usuario: bool):
        # Creación de la ventana
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Registro de Objetivo")
        self.root.geometry("400x700+500+100")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        self.ventana_base = ventana_base
        self.objetivo = tk.IntVar()
        self.objetivo.set(1)
        self.dict_objetivos = {1: "mantenimiento", 2: "definicion", 3: "hipertrofia"}
        self.actividad_fisica = tk.IntVar()
        self.actividad_fisica.set(1)
        self.dict_actividades = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}
        self.nro_comidas = tk.StringVar()
        self.nuevo_usuario = nuevo_usuario

        # Widgets
        self.logo = tk.Label(self.root, image=logo, anchor='center')
        self.titulo_logo = tk.Label(self.root, text="Registro de Objetivo", font=("Arial", 24))
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.lframe_objetivo = ttk.LabelFrame(self.root, text="Indique su Objetivo")
        self.botonradio_mantenimiento = ttk.Radiobutton(self.lframe_objetivo, text="Mantenimiento", variable=self.objetivo, value=1)
        self.botonradio_definicion = ttk.Radiobutton(self.lframe_objetivo, text="Perder grasa", variable=self.objetivo, value=2)
        self.botonradio_volumen = ttk.Radiobutton(self.lframe_objetivo, text="Ganar masa muscular", variable=self.objetivo, value=3)
        self.lframe_actividad = ttk.LabelFrame(self.root, text="Indique la Actividad Física que hará")
        self.botonradio_sedentario = ttk.Radiobutton(self.lframe_actividad, text="Sedentario", variable=self.actividad_fisica, value=1)
        self.botonradio_ligera = ttk.Radiobutton(self.lframe_actividad, text="Ligera (1-3 veces por semana)", 
            variable=self.actividad_fisica, value=2)
        self.botonradio_moderada = ttk.Radiobutton(self.lframe_actividad, text="Moderada (3-5 veces por semana)", 
            variable=self.actividad_fisica, value=3)
        self.botonradio_intensa = ttk.Radiobutton(self.lframe_actividad, text="Intensa (6-7 veces por semana)", 
            variable=self.actividad_fisica, value=4)
        self.botonradio_muy_intensa = ttk.Radiobutton(self.lframe_actividad, text="Muy intensa (2 veces por día)", 
            variable=self.actividad_fisica, value=5)
        self.lframe_comidas = ttk.LabelFrame(self.root, text="Número de Comidas al día")
        self.label_comidas = ttk.Label(self.lframe_comidas, text="Indique el N° de comidas que podrá hacer al día:")
        self.entry_comidas = ttk.Entry(self.lframe_comidas, textvariable=self.nro_comidas)
        self.boton_aceptar = ttk.Button(self.root, text="Aceptar", command=self.aceptar)
        self.boton_cancelar = ttk.Button(self.root, text="Cancelar", command=self.cancelar)

        # Configuración de widgets
        self.logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.titulo_logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.separador.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.lframe_objetivo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.botonradio_mantenimiento.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.botonradio_definicion.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.botonradio_volumen.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lframe_actividad.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.botonradio_sedentario.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.botonradio_ligera.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.botonradio_moderada.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.botonradio_intensa.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.botonradio_muy_intensa.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lframe_comidas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.label_comidas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.entry_comidas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.boton_aceptar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.boton_cancelar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configuración de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.cancelar)
        self.root.grab_set()
        self.ventana_base.withdraw()
        self.ventana_base.wait_window(self.root)

    def aceptar(self):
        try:
            if self.nro_comidas.get() == "":
                msg.showerror("Error", "Debe completar el registro para poder continuar")
            elif not str(self.nro_comidas.get()).isdigit():
                msg.showerror("Error", "El número de comidas debe ser un número entero")
            elif int(self.nro_comidas.get()) < 2 or int(self.nro_comidas.get()) > 6:
                msg.showerror("Error", "El número de comidas debe estar entre 2 y 6")
            else:
                g_total = self.dict_actividades[self.actividad_fisica.get()] * asesorado_activo.gasto
                if self.objetivo.get() == 1:
                    protes = 2.2 * asesorado_activo.peso
                    grasas = 1 * asesorado_activo.peso
                    g_fase = g_total
                elif self.objetivo.get() == 2:
                    protes = 1.8 * asesorado_activo.peso
                    grasas = 0.5 * asesorado_activo.peso
                    if asesorado_activo.somatotipo == 'E':
                        g_fase = 0.9 * g_total
                    elif asesorado_activo.somatotipo == 'M':
                        g_fase = 0.8 * g_total
                    else:
                        g_fase = 0.7 * g_total
                else:
                    protes = 2.5 * asesorado_activo.peso
                    grasas = 1.5 * asesorado_activo.peso
                    if asesorado_activo.somatotipo == 'E':
                        g_fase = 1.2 * g_total
                    elif asesorado_activo.somatotipo == 'M':
                        g_fase = 1.15 * g_total
                    else:
                        g_fase = 1.1 * g_total
                macros = g_fase - (protes * 4) - (grasas * 9)
                carbos = macros / 4

                global objetivo
                objetivo = fase_entrenamiento.FaseEntrenamiento(self.dict_objetivos[self.objetivo.get()],
                                                                       "", g_fase, asesorado_activo.nombre, protes, grasas,
                                                                       carbos, int(self.nro_comidas.get()))
                objetivo.iniciarFase()
                msg.showinfo("Éxito", "Fase de entrenamiento iniciada con éxito")
                self.ventana_base.deiconify()
                self.root.destroy()
        except ValueError:
            msg.showerror("Error", "Hubo un error al intentar iniciar la fase de entrenamiento.")

    def cancelar(self):
        if not self.nuevo_usuario:
            self.ventana_base.deiconify()
            self.root.destroy()
        else:
            msg.showerror("Error", "Debe completar el registro para poder continuar")
# --- Fin de la clase VentanaRegistrObjetivo --- #


class VentanaProgresoAsesorado:
    """Clase que representa la ventana de progreso del asesorado."""
    def __init__(self, ventana_base):
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Progreso del asesorado")
        self.root.geometry("800x700+500+100")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        ffmi = tk.PhotoImage(file=os.path.join("assets", "FFMI.png"))
        nro_ffmi, estado_ffmi = asesorado_activo.ffmi()
        self.ventana_base = ventana_base

        # Widgets
        self.frame_frames = tk.Frame(self.root)
        self.label_logo = tk.Label(self.root, image=logo)
        self.titulo_logo = tk.Label(self.root, text=f"Progreso de {asesorado_activo.nombre.title()}", font=("Arial", 16))
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.lframe_datos_personales = ttk.Labelframe(self.frame_frames, text="Datos personales")
        self.label_fecha_nacimiento = tk.Label(self.lframe_datos_personales, text=f"Fecha de nacimiento: {asesorado_activo.fecha_nacido}")
        self.label_sexo = tk.Label(self.lframe_datos_personales, text=f"Sexo: {'Masculino' if asesorado_activo.sexo == 'H' else 'Femenino'}")
        self.label_altura = tk.Label(self.lframe_datos_personales, text=f"Altura (cm): {asesorado_activo.altura}")
        self.label_peso = tk.Label(self.lframe_datos_personales, text=f"Peso (kg): {asesorado_activo.peso}")
        self.label_somatotipo = tk.Label(self.lframe_datos_personales, 
            text=f"Somatotipo: {'Ectomorfo' if asesorado_activo.somatotipo == 'E' else 'Mesomorfo' if asesorado_activo.somatotipo == 'M' else 'Endomorfo'}")
        self.label_tmb = tk.Label(self.lframe_datos_personales, text=f"Gasto Energético Basal: {round(asesorado_activo.gasto, 2)}")
        self.lframe_ffmi = ttk.Labelframe(self.frame_frames, text="Nivel de desarrollo")
        self.label_ffmi = tk.Label(self.lframe_ffmi, text=f"""{asesorado_activo.nombre.title()}, tu nivel de desarrollo es: {nro_ffmi}

Se podría decir que tu estado físico actual está... {estado_ffmi}. 
Aquí puedes ver una tabla con los niveles de desarrollo y sus respectivas descripciones:""")
        self.label_imagen_ffmi = tk.Label(self.lframe_ffmi, image=ffmi)
        self.boton_volver = tk.Button(self.root, text="Volver", command=self.volver)
        
        # Posicionamiento
        self.label_logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.titulo_logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.separador.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=5)
        self.frame_frames.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lframe_datos_personales.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.label_fecha_nacimiento.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_sexo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_altura.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_peso.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_somatotipo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_tmb.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lframe_ffmi.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.label_ffmi.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_imagen_ffmi.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.boton_volver.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.boton_volver.configure(width=30)
        
        # Configuración de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.volver)
        self.root.grab_set()
        self.ventana_base.withdraw()
        self.ventana_base.wait_window(self.root)

    def volver(self):
        self.ventana_base.deiconify()
        self.root.destroy()


class VentanaVerObjetivo:
    """Clase que representa la ventana de ver objetivo."""
    def __init__(self, ventana_base):
        self.root = tk.Toplevel(ventana_base)
        self.root.title(f"Training Tool - Objetivo actual de {asesorado_activo.nombre.title()}")
        self.root.geometry("800x700+500+100")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)

    # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        ffmi = asesorado_activo.ffmi()
        self.ventana_base = ventana_base

    # Widgets
        self.label_logo = tk.Label(self.root, image=logo)
        self.titulo_logo = tk.Label(self.root, text=f"Objetivo Actual", font=("Arial", 16))
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.frame_frames = tk.Frame(self.root)
        self.lframe_datos_personales = ttk.Labelframe(self.frame_frames, text="Datos personales")
        self.label_nombre = tk.Label(self.lframe_datos_personales, text=f"Nombre Asesorado: {asesorado_activo.nombre.title()}")
        self.label_peso_actual = tk.Label(self.lframe_datos_personales, text=f"Peso actual (kg): {asesorado_activo.peso}")
        self.label_porcentaje_grasa = tk.Label(self.lframe_datos_personales, text=f"Porcentaje de grasa: {asesorado_activo.porcen_graso}%")
        self.label_tmb = tk.Label(self.lframe_datos_personales, text=f"Gasto Energético Basal: {round(asesorado_activo.gasto, 2)}Kcal")
        self.label_ffmi = tk.Label(self.lframe_datos_personales, text=f"FFMI: {round(ffmi[0], 2)}")
        self.lframe_objetivo = ttk.Labelframe(self.frame_frames, text="Objetivos")
        self.label_objetivo = tk.Label(self.lframe_objetivo, text=f"Objetivo: {objetivo.tipo.title()}")
        self.label_get_objetivo = tk.Label(self.lframe_objetivo, text=f"GET objetivo: {round(objetivo.gasto_t, 2)}Kcal")
        self.label_proteinas = tk.Label(self.lframe_objetivo, text=f"Proteínas objetivo: {round(objetivo.proteinas, 2)}gr al día")
        self.label_grasas = tk.Label(self.lframe_objetivo, text=f"Grasas objetivo: {round(objetivo.grasas, 2)}gr al día")
        self.label_hidratos = tk.Label(self.lframe_objetivo, text=f"Hidratos objetivo: {round(objetivo.carbohidratos, 2)}gr al día")
        self.lframe_comidas = ttk.Labelframe(self.root, text="Comidas")
        self.label_explicacion_comidas = tk.Label(self.lframe_comidas,
        text=f"""Para cada una de las {objetivo.comidas} comidas del día, se recomienda consumir las siguientes cantidades de macronutrientes:
        
    * Proteínas: {round(objetivo.proteinas / objetivo.comidas, 2)}gr
    * Grasas: {round(objetivo.grasas / objetivo.comidas, 2)}gr
    * Hidratos: {round(objetivo.carbohidratos / objetivo.comidas, 2)}gr

La suma de estos valores es la división de las cantidades totales de macronutrientes entre el número de comidas del día. 
Recuerda que la cantidad de estos macronutrientes no necesariamente debe ser igual en cada comida.
Lo unico que se debe cumplir es que la suma de las cantidades de macronutrientes de cada comida sea igual a la 
cantidad total de macronutrientes del día.
        """)
        self.boton_volver = tk.Button(self.root, text="Volver", command=self.volver)

    # Configuración de widgets
        self.label_logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.titulo_logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.separador.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=5)
        self.frame_frames.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.lframe_datos_personales.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_nombre.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_peso_actual.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_porcentaje_grasa.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_tmb.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_ffmi.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lframe_objetivo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.label_objetivo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_get_objetivo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_proteinas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_grasas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_hidratos.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lframe_comidas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.label_explicacion_comidas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.boton_volver.pack(side=tk.BOTTOM, padx=5, pady=20)
        self.boton_volver.config(width=30)

    # Configuración de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.volver)
        self.root.grab_set()
        self.ventana_base.withdraw()
        self.ventana_base.wait_window(self.root)

    def volver(self):
        self.ventana_base.deiconify()
        self.root.destroy()
# --- Fin de la clase VentanaVerObjetivo --- #

class MenuAlimentos:
    """Clase que representa el menú de objetivos del asesorado."""
    def __init__(self, ventana_base):
        # Creación de la ventana
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Alimentación y dieta")
        self.root.geometry("400x600+500+200")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)
        
        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        self.ventana_base = ventana_base
        
        # Widgets de la ventana
        self.logo = tk.Label(self.root, image=logo)
        self.separador = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.label_objetivos = tk.Label(self.root, text="Alimentación y Dieta")
        self.label_objetivos.configure(font=("Arial", 16))
        self.boton_inventario = ttk.Button(self.root, text="Inventario", command=self.ver_alimentos)
        self.boton_comidas = ttk.Button(self.root, text="Platos y Comidas", command=self.ver_comidas)
        self.boton_menu_semanal = ttk.Button(self.root, text="Menú Semanal", command=self.ver_menu_semanal)
        self.boton_volver = ttk.Button(self.root, text="Volver", command=self.volver)
        self.label_copy = tk.Label(self.root, text="© 2020 Training Tool. Todos los derechos reservados.")

        # Configuración de widgets
        self.logo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.label_objetivos.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.separador.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=5)
        self.boton_inventario.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.boton_comidas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.boton_menu_semanal.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.boton_volver.pack(side=tk.BOTTOM, padx=5, pady=20)
        self.boton_volver.config(width=30)
        self.label_copy.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configuración de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.volver)
        self.root.grab_set()
        self.ventana_base.withdraw()
        self.ventana_base.wait_window(self.root)

    def volver(self):
        self.ventana_base.deiconify()
        self.root.destroy()

    def ver_alimentos(self):
        msg.showinfo("Training Tool", "Esta funcionalidad aún no está disponible.")

    def ver_comidas(self):
        msg.showinfo("Training Tool", "Esta funcionalidad aún no está disponible.")

    def ver_menu_semanal(self):
        msg.showinfo("Training Tool", "Esta funcionalidad aún no está disponible.")
# --- Fin de la clase MenuAlimentos --- #


class InventarioAlimentos:
    """Clase que representa el inventario de alimentos del asesorado."""
    def __init__(self, ventana_base):
        # Creación de la ventana
        self.root = tk.Toplevel(ventana_base)
        self.root.title("Training Tool - Inventario de alimentos")
        self.root.geometry("900x600+500+200")
        self.root.resizable(False, False)
        ico = tk.PhotoImage(file=os.path.join("assets", "saludable.ico"))
        self.root.iconphoto(True, ico)

        # Variables de control
        logo = tk.PhotoImage(file=os.path.join("assets", "logo.png"))
        self.ventana_base = ventana_base
        self.id_alimento = tk.StringVar()
        self.nombre_alimento = tk.StringVar()
        self.cantidad_alimento = tk.StringVar()


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
