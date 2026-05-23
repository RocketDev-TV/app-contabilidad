# src/logic/almacen.py

# Esta lista va a actuar como si fuera una "base de datos" en memoria durante la ejecución.
# Aquí se irán guardando todos los renglones de la tarjeta de almacén.
historial_almacen = []

def inicializar_almacen():
    """
    Limpia el historial. Útil cuando la profa quiera iniciar un ejercicio nuevo
    sin reiniciar la aplicación completa.
    """
    global historial_almacen
    historial_almacen = []

def registrar_movimiento(concepto, cantidad, costo_unitario=0.0):
    """
    Cada vez que el usuario use tus inputs (Concepto, Cantidad, Costo) y le dé al botón
    de 'Registrar', debes mandar llamar esta función pasándole esos datos.
    
    Argumentos:
        concepto (str): 'Apertura', 'Compra', o 'Producción' (Salida)
        cantidad (int): Cuántas piezas entran o salen
        costo_unitario (float): El costo por pieza (solo obligatorio en Apertura y Compras)
    
    Devuelve:
        dict: Un diccionario con el estado actual del Almacén (inventario final y el historial listo para tu tabla).
    """
    global historial_almacen

    # 1. Recuperamos los valores del último renglón para poder hacer las fórmulas acumulativas
    if len(historial_almacen) == 0:
        existencia_anterior = 0
        saldo_anterior = 0.0
        costo_promedio_anterior = 0.0
    else:
        ultimo_renglon = historial_almacen[-1]
        existencia_anterior = ultimo_renglon["existencia"]
        saldo_anterior = ultimo_renglon["saldo"]
        costo_promedio_anterior = ultimo_renglon["costo_promedio"]

    # 2. Inicializamos las variables del renglón actual
    entrada = 0
    salida = 0
    debe = 0.0
    haber = 0.0

    # 3. Lógica contable según el tipo de movimiento
    concepto_lower = concepto.lower()
    
    if "apertura" in concepto_lower or "compra" in concepto_lower:
        # ENTRADAS: Aumenta la existencia y el dinero (Debe)
        entrada = cantidad
        existencia_actual = existencia_anterior + entrada
        debe = cantidad * costo_unitario
        saldo_actual = saldo_anterior + debe
        
        # FÓRMULA CLAVE: El costo promedio cambia solo cuando compramos más mercancía
        costo_promedio_actual = round(saldo_actual / existencia_actual, 2) if existencia_actual > 0 else 0.0

    elif "produccion" in concepto_lower or "salida" in concepto_lower:
        # SALIDAS: Disminuye la existencia. El costo se toma del último promedio calculado.
        salida = cantidad
        existencia_actual = existencia_anterior - salida
        
        # Se valúa al costo promedio que teníamos guardado del renglón anterior
        costo_unitario = costo_promedio_anterior 
        haber = cantidad * costo_unitario
        saldo_actual = saldo_anterior - haber
        
        # En las salidas, el costo promedio se mantiene exactamente igual
        costo_promedio_actual = costo_promedio_anterior
    else:
        # Por si acaso mandan un concepto no válido
        raise ValueError("Concepto no reconocido. Usa: 'Apertura', 'Compra' o 'Producción'.")

    # 4. Creamos el objeto del renglón con los datos finales formateados
    renglon = {
        "concepto": concepto,
        "entrada": entrada,
        "salida": salida,
        "existencia": existencia_actual,
        "costo_unitario": round(costo_unitario, 2),
        "costo_promedio": round(costo_promedio_actual, 2),
        "debe": round(debe, 2),
        "haber": round(haber, 2),
        "saldo": round(saldo_actual, 2)
    }

    # Guardamos el renglón en nuestro histórico
    historial_almacen.append(renglon)

    # 5. Retornamos la respuesta estructurada para que Andy la consuma
    return obtener_resumen_almacen()


def obtener_resumen_almacen():
    """
    Andy, usa esto para actualizar tu pantalla en cualquier momento. Te regresa la lista 
    completa de filas para tu tabla y los totales que ocuparemos en los estados financieros finales.
    """
    global historial_almacen
    
    if not historial_almacen:
        return {"materia_prima_utilizada": 0.0, "inventario_final": 0.0, "filas": []}
    
    # El inventario final en dinero es el 'saldo' del último movimiento registrado
    inventario_final_dinero = historial_almacen[-1]["saldo"]
    
    # La materia prima utilizada es la SUMA de todo lo que salió al Haber (para las órdenes de producción)
    mp_utilizada = sum(row["haber"] for row in historial_almacen if row["salida"] > 0)

    return {
        "materia_prima_utilizada": round(mp_utilizada, 2),
        "inventario_final": round(inventario_final_dinero, 2),
        "filas": historial_almacen #Itera sobre esta lista para pintar los labels en tu CTkScrollableFrame
    }