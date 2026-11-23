
import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://127.0.0.1:8000/"
LIMITE_SEGUNDOS = 3
NUMERO_MEDICIONES = 5

# Carpeta para guardar evidencias
EVIDENCIAS = Path(__file__).resolve().parent / "evidencias"
EVIDENCIAS.mkdir(exist_ok=True)

# Credenciales de prueba
USUARIO = os.environ.get("PARKCONTROL_TEST_USER")
CONTRASENA = os.environ.get("PARKCONTROL_TEST_PASSWORD")

if not USUARIO or not CONTRASENA:
    raise SystemExit(
        "Primero configura las credenciales de prueba."
    )

driver = None

try:
    # Abrir Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()
    espera = WebDriverWait(driver, 10)

    # PASO 1: abrir ParkControl
    driver.get(URL)

    espera.until(
        EC.url_contains("/login/")
    )

    print("Paso 1: ParkControl abierto.")

    # PASO 2: iniciar sesión
    usuario = driver.find_element(
        By.CSS_SELECTOR,
        "input[name='username']"
    )

    contrasena = driver.find_element(
        By.CSS_SELECTOR,
        "input[type='password']"
    )

    usuario.send_keys(USUARIO)
    contrasena.send_keys(CONTRASENA)

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    espera.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//h1[contains(., 'Gestión del parqueadero')]"
            )
        )
    )

    print("Paso 2: inicio de sesión correcto.")

    # PASO 3: medir el tiempo de carga
    tiempos = []

    for numero in range(1, NUMERO_MEDICIONES + 1):

        inicio = time.perf_counter()

        driver.get(URL)

        espera.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(., 'Gestión del parqueadero')]"
                )
            )
        )

        fin = time.perf_counter()
        duracion = fin - inicio

        tiempos.append(duracion)

        print(
            f"Medición {numero}: {duracion:.3f} segundos"
        )

    # PASO 4: calcular promedio
    promedio = sum(tiempos) / len(tiempos)

    print("-----------------------------")
    print(f"Tiempo promedio: {promedio:.3f} segundos")
    print(f"Tiempo mínimo: {min(tiempos):.3f} segundos")
    print(f"Tiempo máximo: {max(tiempos):.3f} segundos")
    print(f"Límite establecido: {LIMITE_SEGUNDOS} segundos")

    # Guardar captura del panel
    driver.save_screenshot(
        str(EVIDENCIAS / "REN-001_panel.png")
    )

    # PASO 5: comprobar el resultado
    assert promedio <= LIMITE_SEGUNDOS, (
        "El tiempo promedio superó el límite establecido."
    )

    print("PRUEBA REN-001 APROBADA")

except Exception as error:
    print("PRUEBA REN-001 FALLIDA")
    print("Error:", error)

    if driver is not None:
        driver.save_screenshot(
            str(EVIDENCIAS / "REN-001_error.png")
        )

finally:
    if driver is not None:
        driver.quit()
