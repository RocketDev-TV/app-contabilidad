import customtkinter as ctk
from tkinter import ttk, messagebox
import logic.nomina as logica_nomina

class TabNomina(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Iniciar la base de datos de nómina vacía
        logica_nomina.inicializar_nomina()
        
        # Aplicar el estilo de CustomTkinter a los Treeviews clásicos
        self.configurar_estilo_tablas()
        
        self.setup_ui()

    def configurar_estilo_tablas(self):
        """Aplica un tema oscuro/claro al Treeview para que coincida con CTk."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#e0e0e0"
        fg_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        
        self.style.configure("Treeview", background=bg_color, foreground=fg_color, rowheight=30, fieldbackground=bg_color, borderwidth=0, font=("Arial", 10))
        self.style.map('Treeview', background=[('selected', '#1f538d')])
        self.style.configure("Treeview.Heading", background="#1f538d", foreground="white", relief="flat", font=("Arial", 11, "bold"))
        self.style.map("Treeview.Heading", background=[('active', '#14375e')])

    def setup_ui(self):
        # ==========================================
        # ZONA SUPERIOR: CAPTURA DE DATOS
        # ==========================================
        frame_top = ctk.CTkFrame(self)
        frame_top.pack(fill="x", padx=10, pady=10)
        
        # --- Selector de Departamento ---
        frame_depto = ctk.CTkFrame(frame_top, fg_color="transparent")
        frame_depto.pack(fill="x", pady=(10, 5), padx=10)
        
        ctk.CTkLabel(frame_depto, text="Departamento / Área:", font=("Arial", 14, "bold")).pack(side="left", padx=(0, 10))
        self.combo_depto = ctk.CTkOptionMenu(frame_depto, values=["Ventas", "Admin", "MOD", "MOI"], width=200, fg_color="#1f538d", button_color="#14375e", button_hover_color="#0e2643")
        self.combo_depto.pack(side="left")

        # --- Contenedor divido para Percepciones y Deducciones ---
        frame_inputs = ctk.CTkFrame(frame_top, fg_color="transparent")
        frame_inputs.pack(fill="x", padx=10, pady=5)
        
        # Bloque Percepciones (Izquierda)
        frame_perc = ctk.CTkFrame(frame_inputs)
        frame_perc.pack(side="left", fill="both", expand=True, padx=(0, 5))
        ctk.CTkLabel(frame_perc, text="PERCEPCIONES", text_color="#28a745", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        ctk.CTkLabel(frame_perc, text="Normal:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_normal = ctk.CTkEntry(frame_perc, width=120)
        self.ent_normal.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frame_perc, text="Extra:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.ent_extra = ctk.CTkEntry(frame_perc, width=120)
        self.ent_extra.grid(row=2, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frame_perc, text="Otros:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.ent_otros_p = ctk.CTkEntry(frame_perc, width=120)
        self.ent_otros_p.grid(row=3, column=1, padx=5, pady=5)

        # Bloque Deducciones (Derecha)
        frame_deducc = ctk.CTkFrame(frame_inputs)
        frame_deducc.pack(side="left", fill="both", expand=True, padx=(5, 0))
        ctk.CTkLabel(frame_deducc, text="DEDUCCIONES", text_color="#dc3545", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        ctk.CTkLabel(frame_deducc, text="Retención:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_retencion = ctk.CTkEntry(frame_deducc, width=120)
        self.ent_retencion.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frame_deducc, text="Cuotas IMSS:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.ent_imss = ctk.CTkEntry(frame_deducc, width=120)
        self.ent_imss.grid(row=2, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frame_deducc, text="Otros:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.ent_otros_d = ctk.CTkEntry(frame_deducc, width=120)
        self.ent_otros_d.grid(row=3, column=1, padx=5, pady=5)

        # Botón de Registro
        btn_registrar = ctk.CTkButton(frame_top, text="Registrar / Actualizar Renglón", fg_color="#1f538d", hover_color="#14375e", command=self.registrar_datos)
        btn_registrar.pack(pady=10)

        # ==========================================
        # ZONA INFERIOR: VISUALIZACIÓN (CÉDULA)
        # ==========================================
        columnas = ("Depto", "Normal", "Extra", "Otros_P", "Total_P", "Retencion", "IMSS", "Otros_D", "Total_D", "Neto")
        
        # Usamos un Frame contenedor para poder ponerle scroll si la pantalla es pequeña
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="none")
        
        # Configurar encabezados (alineados a tu cuaderno)
        self.tree.heading("Depto", text="Departamento")
        self.tree.heading("Normal", text="Normal")
        self.tree.heading("Extra", text="Extra")
        self.tree.heading("Otros_P", text="Otros P.")
        self.tree.heading("Total_P", text="TOTAL PERC.")
        self.tree.heading("Retencion", text="Retención")
        self.tree.heading("IMSS", text="IMSS")
        self.tree.heading("Otros_D", text="Otros D.")
        self.tree.heading("Total_D", text="TOTAL DED.")
        self.tree.heading("Neto", text="NETO A PAGAR")
        
        # Configurar anchos
        self.tree.column("Depto", width=120, anchor="w")
        for col in columnas[1:]:
            self.tree.column(col, width=90, anchor="center")
            
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tag para la fila de Totales
        self.tree.tag_configure("total_row", background="#14375e", foreground="white", font=("Arial", 10, "bold"))

        # Dibujar la tabla vacía inicialmente
        self.actualizar_tabla()

    def registrar_datos(self):
        depto = self.combo_depto.get()
        
        try:
            # Leer valores, asumiendo 0.0 si está en blanco
            normal = float(self.ent_normal.get() or 0)
            extra = float(self.ent_extra.get() or 0)
            otros_p = float(self.ent_otros_p.get() or 0)
            
            retencion = float(self.ent_retencion.get() or 0)
            imss = float(self.ent_imss.get() or 0)
            otros_d = float(self.ent_otros_d.get() or 0)
            
            # Enviar a la lógica
            logica_nomina.registrar_renglon_nomina(depto, normal, extra, otros_p, retencion, imss, otros_d)
            
            # Limpiar campos después de registrar
            self.limpiar_inputs()
            
            # Refrescar la vista
            self.actualizar_tabla()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa únicamente valores numéricos.")

    def limpiar_inputs(self):
        self.ent_normal.delete(0, 'end')
        self.ent_extra.delete(0, 'end')
        self.ent_otros_p.delete(0, 'end')
        self.ent_retencion.delete(0, 'end')
        self.ent_imss.delete(0, 'end')
        self.ent_otros_d.delete(0, 'end')

    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        resumen = logica_nomina.obtener_resumen_nomina()
        nomina = resumen["nomina_completa"]
        
        # Variables para calcular los totales de la última fila
        totales = { "normal": 0, "extra": 0, "otros_p": 0, "tot_p": 0, 
                    "retencion": 0, "imss": 0, "otros_d": 0, "tot_d": 0, "neto": 0 }
        
        # Orden fijo de departamentos (como en tu cuaderno)
        orden_deptos = ["Ventas", "Admin", "MOD", "MOI"]
        
        for depto in orden_deptos:
            if depto in nomina:
                datos = nomina[depto]
                
                # Sumar a totales
                totales["normal"] += datos["normal"]
                totales["extra"] += datos["extra"]
                totales["otros_p"] += datos["otros_perc"]
                totales["tot_p"] += datos["total_percepciones"]
                totales["retencion"] += datos["retencion"]
                totales["imss"] += datos["imss"]
                totales["otros_d"] += datos["otros_ded"]
                totales["tot_d"] += datos["total_deducciones"]
                totales["neto"] += datos["neto_a_pagar"]
                
                # Insertar fila
                self.tree.insert("", "end", values=(
                    f"Depto. {depto}" if depto in ["Ventas", "Admin"] else depto,
                    f"$ {datos['normal']:,.2f}",
                    f"$ {datos['extra']:,.2f}",
                    f"$ {datos['otros_perc']:,.2f}",
                    f"$ {datos['total_percepciones']:,.2f}",
                    f"$ {datos['retencion']:,.2f}",
                    f"$ {datos['imss']:,.2f}",
                    f"$ {datos['otros_ded']:,.2f}",
                    f"$ {datos['total_deducciones']:,.2f}",
                    f"$ {datos['neto_a_pagar']:,.2f}"
                ))
            else:
                # Si no hay datos registrados aún, mostrar fila en ceros
                self.tree.insert("", "end", values=(
                    f"Depto. {depto}" if depto in ["Ventas", "Admin"] else depto,
                    "$ 0.00", "$ 0.00", "$ 0.00", "$ 0.00", 
                    "$ 0.00", "$ 0.00", "$ 0.00", "$ 0.00", "$ 0.00"
                ))
        
        # Insertar fila de TOTALES al final
        self.tree.insert("", "end", values=(
            "TOTALES",
            f"$ {totales['normal']:,.2f}",
            f"$ {totales['extra']:,.2f}",
            f"$ {totales['otros_p']:,.2f}",
            f"$ {totales['tot_p']:,.2f}",
            f"$ {totales['retencion']:,.2f}",
            f"$ {totales['imss']:,.2f}",
            f"$ {totales['otros_d']:,.2f}",
            f"$ {totales['tot_d']:,.2f}",
            f"$ {totales['neto']:,.2f}"
        ), tags=("total_row",))