
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://127.0.0.1:8000/"

EVIDENCIAS = Path(__file__).resolve().parent / "evidencias"
EVIDENCIAS.mkdir(exist_ok=True)

driver = None

try:
    # PASO 1: abrir un navegador nuevo
    driver = webdriver.Chrome()
    driver.maximize_window()

    print("Paso 1: navegador abierto sin iniciar sesión.")

    # PASO 2: intentar acceder al panel directamente
    driver.get(URL)

    print("Paso 2: acceso directo al panel solicitado.")

    # PASO 3: comprobar la redirección
    WebDriverWait(driver, 10).until(
        EC.url_contains("/login/")
    )

    print("Paso 3: redirección al login detectada.")

    # PASO 4: verificar que no se permitió el acceso
    assert "/login/" in driver.current_url

    print("Paso 4: acceso no autorizado bloqueado.")

    # Guardar captura
    driver.save_screenshot(
        str(EVIDENCIAS / "SEG-001_acceso_protegido.png")
    )

    # PASO 5: resultado
    print("PRUEBA SEG-001 APROBADA")

except Exception as error:
    print("PRUEBA SEG-001 FALLIDA")
    print("Error:", error)

    if driver is not None:
        driver.save_screenshot(
            str(EVIDENCIAS / "SEG-001_error.png")
        )

finally:
    if driver is not None:
        driver.quit()
