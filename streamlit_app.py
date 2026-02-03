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
    df_b = pd.DataFrame({
        "id": range(100),
        "edad": np.random.normal(30, 5, 100),  # Media 30
        "ingresos": np.random.normal(50000, 2000, 100),
        "categoria": np.random.choice(["A", "B"], 100),
    })
    # Current: Datos con DRIFT
    df_c = pd.DataFrame({
        "id": range(100),
        "edad": np.random.normal(35, 5, 100),  # DRIFT: Media sube a 35
        "ingresos": np.random.normal(50000, 2000, 100),  # Sin drift
        "descuento": np.random.uniform(0, 10, 100),  # DRIFT: Columna nueva
        # 'categoria': desaparece (DRIFT: Columna faltante)
    })
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
    
    # --- FIX DE EMERGENCIA PARA ERROR LargeUtf8 ---
    # Convertimos forzosamente cualquier texto a objeto Python estándar
    # Lo aplicamos AQUÍ para que funcione tanto en Demo como en CSV subidos
    def clean_large_utf8(df):
        for col in df.select_dtypes(include=['object', 'string']).columns:
            df[col] = df[col].astype("object")
        return df

    df_base = clean_large_utf8(df_base)
    df_curr = clean_large_utf8(df_curr)
    # -----------------------------------------------

    # Instanciamos la clase lógica
    analyzer = DriftAnalyzer(df_base, df_curr)

    st.markdown("---")

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

    with col_metrics_1:
        st.metric("Columnas Faltantes", len(missing), delta=-len(missing) if missing else 0, delta_color="inverse")
        if missing:
            st.error(f"❌ Desaparecieron: {', '.join(missing)}")
        else:
            st.success("✅ Sin columnas perdidas")

    with col_metrics_2:
        st.metric("Columnas Nuevas", len(new_cols), delta=len(new_cols) if new_cols else 0)
        if new_cols:
            st.info(f"🆕 Nuevas detectadas: {', '.join(new_cols)}")
        else:
            st.success("✅ Sin columnas inesperadas")

    # 3. NUMERICAL DRIFT
    st.header("2. Numerical Drift (Estadístico)")
    st.caption("Usando Test Kolmogorov-Smirnov (KS-Test). Si p-value < 0.05, detectamos cambio significativo.")

    try:
        drift_report = analyzer.check_numeric_drift()

        # Estilizar el dataframe para resaltar alertas
        def highlight_drift(row):
            return ['background-color: #ffcccc' if row['Drift Detectado'] == '🔴 SÍ' else '' for _ in row]

        st.dataframe(drift_report.style.apply(highlight_drift, axis=1), use_container_width=True)

        # Alerta global
        if 'Drift Detectado' in drift_report.columns:
            drift_count = len(drift_report[drift_report['Drift Detectado'] == '🔴 SÍ'])
            if drift_count > 0:
                st.warning(f"⚠️ ¡Atención! Se han detectado {drift_count} variables con drift estadístico.")
            else:
                st.balloons()
                st.success("Todo parece estable. No hay drift numérico significativo.")

    except Exception as e:
        st.error(f"Error calculando drift numérico: {e}")

else:
    st.info("👈 Sube tus archivos CSV o activa el 'Modo Demo' para comenzar.")
