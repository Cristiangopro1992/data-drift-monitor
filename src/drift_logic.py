import pandas as pd
from scipy.stats import ks_2samp


class DriftAnalyzer:
    def __init__(self, df_baseline, df_target):
        """
        Clase para detectar data drift entre dos datasets.

        :param df_baseline: El DataFrame de referencia (entrenamiento/ayer)
        :param df_target: El DataFrame actual (producción/hoy)
        """
        self.base = df_baseline.copy()
        self.current = df_target.copy()

    def check_schema_drift(self):
        """
        Compara las columnas base con las del target para detectar cambios de esquema.
        Usa conjuntos (sets) para una comparación eficiente O(1).

        :return: Diccionario con listas de "columnas_faltantes" y "columnas_nuevas".
        """
        base_cols = set(self.base.columns)
        current_cols = set(self.current.columns)

        # Calculamos las diferencia
        missing = base_cols - current_cols
        new = current_cols - base_cols

        return {"columnas faltantes": list(missing), "columnas nuevas": list(new)}

    def check_numeric_drift(self, p_value_threshold=0.05):
        """
        Detecta drift en la distribución de columnas numéricas usando el test de Kolmogorov-Smirnov.

        Si el p_value < threshold, rechazamos la hipótesis nula (las distribuciones son diferentes).

        :param p_value_threshold: Umbral de sensibilidad (default 0.05).
        :return: DataFrame con el reporte de métricas y alerta de drift.
        """
        # 1. Identificar columnas numéricas comunes en ambos dataframes
        common_cols = list(set(self.base.columns) & set(self.current.columns))
        numeric_cols = [
            c for c in common_cols if pd.api.types.is_numeric_dtype(self.base[c])
        ]

        report = []

        for col in numeric_cols:
            # Eliminamos nulos para el cálculo estadístico
            b_data = self.base[col].dropna()
            c_data = self.current[col].dropna()

            if b_data.empty or c_data.empty:
                continue

            # --- Test Estadístico (KS Test) ---
            # ks_2samp compara si dos muestras provienen de la misma distribución continua
            statistic, p_value = ks_2samp(b_data, c_data)

            # --- Detección ---
            drift_detected = p_value < p_value_threshold

            report.append(
                {
                    "Columna": col,
                    "Media Base": round(b_data.mean(), 2),
                    "Media Actual": round(c_data.mean(), 2),
                    "KS P-Value": round(p_value, 4),
                    "Drift Detectado": "🔴 SÍ" if drift_detected else "🟢 NO",
                }
            )

        return pd.DataFrame(report)
