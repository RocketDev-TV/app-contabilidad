# NOTA DE ARQUITECTURA: Conexión GUI - Lógica de Costos

Te dejo la guia de como esta estructurado el proyecto y qué pantallas/componentes necesitamos mapear en el Front con **CustomTkinter** para que se conecten limpio con el Backend que estoy programando.

## Regla principal del proyecto
**Separación total:** Ningún archivo dentro de la carpeta `src/gui/` debe hacer cálculos contables directos. La GUI solo se encarga de:
1. Capturar los datos del usuario (Inputs).
2. Pasárselos como argumentos a las funciones de `src/logic/`.
3. Recibir el resultado y pintarlo en tablas o etiquetas.

---

## Componentes a programar por Pestaña

### 1. Pestaña: Almacén (Valuación Promedio)
* **Inputs:** Campos de texto (`CTkEntry`) para registrar un movimiento: *Concepto* (Apertura, Compra, Producción), *Cantidad* y *Costo Unitario*. Un botón de "Registrar".
* **Outputs:** Una tabla o contenedor donde se muestre el histórico de la Tarjeta de Almacén (Entradas, Salidas, Existencia, Debe, Haber, Saldo y Costo Promedio). Un label que resalte el **Costo de Materia Prima Utilizada** y el **Inventario Final**.

### 2. Pestaña: Nómina (Mano de Obra)
* **Inputs:** Campos para ingresar las *Horas Directas trabajadas* por orden de producción (ej. Orden 101, 102) y la *Cuota por hora*.
* **Outputs:** Visualización de la Cédula de Mano de Obra con el total de MOD asignada a cada orden.

### 3. Pestaña: Prorrateos (Cargos Indirectos)
* **Sub-pestaña Primario:** Inputs para capturar costos globales (Renta, Luz, Depreciación) y las bases (m2, Kw, inversión). Muestra el reparto entre departamentos productivos y de servicio.
* **Sub-pestaña Secundario:** Botón para redistribuir el costo de los departamentos de servicio hacia los productivos.
* **Sub-pestaña Final:** Aplica los costos acumulados a las **Órdenes de Producción** usando la tasa determinada.

### 4. Pestaña: Resultados (Entregables Finales)
* **Outputs:**
    * **Órdenes de Producción:** Vista para elegir una orden y desglosar su Costo Total (MP + MO + CI).
    * **Estado de Costos de Producción y de lo Vendido.**
    * **Estado de Resultados.**

---

## Ejemplo de Conexión (Código)

Cuando programes los botones, llamarás a mis funciones pasándole diccionarios con lo que captures en los inputs:

```python
from logic.prorrateo import calcular_prorrateo_primario

def al_dar_clic_en_primario(self):
    gastos = {"renta": 12000, "luz": 5000}
    bases = {"taller": 150, "oficinas": 50}
    
    resultado_tabla = calcular_prorrateo_primario(gastos, bases)
    self.mostrar_tabla_en_pantalla(resultado_tabla)

Tip: Para las tablas puede usar un CTkScrollableFrame con filas de CTkLabel para simular las celdas.
```

Mas adelante mi idea es implementar una libreria de conversion para poder pasar la pantalla final a un pdf o un excel