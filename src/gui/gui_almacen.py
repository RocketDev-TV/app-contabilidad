import customtkinter as ctk
from tkinter import ttk, messagebox
from logic.almacen import registrar_movimiento, obtener_resumen_almacen

class TabAlmacen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # =========================================================
        # FRAME SUPERIOR: Controles de Entrada (Inputs)
        # =========================================================
        frame_inputs = ctk.CTkFrame(self)
        frame_inputs.pack(padx=10, pady=10, fill="x")
        frame_inputs.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        ctk.CTkLabel(frame_inputs, text="Concepto:", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=5, pady=15, sticky="e")
        self.combo_concepto = ctk.CTkOptionMenu(frame_inputs, values=["Apertura", "Compra", "Salida"])
        self.combo_concepto.grid(row=0, column=1, padx=5, pady=15, sticky="w")

        ctk.CTkLabel(frame_inputs, text="Cantidad:", font=("Arial", 13, "bold")).grid(row=0, column=2, padx=5, pady=15, sticky="e")
        self.entry_cantidad = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 100", width=100)
        self.entry_cantidad.grid(row=0, column=3, padx=5, pady=15, sticky="w")

        ctk.CTkLabel(frame_inputs, text="Costo Unitario:", font=("Arial", 13, "bold")).grid(row=0, column=4, padx=5, pady=15, sticky="e")
        self.entry_costo = ctk.CTkEntry(frame_inputs, placeholder_text="Ej. 15.50", width=100)
        self.entry_costo.grid(row=0, column=5, padx=5, pady=15, sticky="w")

        btn_registrar = ctk.CTkButton(frame_inputs, text="Registrar", fg_color="#1f538d", hover_color="#14375e", command=self.procesar_movimiento)
        btn_registrar.grid(row=0, column=6, padx=15, pady=15)

        # =========================================================
        # FRAME CENTRAL: Tabla (Tarjeta de Almacén)
        # =========================================================
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.pack(padx=10, pady=5, fill="both", expand=True)

        # Estilo del Treeview para que coincida con CustomTkinter
        style = ttk.Style()
        style.theme_use("default")
        bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#e0e0e0"
        fg_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        
        style.configure("Treeview", background=bg_color, foreground=fg_color, rowheight=30, fieldbackground=bg_color, borderwidth=0, font=("Arial", 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#1f538d", foreground="white", relief="flat", font=("Arial", 12, "bold"))
        style.map("Treeview.Heading", background=[('active', '#14375e')])

        # Columnas solicitadas
        columnas = ("Concepto", "Entradas", "Salidas", "Existencia", "Costo Prom.", "Debe", "Haber", "Saldo")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        anchos = {"Concepto": 140, "Entradas": 80, "Salidas": 80, "Existencia": 90, 
                  "Costo Prom.": 100, "Debe": 100, "Haber": 100, "Saldo": 110}
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=anchos[col], anchor="center")

        self.tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=10)

        # =========================================================
        # FRAME INFERIOR: Outputs (Labels de Resumen)
        # =========================================================
        frame_resumen = ctk.CTkFrame(self, fg_color="transparent")
        frame_resumen.pack(padx=10, pady=10, fill="x")
        
        self.lbl_mp_utilizada = ctk.CTkLabel(frame_resumen, text="Materia Prima Utilizada: $ 0.00", font=("Arial", 16, "bold"), text_color="#3A7EBF")
        self.lbl_mp_utilizada.pack(side="left", padx=20)

        self.lbl_inv_final = ctk.CTkLabel(frame_resumen, text="Inventario Final: $ 0.00", font=("Arial", 16, "bold"), text_color="#3A7EBF")
        self.lbl_inv_final.pack(side="right", padx=20)

        # Inicializar datos
        self.actualizar_vista()

    def procesar_movimiento(self):
        concepto_raw = self.combo_concepto.get()
        concepto = "Producción" if "Producción" in concepto_raw else concepto_raw

        try:
            cantidad_texto = self.entry_cantidad.get()
            if not cantidad_texto:
                raise ValueError("El campo 'Cantidad' está vacío.")
            
            cantidad = int(cantidad_texto)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            costo_texto = self.entry_costo.get()
            costo_unitario = float(costo_texto) if costo_texto else 0.0

            if concepto in ["Apertura", "Compra"] and costo_unitario <= 0:
                messagebox.showwarning("Faltan datos", "Para Apertura o Compra debes ingresar el Costo Unitario.")
                return

        except ValueError as e:
            messagebox.showerror("Error", f"Verifica los datos:\n{str(e)}")
            return

        try:
            registrar_movimiento(concepto, cantidad, costo_unitario)
            self.actualizar_vista()
            
            self.entry_cantidad.delete(0, 'end')
            self.entry_costo.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_vista(self):
        # 1. Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # 2. Obtener datos de la lógica
        resumen = obtener_resumen_almacen()
        
        # 3. Llenar tabla
        for f in resumen.get("filas", []):
            valores = (
                f["concepto"],
                f["entrada"] if f["entrada"] > 0 else "-",
                f["salida"] if f["salida"] > 0 else "-",
                f["existencia"],
                f"$ {f['costo_promedio']:,.2f}",
                f"$ {f['debe']:,.2f}" if f["debe"] > 0 else "-",
                f"$ {f['haber']:,.2f}" if f["haber"] > 0 else "-",
                f"$ {f['saldo']:,.2f}"
            )
            self.tabla.insert("", "end", values=valores)
            
        # 4. Actualizar Labels de resumen
        mp_val = resumen.get("materia_prima_utilizada", 0.0)
        inv_val = resumen.get("inventario_final", 0.0)
        
        self.lbl_mp_utilizada.configure(text=f"Materia Prima Utilizada: $ {mp_val:,.2f}")
        self.lbl_inv_final.configure(text=f"Inventario Final: $ {inv_val:,.2f}")

#CTkComboBox