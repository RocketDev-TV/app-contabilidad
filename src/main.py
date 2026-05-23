import sys
import os

# Truco de paths para que Python encuentre la carpeta 'src' sin importar desde dónde ejecutes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importamos la lógica de todos tus módulos
from logic.almacen import inicializar_almacen, registrar_movimiento
from logic.nomina import inicializar_nomina, registrar_mano_de_obra
from logic.prorrateo import (
    inicializar_prorrateos,
    calcular_prorrateo_primario,
    calcular_prorrateo_secundario,
    calcular_prorrateo_final
)
from logic.estados import generar_estado_costos, generar_estado_resultados

def correr_sistema_completo():
    print("==========================================================")
    # 1. REINICIAR BASES DE MEMORIA
    inicializar_almacen()
    inicializar_nomina()
    inicializar_prorrateos()

    # 2. SIMULACIÓN: TARJETA DE ALMACÉN (Precio Promedio)
    print("[1/4] Procesando Tarjeta de Almacén...")
    registrar_movimiento("Inventario Apertura", 100, 10.0) # 100 pzas a $10
    registrar_movimiento("Compra de Material", 50, 15.0)   # 50 pzas a $15 (Sube promedio a $11.67)
    registrar_movimiento("Salida a Producción", 80)        # Salen 80 pzas para las órdenes

    # 3. SIMULACIÓN: CÉDULA DE MANO DE OBRA (NÓMINA)
    print("[2/4] Procesando Cédula de Mano de Obra...")
    registrar_mano_de_obra("101", 40, 50.0)  # Orden 101: 40 horas a $50
    registrar_mano_de_obra("101", 10, 60.0)  # Orden 101: 10 horas a $60
    registrar_mano_de_obra("102", 25, 45.0)  # Orden 102: 25 horas a $45

    # 4. SIMULACIÓN: CARGOS INDIRECTOS (LOS TRES PRORRATEOS)
    print("[3/4] Ejecutando Direccionamiento de Prorrateos...")
    # -- Primario --
    gastos_globales = {"Renta del Edificio": 15000.0}
    bases_primario = {
        "Renta del Edificio": {"Prod_Taller": 100, "Prod_Pintura": 50, "Serv_Mantenimiento": 50}
    }
    calcular_prorrateo_primario(gastos_globales, bases_primario)

    # -- Secundario -- (Cerramos Mantenimiento mandando su lana a los productivos)
    bases_secundario = {
        "Serv_Mantenimiento": {"Prod_Taller": 70, "Prod_Pintura": 30}
    }
    calcular_prorrateo_secundario(["Serv_Mantenimiento"], bases_secundario)

    # -- Final -- (Asignamos el costo acumulado a las Órdenes 101 y 102)
    bases_final = {
        "Prod_Taller": {"101": 60, "102": 40},
        "Prod_Pintura": {"101": 10, "102": 10}
    }
    calcular_prorrateo_final(bases_final)

    # 5. GENERACIÓN DE ENTREGABLES FINALES (FORMATO DE LA PROFA)
    print("[4/4] Consolidando Estados Financieros...")
    print("==========================================================\n")
    
    # Sacamos el Estado de Costos
    cedula_costos = generar_estado_costos()
    
    # Sacamos el Estado de Resultados simulando que vendimos la producción en $25,000.00
    ingresos_ventas = 25000.00
    cedula_resultados = generar_estado_resultados(ingresos_ventas, gastos_operacion=1500.0)

    # --- PINTAMOS EL FORMATO DEL PDF ---
    print("CÍA. VALIDADORA DE COSTOS S.A.")
    print("ESTADO DE COSTO DE PRODUCCIÓN Y DE LO VENDIDO")
    print("----------------------------------------------------------")
    print(f"   Inventario inicial de materia prima:       $ {cedula_costos['inventario_inicial_mp']:>10.2f}")
    print(f"   + Compras netas de materia prima:          $ {cedula_costos['compras_netas_mp']:>10.2f}")
    print(f"   = Materia prima disponible:                $ {cedula_costos['materia_prima_disponible']:>10.2f}")
    print(f"   - Inventario final de materia prima:       $ {cedula_costos['inventario_final_mp']:>10.2f}")
    print(f"   = Materia prima directa o consumida:       $ {cedula_costos['materia_prima_directa_consumida']:>10.2f}")
    print(f"   + Mano de obra directa:                    $ {cedula_costos['mano_de_obra_directa']:>10.2f}")
    print(f"   + Cargos indirectos:                       $ {cedula_costos['cargos_indirectos']:>10.2f}")
    print(f"   = Costo incurrido:                         $ {cedula_costos['costo_incurrido']:>10.2f}")
    print(f"   + Inventario inicial de prod. en proceso:  $ {cedula_costos['inventario_inicial_proceso']:>10.2f}")
    print(f"   = Total procesado:                         $ {cedula_costos['total_processed'] if 'total_processed' in cedula_costos else cedula_costos['total_procesado']:>10.2f}")
    print(f"   - Inventario final de prod. en proceso:    $ {cedula_costos['inventario_final_proceso']:>10.2f}")
    print(f"   = Costo de la producción terminada:        $ {cedula_costos['costo_production_terminada'] if 'costo_production_terminada' in cedula_costos else cedula_costos['costo_produccion_terminada']:>10.2f}")
    print(f"   + Inventario inicial de prod. terminada:   $ {cedula_costos['inventario_inicial_terminada']:>10.2f}")
    print(f"   = Producción terminada disponible:         $ {cedula_costos['produccion_terminada_disponible']:>10.2f}")
    print(f"   - Inventario final de prod. terminada:     $ {cedula_costos['inventario_final_terminada']:>10.2f}")
    print(f"   = Costo de lo vendido:                     $ {cedula_costos['costo_de_lo_vendido']:>10.2f}")
    print("----------------------------------------------------------\n")

    print("ESTADO DE RESULTADOS")
    print("----------------------------------------------------------")
    print(f"   Ventas Totales:                            $ {cedula_resultados['ventas_totales']:>10.2f}")
    print(f"   (-) Costo de lo Vendido:                   $ {cedula_resultados['costo_de_lo_vendido']:>10.2f}")
    print(f"   (=) Utilidad Bruta:                        $ {cedula_resultados['utilidad_bruta']:>10.2f}")
    print(f"   (-) Gastos de Operación:                   $ {cedula_resultados['gastos_operation'] if 'gastos_operation' in cedula_resultados else cedula_resultados['gastos_operacion']:>10.2f}")
    print(f"   (=) Utilidad Neta de Operación:            $ {cedula_resultados['utilidad_neta_operacion']:>10.2f}")
    print("==========================================================")

if __name__ == "__main__":
    correr_sistema_completo()