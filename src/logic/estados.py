# src/logic/estados.py

from logic.almacen import obtener_resumen_almacen, historial_almacen
from logic.nomina import obtener_resumen_nomina
from logic.prorrateo import obtener_cargos_indirectos_orden

def generar_estado_costos():
    """
    esta función ya devuelve el formato EXACTO del PDF de estado de costos de erly.
    Sigue este orden de arriba hacia abajo para pintar la cédula en la GUI.
    """
    resumen_almacen = obtener_resumen_almacen()
    resumen_nomina = obtener_resumen_nomina()

    # --- ESCARBAMOS EN EL ALMACÉN PARA EL DESGLOSE DE MATERIA PRIMA ---
    # Inventario Inicial: Es el 'saldo' o 'debe' del primer movimiento (Apertura)
    if historial_almacen and "apertura" in historial_almacen[0]["concepto"].lower():
        inv_inicial_mp = historial_almacen[0]["debe"]
    else:
        inv_inicial_mp = 0.0

    # Compras Netas: Sumamos todo lo que entró al almacén que NO sea la apertura
    compras_netas_mp = sum(
        row["debe"] for row in historial_almacen 
        if "compra" in row["concepto"].lower()
    )

    # Materia Prima Disponible = Inicial + Compras
    mp_disponible = inv_inicial_mp + compras_netas_mp

    # Inventario Final de MP: Es el saldo final que quedó en la tarjeta de almacén
    inv_final_mp = resumen_almacen["inventario_final"]

    # Materia Prima Directa o Consumida = Disponible - Inventario Final
    # (Matemáticamente da igual al total de salidas al Haber que ya calculabas)
    mp_directa_consumida = resumen_almacen["materia_prima_utilizada"]


    # --- ELEMENTOS DIRECTOS E INDIRECTOS ---
    # Mano de Obra Directa
    mo_directa = resumen_nomina["total_mano_obra_directa"]

    # Cargos Indirectos (Suma del prorrateo final de todas las órdenes)
    desglose_ordenes = resumen_nomina["desglose_por_orden"]
    cargos_indirectos_totales = sum(
        obtener_cargos_indirectos_orden(orden) for orden in desglose_ordenes.keys()
    )


    # --- CÁLCULO DE COSTOS SECUENCIALES ---
    # Costo Incurrido = MP Consumida + MO Directa + Cargos Indirectos
    costo_incurrido = mp_directa_consumida + mo_directa + cargos_indirectos_totales

    # Inventarios de Producción en Proceso (Los dejamos en 0 de forma genérica o inputs vacíos si la no se da el dato)
    inv_inicial_proceso = 0.0
    total_procesado = costo_incurrido + inv_inicial_proceso
    inv_final_proceso = 0.0
    
    # Costo de la Producción Terminada
    costo_produccion_terminada = total_procesado - inv_final_proceso

    # Inventarios de Producción Terminada
    inv_inicial_terminada = 0.0
    produccion_terminada_disponible = costo_produccion_terminada + inv_inicial_terminada
    inv_final_terminada = 0.0

    # (=) Costo de lo vendido
    costo_de_lo_vendido = produccion_terminada_disponible - inv_final_terminada

    # Retornamos el diccionario mapeado uno a uno
    return {
        "inventario_inicial_mp": round(inv_inicial_mp, 2),
        "compras_netas_mp": round(compras_netas_mp, 2),
        "materia_prima_disponible": round(mp_disponible, 2),
        "inventario_final_mp": round(inv_final_mp, 2),
        "materia_prima_directa_consumida": round(mp_directa_consumida, 2),
        "mano_de_obra_directa": round(mo_directa, 2),
        "cargos_indirectos": round(cargos_indirectos_totales, 2),
        "costo_incurrido": round(costo_incurrido, 2),
        "inventario_inicial_proceso": round(inv_inicial_proceso, 2),
        "total_procesado": round(total_procesado, 2),
        "inventario_final_proceso": round(inv_final_proceso, 2),
        "costo_produccion_terminada": round(costo_produccion_terminada, 2),
        "inventario_inicial_terminada": round(inv_inicial_terminada, 2),
        "produccion_terminada_disponible": round(produccion_terminada_disponible, 2),
        "inventario_final_terminada": round(inv_final_terminada, 2),
        "costo_de_lo_vendido": round(costo_de_lo_vendido, 2)
    }

def generar_estado_resultados(ingresos_ventas, gastos_operacion=0.0):
    """
    Genera el Estado de Resultados final.
    
    Argumentos:
        ingresos_ventas (float): Cuánto dinero entró por vender los productos (Input de la GUI)
        gastos_operacion (float): Gastos de administración y venta (Opcional, default 0)
    """
    # Necesitamos el Costo de lo Vendido para poder restar
    estado_costos = generar_estado_costos()
    costo_de_lo_vendido = estado_costos["costo_de_lo_vendido"]

    # FÓRMULA: Utilidad Bruta = Ventas - Costo de lo Vendido
    utilidad_bruta = float(ingresos_ventas) - costo_de_lo_vendido

    # FÓRMULA: Utilidad de Operación = Utilidad Bruta - Gastos de Operación
    utilidad_operacion = utilidad_bruta - float(gastos_operacion)

    return {
        "ventas_totales": round(float(ingresos_ventas), 2),
        "costo_de_lo_vendido": round(costo_de_lo_vendido, 2),
        "utilidad_bruta": round(utilidad_bruta, 2),
        "gastos_operacion": round(float(gastos_operacion), 2),
        "utilidad_neta_operacion": round(utilidad_operacion, 2)
    }