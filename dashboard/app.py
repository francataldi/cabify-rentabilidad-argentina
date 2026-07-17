import os
import sys

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.modelo import MANTENIMIENTO_POR_KM_ARS, PARAMETROS, calcular_rentabilidad
from src.precios_combustible import get_precios_combustible

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
Analizá la rentabilidad de 15 modelos de autos usados para trabajar en Cabify en AMBA.
Ajustá los parámetros según tu situación y obtené un ranking personalizado.
""")

st.info("""
⚠️ **Importante antes de usar este análisis:**
Este estudio analiza autos **usados** del mercado argentino scrapeados de MercadoLibre.
Los precios de compra corresponden al **valor mediano de mercado** para cada modelo,
no a unidades 0km. Comprar un auto más caro o más nuevo que el mediano del análisis
va a reducir significativamente la rentabilidad estimada.
Más abajo podés ver las características del auto "tipo" analizado para cada modelo.
""")

st.divider()

# ============================================================
# TIPO DE CAMBIO EN TIEMPO REAL
# ============================================================
@st.cache_data(ttl=3600)
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
        return 1420.0

TIPO_CAMBIO = get_tipo_cambio()

@st.cache_data(ttl=3600)
def get_precios_combustible_cached():
    return get_precios_combustible()

precios_comb = get_precios_combustible_cached()
PRECIO_NAFTA_AUTO = precios_comb["nafta_super"]
PRECIO_GNC_AUTO = precios_comb["gnc"]

st.caption(f"💱 Dólar blue: ${TIPO_CAMBIO:,.0f} ARS | ⛽ Nafta Súper CABA: ${PRECIO_NAFTA_AUTO:,.0f} ARS/litro — actualizados automáticamente")

# ============================================================
# DATOS BASE
# ============================================================
@st.cache_data
def cargar_datos():
    return pd.read_csv("dashboard/precios_autos_procesado.csv")

df = cargar_datos()
precio_mediano = df.groupby("modelo")["precio_usd"].median()
km_mediano = df.groupby("modelo")["km_num"].median()
año_mediano = df.groupby("modelo")["año"].median().astype(int)

consumo_por_modelo = {
    "Toyota Etios": 8.5, "Toyota Corolla": 9.0, "Toyota Yaris": 8.0,
    "Chevrolet Prisma": 8.5, "Chevrolet Onix Plus": 7.8, "Renault Logan": 8.0,
    "Nissan Versa": 9.0, "VW Virtus": 8.5, "VW Voyage": 9.5, "VW Gol": 9.0,
    "Ford Ka": 8.0, "Ford Fiesta": 9.0, "Fiat Siena": 9.5, "Fiat Cronos": 8.4,
    "Peugeot 208": 7.5,
}

tiene_gnc = {
    "Toyota Etios": False, "Toyota Corolla": False, "Toyota Yaris": False,
    "Chevrolet Prisma": True, "Chevrolet Onix Plus": False, "Renault Logan": True,
    "Nissan Versa": False, "VW Virtus": False, "VW Voyage": True, "VW Gol": True,
    "Ford Ka": False, "Ford Fiesta": False, "Fiat Siena": True, "Fiat Cronos": True,
    "Peugeot 208": False,
}

# ============================================================
# SIDEBAR — PARÁMETROS CONFIGURABLES
# ============================================================
st.sidebar.header("⚙️ Configurá tu escenario")

st.sidebar.markdown("**💵 Ingreso bruto mensual (ARS)**")
st.sidebar.caption("Total facturado a Cabify antes de descontar la comisión del 12,5%. No es lo que te depositan — es lo que generás en viajes.")
ingreso_bruto = st.sidebar.slider(
    "Ingreso bruto mensual",
    min_value=1_000_000, max_value=3_500_000,
    value=2_000_000, step=100_000,
    format="$%d",
    label_visibility="collapsed"
)

st.sidebar.markdown("**🛣️ Km diarios trabajados**")
st.sidebar.caption("Kilómetros que recorrés en un día de trabajo completo, incluyendo viajes con pasajero y traslados en vacío.")
km_diarios = st.sidebar.slider(
    "Km diarios",
    min_value=80, max_value=250,
    value=150, step=10,
    label_visibility="collapsed"
)

st.sidebar.markdown("**⛽ Precio nafta super (ARS/litro)**")
st.sidebar.caption("Precio actual de la nafta super en tu zona. Consultá en surtidores.com.ar.")
precio_nafta = st.sidebar.slider(
    "Precio nafta",
    min_value=700, max_value=3000,
    value=int(PRECIO_NAFTA_AUTO), step=50,
    format="$%d",
    label_visibility="collapsed"
)

st.sidebar.markdown("**🔵 Precio GNC (ARS/m³)**")
st.sidebar.caption("Precio del metro cúbico de GNC en tu zona.")
precio_gnc = st.sidebar.slider(
    "Precio GNC",
    min_value=150, max_value=1000,
    value=int(PRECIO_GNC_AUTO), step=10,
    format="$%d",
    label_visibility="collapsed"
)

st.sidebar.markdown("**🛡️ Seguro mensual (ARS)**")
st.sidebar.caption("Costo mensual del seguro todo riesgo para el auto. Varía según modelo, año y aseguradora.")
seguro = st.sidebar.slider(
    "Seguro mensual",
    min_value=80_000, max_value=800_000,
    value=180_000, step=10_000,
    format="$%d",
    label_visibility="collapsed"
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
        costo_mantenimiento_km=MANTENIMIENTO_POR_KM_ARS[modelo],
        parametros=p
    )
    r["modelo"] = modelo
    r["tiene_gnc"] = tiene_gnc[modelo]
    resultados.append(r)

df_res = pd.DataFrame(resultados).set_index("modelo")

# ============================================================
# VALIDACIÓN — escenario económicamente viable
# ============================================================
hay_ganancia_positiva = (df_res["ganancia_neta_usd"] > 0).any()

if not hay_ganancia_positiva:
    st.error("""
    ⚠️ **Escenario inviable:** con los parámetros actuales ningún auto genera ganancia positiva.
    Los costos superan los ingresos. Probá aumentar el ingreso bruto o reducir los km diarios.
    """)
    st.stop()

# ============================================================
# SCORING POR PERFIL
# ============================================================
def minmax(serie):
    if serie.max() == serie.min():
        return pd.Series(50, index=serie.index)
    return (serie - serie.min()) / (serie.max() - serie.min()) * 100

df_pos = df_res[df_res["ganancia_neta_usd"] > 0].copy()

scores = pd.DataFrame(index=df_pos.index)
scores["rentabilidad"] = minmax(df_pos["ganancia_neta_usd"])
scores["accesibilidad"] = minmax(-df_pos["precio_compra_usd"])
scores["payback"]       = minmax(-df_pos["payback_meses"])

pesos_perfil = {
    "Maximizador 💰":    {"rentabilidad": 0.60, "accesibilidad": 0.10, "payback": 0.30},
    "Conservador 🛡️":   {"rentabilidad": 0.30, "accesibilidad": 0.30, "payback": 0.40},
    "Capital limitado 💵":{"rentabilidad": 0.20, "accesibilidad": 0.40, "payback": 0.40},
}

pesos = pesos_perfil[perfil]
df_pos["score_perfil"] = (
    scores["rentabilidad"] * pesos["rentabilidad"] +
    scores["accesibilidad"] * pesos["accesibilidad"] +
    scores["payback"] * pesos["payback"]
)

# ============================================================
# MÉTRICAS PRINCIPALES
# ============================================================
st.subheader("📊 Resultados para tu escenario")

mejor = df_pos["score_perfil"].idxmax()
col1, col2, col3 = st.columns(3)
col1.metric("🏆 Mejor auto para tu perfil", mejor)
col2.metric("💵 Ganancia mensual", f"${df_pos.loc[mejor, 'ganancia_neta_usd']:,.0f} USD")
col3.metric("⏱️ Payback", f"{df_pos.loc[mejor, 'payback_meses']:.1f} meses")

st.divider()

# ============================================================
# GRÁFICOS
# ============================================================
col_izq, col_der = st.columns(2)

patch_gnc   = mpatches.Patch(color="#2ecc71", label="Con GNC")
patch_nafta = mpatches.Patch(color="#3498db", label="Nafta")

with col_izq:
    st.subheader("Ranking por tu perfil (score 0-100)")
    df_plot = df_pos.sort_values("score_perfil", ascending=True)
    colores = ["#2ecc71" if tiene_gnc[m] else "#3498db" for m in df_plot.index]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(df_plot.index, df_plot["score_perfil"], color=colores)
    for i, v in enumerate(df_plot["score_perfil"]):
        ax.text(v + 0.5, i, f"{v:.0f}", va="center", fontsize=8)
    ax.legend(handles=[patch_gnc, patch_nafta])
    ax.set_xlabel("Score (0-100)")
    ax.set_xlim(0, 110)
    st.pyplot(fig)
    plt.close()

with col_der:
    st.subheader("Ganancia neta mensual (USD)")
    df_plot2 = df_pos.sort_values("ganancia_neta_usd", ascending=True)
    colores2 = ["#2ecc71" if tiene_gnc[m] else "#3498db" for m in df_plot2.index]

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.barh(df_plot2.index, df_plot2["ganancia_neta_usd"], color=colores2)
    for i, v in enumerate(df_plot2["ganancia_neta_usd"]):
        ax2.text(v + 2, i, f"${v:,.0f}", va="center", fontsize=8)
    ax2.legend(handles=[patch_gnc, patch_nafta])
    ax2.set_xlabel("USD/mes")
    st.pyplot(fig2)
    plt.close()

st.divider()

# ============================================================
# PERFIL DEL AUTO TIPO POR MODELO
# ============================================================
st.subheader("🔍 ¿Qué auto representa cada modelo en el análisis?")
st.markdown("""
Los precios de compra son medianas del mercado de **autos usados** en MercadoLibre.
Antes de tomar una decisión, verificá que el auto que vas a comprar se acerque
a estas características — de lo contrario la rentabilidad real va a diferir.
""")

tabla_perfil = pd.DataFrame({
    "Modelo": list(consumo_por_modelo.keys()),
    "Precio mediano (USD)": [f"${precio_mediano[m]:,.0f}" for m in consumo_por_modelo],
    "Año típico": [str(año_mediano[m]) for m in consumo_por_modelo],
    "Km típicos": [f"{km_mediano[m]:,.0f} km" for m in consumo_por_modelo],
    "GNC": ["✅" if tiene_gnc[m] else "❌" for m in consumo_por_modelo],
    "Ganancia/mes (USD)": [
        f"${df_res.loc[m, 'ganancia_neta_usd']:,.0f}" 
        if df_res.loc[m, 'ganancia_neta_usd'] > 0 
        else "❌ Negativa" 
        for m in consumo_por_modelo
    ],
}).sort_values("Precio mediano (USD)")

st.dataframe(tabla_perfil, use_container_width=True, hide_index=True)

st.divider()

# ============================================================
# TABLA COMPARATIVA COMPLETA
# ============================================================
st.subheader("📋 Tabla comparativa completa")
tabla = df_res[[
    "precio_compra_usd", "ganancia_neta_usd", "payback_meses",
    "costo_combustible_ars", "amortizacion_mensual_ars",
    "mantenimiento_mensual_ars", "tiene_gnc"
]].sort_values("ganancia_neta_usd", ascending=False).copy()

tabla["ganancia_neta_usd"] = tabla["ganancia_neta_usd"].apply(
    lambda x: f"${x:,.0f}" if x > 0 else f"❌ -${abs(x):,.0f}"
)
tabla["payback_meses"] = tabla["payback_meses"].apply(
    lambda x: f"{x:.1f} meses" if x > 0 else "N/A"
)
tabla.columns = ["Precio compra (USD)", "Ganancia/mes (USD)", "Payback",
                 "Combustible (ARS)", "Amortización (ARS)",
                 "Mantenimiento (ARS)", "GNC"]
tabla["GNC"] = tabla["GNC"].map({True: "✅", False: "❌"})

st.dataframe(tabla, use_container_width=True)

st.divider()
st.caption("Proyecto de Data Science — Franco Cataldi Gagliardi | Datos: MercadoLibre, DolarHoy.com | 2026")