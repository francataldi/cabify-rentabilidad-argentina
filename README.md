# 🚗 Análisis de Rentabilidad de Vehículos para Cabify en Argentina

## 🏆 Resultado principal
El **VW Gol con GNC** es el auto más rentable para Cabify en AMBA:
- Ganancia neta mensual: ~$926 USD
- Recupero de inversión: 6.6 meses
- Ventaja clave: combina el precio de entrada más bajo con el combustible más barato

## 📌 Descripción
Proyecto de Data Science que analiza qué vehículo es más rentable para trabajar
en plataformas de ride-hailing (Cabify) en Argentina, considerando costos de
adquisición, combustible, mantenimiento, depreciación y simulación de escenarios
macroeconómicos.

## 🎯 Objetivo
Construir un modelo de rentabilidad completo que permita a cualquier conductor
tomar una decisión informada sobre qué auto comprar para maximizar sus ingresos netos.

## 🔍 Metodología
- Recolección de datos via web scraping (MercadoLibre, precios de combustible)
- Análisis Exploratorio de Datos (EDA)
- Modelo de costos y TCO (Total Cost of Ownership)
- Simulación de Montecarlo (10.000 escenarios)
- Análisis de sensibilidad
- Scoring multicriterio

## 📁 Estructura del proyecto
    cabify-rentabilidad-argentina/
    ├── data/
    │   ├── raw/          # Datos crudos sin procesar
    │   ├── processed/    # Datos limpios
    │   └── external/     # Datos de fuentes externas
    ├── notebooks/        # Jupyter notebooks de análisis
    ├── src/              # Código fuente
    ├── reports/          # Reportes y gráficos
    ├── dashboard/        # App Streamlit
    └── requirements.txt

## 🛠️ Stack tecnológico
- **Python 3.11** · pandas · numpy · scikit-learn
- **Visualización:** matplotlib · seaborn · plotly
- **Dashboard:** Streamlit
- **Scraping:** Playwright · BeautifulSoup

## 🚀 Cómo ejecutar el proyecto
    conda activate cabify-ds
    pip install -r requirements.txt
    jupyter lab

## 📊 Dashboard interactivo
🚀 **[Ver dashboard en vivo](https://cabify-rentabilidad-argentina.streamlit.app)**

Permite configurar parámetros personalizados (km diarios, precio de nafta, GNC, seguro)
y obtener un ranking de rentabilidad en tiempo real para tu perfil de conductor.

## 👤 Autor
Franco Cataldi Gagliardi · [LinkedIn](https://www.linkedin.com/in/franco-cataldi-gagliardi-2347a9268/) · [GitHub](https://github.com/francataldi).
