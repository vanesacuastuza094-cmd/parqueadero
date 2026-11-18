
from django.shortcuts import render
from .models import Cliente, Vehiculo, IngresoSalida, TipoVehiculo


def inicio(request):
    contexto = {
        "clientes": Cliente.objects.count(),
        "vehiculos": Vehiculo.objects.count(),
        "dentro": IngresoSalida.objects.filter(
            fecha_salida__isnull=True
        ).count(),
        "tipos": TipoVehiculo.objects.filter(
            estado=True
        ).count(),
        "ultimos": IngresoSalida.objects.select_related(
            "vehiculo"
        ).order_by("-fecha_entrada")[:5],
    }

    return render(request, "crud/inicio.html", contexto)
