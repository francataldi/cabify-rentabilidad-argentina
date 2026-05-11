# ============================================================
# MODELO DE COSTOS — Rentabilidad por auto para Cabify AMBA
# ============================================================
# Fuentes:
# - Ingresos: iProfesional, relevamiento 25+ choferes activos (2025)
# - Comisión Cabify: 12.5% (fuente oficial Cabify Argentina)
# - Tipo de cambio: dolarhoy.com (scrapeado en tiempo real)
# ============================================================

PARAMETROS = {
    # Ingresos
    "ingreso_bruto_mensual_ars": 2_000_000,   # promedio jornada 8hs, lunes a sábado
    "comision_cabify": 0.125,                  # 12.5% oficial

    # Operación
    "km_diarios": 150,                         # estimado 8hs de trabajo en AMBA
    "dias_laborales_mes": 26,                  # lunes a sábado

    # Combustible (nafta super AMBA, mayo 2025)
    "precio_nafta_ars_litro": 1100,
    "precio_gnc_ars_m3": 280,

    # Seguro (todo riesgo promedio AMBA)
    "seguro_mensual_ars": 180_000,

    # Patente (promedio autos del segmento)
    "patente_anual_ars": 400_000,

    # Vida útil del auto para Cabify (km totales antes de renovar)
    "vida_util_km": 300_000,
}


def calcular_rentabilidad(precio_compra_usd, consumo_l_100km, tiene_gnc,
                          tipo_cambio, parametros=PARAMETROS):
    p = parametros

    # 1. Ingresos netos después de comisión Cabify
    ingreso_neto_cabify = p["ingreso_bruto_mensual_ars"] * (1 - p["comision_cabify"])

    # 2. Km mensuales
    km_mensuales = p["km_diarios"] * p["dias_laborales_mes"]

    # 3. Costo de combustible mensual
    if tiene_gnc:
        # GNC: consumo equivalente aprox 10 m3/100km
        consumo_gnc_m3 = (km_mensuales / 100) * 10
        costo_combustible = consumo_gnc_m3 * p["precio_gnc_ars_m3"]
    else:
        litros_mes = (km_mensuales / 100) * consumo_l_100km
        costo_combustible = litros_mes * p["precio_nafta_ars_litro"]

    # 4. Amortización mensual (precio de compra / vida útil en km * km mensuales)
    precio_compra_ars = precio_compra_usd * tipo_cambio
    amortizacion_mensual = (precio_compra_ars / p["vida_util_km"]) * km_mensuales

    # 5. Patente mensual
    patente_mensual = p["patente_anual_ars"] / 12

    # 6. Costos totales mensuales
    costos_totales = (
        costo_combustible +
        amortizacion_mensual +
        p["seguro_mensual_ars"] +
        patente_mensual
    )

    # 7. Ganancia neta mensual
    ganancia_neta_ars = ingreso_neto_cabify - costos_totales
    ganancia_neta_usd = ganancia_neta_ars / tipo_cambio

    # 8. Payback period (meses para recuperar inversión)
    payback_meses = precio_compra_ars / ganancia_neta_ars if ganancia_neta_ars > 0 else float("inf")

    return {
        "precio_compra_usd": precio_compra_usd,
        "ingreso_neto_cabify_ars": ingreso_neto_cabify,
        "costo_combustible_ars": costo_combustible,
        "amortizacion_mensual_ars": amortizacion_mensual,
        "seguro_mensual_ars": p["seguro_mensual_ars"],
        "patente_mensual_ars": patente_mensual,
        "costos_totales_ars": costos_totales,
        "ganancia_neta_ars": ganancia_neta_ars,
        "ganancia_neta_usd": ganancia_neta_usd,
        "payback_meses": payback_meses,
        "km_mensuales": km_mensuales,
    }