import os
import sys

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.modelo import PARAMETROS, calcular_rentabilidad

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Cabify Rentabilidad Argentina",
    page_icon="🚗",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================
st.title("🚗 ¿Qué auto es más rentable para Cabify en Argentina?")
st.markdown("""
Analizá la rentabilidad de 13 modelos de autos para trabajar en Cabify en AMBA.
Ajustá los parámetros según tu situación y obtené un ranking personalizado.
""")
st.divider()

# ============================================================
# TIPO DE CAMBIO EN TIEMPO REAL
# ============================================================
@st.cache_data(ttl=3600)  # cachea por 1 hora
def get_tipo_cambio():
    try:
        url = "https://dolarhoy.com/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        valores = soup.find_all("div", class_="val")
        venta_blue = valores[5].text.strip().replace("$","").replace(".","").replace(",",".")
        return float(venta_blue)
    except:
        return 1420.0  # fallback si falla el scraping

TIPO_CAMBIO = get_tipo_cambio()
st.caption(f"💱 Tipo de cambio dólar blue (venta): ${TIPO_CAMBIO:,.0f} ARS — actualizado automáticamente")

# ============================================================
# DATOS BASE
# ============================================================
@st.cache_data
def cargar_datos():
    return pd.read_csv("dashboard/precios_autos_procesado.csv")

df = cargar_datos()
precio_mediano = df.groupby("modelo")["precio_usd"].median()

consumo_por_modelo = {
    "Toyota Etios": 8.5, "Toyota Corolla": 9.0, "Toyota Yaris": 8.0,
    "Chevrolet Prisma": 8.5, "Renault Logan": 8.0, "Nissan Versa": 9.0,
    "VW Virtus": 8.5, "VW Voyage": 9.5, "VW Gol": 9.0,
    "Ford Ka": 8.0, "Ford Fiesta": 9.0, "Fiat Siena": 9.5, "Peugeot 208": 7.5,
}

tiene_gnc = {
    "Toyota Etios": False, "Toyota Corolla": False, "Toyota Yaris": False,
    "Chevrolet Prisma": True, "Renault Logan": True, "Nissan Versa": False,
    "VW Virtus": False, "VW Voyage": True, "VW Gol": True,
    "Ford Ka": False, "Ford Fiesta": False, "Fiat Siena": True, "Peugeot 208": False,
}

# ============================================================
# SIDEBAR — PARÁMETROS CONFIGURABLES
# ============================================================
st.sidebar.header("⚙️ Configurá tu escenario")

ingreso_bruto = st.sidebar.slider(
    "Ingreso bruto mensual (ARS)",
    min_value=1_000_000, max_value=3_500_000,
    value=2_000_000, step=100_000,
    format="$%d"
)

km_diarios = st.sidebar.slider(
    "Km diarios trabajados",
    min_value=80, max_value=250,
    value=150, step=10
)

precio_nafta = st.sidebar.slider(
    "Precio nafta super (ARS/litro)",
    min_value=700, max_value=3000,
    value=1100, step=50,
    format="$%d"
)

precio_gnc = st.sidebar.slider(
    "Precio GNC (ARS/m³)",
    min_value=150, max_value=1000,
    value=540, step=10,
    format="$%d"
)

seguro = st.sidebar.slider(
    "Seguro mensual (ARS)",
    min_value=80_000, max_value=800_000,
    value=180_000, step=10_000,
    format="$%d"
)

st.sidebar.divider()
st.sidebar.header("👤 Tu perfil")

perfiles_desc = {
    "Maximizador 💰": "Tengo capital disponible y quiero maximizar mi ganancia mensual sin importar el riesgo.",
    "Conservador 🛡️": "Prefiero ganancias estables y predecibles. Me preocupa más no perder que ganar mucho.",
    "Capital limitado 💵": "Mi presupuesto es acotado. Necesito recuperar la inversión rápido y entrar barato."
}

perfil = st.sidebar.radio(
    "¿Qué priorizás?",
    list(perfiles_desc.keys())
)

