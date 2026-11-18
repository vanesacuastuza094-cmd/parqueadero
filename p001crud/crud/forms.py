
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
