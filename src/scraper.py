import random
import time

import pandas as pd
from playwright.sync_api import sync_playwright

MODELOS = {
    "toyota/etios": "Toyota Etios",
    "toyota/corolla": "Toyota Corolla",
    "toyota/yaris": "Toyota Yaris",
    "chevrolet/onix-plus": "Chevrolet Onix Plus",
    "chevrolet/prisma": "Chevrolet Prisma",
    "fiat/cronos": "Fiat Cronos",
    "renault/logan": "Renault Logan",
    "volkswagen/virtus": "VW Virtus",
    "volkswagen/voyage": "VW Voyage",
    "nissan/versa": "Nissan Versa",
    "fiat/siena": "Fiat Siena",
    "volkswagen/polo": "VW Polo",
    "volkswagen/gol": "VW Gol",
    "ford/fiesta": "Ford Fiesta",
    "ford/ka": "Ford Ka",
    "peugeot/208": "Peugeot 208",
}

def scrape_modelo(page, slug, nombre, paginas=5):
    resultados = []

    for pagina in range(1, paginas + 1):
        offset = (pagina - 1) * 48
        if pagina == 1:
            url = f"https://autos.mercadolibre.com.ar/{slug}/"
        else:
            url = f"https://autos.mercadolibre.com.ar/{slug}/_Desde_{offset + 1}_NoIndex_True"

        try:
            page.goto(url, timeout=30000)
            page.wait_for_selector("li.ui-search-layout__item", timeout=15000)
            publicaciones = page.query_selector_all("li.ui-search-layout__item")

            for pub in publicaciones:
                try:
                    titulo_el = pub.query_selector("a.poly-component__title")
                    titulo = titulo_el.inner_text() if titulo_el else None
                    
                    precio_el = pub.query_selector("span.andes-money-amount__fraction")
                    precio_txt = precio_el.inner_text() if precio_el else None
                    precio = float(precio_txt.replace(".", "").replace(",", ".")) if precio_txt else None

                    moneda_el = pub.query_selector("span.andes-money-amount__currency-symbol")
                    moneda = moneda_el.inner_text().strip() if moneda_el else None

                    atributos = pub.query_selector_all("li.poly-attributes_list__item")
                    año = atributos[0].inner_text().strip() if len(atributos) > 0 else None
                    km = atributos[1].inner_text().strip() if len(atributos) > 1 else None

                    ubicacion_el = pub.query_selector("span.poly-component__location")
                    ubicacion = ubicacion_el.inner_text().strip() if ubicacion_el else None

                    resultados.append({
                        "modelo": nombre,
                        "titulo": titulo,
                        "precio": precio,
                        "moneda": moneda,
                        "año": año,
                        "km": km,
                        "ubicacion": ubicacion
                    })
                except:
                    continue

        except Exception as e:
            print(f"  ⚠ Error en {nombre} página {pagina}: {e}")

        time.sleep(random.uniform(2.0, 4.0))

    return resultados


def main():
    todos = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="es-AR",
        )
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = context.new_page()

        for slug, nombre in MODELOS.items():
            print(f"Scrapeando {nombre}...")
            datos = scrape_modelo(page, slug, nombre)
            todos.extend(datos)
            print(f"  → {len(datos)} publicaciones encontradas")

        browser.close()

    df = pd.DataFrame(todos)
    df.to_csv("data/raw/precios_autos_raw.csv", index=False)
    print(f"\nTotal: {len(df)} registros guardados en data/raw/precios_autos_raw.csv")


if __name__ == "__main__":
    main()