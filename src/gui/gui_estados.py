import customtkinter as ctk
from tkinter import ttk, messagebox
import logic.estados as logica_estados

class TabEstados(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Crear el contenedor de pestañas nativo de CustomTkinter
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear las sub-pestañas
        self.tab_costos = self.tabview.add("Estado de Costos")
        self.tab_resultados = self.tabview.add("Estado de Resultados")
        
        # Variable para guardar el costo de lo vendido y pasarlo a resultados
        self.costo_vendido_actual = 0.0
        
        # Aplicar el estilo de CustomTkinter a los Treeviews clásicos
        self.configurar_estilo_tablas()
        
        self.setup_tab_costos()
        self.setup_tab_resultados()

    def configurar_estilo_tablas(self):
        """Aplica un tema oscuro/claro al Treeview para que coincida con CTk."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#e0e0e0"
        fg_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        
        self.style.configure("Treeview", background=bg_color, foreground=fg_color, rowheight=30, fieldbackground=bg_color, borderwidth=0, font=("Arial", 11))
        self.style.map('Treeview', background=[('selected', '#1f538d')])
        self.style.configure("Treeview.Heading", background="#1f538d", foreground="white", relief="flat", font=("Arial", 12, "bold"))
        self.style.map("Treeview.Heading", background=[('active', '#14375e')])

    # ==========================================
    # PESTAÑA 1: ESTADO DE COSTOS
    # ==========================================
    def setup_tab_costos(self):
        # --- Zona de Inputs ---
        frame_inputs = ctk.CTkFrame(self.tab_costos)
        frame_inputs.pack(fill="x", padx=10, pady=10)
        
        # Título del Frame (reemplazo visual de ttk.LabelFrame)
        ctk.CTkLabel(frame_inputs, text="Inventarios de Producción", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=5, pady=(10, 5))
        
        ctk.CTkLabel(frame_inputs, text="Inv. Inicial Prod. Proceso:").grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.ent_ii_pp = ctk.CTkEntry(frame_inputs, width=120)
        self.ent_ii_pp.grid(row=1, column=1, padx=5, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Inv. Final Prod. Proceso:").grid(row=1, column=2, padx=5, pady=10, sticky="e")
        self.ent_if_pp = ctk.CTkEntry(frame_inputs, width=120)
        self.ent_if_pp.grid(row=1, column=3, padx=5, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Inv. Inicial Prod. Terminada:").grid(row=2, column=0, padx=5, pady=10, sticky="e")
        self.ent_ii_pt = ctk.CTkEntry(frame_inputs, width=120)
        self.ent_ii_pt.grid(row=2, column=1, padx=5, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Inv. Final Prod. Terminada:").grid(row=2, column=2, padx=5, pady=10, sticky="e")
        self.ent_if_pt = ctk.CTkEntry(frame_inputs, width=120)
        self.ent_if_pt.grid(row=2, column=3, padx=5, pady=10)
        
        btn_generar_costos = ctk.CTkButton(frame_inputs, text="Generar Estado de Costos", fg_color="#1f538d", hover_color="#14375e", command=self.ejecutar_estado_costos)
        btn_generar_costos.grid(row=1, column=4, rowspan=2, padx=20, pady=10)

        # --- Zona de Visualización (Cédula) ---
        columnas = ("Concepto", "Monto")
        self.tree_costos = ttk.Treeview(self.tab_costos, columns=columnas, show="headings", selectmode="none")
        self.tree_costos.heading("Concepto", text="Concepto")
        self.tree_costos.heading("Monto", text="Monto ($)")
        self.tree_costos.column("Concepto", width=400, anchor="w")
        self.tree_costos.column("Monto", width=150, anchor="center")
        self.tree_costos.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tags para estilos dentro del Treeview
        self.tree_costos.tag_configure("total", background="#14375e", foreground="white")
        self.tree_costos.tag_configure("resta", foreground="#ff4d4d")

    def ejecutar_estado_costos(self):
        try:
            # Leer inputs (si están vacíos, asume 0)
            ii_pp = float(self.ent_ii_pp.get() or 0)
            if_pp = float(self.ent_if_pp.get() or 0)
            ii_pt = float(self.ent_ii_pt.get() or 0)
            if_pt = float(self.ent_if_pt.get() or 0)
            
            # Llamar a la lógica
            res = logica_estados.generar_estado_costos(ii_pp, if_pp, ii_pt, if_pt)
            
            # Guardar el costo de lo vendido para la otra pestaña
            self.costo_vendido_actual = res.get("costo_de_lo_vendido", 0)
            
            # Limpiar tabla
            for item in self.tree_costos.get_children(): self.tree_costos.delete(item)
            
            # Insertar filas con el formato requerido
            formato = [
                ("Inventario inicial de materia prima", res["inventario_inicial_mp"], ""),
                ("(+) Compras netas de materia prima", res["compras_netas_mp"], ""),
                ("(=) Materia prima disponible", res["materia_prima_disponible"], "total"),
                ("(-) Inventario final de materia prima", res["inventario_final_mp"], "resta"),
                ("(=) Materia prima directa utilizada", res["materia_prima_directa_consumida"], "total"),
                ("(+) Mano de obra directa", res["mano_de_obra_directa"], ""),
                ("(+) Cargos indirectos", res["cargos_indirectos"], ""),
                ("(=) Costo incurrido", res["costo_incurrido"], "total"),
                ("(+) Inventario inicial de prod. en proceso", res["inventario_inicial_proceso"], ""),
                ("(=) Producción procesada disponible", res["total_procesado"], "total"),
                ("(-) Inventario final de prod. en proceso", res["inventario_final_proceso"], "resta"),
                ("(=) Costo de la producción terminada", res["costo_produccion_terminada"], "total"),
                ("(+) Inventario inicial de prod. terminada", res["inventario_inicial_terminada"], ""),
                ("(=) Producción terminada disponible", res["produccion_terminada_disponible"], "total"),
                ("(-) Inventario final de prod. terminada", res["inventario_final_terminada"], "resta"),
                ("(=) COSTO DE LO VENDIDO", res["costo_de_lo_vendido"], "total")
            ]
            
            for concepto, monto, tag in formato:
                self.tree_costos.insert("", "end", values=(concepto, f"$ {monto:,.2f}"), tags=(tag,))
                
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos en los inventarios.")

    # ==========================================
    # PESTAÑA 2: ESTADO DE RESULTADOS
    # ==========================================
    def setup_tab_resultados(self):
        # --- Zona de Inputs ---
        frame_inputs = ctk.CTkFrame(self.tab_resultados)
        frame_inputs.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Datos de Operación", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=5, pady=(10, 5))
        
        ctk.CTkLabel(frame_inputs, text="Ventas Netas:").grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.ent_ventas = ctk.CTkEntry(frame_inputs, width=150)
        self.ent_ventas.grid(row=1, column=1, padx=5, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Gastos de Operación (Ventas + Admin):").grid(row=1, column=2, padx=5, pady=10, sticky="e")
        self.ent_gastos = ctk.CTkEntry(frame_inputs, width=150)
        self.ent_gastos.grid(row=1, column=3, padx=5, pady=10)
        
        btn_generar_res = ctk.CTkButton(frame_inputs, text="Generar Estado de Resultados", fg_color="#1f538d", hover_color="#14375e", command=self.ejecutar_estado_resultados)
        btn_generar_res.grid(row=1, column=4, padx=20, pady=10)

        # --- Zona de Visualización (Cédula) ---
        columnas = ("Concepto", "Monto")
        self.tree_resultados = ttk.Treeview(self.tab_resultados, columns=columnas, show="headings", selectmode="none")
        self.tree_resultados.heading("Concepto", text="Concepto")
        self.tree_resultados.heading("Monto", text="Monto ($)")
        self.tree_resultados.column("Concepto", width=400, anchor="w")
        self.tree_resultados.column("Monto", width=150, anchor="center")
        self.tree_resultados.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree_resultados.tag_configure("total", background="#14375e", foreground="white")
        self.tree_resultados.tag_configure("resta", foreground="#ff4d4d") #vemos si se edita o no

    def ejecutar_estado_resultados(self):
        #if self.costo_vendido_actual == 0.0:
        #   messagebox.showwarning("Aviso", "Es recomendable generar primero el Estado de Costos para obtener el Costo de lo Vendido real.")
            
        try:
            ventas = float(self.ent_ventas.get() or 0)
            gastos = float(self.ent_gastos.get() or 0)
            
            res = logica_estados.generar_estado_resultados(ventas, self.costo_vendido_actual, gastos)
            
            # Limpiar tabla
            for item in self.tree_resultados.get_children(): self.tree_resultados.delete(item)
            
            # Insertar filas
            formato = [
                ("Ventas Netas", res["ventas_totales"], ""),
                ("(-) Costo de lo vendido", res["costo_de_lo_vendido"], "resta"),
                ("(=) Utilidad Bruta", res["utilidad_bruta"], "total"),
                ("(-) Gastos de Operación", res["gastos_operacion"], "resta"),
                ("(=) Utilidad Antes de Impuestos", res["utilidad_neta_operacion"], "total")
            ]
            
            for concepto, monto, tag in formato:
                self.tree_resultados.insert("", "end", values=(concepto, f"$ {monto:,.2f}"), tags=(tag,))
                
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos en ventas y gastos.")