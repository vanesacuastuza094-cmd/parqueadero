
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# CONFIGURACIÓN
URL = "http://127.0.0.1:8000/"

EVIDENCIAS = Path(__file__).resolve().parent / "evidencias"
EVIDENCIAS.mkdir(exist_ok=True)

USUARIO = os.environ.get("PARKCONTROL_TEST_USER")
CONTRASENA = os.environ.get("PARKCONTROL_TEST_PASSWORD")

if not USUARIO or not CONTRASENA:
    raise SystemExit(
        "Configura el usuario y la contraseña de prueba."
    )

driver = None

try:
    # PASO 1: ABRIR CHROME E INICIAR SESIÓN
    driver = webdriver.Chrome()
    driver.maximize_window()

    espera = WebDriverWait(driver, 10)

    driver.get(URL)

    espera.until(
        EC.url_contains("/login/")
    )

    driver.find_element(
        By.CSS_SELECTOR,
        "input[name='username']"
    ).send_keys(USUARIO)

    driver.find_element(
        By.CSS_SELECTOR,
        "input[type='password']"
    ).send_keys(CONTRASENA)

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

    print("Paso 1: sesión iniciada correctamente.")

    # PASO 2: ABRIR GESTIÓN DE CLIENTES
    enlace_clientes = espera.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[contains(@class, 'boton-acceso') "
                "and .//strong[contains(., 'Gestión de clientes')]]"
            )
        )
    )

    enlace_clientes.click()

    print("Paso 2: módulo de clientes abierto.")

    # PASO 3: ABRIR REGISTRO DE CLIENTES
    enlace_registro = espera.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[contains(., 'Registrar') "
                "or contains(., 'Nuevo cliente') "
                "or contains(., 'Agregar cliente')]"
            )
        )
    )

    enlace_registro.click()

    encabezado = espera.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//h1[contains(., 'Registrar nuevo cliente')]"
            )
        )
    )

    assert encabezado.is_displayed()

    print("Paso 3: formulario de registro encontrado.")

    # PASO 4: VERIFICAR LOS CAMPOS Y BOTONES
    formulario = driver.find_element(
        By.CSS_SELECTOR,
        "form.formulario-cliente"
    )

    campos = formulario.find_elements(
        By.CSS_SELECTOR,
        "input:not([type='hidden']), select, textarea"
    )

    campos_visibles = [
        campo for campo in campos
        if campo.is_displayed()
    ]

    assert len(campos_visibles) > 0, (
        "No se encontraron campos visibles."
    )

    boton_guardar = formulario.find_element(
        By.XPATH,
        ".//button[contains(., 'Guardar cliente')]"
    )

    boton_cancelar = formulario.find_element(
        By.LINK_TEXT,
        "Cancelar"
    )

    assert boton_guardar.is_displayed()
    assert boton_cancelar.is_displayed()

    print("Paso 4: campos y botones disponibles.")
    print("Cantidad de campos visibles:", len(campos_visibles))

    # PASO 5: VERIFICAR LAS INSTRUCCIONES
    instrucciones = driver.find_element(
        By.XPATH,
        "//p[contains(., 'Completa los datos para registrar un cliente')]"
    )

    assert instrucciones.is_displayed()

    print("Paso 5: instrucciones visibles.")

    # GUARDAR EVIDENCIA
    driver.save_screenshot(
        str(EVIDENCIAS / "USA-001_formulario.png")
    )

    print("--------------------------------")
    print("PRUEBA AUTOMATIZADA USA-001 APROBADA")
    print("Evidencia guardada correctamente.")

except Exception as error:
    print("--------------------------------")
    print("PRUEBA AUTOMATIZADA USA-001 FALLIDA")
    print("Error:", error)

    if driver is not None:
        driver.save_screenshot(
            str(EVIDENCIAS / "USA-001_error.png")
        )

finally:
    if driver is not None:
        driver.quit()
