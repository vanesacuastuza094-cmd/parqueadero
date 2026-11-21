
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Vehiculo, IngresoSalida, TipoVehiculo, Tarifa
from .forms import ClienteForm, VehiculoForm, TarifaForm, EmpleadoForm
from django.utils import timezone
from django.db import transaction
from .models import Empleado, Tarifa
from .forms import IngresoForm
from decimal import Decimal
from datetime import timedelta
from .forms import SalidaForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.views.decorators.http import require_POST
from .forms import CuentaEmpleadoForm, InicioSesionForm


from io import BytesIO
from xml.sax.saxutils import escape

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)


@login_required
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

@login_required
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


@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

def calcular_cobro(ingreso, fecha_salida=None):
    """
    Calcula el cobro usando la tarifa elegida al ingresar.

    Las fracciones de hora, día o mes se cobran
    como una unidad completa.
    """
    if fecha_salida is None:
        fecha_salida = timezone.now()

    diferencia = fecha_salida - ingreso.fecha_entrada

    segundos = max(0, diferencia.total_seconds())

    # Minutos reales transcurridos, redondeados hacia arriba.
    minutos = max(1, -(-int(segundos + 0.999999) // 60))

    modalidad = ingreso.tarifa.tiempo.strip().lower()

    if modalidad in ("hora", "horas"):
        unidades = (minutos + 59) // 60
        descripcion = "hora(s)"

    elif modalidad in ("dia", "día", "dias", "días"):
        unidades = (minutos + 1439) // 1440
        descripcion = "día(s)"

    elif modalidad in ("mes", "meses"):
        # Para este proyecto: cada mes equivale a 30 días.
        minutos_mes = 30 * 24 * 60
        unidades = (minutos + minutos_mes - 1) // minutos_mes
        descripcion = "mes(es) de 30 días"

    else:
        raise ValueError(
            "La modalidad de la tarifa no es válida."
        )

    total = ingreso.tarifa.valor * Decimal(unidades)

    return {
        "minutos": minutos,
        "unidades": unidades,
        "descripcion": descripcion,
        "total": total,
        "fecha_salida": fecha_salida,
    }

@login_required
def lista_salidas(request):
    busqueda = request.GET.get("buscar", "").strip()

    ingresos = IngresoSalida.objects.filter(
        fecha_salida__isnull=True
    ).select_related(
        "vehiculo",
        "cliente",
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
        "crud/salidas.html",
        {
            "ingresos_lista": ingresos,
            "busqueda": busqueda,
            "total_ingresos": ingresos.count(),
        }
    )

@login_required
def registrar_salida(request, ingreso_id):
    ingreso = get_object_or_404(
        IngresoSalida.objects.select_related(
            "vehiculo",
            "cliente",
            "tarifa"
        ),
        pk=ingreso_id,
        fecha_salida__isnull=True
    )

    if request.method == "POST":
        formulario = SalidaForm(request.POST)

        if formulario.is_valid():
            with transaction.atomic():
                # Evitar procesar dos veces una salida.
                ingreso_actual = IngresoSalida.objects.get(
                    pk=ingreso_id
                )

                if ingreso_actual.fecha_salida is not None:
                    return redirect("lista_salidas")

                resultado = calcular_cobro(
                    ingreso_actual,
                    timezone.now()
                )

                ingreso_actual.fecha_salida = (
                    resultado["fecha_salida"]
                )
                ingreso_actual.tiempo_total = (
                    resultado["minutos"]
                )
                ingreso_actual.total_pago = (
                    resultado["total"]
                )
                ingreso_actual.forma_pago_descripcion = (
                    formulario.cleaned_data[
                        "forma_pago_descripcion"
                    ]
                )
                ingreso_actual.estado = False

                ingreso_actual.save()

            return redirect("detalle_salida", ingreso_id=ingreso_id)
    else:
        formulario = SalidaForm()

    resultado = calcular_cobro(ingreso)

    return render(
        request,
        "crud/registrar_salida.html",
        {
            "ingreso": ingreso,
            "formulario": formulario,
            "calculo": resultado,
        }
    )

@login_required
def detalle_salida(request, ingreso_id):
    ingreso = get_object_or_404(
        IngresoSalida.objects.select_related(
            "vehiculo",
            "cliente",
            "tarifa",
            "empleado"
        ),
        pk=ingreso_id,
        fecha_salida__isnull=False
    )

    calculo = calcular_cobro(
        ingreso,
        ingreso.fecha_salida
    )

    return render(
        request,
        "crud/detalle_salida.html",
        {
            "ingreso": ingreso,
            "calculo": calculo,
        }
    )

@login_required
def lista_empleados(request):
    busqueda = request.GET.get("buscar", "").strip()

    empleados = Empleado.objects.all().order_by(
        "nombre", "apellido"
    )

    if busqueda:
        empleados = empleados.filter(
            Q(identificacion__icontains=busqueda)
            | Q(nombre__icontains=busqueda)
            | Q(apellido__icontains=busqueda)
            | Q(telefono__icontains=busqueda)
            | Q(rol__icontains=busqueda)
        )

    return render(
        request,
        "crud/empleados.html",
        {
            "empleados_lista": empleados,
            "busqueda": busqueda,
            "total_empleados": empleados.count(),
        }
    )

@login_required
def registrar_empleado(request):
    if request.method == "POST":
        formulario = EmpleadoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect("lista_empleados")
    else:
        formulario = EmpleadoForm()

    return render(
        request,
        "crud/registrar_empleado.html",
        {"formulario": formulario}
    )

@login_required
def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(
        Empleado,
        pk=empleado_id
    )

    if request.method == "POST":
        formulario = EmpleadoForm(
            request.POST,
            instance=empleado
        )

        if formulario.is_valid():
            formulario.save()
            return redirect("lista_empleados")
    else:
        formulario = EmpleadoForm(instance=empleado)

    return render(
        request,
        "crud/editar_empleado.html",
        {
            "formulario": formulario,
            "empleado": empleado,
        }
    )

def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        formulario = InicioSesionForm(
            request,
            data=request.POST
        )

        if formulario.is_valid():
            usuario = formulario.get_user()

            try:
                empleado = usuario.empleado_parkcontrol
            except Empleado.DoesNotExist:
                formulario.add_error(
                    None,
                    "Este usuario no tiene un empleado asociado."
                )
            else:
                if not empleado.estado:
                    formulario.add_error(
                        None,
                        "La cuenta del empleado está inactiva."
                    )
                else:
                    login(request, usuario)
                    return redirect("inicio")
    else:
        formulario = InicioSesionForm(request)

    return render(
        request,
        "crud/login.html",
        {"formulario": formulario}
    )


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect("iniciar_sesion")


@staff_member_required(login_url="iniciar_sesion")
def crear_cuenta_empleado(request):
    if request.method == "POST":
        formulario = CuentaEmpleadoForm(request.POST)

        if formulario.is_valid():
            with transaction.atomic():
                empleado = Empleado.objects.select_for_update().get(
                    pk=formulario.cleaned_data["empleado"].pk
                )

                if empleado.usuario_django_id:
                    formulario.add_error(
                        "empleado",
                        "Este empleado ya tiene una cuenta."
                    )
                else:
                    usuario = User.objects.create_user(
                        username=formulario.cleaned_data["username"],
                        password=formulario.cleaned_data["password"]
                    )

                    empleado.usuario_django = usuario
                    empleado.save(
                        update_fields=["usuario_django"]
                    )

                    return redirect("lista_empleados")
    else:
        formulario = CuentaEmpleadoForm()

    return render(
        request,
        "crud/crear_cuenta_empleado.html",
        {"formulario": formulario}
    )



@login_required
def descargar_recibo(request, ingreso_id):
    ingreso = get_object_or_404(
        IngresoSalida.objects.select_related(
            "vehiculo__tipo_vehiculo",
            "cliente",
            "tarifa",
            "empleado"
        ),
        pk=ingreso_id,
        fecha_salida__isnull=False
    )

    # FUNCIONES AUXILIARES

    def seguro(valor):
        return escape(str(valor if valor is not None else ""))

    def fecha_local(valor):
        if not valor:
            return "No registrada"
        return timezone.localtime(valor).strftime("%d/%m/%Y %H:%M")

    def moneda(valor):
        numero = f"{valor:,.0f}"
        return "$ " + numero.replace(",", ".")

    def duracion(minutos):
        horas, minutos_restantes = divmod(int(minutos), 60)
        if horas:
            return f"{horas} h {minutos_restantes} min"
        return f"{minutos_restantes} min"

    calculo = calcular_cobro(
        ingreso,
        ingreso.fecha_salida
    )

    # COLORES DEL RECIBO

    azul = colors.HexColor("#102E43")
    verde = colors.HexColor("#25B98A")
    gris = colors.HexColor("#657987")
    claro = colors.HexColor("#EDF3F5")
    blanco = colors.white

    # ESTILOS DE TEXTO

    estilo_marca = ParagraphStyle(
        "MarcaRecibo",
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=23,
        textColor=blanco,
        alignment=TA_LEFT
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloRecibo",
        fontName="Helvetica",
        fontSize=7,
        leading=10,
        textColor=colors.HexColor("#C5D7DF")
    )

    estilo_seccion = ParagraphStyle(
        "SeccionRecibo",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=azul,
        spaceBefore=12,
        spaceAfter=7
    )

    estilo_etiqueta = ParagraphStyle(
        "EtiquetaRecibo",
        fontName="Helvetica",
        fontSize=7,
        leading=10,
        textColor=gris
    )

    estilo_valor = ParagraphStyle(
        "ValorRecibo",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=azul
    )

    estilo_total = ParagraphStyle(
        "TotalRecibo",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=23,
        alignment=TA_CENTER,
        textColor=verde
    )

    estilo_centrado = ParagraphStyle(
        "CentradoRecibo",
        fontName="Helvetica",
        fontSize=8,
        leading=12,
        alignment=TA_CENTER,
        textColor=gris
    )

    # FUNCIÓN PARA CREAR FILAS

    def dato(etiqueta, valor):
        return [
            Paragraph(seguro(etiqueta), estilo_etiqueta),
            Paragraph(seguro(valor), estilo_valor)
        ]

    # CONFIGURACIÓN DEL PDF

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=(100 * mm, 270 * mm),
        leftMargin=9 * mm,
        rightMargin=9 * mm,
        topMargin=8 * mm,
        bottomMargin=8 * mm,
        title=f"Recibo {ingreso.numero_recibo}",
        author="ParkControl"
    )

    contenido = []

    # =====================================
    # ENCABEZADO PARKCONTROL
    # =====================================

    marca = Table(
        [[
            [
                Paragraph("PARKCONTROL", estilo_marca),
                Paragraph(
                    "SISTEMA DE GESTION DE PARQUEADERO",
                    estilo_subtitulo
                )
            ]
        ]],
        colWidths=[82 * mm]
    )

    marca.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), azul),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))

    contenido.append(marca)
    contenido.append(Spacer(1, 7 * mm))

    # =====================================
    # NÚMERO DEL RECIBO
    # =====================================

    contenido.append(
        Paragraph(
            "COMPROBANTE DE PAGO",
            estilo_seccion
        )
    )

    contenido.append(
        Paragraph(
            f"<b>{seguro(ingreso.numero_recibo)}</b>",
            estilo_valor
        )
    )

    contenido.append(Spacer(1, 5 * mm))

    # =====================================
    # DATOS DEL VEHÍCULO Y CLIENTE
    # =====================================

    contenido.append(
        Paragraph(
            "VEHICULO Y CLIENTE",
            estilo_seccion
        )
    )

    datos_vehiculo = [
        dato(
            "Placa",
            ingreso.vehiculo.placa
        ),
        dato(
            "Tipo de vehiculo",
            ingreso.vehiculo.tipo_vehiculo.nombre
        ),
        dato(
            "Cliente",
            f"{ingreso.cliente.nombre} "
            f"{ingreso.cliente.apellido}"
        ),
    ]

    tabla_vehiculo = Table(
        datos_vehiculo,
        colWidths=[31 * mm, 51 * mm]
    )

    tabla_vehiculo.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), claro),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))

    contenido.append(tabla_vehiculo)

    # =====================================
    # DETALLE DE PERMANENCIA
    # =====================================

    contenido.append(
        Paragraph(
            "DETALLE DE PERMANENCIA",
            estilo_seccion
        )
    )

    datos_tiempo = [
        dato(
            "Entrada",
            fecha_local(ingreso.fecha_entrada)
        ),
        dato(
            "Salida",
            fecha_local(ingreso.fecha_salida)
        ),
        dato(
            "Duracion",
            duracion(ingreso.tiempo_total)
        ),
        dato(
            "Modalidad",
            ingreso.tarifa.tiempo
        ),
        dato(
            "Unidades cobradas",
            f"{calculo['unidades']} "
            f"{calculo['descripcion']}"
        ),
        dato(
            "Valor de tarifa",
            moneda(ingreso.tarifa.valor)
        ),
    ]

    tabla_tiempo = Table(
        datos_tiempo,
        colWidths=[31 * mm, 51 * mm]
    )

    tabla_tiempo.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, claro),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))

    contenido.append(tabla_tiempo)

    # =====================================
    # INFORMACIÓN DEL PAGO
    # =====================================

    contenido.append(
        Paragraph(
            "INFORMACION DEL PAGO",
            estilo_seccion
        )
    )

    contenido.append(
        Paragraph(
            "Metodo de pago: "
            + seguro(
                ingreso.forma_pago_descripcion
                or "No especificado"
            ),
            estilo_valor
        )
    )

    contenido.append(Spacer(1, 6 * mm))

    # =====================================
    # TOTAL PAGADO
    # =====================================

    bloque_total = Table(
        [[
            [
                Paragraph(
                    "TOTAL PAGADO",
                    ParagraphStyle(
                        "EtiquetaTotal",
                        fontName="Helvetica-Bold",
                        fontSize=9,
                        leading=13,
                        textColor=blanco,
                        alignment=TA_CENTER
                    )
                ),
                Spacer(1, 2 * mm),
                Paragraph(
                    seguro(
                        moneda(ingreso.total_pago)
                    ),
                    estilo_total
                )
            ]
        ]],
        colWidths=[82 * mm]
    )

    bloque_total.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), azul),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    contenido.append(bloque_total)
    contenido.append(Spacer(1, 8 * mm))

    # =====================================
    # PIE DEL RECIBO
    # =====================================

    contenido.append(
        KeepTogether([
            Paragraph(
                "Atendido por: "
                + seguro(
                    f"{ingreso.empleado.nombre} "
                    f"{ingreso.empleado.apellido}"
                ),
                estilo_centrado
            ),
            Spacer(1, 3 * mm),
            Paragraph(
                "Gracias por confiar en ParkControl",
                estilo_centrado
            ),
            Paragraph(
                "Comprobante generado automaticamente",
                estilo_centrado
            )
        ])
    )

    # GENERAR PDF

    documento.build(contenido)

    # RESPUESTA DE DESCARGA

    respuesta = HttpResponse(
        buffer.getvalue(),
        content_type="application/pdf"
    )

    respuesta["Content-Disposition"] = (
        f'attachment; filename="recibo_{ingreso.pk}.pdf"'
    )

    buffer.close()

    return respuesta
