# app-contabilidad
Aplicación de escritorio desarrollada en Python y CustomTkinter para la automatización de ejercicios de costos históricos. Genera tarjetas de almacén, nóminas, prorrateos (primario, secundario y final), estados de costos y resultados. Portable en un .exe.

# 📊 Sistema de Automatización de Costos Históricos

¡Bienvenido! Este es un proyecto de escritorio desarrollado en **Python** utilizando **CustomTkinter** para la interfaz gráfica. El objetivo principal de la aplicación es resolver de manera automatizada ejercicios de contabilidad de costos históricos, estructurando la información a través de cédulas y reportes financieros clave.

La aplicación está diseñada bajo un enfoque modular, facilitando el procesamiento aritmético de los datos y garantizando una experiencia de usuario intuitiva mediante un flujo secuencial de pestañas.

---

## ✨ Características Principales & Reportes

El software automatiza y genera los siguientes entregables contables a partir de los datos de entrada del usuario:

*   📦 **Tarjeta de Almacén:** Control de inventarios (Entradas/Salidas) utilizando el método de valuación correspondiente (PEPS / Promedio Ponderado).
*   📋 **Cédula de Mano de Obra (Nómina):** Registro y distribución del costo de mano de obra directa aplicable a la producción.
*   ⚡ **Cargos Indirectos (Prorrateo):** Módulo secuencial para el cálculo automático de prorrateo **primario, secundario y final**.
*   🏭 **Órdenes de Producción:** Concentrado de asignación de costos directos e indirectos por cada orden de trabajo.
*   📈 **Estados Financieros:** Generación de la Cédula de Estado de Costos de Producción y lo Vendido, y el Estado de Resultados.
*   💾 **Inventario Final:** Resumen valorizado de las existencias al cierre del ejercicio.

---

## 🛠️ Stack Tecnológico

*   **Lenguaje:** Python 3.x
*   **Interfaz Gráfica (GUI):** [CustomTkinter](httpsve/github.com/TomSchimansky/CustomTkinter) (UI moderna y adaptativa).
*   **Procesamiento de Datos:** Pandas (para la estructuración de tablas y posible exportación).
*   **Empaquetado:** PyInstaller (para la generación del binario autónomo ejecutable `.exe` para Windows).

---

## 🚀 Portabilidad (Cero Instalaciones)

Siguiendo las restricciones del proyecto, la aplicación no requiere la instalación previa de un entorno de ejecución (como Python o un JDK) en la máquina final. 

> 💡 **Nota para evaluación:** El software se distribuye como un archivo ejecutable único (`.exe`). Para correr la aplicación, el usuario final solo requiere arrastrar el archivo a su computadora con Windows y dar **doble clic**.

---

## 📁 Estructura del Proyecto

```text
├── src/
│   ├── logica/         # Algoritmos de cálculo (Almacén, Nómina, Prorrateos)
│   ├── gui/            # Componentes, ventanas y maquetación de la interfaz
│   └── main.py         # Punto de entrada de la aplicación
├── instructivo/        # Manual de usuario con imágenes/videos de soporte
├── requirements.txt    # Dependencias del proyecto para desarrollo
└── README.md