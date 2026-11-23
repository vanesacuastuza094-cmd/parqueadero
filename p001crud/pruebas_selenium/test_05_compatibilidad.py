
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
        "Configura las credenciales de prueba."
    )


# FUNCIÓN PARA PROBAR CADA NAVEGADOR
def probar_navegador(nombre, crear_driver):

    driver = None

    try:
        print("-----------------------------")
        print(f"Probando navegador: {nombre}")

        # PASO 1: abrir navegador
        driver = crear_driver()
        driver.maximize_window()

        espera = WebDriverWait(driver, 10)

        # PASO 2: abrir ParkControl
        driver.get(URL)

        espera.until(
            EC.url_contains("/login/")
        )

        print("Paso 1: formulario de acceso encontrado.")

        # PASO 3: iniciar sesión
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

        # PASO 4: verificar panel principal
        encabezado = espera.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(., 'Gestión del parqueadero')]"
                )
            )
        )

        assert encabezado.is_displayed()
        assert "/login/" not in driver.current_url

        print("Paso 2: inicio de sesión correcto.")
        print("Paso 3: panel principal visible.")

        # PASO 5: verificar módulos principales
        modulos = [
            "Gestión de clientes",
            "Gestión de vehículos",
            "Gestión de tarifas",
            "Registro de ingresos",
            "Registro de salidas",
            "Gestión de empleados"
        ]

        for modulo in modulos:
            elemento = driver.find_element(
                By.XPATH,
                f"//a[contains(@class, 'boton-acceso') "
                f"and .//strong[contains(., '{modulo}')]]"
            )

            assert elemento.is_displayed(), (
                f"No se encontró el módulo: {modulo}"
            )

        print("Paso 4: módulos principales visibles.")

        # Guardar captura de evidencia
        nombre_archivo = (
            f"COM-001_{nombre.lower().replace(' ', '_')}.png"
        )

        driver.save_screenshot(
            str(EVIDENCIAS / nombre_archivo)
        )

        print("Paso 5: evidencia guardada.")
        print(f"PRUEBA COM-001 {nombre}: APROBADA")

        return True

    except Exception as error:
        print(f"PRUEBA COM-001 {nombre}: FALLIDA")
        print("Error:", error)

        if driver is not None:
            driver.save_screenshot(
                str(
                    EVIDENCIAS /
                    f"COM-001_error_{nombre.lower().replace(' ', '_')}.png"
                )
            )

        return False

    finally:
        if driver is not None:
            driver.quit()


# EJECUTAR EN CHROME
resultado_chrome = probar_navegador(
    "Google Chrome",
    webdriver.Chrome
)

# EJECUTAR EN EDGE
resultado_edge = probar_navegador(
    "Microsoft Edge",
    webdriver.Edge
)


# RESULTADO GENERAL
print("-----------------------------")

if resultado_chrome and resultado_edge:
    print("PRUEBA COM-001 APROBADA")
    print("ParkControl funciona en ambos navegadores.")
else:
    print("PRUEBA COM-001 FALLIDA")
    print("Revisar los resultados de cada navegador.")
