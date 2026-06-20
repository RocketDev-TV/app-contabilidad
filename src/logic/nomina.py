# src/logic/nomina.py

# Base de datos en memoria para la matriz de nómina general (Formato del cuaderno)
nomina_general = {}

# Base de datos para saber cómo se reparte la MOD entre las Órdenes de Producción
nomina_por_orden = {}

def inicializar_nomina():
    global nomina_general, nomina_por_orden
    nomina_general = {}
    nomina_por_orden = {}

def registrar_renglon_nomina(departamento, normal, extra, otros_perc, retencion, imss, otros_ded):
    """
    Registra un renglón
    'departamento' debe ser un texto como: 'Ventas', 'Admin', 'MOD', o 'MOI'
    """
    global nomina_general
    
    total_percepciones = normal + extra + otros_perc
    total_deducciones = retencion + imss + otros_ded
    neto_a_pagar = total_percepciones - total_deducciones
    
    nomina_general[departamento] = {
        "normal": normal,
        "extra": extra,
        "otros_perc": otros_perc,
        "total_percepciones": total_percepciones,
        "retencion": retencion,
        "imss": imss,
        "otros_ded": otros_ded,
        "total_deducciones": total_deducciones,
        "neto_a_pagar": neto_a_pagar
    }
    
    return nomina_general

def distribuir_mod_a_orden(no_orden, monto_asignado):
    global nomina_por_orden
    orden_key = str(no_orden)
    
    if orden_key in nomina_por_orden:
        nomina_por_orden[orden_key] += float(monto_asignado)
    else:
        nomina_por_orden[orden_key] = float(monto_asignado)
        
    return nomina_por_orden

def obtener_resumen_nomina():

    global nomina_general, nomina_por_orden

    total_mod = 0.0
    if "MOD" in nomina_general:
        total_mod = nomina_general["MOD"]["total_percepciones"]

    return {
        "total_mano_obra_directa": round(total_mod, 2),
        "desglose_por_orden": {k: round(v, 2) for k, v in nomina_por_orden.items()},
        "nomina_completa": nomina_general
    }