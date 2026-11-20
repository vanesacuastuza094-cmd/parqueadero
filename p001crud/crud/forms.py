
from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):

    TIPOS_IDENTIFICACION = [
        ("", "Seleccione un tipo de documento"),
        ("CC", "Cédula de ciudadanía"),
        ("TI", "Tarjeta de identidad"),
        ("CE", "Cédula de extranjería"),
        ("PA", "Pasaporte"),
    ]

    tipo_identificacion = forms.ChoiceField(
        label="Tipo de identificación",
        choices=TIPOS_IDENTIFICACION,
        required=True
    )

    class Meta:
        model = Cliente

        fields = [
            "tipo_identificacion",
            "identificacion",
            "nombre",
            "apellido",
            "telefono",
            "direccion",
            "estado",
        ]

        widgets = {
            "identificacion": forms.TextInput(
                attrs={"placeholder": "Número de identificación"}
            ),
            "nombre": forms.TextInput(
                attrs={"placeholder": "Nombre del cliente"}
            ),
            "apellido": forms.TextInput(
                attrs={"placeholder": "Apellido del cliente"}
            ),
            "telefono": forms.TextInput(
                attrs={"placeholder": "Número de teléfono"}
            ),
            "direccion": forms.TextInput(
                attrs={"placeholder": "Dirección"}
            ),
        }

    def clean_identificacion(self):
        identificacion = self.cleaned_data["identificacion"]

        if Cliente.objects.filter(
            identificacion=identificacion
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Ya existe un cliente con esta identificación."
            )

        return identificacion

from .models import Vehiculo, Cliente, TipoVehiculo


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            "placa",
            "tipo_vehiculo",
            "cliente",
            "marca",
            "color",
            "estado",
        ]
        labels = {
            "placa": "Placa",
            "tipo_vehiculo": "Tipo de vehículo",
            "cliente": "Propietario",
            "marca": "Marca",
            "color": "Color",
            "estado": "Vehículo activo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["tipo_vehiculo"].queryset = (
            TipoVehiculo.objects.filter(estado=True)
        )

        self.fields["cliente"].queryset = (
            Cliente.objects.filter(estado=True)
        )

        # Permitir conservar el propietario o tipo actual al editar.
        if self.instance.pk:
            self.fields["cliente"].queryset = (
                Cliente.objects.filter(estado=True)
                | Cliente.objects.filter(pk=self.instance.cliente_id)
            ).distinct()

            self.fields["tipo_vehiculo"].queryset = (
                TipoVehiculo.objects.filter(estado=True)
                | TipoVehiculo.objects.filter(
                    pk=self.instance.tipo_vehiculo_id
                )
            ).distinct()

        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

    def clean_placa(self):
        placa = self.cleaned_data["placa"].strip().upper()

        if Vehiculo.objects.filter(placa__iexact=placa).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "Ya existe un vehículo registrado con esta placa."
            )

        return placa


from .models import Tarifa


class TarifaForm(forms.ModelForm):
    MODALIDADES = [
        ("Hora", "Por hora"),
        ("Dia", "Por día"),
        ("Mes", "Por mes"),
    ]

    tiempo = forms.ChoiceField(
        choices=MODALIDADES,
        label="Modalidad de cobro"
    )

    class Meta:
        model = Tarifa
        fields = [
            "tipo_vehiculo",
            "tiempo",
            "valor",
            "estado",
        ]
        labels = {
            "tipo_vehiculo": "Tipo de vehículo",
            "valor": "Valor en pesos colombianos (COP)",
            "estado": "Tarifa activa",
        }
        widgets = {
            "valor": forms.NumberInput(
                attrs={"min": "0.01", "step": "0.01"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tipos = TipoVehiculo.objects.filter(estado=True)

        if self.instance.pk:
            tipos = (
                tipos
                | TipoVehiculo.objects.filter(
                    pk=self.instance.tipo_vehiculo_id
                )
            ).distinct()

        self.fields["tipo_vehiculo"].queryset = tipos

    def clean(self):
        datos = super().clean()
        tipo = datos.get("tipo_vehiculo")
        tiempo = datos.get("tiempo")

        if tipo and tiempo:
            duplicada = Tarifa.objects.filter(
                tipo_vehiculo=tipo,
                tiempo=tiempo
            ).exclude(pk=self.instance.pk)

            if duplicada.exists():
                raise forms.ValidationError(
                    "Ya existe una tarifa para este tipo "
                    "de vehículo y modalidad."
                )

        return datos


from .models import IngresoSalida, Empleado, Tarifa


class IngresoForm(forms.Form):
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.none(),
        label="Vehículo",
        empty_label="Seleccione un vehículo"
    )

    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.none(),
        label="Empleado responsable",
        empty_label="Seleccione un empleado"
    )

    tarifa = forms.ModelChoiceField(
        queryset=Tarifa.objects.none(),
        label="Modalidad de cobro",
        empty_label="Seleccione una tarifa"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        vehiculos_dentro = IngresoSalida.objects.filter(
            fecha_salida__isnull=True
        ).values_list("vehiculo_id", flat=True)

        self.fields["vehiculo"].queryset = (
            Vehiculo.objects.filter(
                estado=True,
                cliente__estado=True,
                tipo_vehiculo__estado=True
            )
            .exclude(pk__in=vehiculos_dentro)
            .select_related("cliente", "tipo_vehiculo")
            .order_by("placa")
        )

        self.fields["empleado"].queryset = (
            Empleado.objects.filter(estado=True)
            .order_by("nombre", "apellido")
        )

        self.fields["tarifa"].queryset = (
            Tarifa.objects.filter(
                estado=True,
                tipo_vehiculo__estado=True
            )
            .select_related("tipo_vehiculo")
            .order_by("tipo_vehiculo__nombre", "tiempo")
        )

        self.fields["vehiculo"].label_from_instance = (
            lambda obj: (
                f"{obj.placa} - {obj.tipo_vehiculo.nombre} - "
                f"{obj.cliente.nombre} {obj.cliente.apellido}"
            )
        )

        self.fields["empleado"].label_from_instance = (
            lambda obj: f"{obj.nombre} {obj.apellido}"
        )

        self.fields["tarifa"].label_from_instance = (
            lambda obj: (
                f"{obj.tipo_vehiculo.nombre} - "
                f"{obj.tiempo} - ${obj.valor:,.0f}"
            )
        )

    def clean(self):
        datos = super().clean()

        vehiculo = datos.get("vehiculo")
        tarifa = datos.get("tarifa")

        if vehiculo and tarifa:
            if vehiculo.tipo_vehiculo_id != tarifa.tipo_vehiculo_id:
                raise forms.ValidationError(
                    "La tarifa seleccionada no corresponde "
                    "al tipo de vehículo."
                )

        if vehiculo:
            if IngresoSalida.objects.filter(
                vehiculo=vehiculo,
                fecha_salida__isnull=True
            ).exists():
                raise forms.ValidationError(
                    "Este vehículo ya se encuentra dentro "
                    "del parqueadero."
                )

        return datos
