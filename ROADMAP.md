# 🗺️ Roadmap de mejoras — cabify-rentabilidad-argentina

Estado actual del proyecto y lista priorizada de mejoras identificadas a partir
de tres reviews técnicas independientes (mayo 2026).

---

## 🔴 Crítico — afecta validez del análisis

| # | Mejora | Tiempo estimado | Estado |
|---|---|---|---|
| 1 | Filtro año ≥ 2016 (regulaciones Cabify GCBA) | 30 min | ⏳ Pendiente |
| 2 | Valor residual en amortización (precio_compra - valor_reventa) | 2hs | ⏳ Pendiente |
| 3 | GNC validado desde títulos del scraping | 1h | ⏳ Pendiente |

## 🟡 Importante — mejora credibilidad del modelo

| # | Mejora | Tiempo estimado | Estado |
|---|---|---|---|
| 4 | Costos de mantenimiento por km | 3hs | ⏳ Pendiente |
| 5 | Seguro y patente diferenciados por modelo | 2hs | ⏳ Pendiente |
| 6 | Documentar fuentes del consumo de combustible | 1h | ⏳ Pendiente |
| 7 | Consumo GNC diferenciado por modelo | 1h | ⏳ Pendiente |

## 🟣 Alto impacto — capa de Machine Learning

| # | Mejora | Tiempo estimado | Estado |
|---|---|---|---|
| 8 | Modelo de predicción de precio (Random Forest/XGBoost) | 4hs | ⏳ Pendiente |
| 9 | Predicción de depreciación a 3 años | 3hs | ⏳ Pendiente |
| 10 | Documentar limitación distribuciones Montecarlo (Log-Normal) | 1h | ⏳ Pendiente |

## 🟢 Rápido — higiene del proyecto

| # | Mejora | Tiempo estimado | Estado |
|---|---|---|---|
| 11 | Sacar __pycache__ del repo | 10 min | ⏳ Pendiente |
| 12 | Eliminar CSVs intermedios de data/processed/ | 10 min | ⏳ Pendiente |
| 13 | Consistencia scoring notebook 05 vs dashboard | 1h | ⏳ Pendiente |
| 14 | Screenshots del dashboard en el README | 20 min | ⏳ Pendiente |
| 15 | Actualizar fechas y estructura en README | 10 min | ⏳ Pendiente |
| 16 | GitHub Actions para automatizar scraping | 5hs | ⏳ Pendiente |

---

> A medida que se completan las mejoras, cambiar ⏳ Pendiente por ✅ Completado.