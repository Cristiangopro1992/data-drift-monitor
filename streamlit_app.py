import streamlit as st
import pandas as pd
import numpy as np
from src.drift_logic import DriftAnalyzer

# Configuración de página
st.set_page_config(page_title="Data Drift Monitor", page_icon="🔍", layout="wide")

st.title("🔍 Data Drift Monitor")
st.markdown("""
Esta herramienta detecta **Schema Drift** (cambios estructurales) y **Numerical Drift** (cambios estadísticos) 
entre un dataset de referencia (Training/Base) y uno actual (Production/Target).
""")

# --- SIDEBAR: CONFIGURACIÓN ---
st.sidebar.header("1. Carga de Datos")


# Función auxiliar para crear datos fake (Para modo Demo)
def generate_fake_data():
    np.random.seed(42)
    # Base: Datos normales
    df_b = pd.DataFrame(
        {
            "id": range(100),
            "edad": np.random.normal(30, 5, 100),  # Media 30
            "ingresos": np.random.normal(50000, 2000, 100),
            "categoria": np.random.choice(["A", "B"], 100),
        }
    )
    # Current: Datos con DRIFT
    df_c = pd.DataFrame(
        {
            "id": range(100),
            "edad": np.random.normal(35, 5, 100),  # DRIFT: Media sube a 35
            "ingresos": np.random.normal(50000, 2000, 100),  # Sin drift
            "descuento": np.random.uniform(0, 10, 100),  # DRIFT: Columna nueva
            # 'categoria': desaparece (DRIFT: Columna faltante)
        }
    )
    return df_b, df_c


# Opción de Demo
use_demo = st.sidebar.checkbox("⚡ Usar Datos de Ejemplo (Modo Demo)", value=False)

df_base = None
df_curr = None

if use_demo:
    df_base, df_curr = generate_fake_data()
    st.sidebar.success("Datos de ejemplo cargados")
else:
    uploaded_base = st.sidebar.file_uploader("Subir Dataset Base (CSV)", type="csv")
    uploaded_curr = st.sidebar.file_uploader("Subir Dataset Actual (CSV)", type="csv")

    if uploaded_base and uploaded_curr:
        df_base = pd.read_csv(uploaded_base)
        df_curr = pd.read_csv(uploaded_curr)

# --- LOGICA PRINCIPAL ---
if df_base is not None and df_curr is not None:
    # Instanciamos la clase lógica
    analyzer = DriftAnalyzer(df_base, df_curr)

    st.divider()

    # 1. VISUALIZACIÓN DE DATASETS
    with st.expander("👀 Ver Datasets (Primeras 5 filas)"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Base (Referencia)")
            st.dataframe(df_base.head())
        with col2:
            st.subheader("Current (Producción)")
            st.dataframe(df_curr.head())

    # 2. SCHEMA DRIFT
    st.header("1. Schema Drift (Estructura)")
    schema_drift = analyzer.check_schema_drift()

    col_metrics_1, col_metrics_2 = st.columns(2)

    missing = schema_drift["columnas faltantes"]
    new_cols = schema_drift["columnas nuevas"]
