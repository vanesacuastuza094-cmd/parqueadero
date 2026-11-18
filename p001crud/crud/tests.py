
from django.test import TestCase
from django.urls import reverse
from .models import Vehiculo, TipoVehiculo, Cliente



class PanelPrincipalTests(TestCase):

    def test_pagina_principal_responde(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertEqual(respuesta.status_code, 200)

    def test_pagina_muestra_titulo(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertContains(
            respuesta,
            "Gestión del parqueadero"
        )

    def test_pagina_sin_movimientos(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertContains(
            respuesta,
            "Todavía no hay movimientos registrados."
        )

    def test_representacion_vehiculo(self):
        tipo = TipoVehiculo.objects.create(nombre="Carro")

        vehiculo = Vehiculo.objects.create(
            placa="ABC123",
            tipo_vehiculo=tipo,
            marca="Renault",
            color="Blanco"
        )

        self.assertIn("ABC123", str(vehiculo))
        self.assertIn("Renault", str(vehiculo))

    
def test_boton_gestion_clientes(self):
    respuesta = self.client.get(reverse("inicio"))

    self.assertContains(
        respuesta,
        reverse("lista_clientes")
    )

    self.assertContains(
        respuesta,
        "Gestión de clientes"
    )



class GestionClientesTests(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(
            tipo_identificacion="CC",
            identificacion="123456789",
            nombre="Carlos",
            apellido="Perez",
            direccion="Calle 10",
            telefono="3001234567",
        )

    def test_pagina_clientes_responde(self):
        respuesta = self.client.get(
            reverse("lista_clientes")
        )
        self.assertEqual(respuesta.status_code, 200)

    def test_mostrar_cliente_registrado(self):
        respuesta = self.client.get(
            reverse("lista_clientes")
        )
        self.assertContains(respuesta, "Carlos")
        self.assertContains(respuesta, "123456789")

    def test_buscar_cliente_por_nombre(self):
        respuesta = self.client.get(
            reverse("lista_clientes"),
            {"buscar": "Carlos"}
        )
        self.assertContains(respuesta, "Carlos")

    def test_buscar_cliente_inexistente(self):
        respuesta = self.client.get(
            reverse("lista_clientes"),
            {"buscar": "NombreInexistente"}
        )
        self.assertContains(
            respuesta,
            "No se encontraron clientes."
        )
        self.assertNotContains(respuesta, "Carlos")
