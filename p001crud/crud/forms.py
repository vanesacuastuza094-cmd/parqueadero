
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
