# src/logic/nomina.py

# Diccionario en memoria que actuará como base de datos para la nómina asignada.
# La estructura clave será: { "Num_Orden": costo_total_acumulado_de_mano_de_obra }
nomina_por_orden = {}

def inicializar_nomina():
    """
    Limpia los registros de mano de obra para iniciar un nuevo ejercicio.
    """
    global nomina_por_orden
    nomina_por_orden = {}

def registrar_mano_de_obra(no_orden, horas_trabajadas, cuota_por_hora):
    """
    en la pestaña de Nómina vas a ocupar inputs para el número de Orden (ej. 101),
    las Horas que se trabajaron en esa orden y cuánto se paga la hora. 
    Al dar clic en 'Asignar a Orden', invocas esta función.
    
    Argumentos:
        no_orden (str/int): Identificador de la orden (ej. "Orden 101" o 101)
        horas_trabajadas (float): Cantidad de horas dedicadas
        cuota_por_hora (float): El costo monetario de cada hora de trabajo
        
    Devuelve:
        dict: El estado resumido de la distribución de mano de obra actual.
    """
    global nomina_por_orden

    # Aseguramos que el ID de la orden se maneje limpio como string
    orden_key = str(no_orden)

    # FÓRMULA: Costo de Mano de Obra Directa (MOD) para esta asignación
    costo_mod = float(horas_trabajadas) * float(cuota_por_hora)

    # Si la orden ya tenía mano de obra registrada antes, le sumamos lo nuevo; si no, la creamos
    if orden_key in nomina_por_orden:
        nomina_por_orden[orden_key] += costo_mod
    else:
        nomina_por_orden[orden_key] = costo_mod

    return obtener_resumen_nomina()

def obtener_resumen_nomina():
    """
    Manda llamar esto para actualizar las etiquetas de totales en tu GUI 
    o para pintar el desglose de cuánta lana se ha gastado de mano de obra por cada orden.
    """
    global nomina_por_orden

    # Sumamos el costo de todas las órdenes para sacar el gran total de la nómina fabril
    total_nomina_directa = sum(nomina_por_orden.values())

    return {
        "total_mano_obra_directa": round(total_nomina_directa, 2),
        "desglose_por_orden": {k: round(v, 2) for k, v in nomina_por_orden.items()}
        # el 'desglose_por_orden' es un diccionario listo para que lo recorras 
        # con un ciclo .items() y pintes qué orden lleva cuánta lana acumulada.
    }