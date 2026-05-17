import requests
from bs4 import BeautifulSoup


def get_precios_combustible():
    """
    Obtiene precios de nafta super en CABA desde surtidores.com.ar
    Retorna dict con 'nafta_super' y 'gnc' en ARS
    """
    FALLBACK = {"nafta_super": 2034, "gnc": 540}

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-AR,es;q=0.9",
        }
        response = requests.get(
            "https://www.surtidores.com.ar/precios/",
            headers=headers,
            timeout=15
        )
        soup = BeautifulSoup(response.text, "html.parser")

        filas = soup.find_all("tr")
        for fila in filas:
            celdas = fila.find_all("td")
            if not celdas:
                continue
            texto_primera = celdas[0].get_text(strip=True).lower()
            if "super" in texto_primera or "súper" in texto_primera:
                valores = [c.get_text(strip=True) for c in celdas[1:]]
                valores = [v for v in valores if v and v.replace(".", "").replace(",", "").isdigit()]
                if valores:
                    ultimo = valores[-1].replace(".", "").replace(",", ".")
                    precio_super = float(ultimo)
                    return {"nafta_super": precio_super, "gnc": FALLBACK["gnc"]}

        return FALLBACK

    except Exception as e:
        print(f"Error scrapeando combustible: {e}")
        return FALLBACK


if __name__ == "__main__":
    precios = get_precios_combustible()
    print(f"Resultado: {precios}")