# src/logic/prorrateo.py

# Almacenes de memoria para guardar los resultados de cada etapa del prorrateo
resultados_primario = {}
resultados_secundario = {}
resultados_final = {}

def inicializar_prorrateos():
    global resultados_primario, resultados_secundario, resultados_final
    resultados_primario = {}
    resultados_secundario = {}
    resultados_final = {}

def calcular_prorrateo_primario(gastos_globales, bases_departamentos):
    """
    (Etapa 1):
    Recibe los gastos acumulados de la fábrica y las bases de medición por departamento.
    
    Argumentos:
        gastos_globales (dict): Ej: {"Renta": 10000, "Luz": 6000}
        bases_departamentos (dict): Ej: {
            "Renta": {"Prod_Ensamble": 120, "Prod_Acabado": 80, "Serv_Mantenimiento": 50},
            "Luz": {"Prod_Ensamble": 500, "Prod_Acabado": 300, "Serv_Mantenimiento": 200}
        }
    """
    global resultados_primario
    
    # Inicializamos la matriz donde acumularemos el total por departamento
    # Ej: {"Prod_Ensamble": 0.0, "Prod_Acabado": 0.0, ...}
    todos_los_deps = set()
    for dep_base in bases_departamentos.values():
        todos_los_deps.update(dep_base.keys())
        
    acumulado_por_dep = {dep: 0.0 for dep in todos_los_deps}
    tabla_desglose = {} # Para que se dibuje la matriz completa si se necesita

    # Aplicamos la fórmula contable: Factor = Gasto Total / Suma de las Bases
    for gasto, monto in gastos_globales.items():
        if gasto in bases_departamentos:
            base_del_gasto = bases_departamentos[gasto]
            suma_base = sum(base_del_gasto.values())
            
            # FÓRMULA CLAVE: Factor de direccionamiento
            factor = monto / suma_base if suma_base > 0 else 0.0
            
            tabla_desglose[gasto] = {"factor": round(factor, 4), "distribucion": {}}
            
            # Repartimos el gasto a cada departamento multiplicando su base por el factor
            for dep, valor_base in base_del_gasto.items():
                asignado = valor_base * factor
                acumulado_por_dep[dep] += asignado
                tabla_desglose[gasto]["distribucion"][dep] = round(asignado, 2)

    # Redondeamos los totales acumulados por departamento
    resultados_primario = {dep: round(total, 2) for dep, total in acumulado_por_dep.items()}

    return {
        "totales_departamentos": resultados_primario,
        "desglose_por_gasto": tabla_desglose
    }


def calcular_prorrateo_secundario(deps_servicio_a_cerrar, bases_redistribucion):
    """
    (Etapa 2):
    Agarra los totales que quedaron en el Primario y liquida los departamentos de servicio.
    
    Argumentos:
        deps_servicio_a_cerrar (list): Lista de nombres, Ej: ["Serv_Mantenimiento"]
        bases_redistribucion (dict): Bases para pasar de Servicio a Productivo. Ej:
            {"Serv_Mantenimiento": {"Prod_Ensamble": 60, "Prod_Acabado": 40}}
    """
    global resultados_primario, resultados_secundario
    
    # Copiamos los valores que traíamos del prorrateo primario
    costos_actuales = resultados_primario.copy()
    
    # Recorremos los departamentos de servicio que se van a cerrar
    for dep_serv in deps_servicio_a_cerrar:
        if dep_serv in costos_actuales and dep_serv in bases_redistribucion:
            monto_a_repartir = costos_actuales[dep_serv]
            base_reparto = bases_redistribucion[dep_serv]
            suma_base = sum(base_reparto.values())
            
            # FÓRMULA: Nuevo factor basado en el costo acumulado del depto de servicio
            factor_secundario = monto_a_repartir / suma_base if suma_base > 0 else 0.0
            
            # Pasamos la lana a los departamentos productivos correspondientes
            for dep_prod, valor_base in base_reparto.items():
                if dep_prod in costos_actuales:
                    costos_actuales[dep_prod] += valor_base * factor_secundario
            
            # El departamento de servicio queda en CERO porque ya se vació por completo
            costos_actuales[dep_serv] = 0.0

    # Guardamos solo los departamentos productivos que mantuvieron el costo final
    resultados_secundario = {k: round(v, 2) for k, v in costos_actuales.items() if v > 0}
    return resultados_secundario


def calcular_prorrateo_final(base_ordenes):
    """
    (Etapa 3):
    Aplica el costo acumulado de los departamentos productivos a las Órdenes de Trabajo reales.
    
    Argumentos:
        base_ordenes (dict): Horas o costos base por orden en cada departamento. Ej:
            {
                "Prod_Ensamble": {"Orden_101": 30, "Orden_102": 20},
                "Prod_Acabado": {"Orden_101": 15, "Orden_102": 25}
            }
    """
    global resultados_secundario, resultados_final
    
    cargos_indirectos_por_orden = {}

    # Procesamos cada departamento productivo por separado
    for dep_prod, monto_acumulado in resultados_secundario.items():
        if dep_prod in base_ordenes:
            ordenes_en_dep = base_ordenes[dep_prod]
            suma_base_ordenes = sum(ordenes_en_dep.values())
            
            # FÓRMULA: Tasa de aplicación = Costo del Depto / Suma de bases de las Órdenes
            tasa_aplicacion = monto_acumulado / suma_base_ordenes if suma_base_ordenes > 0 else 0.0
            
            # Aplicamos el costo indirecto a cada orden
            for orden, valor_base in ordenes_en_dep.items():
                costo_indirecto_asignado = valor_base * tasa_aplicacion
                
                if orden in cargos_indirectos_por_orden:
                    cargos_indirectos_por_orden[orden] += costo_indirecto_asignado
                else:
                    cargos_indirectos_por_orden[orden] = costo_indirecto_asignado

    resultados_final = {k: round(v, 2) for k, v in cargos_indirectos_por_orden.items()}
    return resultados_final

def obtener_cargos_indirectos_orden(no_orden):
    """
    Regresa los cargos indirectos finales calculados para una orden específica.
    """
    global resultados_final
    return resultados_final.get(str(no_orden), 0.0)