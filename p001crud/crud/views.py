
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Vehiculo, IngresoSalida, TipoVehiculo
from .forms import ClienteForm, VehiculoForm
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


