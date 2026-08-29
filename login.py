print("Hola mundo")


import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from menu import abrir_menu
from sistema_facade import SistemaFacade
import re

sistema = SistemaFacade()
ventana_login_global = None


# =========================================================
# RUTA COMPATIBLE CON PYINSTALLER
# =========================================================
def resolver_ruta(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ruta_relativa)


def iniciar_login():

    # =========================================================
    # LOGIN
    # =========================================================
    def verificar_login():

        usuario = entry_usuario.get().strip()
        clave = entry_clave.get().strip()

        if not usuario or not clave:
            messagebox.showerror("Error", "Ingrese usuario y contraseña", parent=ventana_login)
            return

        try:
            resultado = sistema.login(usuario, clave)
        except Exception as e:
            messagebox.showerror("Error", f"Error del sistema:\n{e}", parent=ventana_login)
            return

        if resultado:
            # 🔥 FIX IMPORTANTE (NO ROMPE TU SISTEMA)
            id_usuario = resultado[0]
            usuario_db = resultado[1]
            rol = resultado[2] if len(resultado) > 2 else "cliente"

            messagebox.showinfo("Bienvenido", f"Hola {usuario_db}", parent=ventana_login)

            ventana_login.withdraw()
            abrir_menu(rol, id_usuario, usuario_db)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos", parent=ventana_login)

    # =========================================================
    # REGISTRO
    # =========================================================
    def abrir_registro():

        ventana_registro = tk.Toplevel(ventana_login)
        ventana_registro.title("Crear cuenta")
        ventana_registro.geometry("450x650")
        ventana_registro.config(bg="#d2b48c")
        ventana_registro.resizable(False, False)

        tk.Label(ventana_registro, text="CREAR CUENTA",
                 font=("Impact", 24), bg="#d2b48c", fg="#5c3317").pack(pady=15)

        def crear_entry(label):
            tk.Label(ventana_registro, text=label,
                     font=("Arial", 11, "bold"), bg="#d2b48c").pack()
            entry = tk.Entry(ventana_registro, font=("Arial", 11), width=28)
            entry.pack(pady=3)
            return entry

        entry_user = crear_entry("Usuario")

        entry_pass = crear_entry("Contraseña")
        entry_pass.config(show="*")

        entry_confirmar = crear_entry("Confirmar contraseña")
        entry_confirmar.config(show="*")

        entry_edad = crear_entry("Edad")
        entry_genero = crear_entry("Género")
        entry_tel = crear_entry("Teléfono")
        entry_correo = crear_entry("Correo")

        # =========================================================
        # VALIDACIONES PROFESIONALES
        # =========================================================
        def validar_datos(usuario, clave, confirmar, edad, genero, telefono, correo):

            if not all([usuario, clave, confirmar, edad, genero, telefono, correo]):
                return "Todos los campos son obligatorios"

            # ===== USUARIO =====
            if len(usuario) < 3:
                return "Usuario muy corto"

            if " " in usuario:
                return "El usuario no debe tener espacios"

            # ===== CONTRASEÑA =====
            if len(clave) < 4:
                return "Contraseña muy corta (mínimo 4 caracteres)"

            if clave != confirmar:
                return "Las contraseñas no coinciden"

            # ===== EDAD =====
            if not edad.isdigit():
                return "Edad inválida (solo números)"

            edad_int = int(edad)
            if edad_int < 10 or edad_int > 100:
                return "Edad fuera de rango (10 - 100)"

            # ===== TELÉFONO =====
            if not telefono.isdigit():
                return "El teléfono debe contener solo números"

            if len(telefono) < 7 or len(telefono) > 10:
                return "Teléfono inválido (7 a 10 dígitos)"

            # ===== GÉNERO =====
            if genero.lower() not in ["hombre", "mujer", "otro"]:
                return "Género inválido (Hombre, Mujer, Otro)"

            # ===== CORREO =====
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", correo):
                return "Correo inválido"

            return None

        def registrar():

            usuario = entry_user.get().strip()
            clave = entry_pass.get().strip()
            confirmar = entry_confirmar.get().strip()
            edad = entry_edad.get().strip()
            genero = entry_genero.get().strip()
            telefono = entry_tel.get().strip()
            correo = entry_correo.get().strip()

            error_validacion = validar_datos(
                usuario, clave, confirmar, edad, genero, telefono, correo
            )

            if error_validacion:
                messagebox.showerror("Error", error_validacion, parent=ventana_registro)
                return

            try:
                creado = sistema.registrar_usuario(
                    usuario, clave, edad, genero, telefono, correo
                )
            except Exception as e:
                messagebox.showerror("Error", f"Error del sistema:\n{e}", parent=ventana_registro)
                return

            if creado:
                messagebox.showinfo("Éxito", "Cuenta creada correctamente", parent=ventana_registro)
                ventana_registro.destroy()
            else:
                messagebox.showerror("Error", "El usuario ya existe", parent=ventana_registro)

        tk.Button(ventana_registro,
                  text="Crear Cuenta",
                  font=("Arial", 11, "bold"),
                  bg="#ff8c00",
                  fg="white",
                  width=20,
                  cursor="hand2",
                  command=registrar).pack(pady=18)

    # =========================================================
    # VENTANA PRINCIPAL
    # =========================================================
    global ventana_login_global

    ventana_login = tk.Tk()
    ventana_login_global = ventana_login

    ventana_login.title("GuepardFast")
    ventana_login.config(bg="#d9c29c")

    try:
        ventana_login.state("zoomed")
    except:
        ventana_login.geometry("1400x800")

    contenedor = tk.Frame(ventana_login, bg="#d9c29c")
    contenedor.pack(fill="both", expand=True)

    panel_izquierdo = tk.Frame(contenedor, bg="#5c3317", width=420)
    panel_izquierdo.pack(side="left", fill="y")
    panel_izquierdo.pack_propagate(False)

    panel_derecho = tk.Frame(contenedor, bg="black")
    panel_derecho.pack(side="right", fill="both", expand=True)

    # ===== FONDO =====
    try:
        ruta = resolver_ruta(os.path.join("imagenes", "sabana_dos.jpg"))
        img = Image.open(ruta)

        img = img.resize(
            (ventana_login.winfo_screenwidth(), ventana_login.winfo_screenheight())
        )

        fondo_tk = ImageTk.PhotoImage(img)
        ventana_login.fondo = fondo_tk

        tk.Label(panel_derecho, image=fondo_tk).place(relwidth=1, relheight=1)
    except Exception as e:
        print("Error fondo:", e)

    # ===== LOGO =====
    try:
        ruta_logo = resolver_ruta(os.path.join("imagenes", "logotipo.png"))
        logo = Image.open(ruta_logo).resize((280, 280))

        logo_tk = ImageTk.PhotoImage(logo)
        ventana_login.logo = logo_tk

        tk.Label(panel_izquierdo, image=logo_tk, bg="#5c3317").pack()
    except Exception as e:
        print("Error logo:", e)

    # ===== UI =====
    tk.Label(panel_izquierdo, text="GuepardFast",
             font=("Impact", 34), bg="#5c3317", fg="#ffae42").pack()

    tk.Label(panel_izquierdo,
             text="Envíos rápidos con mayor ferocidad",
             font=("Arial", 11, "bold"),
             bg="#5c3317",
             fg="#ffe082").pack(pady=10)

    tk.Label(panel_izquierdo, text="Usuario",
             bg="#5c3317", fg="white").pack()

    entry_usuario = tk.Entry(panel_izquierdo, width=28)
    entry_usuario.pack(pady=5)

    tk.Label(panel_izquierdo, text="Contraseña",
             bg="#5c3317", fg="white").pack()

    entry_clave = tk.Entry(panel_izquierdo, show="*", width=28)
    entry_clave.pack(pady=5)

    tk.Button(panel_izquierdo, text="Ingresar",
              bg="#ff8c00", fg="white",
              width=24, command=verificar_login).pack(pady=5)

    tk.Button(panel_izquierdo, text="Crear cuenta",
              bg="#c97b30", fg="white",
              width=24, command=abrir_registro).pack(pady=5)

    ventana_login.mainloop()