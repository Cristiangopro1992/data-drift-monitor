# data-drift-monitor
App donde subes el dataset de "Ayer" (Referencia) y el dataset de "Hoy" (Actual), y te dice qué cambios importantes tienes.

# 📊 Data Drift Monitor

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

Una aplicación de **Ingeniería y Observabilidad de Datos** diseñada para detectar automáticamente cambios en la estructura y calidad de los datasets antes de que rompan los pipelines de producción o afecten a modelos de Machine Learning.

---

## El Problema es:
En el mundo real, los datos nunca son estáticos. Los pipelines de datos suelen fallar silenciosamente por tres razones principales:
1.  **Cambios de Esquema:** Columnas que desaparecen, se renombran o aparecen nuevas sin aviso.
2.  **Cambios de Tipo:** Datos numéricos que llegan como texto, rompiendo transformaciones downstream.
3.  **Desviación Estadística:** Cambios drásticos en la distribución de los datos que degradan el rendimiento de modelos de IA.

## La Solución sería:
**Data Drift Monitor** actúa como un "detective" entre dos versiones de un dataset:
* **Baseline (Referencia):** El dataset histórico validado.
* **Target (Actual):** El nuevo dataset que acaba de llegar y necesita validación.

La herramienta compara ambos archivos y genera un reporte visual instantáneo sobre de los datos.

## Stack Tecnológico
* **Lenguaje:** Python
* **Procesamiento:** Pandas (manipulación eficiente de dataframes).
* **Frontend:** Streamlit (interfaz interactiva y ágil).
* **Entorno:** Gestión de dependencias con `venv` y `pip`.

## Funcionalidades
- [ ] Carga interactiva de archivos CSV (Baseline vs Target).
- [ ] Detección de **Schema Drift** (Columnas nuevas/perdidas).
- [ ] Detección de cambios en tipos de datos.
- [ ] Análisis estadístico básico (conteo de nulos, filas, duplicados).
- [ ] Visualización de distribuciones numéricas.

---

## 📂 Estructura del Proyecto

El proyecto sigue una arquitectura modular separando la lógica de negocio (`src`) de la interfaz (`app.py`) y el laboratorio de pruebas (`notebooks`).

```text
data-drift-monitor/
│
├── data/                # Almacenamiento local de datasets (Ignorado en git)
├── notebooks/           # Laboratorio de pruebas (Jupyter) para prototipar lógica
├── src/                 # Lógica pura de detección de drift (Backend)
│   ├── __init__.py
│   └── drift_logic.py   # Clase DriftAnalyzer
│
├── streamlit_app.py               # Punto de entrada de la aplicación (Streamlit)
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación
