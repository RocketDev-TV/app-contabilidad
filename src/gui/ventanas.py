import customtkinter as ctk
# CAMBIAMOS ESTA LÍNEA PARA IMPORTAR LAS FUNCIONES REALES
from logic.almacen import registrar_movimiento, obtener_resumen_almacen

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.title("Sistema de Costos Históricos")
        self.geometry("800x600")
        
        # Título de la app
        self.titulo = ctk.CTkLabel(self, text="Control de Costos Históricos", font=("Arial", 22, "bold"))
        self.titulo.pack(pady=15)

        # Crear el contenedor de pestañas (Tabs)
        self.pestanas = ctk.CTkTabview(self, width=760, height=500)
        self.pestanas.pack(pady=10, padx=20)

        # Creamos las pestañas solicitadas por la profa
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
        # PARCEH PARA PARA QUE HAGA UN REGISTRO DE PRUEBA Y NO TRUENE
        print("\n[GUI] Picaste el botón. Simulando un registro en la lógica...")
        resultado = registrar_movimiento("Compra de Prueba", 10, 100.0)
        print(f"[GUI] Respuesta recibida de la lógica del almacén:\n{resultado}")