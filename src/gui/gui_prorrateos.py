import customtkinter as ctk
from tkinter import ttk, messagebox
from logic.prorrateo import (
    calcular_prorrateo_primario,
    calcular_prorrateo_secundario,
    calcular_prorrateo_final,
    resultados_primario,
    resultados_secundario
)

class TabProrrateos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # =========================================================
        # SUB-PESTAÑAS
        # =========================================================
        self.sub_tabs = ctk.CTkTabview(self)
        self.sub_tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_prim = self.sub_tabs.add("Prorrateo Primario")
        self.tab_sec = self.sub_tabs.add("Prorrateo Secundario")
        self.tab_fin = self.sub_tabs.add("Prorrateo Final")

        # Nomenclatura estándar universal
        self.gastos_nombres = ["MOI", "Mantenimiento", "Depreciacion", "Miscelaneos"]
        self.deps_servicio = ["Almacen M.P.", "Serv. Generales"]
        self.deps_productivos = ["Proceso 1", "Proceso 2"]
        self.todos_deps = self.deps_servicio + self.deps_productivos
        self.ordenes = ["Orden 1", "Orden 2", "Orden 3"]

        self.configurar_estilo_tablas()

        self.setup_primario()
        self.setup_secundario()
        self.setup_final()

    def configurar_estilo_tablas(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        bg_color = "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#e0e0e0"
        fg_color = "white" if ctk.get_appearance_mode() == "Dark" else "black"
        
        self.style.configure("Treeview", background=bg_color, foreground=fg_color, rowheight=30, fieldbackground=bg_color, borderwidth=0, font=("Arial", 11))
        self.style.map('Treeview', background=[('selected', '#1f538d')])
        self.style.configure("Treeview.Heading", background="#1f538d", foreground="white", relief="flat", font=("Arial", 12, "bold"))

    # ---------------------------------------------------------
    # 1. PRORRATEO PRIMARIO (Matriz Invertida e Intuitiva)
    # ---------------------------------------------------------
    def setup_primario(self):
        scroll_frame = ctk.CTkScrollableFrame(self.tab_prim)
        scroll_frame.pack(fill="both", expand=True)

        # --- SECCIÓN 1: GASTOS GLOBALES ---
        ctk.CTkLabel(scroll_frame, text="1. Gastos Globales a Prorratear", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=5, pady=(5, 5))
        
        self.entries_gastos = {}
        for i, nombre in enumerate(self.gastos_nombres):
            ctk.CTkLabel(scroll_frame, text=nombre, font=("Arial", 11, "bold")).grid(row=1, column=i+1, padx=5)
            ent = ctk.CTkEntry(scroll_frame, width=95)
            ent.insert(0, "0")
            ent.grid(row=2, column=i+1, padx=5, pady=5)
            self.entries_gastos[nombre] = ent

        # --- SECCIÓN 2: BASES DE DISTRIBUCIÓN INVERTIDAS ---
        ctk.CTkLabel(scroll_frame, text="2. Cédula de Bases (Gastos en Filas vs Departamentos en Columnas)", font=("Arial", 14, "bold")).grid(row=3, column=0, columnspan=5, pady=(20, 10))
        
        # Etiquetas de Columnas (Departamentos)
        ctk.CTkLabel(scroll_frame, text="CONCEPTO / GASTO", font=("Arial", 11, "italic")).grid(row=4, column=0, padx=10, sticky="w")
        for col_idx, dep in enumerate(self.todos_deps, start=1):
            ctk.CTkLabel(scroll_frame, text=dep, font=("Arial", 11, "bold")).grid(row=4, column=col_idx, padx=10, pady=5)

        # Diccionario para almacenar los entries indexados por [gasto][dep] de manera natural
        self.entries_bases_prim = {gasto: {} for gasto in self.gastos_nombres}

        # Generar Filas (Gastos) y Columnas (Departamentos)
        for row_idx, gasto in enumerate(self.gastos_nombres, start=5):
            # Etiqueta de la Fila (Nombre del Gasto)
            ctk.CTkLabel(scroll_frame, text=gasto, font=("Arial", 12, "bold")).grid(row=row_idx, column=0, sticky="w", padx=10, pady=5)
            
            for col_idx, dep in enumerate(self.todos_deps, start=1):
                ent = ctk.CTkEntry(scroll_frame, width=100)
                ent.insert(0, "0")
                ent.grid(row=row_idx, column=col_idx, padx=6, pady=4)
                self.entries_bases_prim[gasto][dep] = ent

        # Botón Calcular
        btn_calc = ctk.CTkButton(scroll_frame, text="Calcular Primario", command=self.ejecutar_primario, height=35)
        btn_calc.grid(row=10, column=0, columnspan=5, pady=20)

        # --- TABLA DE RESULTADOS DE SALIDA ---
        columnas = ("Concepto",) + tuple(self.todos_deps) + ("Total",)
        self.tabla_prim = ttk.Treeview(scroll_frame, columns=columnas, show="headings", height=6)
        for col in columnas:
            self.tabla_prim.heading(col, text=col)
            self.tabla_prim.column(col, anchor="center", width=115)
        self.tabla_prim.grid(row=11, column=0, columnspan=5, pady=10, sticky="nsew")

    def ejecutar_primario(self):
        try:
            # 1. Recolectar gastos de la parte superior
            gastos = {nombre: float(ent.get()) for nombre, ent in self.entries_gastos.items()}
            
            # 2. Recolectar las bases directamente desde la estructura limpia [gasto][dep]
            bases = {gasto: {} for gasto in self.gastos_nombres}
            for gasto in self.gastos_nombres:
                for dep in self.todos_deps:
                    bases[gasto][dep] = float(self.entries_bases_prim[gasto][dep].get())
            
            # 3. Limpiar estado interno lógico
            from logic.prorrateo import inicializar_prorrateos
            inicializar_prorrateos()
            
            # 4. Procesar cálculo
            res = calcular_prorrateo_primario(gastos, bases)
            
            # 5. Limpieza dinámica del Treeview
            for item in self.tabla_prim.get_children(): 
                self.tabla_prim.delete(item)
            
            # 6. Renderizar filas calculadas
            for gasto, datos in res["desglose_por_gasto"].items():
                dist = datos["distribucion"]
                fila = [gasto] + [f"$ {dist.get(dep, 0):,.2f}" for dep in self.todos_deps] + [f"$ {gastos[gasto]:,.2f}"]
                self.tabla_prim.insert("", "end", values=fila)
                
            # 7. Fila de Totales actualizada
            tots = res["totales_departamentos"]
            fila_tot = ["TOTALES"] + [f"$ {tots.get(dep, 0):,.2f}" for dep in self.todos_deps] + [f"$ {sum(gastos.values()):,.2f}"]
            self.tabla_prim.insert("", "end", values=fila_tot, tags=('total',))
            self.tabla_prim.tag_configure('total', background='#14375e', foreground='white')
            
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar únicamente valores numéricos en los campos de las bases.")

    # ---------------------------------------------------------
    # 2. PRORRATEO SECUNDARIO
    # ---------------------------------------------------------
    def setup_secundario(self):
        scroll_frame = ctk.CTkScrollableFrame(self.tab_sec)
        scroll_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll_frame, text="Bases de Redistribución (Cierre a Productivos)", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

        for col_idx, prod in enumerate(self.deps_productivos, start=1):
            ctk.CTkLabel(scroll_frame, text=f"Base a {prod}", font=("Arial", 11, "bold")).grid(row=1, column=col_idx)

        self.entries_bases_sec = {serv: {} for serv in self.deps_servicio}

        for row_idx, serv in enumerate(self.deps_servicio, start=2):
            ctk.CTkLabel(scroll_frame, text=f"Desde {serv}:", font=("Arial", 12, "bold")).grid(row=row_idx, column=0, sticky="e", padx=10)
            for col_idx, prod in enumerate(self.deps_productivos, start=1):
                ent = ctk.CTkEntry(scroll_frame, width=95)
                ent.insert(0, "0")
                ent.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                self.entries_bases_sec[serv][prod] = ent

        btn_calc = ctk.CTkButton(scroll_frame, text="Ejecutar Cierre", command=self.ejecutar_secundario)
        btn_calc.grid(row=4, column=0, columnspan=3, pady=15)

        columnas = ("Departamento", "Monto a Repartir") + tuple(self.deps_productivos) + ("Saldo Final",)
        self.tabla_sec = ttk.Treeview(scroll_frame, columns=columnas, show="headings", height=4)
        for col in columnas:
            self.tabla_sec.heading(col, text=col)
            self.tabla_sec.column(col, anchor="center")
        self.tabla_sec.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

    def ejecutar_secundario(self):
        import logic.prorrateo as logica

        if not logica.resultados_primario:
            messagebox.showwarning("Aviso", "Primero debes calcular el Prorrateo Primario.")
            return
            
        try:
            bases_redist = {}
            for serv, prod_dict in self.entries_bases_sec.items():
                bases_redist[serv] = {prod: float(ent.get()) for prod, ent in prod_dict.items()}
            
            saldos_iniciales = logica.resultados_primario.copy()
            res = calcular_prorrateo_secundario(self.deps_servicio, bases_redist)
            
            for item in self.tabla_sec.get_children(): self.tabla_sec.delete(item)
            
            for serv in self.deps_servicio:
                monto_a_repartir = saldos_iniciales.get(serv, 0)
                base_reparto = bases_redist.get(serv, {})
                suma_base = sum(base_reparto.values())
                
                factor = monto_a_repartir / suma_base if suma_base > 0 else 0.0
                
                valores_productivos = []
                for prod in self.deps_productivos:
                    asignado = base_reparto.get(prod, 0) * factor
                    valores_productivos.append(f"$ {asignado:,.2f}")
                
                fila = [serv, f"$ {monto_a_repartir:,.2f}"] + valores_productivos + ["$ 0.00"]
                self.tabla_sec.insert("", "end", values=fila)
                
            fila_tot = ["NUEVOS SALDOS PRODUCTIVOS", "-"] + [f"$ {res.get(prod, 0):,.2f}" for prod in self.deps_productivos] + ["-"]
            self.tabla_sec.insert("", "end", values=fila_tot, tags=('total',))
            self.tabla_sec.tag_configure('total', background='#14375e', foreground='white')
            
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar valores numéricos en las bases.")
        import logic.prorrateo as logica

        print(logica.resultados_primario)

        if not resultados_primario:
            messagebox.showwarning("Aviso", "Primero debes calcular el Prorrateo Primario.")
            return
            
        try:
            bases_redist = {}
            for serv, prod_dict in self.entries_bases_sec.items():
                bases_redist[serv] = {prod: float(ent.get()) for prod, ent in prod_dict.items()}
            
            saldos_iniciales = resultados_primario.copy()
            res = calcular_prorrateo_secundario(self.deps_servicio, bases_redist)
            
            for item in self.tabla_sec.get_children(): self.tabla_sec.delete(item)
            
            for serv in self.deps_servicio:
                monto_a_repartir = saldos_iniciales.get(serv, 0)
                base_reparto = bases_redist.get(serv, {})
                suma_base = sum(base_reparto.values())
                
                factor = monto_a_repartir / suma_base if suma_base > 0 else 0.0
                
                valores_productivos = []
                for prod in self.deps_productivos:
                    asignado = base_reparto.get(prod, 0) * factor
                    valores_productivos.append(f"$ {asignado:,.2f}")
                
                fila = [serv, f"$ {monto_a_repartir:,.2f}"] + valores_productivos + ["$ 0.00"]
                self.tabla_sec.insert("", "end", values=fila)
                
            fila_tot = ["NUEVOS SALDOS PRODUCTIVOS", "-"] + [f"$ {res.get(prod, 0):,.2f}" for prod in self.deps_productivos] + ["-"]
            self.tabla_sec.insert("", "end", values=fila_tot, tags=('total',))
            self.tabla_sec.tag_configure('total', background='#14375e', foreground='white')
            
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar valores numéricos en las bases.")

    # ---------------------------------------------------------
    # 3. PRORRATEO FINAL
    # ---------------------------------------------------------
    def setup_final(self):
        scroll_frame = ctk.CTkScrollableFrame(self.tab_fin)
        scroll_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll_frame, text="Bases de Aplicación a Órdenes/Lotes", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        for col_idx, ord_nom in enumerate(self.ordenes, start=1):
            ctk.CTkLabel(scroll_frame, text=ord_nom, font=("Arial", 11, "bold")).grid(row=1, column=col_idx)

        self.entries_bases_fin = {prod: {} for prod in self.deps_productivos}

        for row_idx, prod in enumerate(self.deps_productivos, start=2):
            ctk.CTkLabel(scroll_frame, text=f"Base de {prod}:", font=("Arial", 12, "bold")).grid(row=row_idx, column=0, sticky="e", padx=10)
            for col_idx, ord_nom in enumerate(self.ordenes, start=1):
                ent = ctk.CTkEntry(scroll_frame, width=95)
                ent.insert(0, "0")
                ent.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                self.entries_bases_fin[prod][ord_nom] = ent

        btn_calc = ctk.CTkButton(scroll_frame, text="Aplicar a Órdenes", command=self.ejecutar_final)
        btn_calc.grid(row=4, column=0, columnspan=4, pady=15)

        columnas = ("Orden / Lote", "Cargo Indirecto Total Asignado")
        self.tabla_fin = ttk.Treeview(scroll_frame, columns=columnas, show="headings", height=4)
        for col in columnas:
            self.tabla_fin.heading(col, text=col)
            self.tabla_fin.column(col, anchor="center")
        self.tabla_fin.grid(row=5, column=0, columnspan=4, pady=10, sticky="nsew")

    def ejecutar_secundario(self):
        import logic.prorrateo as logica
        
        # Leemos directo del módulo global
        saldos_iniciales = logica.resultados_primario.copy()
        
        if not saldos_iniciales:
            messagebox.showwarning("Aviso", "Primero debes calcular el Prorrateo Primario.")
            return
            
        try:
            bases_redist = {}
            for serv, prod_dict in self.entries_bases_sec.items():
                bases_redist[serv] = {prod: float(ent.get()) for prod, ent in prod_dict.items()}
            
            res = calcular_prorrateo_secundario(self.deps_servicio, bases_redist)
            
            for item in self.tabla_sec.get_children(): self.tabla_sec.delete(item)
            
            for serv in self.deps_servicio:
                monto_a_repartir = saldos_iniciales.get(serv, 0)
                base_reparto = bases_redist.get(serv, {})
                suma_base = sum(base_reparto.values())
                
                factor = monto_a_repartir / suma_base if suma_base > 0 else 0.0
                
                valores_productivos = []
                for prod in self.deps_productivos:
                    asignado = base_reparto.get(prod, 0) * factor
                    valores_productivos.append(f"$ {asignado:,.2f}")
                
                fila = [serv, f"$ {monto_a_repartir:,.2f}"] + valores_productivos + ["$ 0.00"]
                self.tabla_sec.insert("", "end", values=fila)
                
            fila_tot = ["NUEVOS SALDOS PRODUCTIVOS", "-"] + [f"$ {res.get(prod, 0):,.2f}" for prod in self.deps_productivos] + ["-"]
            self.tabla_sec.insert("", "end", values=fila_tot, tags=('total',))
            self.tabla_sec.tag_configure('total', background='#14375e', foreground='white')
            
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar valores numéricos en las bases.")

    def ejecutar_final(self):
        import logic.prorrateo as logica
        
        saldos_secundarios = logica.resultados_secundario.copy()

        if not saldos_secundarios:
            messagebox.showwarning("Aviso", "Primero debes calcular el Prorrateo Secundario.")
            return

        try:
            base_ordenes = {}
            for prod, ord_dict in self.entries_bases_fin.items():
                base_ordenes[prod] = {ord_nom: float(ent.get()) for ord_nom, ent in ord_dict.items()}
            
            res = calcular_prorrateo_final(base_ordenes)
            
            for item in self.tabla_fin.get_children(): self.tabla_fin.delete(item)
            
            for lote, monto in res.items():
                self.tabla_fin.insert("", "end", values=(lote, f"$ {monto:,.2f}"))
                
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar valores numéricos en las bases finales.")
        import logic.prorrateo as logica

        if not logica.resultados_secundario:
            messagebox.showwarning("Aviso", "Primero debes calcular el Prorrateo Secundario.")
            return

        try:
            base_ordenes = {}
            for prod, ord_dict in self.entries_bases_fin.items():
                base_ordenes[prod] = {ord_nom: float(ent.get()) for ord_nom, ent in ord_dict.items()}
            
            res = calcular_prorrateo_final(base_ordenes)
            
            for item in self.tabla_fin.get_children(): self.tabla_fin.delete(item)
            
            for lote, monto in res.items():
                self.tabla_fin.insert("", "end", values=(lote, f"$ {monto:,.2f}"))
                
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar valores numéricos en las bases finales.")
        if not resultados_secundario:
            messagebox.showwarning("Aviso", "Primero debes calcular el Prorrateo Secundario.")
            return

        try:
            base_ordenes = {}
            for prod, ord_dict in self.entries_bases_fin.items():
                base_ordenes[prod] = {ord_nom: float(ent.get()) for ord_nom, ent in ord_dict.items()}
            
            res = calcular_prorrateo_final(base_ordenes)
            
            for item in self.tabla_fin.get_children(): self.tabla_fin.delete(item)
            
            for lote, monto in res.items():
                self.tabla_fin.insert("", "end", values=(lote, f"$ {monto:,.2f}"))
                
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar valores numéricos en las bases finales.")