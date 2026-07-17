# ============================================================
# MODELO DE COSTOS v2 — Rentabilidad por auto para Cabify AMBA
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

    # Combustible (nafta super AMBA)
    "precio_nafta_ars_litro": 2034,
    "precio_gnc_ars_m3": 500,

    # Seguro todo riesgo — calculado como % del valor del auto con un piso.
    # Regla aproximada mercado asegurador AMBA: ~1.2% mensual del valor,
    # con un mínimo de $140.000 (autos baratos no bajan de ahí).
    "seguro_pct_mensual": 0.012,
    "seguro_piso_ars": 140_000,

    # Patente AMBA — ~4.5% anual sobre el valor fiscal, que suele ser
    # ~80% del valor de mercado del auto.
    "patente_pct_anual": 0.045,
    "valor_fiscal_pct": 0.80,

    # Vida útil del auto para Cabify (km totales antes de renovar)
    "vida_util_km": 300_000,

    # Valor residual: un auto con 300.000 km no vale $0 — en Argentina
    # conserva aprox. un tercio de su valor de compra. La amortización
    # solo debe cubrir la pérdida de valor, no el precio completo.
    "valor_residual_pct": 0.35,
}


# Mantenimiento por km (ARS/km, estimaciones AMBA 2026).
# Prorratea cubiertas, frenos, aceite, service, embrague y distribución
# sobre la vida útil. Basado en costos de service oficial + consumibles.
# Los autos franceses (Peugeot) y los turbo (Onix Plus) tienen repuestos
# más caros; Fiat/VW/Ford de entrada de gama son los más baratos de mantener.
MANTENIMIENTO_POR_KM_ARS = {
    "Toyota Etios":        95,
    "Toyota Corolla":      120,
    "Toyota Yaris":        100,
    "Chevrolet Prisma":    90,
    "Chevrolet Onix Plus": 95,
    "Fiat Cronos":         85,
    "Renault Logan":       85,
    "VW Virtus":           100,
    "VW Voyage":           90,
    "VW Gol":              80,
    "Nissan Versa":        105,
    "Ford Ka":             85,
    "Ford Fiesta":         90,
    "Fiat Siena":          80,
    "Peugeot 208":         110,
}


def calcular_rentabilidad(precio_compra_usd, consumo_l_100km, tiene_gnc,
                          tipo_cambio, costo_mantenimiento_km=0.0,
                          parametros=PARAMETROS):
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

    # 4. Amortización mensual con valor residual: el auto pierde
    # (precio - residual) a lo largo de la vida útil, no el precio completo
    precio_compra_ars = precio_compra_usd * tipo_cambio
    valor_residual_ars = precio_compra_ars * p["valor_residual_pct"]
    amortizacion_mensual = ((precio_compra_ars - valor_residual_ars)
                            / p["vida_util_km"]) * km_mensuales

    # 5. Mantenimiento mensual (cubiertas, frenos, aceite, service, etc.)
    mantenimiento_mensual = costo_mantenimiento_km * km_mensuales

    # 6. Seguro mensual: % del valor del auto con piso. Si el llamador
    # pasa "seguro_mensual_ars" en parametros (ej: slider del dashboard),
    # ese valor manda.
    seguro_mensual = p.get("seguro_mensual_ars")
    if seguro_mensual is None:
        seguro_mensual = max(precio_compra_ars * p["seguro_pct_mensual"],
                             p["seguro_piso_ars"])

    # 7. Patente mensual: % anual sobre el valor fiscal (~80% del de mercado)
    patente_mensual = (precio_compra_ars * p["valor_fiscal_pct"]
                       * p["patente_pct_anual"]) / 12

    # 8. Costos totales mensuales
    costos_totales = (
        costo_combustible +
        amortizacion_mensual +
        mantenimiento_mensual +
        seguro_mensual +
        patente_mensual
    )

    # 9. Ganancia neta mensual
    ganancia_neta_ars = ingreso_neto_cabify - costos_totales
    ganancia_neta_usd = ganancia_neta_ars / tipo_cambio

    # 10. Payback period (meses para recuperar inversión)
    payback_meses = precio_compra_ars / ganancia_neta_ars if ganancia_neta_ars > 0 else float("inf")

    return {
        "precio_compra_usd": precio_compra_usd,
        "ingreso_neto_cabify_ars": ingreso_neto_cabify,
        "costo_combustible_ars": costo_combustible,
        "amortizacion_mensual_ars": amortizacion_mensual,
        "mantenimiento_mensual_ars": mantenimiento_mensual,
        "seguro_mensual_ars": seguro_mensual,
        "patente_mensual_ars": patente_mensual,
        "valor_residual_ars": valor_residual_ars,
        "costos_totales_ars": costos_totales,
        "ganancia_neta_ars": ganancia_neta_ars,
        "ganancia_neta_usd": ganancia_neta_usd,
        "payback_meses": payback_meses,
        "km_mensuales": km_mensuales,
    }
