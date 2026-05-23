# src/main.py
import sys
import os

# =====================================================================
# CONFIGURACIÓN DE RUTAS (PATH TRICK)
# =====================================================================
# Este truco le permite a Python encontrar la carpeta 'src' y sus módulos
# sin importar desde qué directorio lances la terminal. ¡Indispensable en Linux!
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from gui.ventanas import VentanaPrincipal


# =====================================================================
# PUNTO DE ENTRADA PRINCIPAL DEL SOFTWARE
# =====================================================================
if __name__ == "__main__":
    print("[SISTEMA] Arrancando entorno gráfico con CustomTkinter...")

    # 1. Configuración del estilo visual (Se adapta al OS de la profa)
    ctk.set_appearance_mode("System")  # Detecta si Windows/Linux está en modo oscuro o claro
    ctk.set_default_color_theme("blue") # Color base para los botones y elementos activos

    # 2. Inicialización de la GUI
    # aqui se construye la ventana que programaste en 'gui/ventanas.py'
    app = VentanaPrincipal()
    
    # 3. El loop infinito que mantiene la aplicación abierta y escuchando clics
    app.mainloop()


# =====================================================================
# MÓDULO DE PRUEBAS DE LOGICA EN CONSOLA (OPCIONAL)
# =====================================================================
# si quieres ver cómo funcionan las matemáticas del backend en la terminal
# sin abrir las ventanas, haz lo siguiente:
#   1. Comenta las líneas de arriba (desde 'app = VentanaPrincipal()' hasta 'app.mainloop()')
#   2. Descomenta la línea de aquí abajo 'probar_backend_en_consola()' y ejecuta el archivo.
# =====================================================================

def probar_backend_en_consola():
    """
    Ejecuta un flujo simulado de contabilidad (Almacén -> Nómina -> Prorrateos -> Cédulas).
    Sirve para validar que los números cuadren antes de meterlos a la GUI.
    """
    from logic.almacen import inicializar_almacen, registrar_movimiento
    from logic.nomina import inicializar_nomina, registrar_mano_de_obra
    from logic.prorrateo import inicializar_prorrateos, calcular_prorrateo_primario, calcular_prorrateo_secundario, calcular_prorrateo_final
    from logic.estados import generar_estado_costos, generar_estado_resultados

    inicializar_almacen()
    inicializar_nomina()
    inicializar_prorrateos()

    # Simulación rápida
    registrar_movimiento("Inventario Apertura", 100, 10.0)
    registrar_movimiento("Compra de Material", 50, 15.0)
    registrar_movimiento("Salida a Producción", 80)
    registrar_mano_de_obra("101", 40, 50.0)
    registrar_mano_de_obra("102", 25, 45.0)
    
    calcular_prorrateo_primario({"Renta": 15000.0}, {"Renta": {"Prod_Taller": 100, "Prod_Pintura": 50, "Serv_Mantenimiento": 50}})
    calcular_prorrateo_secundario(["Serv_Mantenimiento"], {"Serv_Mantenimiento": {"Prod_Taller": 70, "Prod_Pintura": 30}})
    calcular_prorrateo_final({"Prod_Taller": {"101": 60, "102": 40}, "Prod_Pintura": {"101": 10, "102": 10}})

    print("\n--- TEST: ESTADO DE COSTOS (FORMATO PROFA) ---")
    for k, v in generar_estado_costos().items():
        print(f"{k:>35}: $ {v:.2f}")

# Para activar el test, quita el '#' de la línea de abajo:
# probar_backend_en_consola()