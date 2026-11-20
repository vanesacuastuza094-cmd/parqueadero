
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Vehiculo, IngresoSalida, TipoVehiculo, Tarifa
from .forms import ClienteForm, VehiculoForm, TarifaForm
from django.utils import timezone
from django.db import transaction
from .models import Empleado, Tarifa
from .forms import IngresoForm

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


from django.db.models import Q


def lista_clientes(request):
    busqueda = request.GET.get("buscar", "").strip()

    clientes = Cliente.objects.all().order_by("nombre", "apellido")

    if busqueda:
        clientes = clientes.filter(
            Q(identificacion__icontains=busqueda)
            | Q(nombre__icontains=busqueda)
            | Q(apellido__icontains=busqueda)
        )

    contexto = {
        "clientes_lista": clientes,
        "busqueda": busqueda,
        "total_clientes": clientes.count(),
    }

    return render(request, "crud/clientes.html", contexto)



def registrar_cliente(request):

    if request.method == "POST":
        formulario = ClienteForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect("lista_clientes")

    else:
        formulario = ClienteForm()

    contexto = {
        "formulario": formulario
    }

    return render(
        request,
        "crud/registrar_cliente.html",
        contexto
    )


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == "POST":
        formulario = ClienteForm(request.POST, instance=cliente)

        if formulario.is_valid():
            formulario.save()
            return redirect("lista_clientes")
    else:
        formulario = ClienteForm(instance=cliente)

    return render(
        request,
        "crud/editar_cliente.html",
        {
            "formulario": formulario,
            "cliente": cliente,
        }
    )


def lista_vehiculos(request):
    busqueda = request.GET.get("buscar", "").strip()

    vehiculos = Vehiculo.objects.select_related(
        "cliente", "tipo_vehiculo"
    ).order_by("placa")

    if busqueda:
        vehiculos = vehiculos.filter(
            Q(placa__icontains=busqueda)
            | Q(marca__icontains=busqueda)
            | Q(color__icontains=busqueda)
            | Q(cliente__nombre__icontains=busqueda)
            | Q(cliente__apellido__icontains=busqueda)
            | Q(cliente__identificacion__icontains=busqueda)
        )

    return render(
        request,
        "crud/vehiculos.html",
        {
            "vehiculos_lista": vehiculos,
            "busqueda": busqueda,
            "total_vehiculos": vehiculos.count(),
        }
    )


def registrar_vehiculo(request):
    if request.method == "POST":
        formulario = VehiculoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect("lista_vehiculos")
    else:
        formulario = VehiculoForm()

    return render(
        request,
        "crud/registrar_vehiculo.html",
        {"formulario": formulario}
    )


def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)

    if request.method == "POST":
        formulario = VehiculoForm(
            request.POST,
            instance=vehiculo
        )

        if formulario.is_valid():
            formulario.save()
            return redirect("lista_vehiculos")
    else:
        formulario = VehiculoForm(instance=vehiculo)

    return render(
        request,
        "crud/editar_vehiculo.html",
        {
            "formulario": formulario,
            "vehiculo": vehiculo,
        }
    )


def lista_tarifas(request):
    busqueda = request.GET.get("buscar", "").strip()

    tarifas = Tarifa.objects.select_related(
        "tipo_vehiculo"
    ).order_by("tipo_vehiculo__nombre", "tiempo")

    if busqueda:
        tarifas = tarifas.filter(
            Q(tipo_vehiculo__nombre__icontains=busqueda)
            | Q(tiempo__icontains=busqueda)
        )

    return render(
        request,
        "crud/tarifas.html",
        {
            "tarifas_lista": tarifas,
            "busqueda": busqueda,
            "total_tarifas": tarifas.count(),
        }
    )


def registrar_tarifa(request):
    if request.method == "POST":
        formulario = TarifaForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect("lista_tarifas")
    else:
        formulario = TarifaForm()

    return render(
        request,
        "crud/registrar_tarifa.html",
        {"formulario": formulario}
    )


def editar_tarifa(request, tarifa_id):
    tarifa = get_object_or_404(Tarifa, pk=tarifa_id)

    if request.method == "POST":
        formulario = TarifaForm(
            request.POST,
            instance=tarifa
        )

        if formulario.is_valid():
            formulario.save()
            return redirect("lista_tarifas")
    else:
        formulario = TarifaForm(instance=tarifa)

    return render(
        request,
        "crud/editar_tarifa.html",
        {
            "formulario": formulario,
            "tarifa": tarifa,
        }
    )


def lista_ingresos(request):
    busqueda = request.GET.get("buscar", "").strip()

    ingresos = IngresoSalida.objects.filter(
        fecha_salida__isnull=True
    ).select_related(
        "vehiculo",
        "cliente",
        "empleado",
        "tarifa"
    ).order_by("-fecha_entrada")

    if busqueda:
        ingresos = ingresos.filter(
            Q(vehiculo__placa__icontains=busqueda)
            | Q(numero_recibo__icontains=busqueda)
            | Q(cliente__nombre__icontains=busqueda)
            | Q(cliente__apellido__icontains=busqueda)
        )

    return render(
        request,
        "crud/ingresos.html",
        {
            "ingresos_lista": ingresos,
            "busqueda": busqueda,
            "total_ingresos": ingresos.count(),
        }
    )


def registrar_ingreso(request):
    if request.method == "POST":
        formulario = IngresoForm(request.POST)

        if formulario.is_valid():
            vehiculo = formulario.cleaned_data["vehiculo"]
            empleado = formulario.cleaned_data["empleado"]
            tarifa = formulario.cleaned_data["tarifa"]

            with transaction.atomic():
                # Bloquear el vehículo durante el registro.
                vehiculo = Vehiculo.objects.select_for_update().get(
                    pk=vehiculo.pk
                )

                ya_dentro = IngresoSalida.objects.filter(
                    vehiculo=vehiculo,
                    fecha_salida__isnull=True
                ).exists()

                if ya_dentro:
                    formulario.add_error(
                        None,
                        "Este vehículo ya tiene un ingreso activo."
                    )
                else:
                    IngresoSalida.objects.create(
                        vehiculo=vehiculo,
                        empleado=empleado,
                        cliente=vehiculo.cliente,
                        tarifa=tarifa,
                        fecha_entrada=timezone.now(),
                        tiempo_total=0,
                        total_pago=0,
                        estado=True
                    )

                    return redirect("lista_ingresos")
    else:
        formulario = IngresoForm()

    return render(
        request,
        "crud/registrar_ingreso.html",
        {"formulario": formulario}
    )
