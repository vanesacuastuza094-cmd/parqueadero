
from django.test import TestCase
from django.urls import reverse
from .models import Vehiculo, TipoVehiculo


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
