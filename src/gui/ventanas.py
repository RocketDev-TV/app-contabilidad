import customtkinter as ctk
from logic.almacen import calcular_almacen

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración basica de la ventana
        self.title("Sistema de Costos Históricos")
        self.geometry("800x600")
        
        # Titulo app
        self.titulo = ctk.CTkLabel(self, text="Control de Costos Históricos", font=("Arial", 22, "bold"))
        self.titulo.pack(pady=15)

        # Crear tabs
        self.pestanas = ctk.CTkTabview(self, width=760, height=500)
        self.pestanas.pack(pady=10, padx=20)

        self.pestanas.add("Almacén")
        self.pestanas.add("Nómina")
        self.pestanas.add("Prorrateos")
        self.pestanas.add("Resultados")

        # --- CONTENIDO DE LA PESTAÑA: ALMACÉN ---
        self.label_almacen = ctk.CTkLabel(self.pestanas.tab("Almacén"), text="Tarjeta de Almacén (Método Promedio)", font=("Arial", 16))
        self.label_almacen.pack(pady=20)

        self.btn_calcular = ctk.CTkButton(self.pestanas.tab("Almacén"), text="Calcular Inventario", command=self.ejecutar_calculo)
        self.btn_calcular.pack(pady=10)

        # --- CONTENIDO DE LAS OTRAS PESTAÑAS (Provisionales) ---
        ctk.CTkLabel(self.pestanas.tab("Nómina"), text="Cédula de Mano de Obra").pack(pady=20)
        ctk.CTkLabel(self.pestanas.tab("Prorrateos"), text="Prorrateo Primario, Secundario y Final").pack(pady=20)
        ctk.CTkLabel(self.pestanas.tab("Resultados"), text="Estado de Resultados y Costos").pack(pady=20)

    def ejecutar_calculo(self):
        # Aquí conectamos la interfaz con la carpeta logic
        resultado = calcular_almacen()
        print(f"Resultado devuelto a la GUI: {resultado}")