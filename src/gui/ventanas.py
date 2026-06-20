import customtkinter as ctk

# Importamos las pestañas modulares
from gui.gui_almacen import TabAlmacen
from gui.gui_estados import TabEstados
from gui.gui_prorrateos import TabProrrateos
from gui.gui_nomina import TabNomina

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Contabilidad de Costos")
        self.geometry("1300x650")
        self.minsize(1200, 600)

        # Contenedor principal de pestañas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Agregar las 4 pestañas
        self.tab_almacen = self.tabview.add("Almacén")
        self.tab_nomina = self.tabview.add("Nómina")
        self.tab_prorrateos = self.tabview.add("Prorrateos")
        self.tab_resultados = self.tabview.add("Resultados")

        # Inyectar el contenido modular en la pestaña de Almacén
        # Le pasamos self.tab_almacen como "master" para que se dibuje adentro
        self.vista_almacen = TabAlmacen(master=self.tab_almacen, fg_color="transparent")
        self.vista_almacen.pack(fill="both", expand=True)

        # Inyectar el contenido modular en la pestaña de Nómina
        self.vista_nomina = TabNomina(master=self.tab_nomina, fg_color="transparent")
        self.vista_nomina.pack(fill="both", expand=True)

        # Inyectar el contenido modular en la pestaña de Prorrateos
        self.vista_prorrateos = TabProrrateos(master=self.tab_prorrateos, fg_color="transparent")
        self.vista_prorrateos.pack(fill="both", expand=True)

        self.vista_estados = TabEstados(master=self.tab_resultados, fg_color="transparent")
        self.vista_estados.pack(fill="both", expand=True)