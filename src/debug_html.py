from playwright.sync_api import sync_playwright

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
    page.goto("https://autos.mercadolibre.com.ar/toyota/etios/", timeout=30000)
    page.wait_for_timeout(6000)
    
    html = page.content()
    with open("data/raw/debug_html.txt", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("HTML guardado")
    browser.close()