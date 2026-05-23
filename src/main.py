import sys
import os

# Truco para que Python encuentre la carpeta 'src' y sus módulos sin importar dónde se ejecute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from gui.ventanas import VentanaPrincipal

if __name__ == "__main__":
    # Configuramos el diseño visual
    ctk.set_appearance_mode("System")  # Toma el tema de tu Linux/Windows automáticamente
    ctk.set_default_color_theme("blue") # Color de botones por defecto

    # Inicializamos y corremos la app
    app = VentanaPrincipal()
    app.mainloop()