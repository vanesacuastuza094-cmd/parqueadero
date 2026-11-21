from django.db import models
from django.conf import settings

class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Tarifa(models.Model):
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    tiempo = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo_vehiculo} - {self.valor}"



class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)

    tipo_vehiculo = models.ForeignKey(
        TipoVehiculo,
        on_delete=models.CASCADE
    )

    cliente = models.ForeignKey(
    "Cliente",
    on_delete=models.PROTECT,
    related_name="vehiculos"
)

    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.placa} - {self.marca} - {self.color}"



class Cliente(models.Model):
    tipo_identificacion = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.apellido} - ¨{self.identificacion}"

class Empleado(models.Model):

    usuario_django = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="empleado_parkcontrol"
    )

    identificacion = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.rol} {self.identificacion}"

class Usuario(models.Model):
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=100)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario} - {self.empleado}"


class IngresoSalida(models.Model):
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE
    )

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    tarifa = models.ForeignKey(
        Tarifa,
        on_delete=models.CASCADE
    )

    fecha_entrada = models.DateTimeField()

    fecha_salida = models.DateTimeField(
        null=True,
        blank=True
    )

    tiempo_total = models.IntegerField(default=0)

    numero_recibo = models.CharField(
        max_length=50,
        blank=True,
        unique=True
    )

    total_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    forma_pago_descripcion = models.CharField(
        max_length=100,
        blank=True
    )

    estado = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Primero se guarda el registro para obtener su ID.
        super().save(*args, **kwargs)

        # Generar el número de recibo automáticamente.
        if not self.numero_recibo:
            self.numero_recibo = f"REC-{self.pk:06d}"

            type(self).objects.filter(pk=self.pk).update(
                numero_recibo=self.numero_recibo
            )

    def __str__(self):
        return (
            f"Registro {self.id} - "
            f"{self.numero_recibo} - "
            f"{self.vehiculo.placa}"
        )

