
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Vehiculo, IngresoSalida, TipoVehiculo
from .forms import ClienteForm

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