st.sidebar.info(perfiles_desc[perfil])

# ============================================================
# CÁLCULO DE RENTABILIDAD
# ============================================================
p = PARAMETROS.copy()
p["ingreso_bruto_mensual_ars"] = ingreso_bruto
p["km_diarios"] = km_diarios
p["precio_nafta_ars_litro"] = precio_nafta
p["precio_gnc_ars_m3"] = precio_gnc
p["seguro_mensual_ars"] = seguro


resultados = []
for modelo in consumo_por_modelo:
    r = calcular_rentabilidad(
        precio_compra_usd=precio_mediano[modelo],
        consumo_l_100km=consumo_por_modelo[modelo],
        tiene_gnc=tiene_gnc[modelo],
        tipo_cambio=TIPO_CAMBIO,
        parametros=p
    )
    r["modelo"] = modelo
    r["tiene_gnc"] = tiene_gnc[modelo]
    resultados.append(r)

df_res = pd.DataFrame(resultados).set_index("modelo")

# ============================================================
# MÉTRICAS PRINCIPALES
# ============================================================
st.subheader("📊 Resultados para tu escenario")

col1, col2, col3 = st.columns(3)
mejor = df_res["ganancia_neta_usd"].idxmax()
col1.metric("🏆 Auto más rentable", mejor)
col2.metric("💵 Ganancia mensual", f"${df_res.loc[mejor, 'ganancia_neta_usd']:,.0f} USD")
col3.metric("⏱️ Payback", f"{df_res.loc[mejor, 'payback_meses']:.1f} meses")

st.divider()

# ============================================================
# GRÁFICO RANKING
# ============================================================
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Ganancia neta mensual (USD)")
    df_plot = df_res.sort_values("ganancia_neta_usd", ascending=True)
    colores = ["#2ecc71" if tiene_gnc[m] else "#3498db" for m in df_plot.index]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(df_plot.index, df_plot["ganancia_neta_usd"], color=colores)
    for i, v in enumerate(df_plot["ganancia_neta_usd"]):
        ax.text(v + 5, i, f"${v:,.0f}", va="center", fontsize=8)
    patch_gnc   = mpatches.Patch(color="#2ecc71", label="Con GNC")
    patch_nafta = mpatches.Patch(color="#3498db", label="Nafta")
    ax.legend(handles=[patch_gnc, patch_nafta])
    ax.set_xlabel("USD/mes")
    st.pyplot(fig)
    plt.close()

with col_der:
    st.subheader("Payback (meses para recuperar inversión)")
    df_plot2 = df_res.sort_values("payback_meses", ascending=False)
    colores2 = ["#2ecc71" if tiene_gnc[m] else "#3498db" for m in df_plot2.index]

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.barh(df_plot2.index, df_plot2["payback_meses"], color=colores2)
    for i, v in enumerate(df_plot2["payback_meses"]):
        ax2.text(v + 0.1, i, f"{v:.1f}m", va="center", fontsize=8)
    ax2.legend(handles=[patch_gnc, patch_nafta])
    ax2.set_xlabel("Meses")
    st.pyplot(fig2)
    plt.close()

st.divider()

# ============================================================
# TABLA DETALLADA
# ============================================================
st.subheader("📋 Tabla comparativa completa")
tabla = df_res[[
    "precio_compra_usd", "ganancia_neta_usd", "payback_meses",
    "costo_combustible_ars", "amortizacion_mensual_ars", "tiene_gnc"
]].sort_values("ganancia_neta_usd", ascending=False).copy()

tabla.columns = ["Precio compra (USD)", "Ganancia/mes (USD)", "Payback (meses)",
                 "Combustible (ARS)", "Amortización (ARS)", "GNC"]
tabla["GNC"] = tabla["GNC"].map({True: "✅", False: "❌"})
tabla = tabla.round(0)
st.dataframe(tabla, use_container_width=True)

st.divider()
st.caption("Proyecto de Data Science — Franco Cataldi Gagliardi | Datos: MercadoLibre, DolarHoy.com | 2025")