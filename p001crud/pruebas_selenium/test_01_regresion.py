
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Dirección de ParkControl
URL = "http://127.0.0.1:8000/"

# Carpeta donde guardaremos las capturas
CARPETA_EVIDENCIAS = (
    Path(__file__).resolve().parent / "evidencias"
)
CARPETA_EVIDENCIAS.mkdir(exist_ok=True)

# Credenciales de una cuenta de prueba
USUARIO = os.environ.get("PARKCONTROL_TEST_USER")
CONTRASENA = os.environ.get("PARKCONTROL_TEST_PASSWORD")

if not USUARIO or not CONTRASENA:
    raise SystemExit(
        "Debes configurar el usuario y la contraseña "
        "de prueba antes de ejecutar Selenium."
    )

driver = webdriver.Chrome()
driver.maximize_window()

try:
    # PASO 1: abrir ParkControl
    driver.get(URL)

    espera = WebDriverWait(driver, 10)

    # PASO 2: esperar el formulario de acceso
    espera.until(
        EC.url_contains("/login/")
    )

    print("Paso 1: formulario de inicio de sesión abierto.")

    # Captura 1: formulario inicial
    driver.save_screenshot(
        str(CARPETA_EVIDENCIAS / "REG-001_antes.png")
    )

    # PASO 3: buscar los campos
    campo_usuario = driver.find_element(
        By.CSS_SELECTOR,
        "input[name='username']"
    )

    campo_contrasena = driver.find_element(
        By.CSS_SELECTOR,
        "input[type='password']"
    )

    # Escribir las credenciales
    campo_usuario.send_keys(USUARIO)
    campo_contrasena.send_keys(CONTRASENA)

    print("Paso 2: credenciales ingresadas.")

    # PASO 4: presionar iniciar sesión
    boton = driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    )

    boton.click()

    print("Paso 3: botón de inicio de sesión presionado.")

    # PASO 5: comprobar que entramos al panel
    espera.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h1[contains(., 'Gestión del parqueadero')]")
        )
    )

    assert "/login/" not in driver.current_url

    # Captura 2: panel principal
    driver.save_screenshot(
        str(CARPETA_EVIDENCIAS / "REG-001_despues.png")
    )

    print("Paso 4: panel principal encontrado.")
    print("PRUEBA REG-001 APROBADA")

except Exception as error:
    print("PRUEBA REG-001 FALLIDA")
    print("Error:", error)

    # Guardar evidencia del error
    driver.save_screenshot(
        str(CARPETA_EVIDENCIAS / "REG-001_error.png")
    )

finally:
    driver.quit()
