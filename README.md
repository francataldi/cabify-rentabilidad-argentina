# 🚗 Análisis de Rentabilidad de Vehículos para Cabify en Argentina

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Playwright](https://img.shields.io/badge/Scraping-Playwright-green?logo=playwright)
![Status](https://img.shields.io/badge/Status-Completado-brightgreen)
![Montecarlo](https://img.shields.io/badge/Simulación-Montecarlo-purple)
![Argentina](https://img.shields.io/badge/Mercado-Argentina-lightblue)

## 🚀 Dashboard interactivo
**[→ Ver dashboard en vivo](https://cabify-rentabilidad-argentina.streamlit.app)**

Configurá tu escenario (km diarios, precio de nafta, GNC, seguro) y obtené un ranking de rentabilidad personalizado en tiempo real.

---

## 🏆 Hallazgos principales

- **El VW Gol con GNC es el auto más rentable** para trabajar en Cabify en AMBA, con una ganancia neta mediana de ~$966 USD/mes y un payback de solo 6.6 meses.
- **El GNC es el factor diferenciador más importante:** reduce el costo de combustible en ~$250.000 ARS/mes respecto a nafta, llevando a los 5 primeros puestos del ranking a autos con GNC.
- **El precio de compra es el segundo factor clave:** dentro de los autos con GNC, el más barato (VW Gol, ~$6.100 USD) supera en rentabilidad al más caro (Renault Logan, ~$11.200 USD) por $69 USD mensuales.
- **La simulación de Montecarlo reveló** que el ingreso bruto mensual es la variable con mayor impacto en la rentabilidad (±$246 USD ante una variación del 20%), por encima del tipo de cambio (±$210 USD) y el precio del combustible (±$15 USD).
- **El Toyota Corolla**, siendo el auto más caro del análisis (~$22.000 USD), es el menos rentable con solo $560 USD/mes de ganancia neta y un payback de 42 meses.

---

## 📌 Descripción
Proyecto de Data Science que analiza qué vehículo es más rentable para trabajar
en plataformas de ride-hailing (Cabify) en Argentina, considerando costos de
adquisición, combustible, mantenimiento, depreciación y simulación de escenarios
macroeconómicos.

El análisis cubre **13 modelos de autos**, **3.690 publicaciones reales de MercadoLibre**
y **10.000 escenarios simulados** por modelo mediante Montecarlo.

---

## 🔍 Metodología

| Fase | Descripción | Herramientas |
|---|---|---|
| 1. Scraping | Recolección de precios de MercadoLibre (3.690 registros) | Playwright, BeautifulSoup |
| 2. Limpieza | Normalización de monedas, outliers con IQR, tipo de cambio en tiempo real | pandas, dolarhoy.com |
| 3. EDA | Análisis exploratorio de precios y km por modelo | matplotlib, seaborn |
| 4. Modelo de costos | TCO mensual: combustible, amortización, seguro, patente | Python |
| 5. Montecarlo | 10.000 escenarios por modelo con variables inciertas | NumPy |
| 6. Sensibilidad | Tornado chart de impacto de cada variable | matplotlib |
| 7. Scoring | Ranking multicriterio por perfil de conductor | pandas |
| 8. Dashboard | App interactiva con parámetros configurables | Streamlit |

---

## 📊 Datos

- **Fuente:** MercadoLibre Argentina — sección autos usados
- **Período de scraping:** 1er mitad de 2026
- **Registros totales:** 3.780 publicaciones scrapeadas → 3.690 tras limpieza
- **Modelos analizados:** 13 (de 16 originales, se excluyeron los sin mercado de usados representativo)
- **Tipo de cambio:** dólar blue scrapeado en tiempo real desde dolarhoy.com

---

## 📁 Estructura del proyecto

    cabify-rentabilidad-argentina/
    ├── data/
    │   ├── raw/                    # Datos crudos scrapeados
    │   ├── processed/              # Datasets limpios
    │   └── external/               # Datos de fuentes externas
    ├── notebooks/
    │   ├── 01_scraping.ipynb       # Scraping de MercadoLibre
    │   ├── 02_limpieza_EDA.ipynb   # Limpieza y análisis exploratorio
    │   ├── 03_modelo_costos.ipynb  # Modelo de rentabilidad
    │   ├── 04_montecarlo.ipynb     # Simulación de Montecarlo
    │   └── 05_scoring.ipynb        # Scoring multicriterio
    ├── src/
    │   ├── scraper.py              # Spider de MercadoLibre
    │   └── modelo.py               # Función de cálculo de rentabilidad
    ├── reports/figures/            # Gráficos generados
    ├── dashboard/
    │   └── app.py                  # App Streamlit
    └── requirements.txt

---

## 🛠️ Stack tecnológico

- **Lenguaje:** Python 3.11
- **Datos:** pandas · numpy · scipy
- **Scraping:** Playwright · BeautifulSoup · requests
- **Visualización:** matplotlib · seaborn · plotly
- **Modelado:** scikit-learn · NumPy (Montecarlo)
- **Dashboard:** Streamlit
- **Deploy:** Streamlit Cloud

---

## 🚀 Cómo ejecutar el proyecto localmente

```bash
# 1. Clonar el repo
git clone https://github.com/francataldi/cabify-rentabilidad-argentina.git

# 2. Crear y activar el entorno
conda create -n cabify-ds python=3.11.8
conda activate cabify-ds
pip install -r requirements.txt

# 3. Correr el scraper (opcional — el dataset ya está incluido)
python src/scraper.py

# 4. Abrir los notebooks
jupyter lab

# 5. Correr el dashboard
streamlit run dashboard/app.py
```

---

## 👤 Autor

**Franco Cataldi Gagliardi**

Estudiante de Ciencia de Datos — Universidad de Buenos Aires (UBA)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Franco_Cataldi-blue?logo=linkedin)](https://www.linkedin.com/in/franco-cataldi-gagliardi-2347a9268/)
[![GitHub](https://img.shields.io/badge/GitHub-francataldi-black?logo=github)](https://github.com/francataldi)
