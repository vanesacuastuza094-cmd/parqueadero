from crud.models import TipoVehiculo,Tarifa,Vehiculo,Cliente,Empleado,Usuario,IngresoSalida

from rest_framework import viewsets, permissions
from .serializers import TipoVehiculoSerializer,TarifaSerializer,VehiculoSerializer,ClienteSerializer,EmpleadoSerializer,UsuarioSerializer,IngresoSalidaSerializer

class TipoVehiculoViewSet(viewsets.ModelViewSet):
    queryset = TipoVehiculo.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TipoVehiculoSerializer



class TarifaViewSet(viewsets.ModelViewSet):
    queryset = Tarifa.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TarifaSerializer


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VehiculoSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ClienteSerializer


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EmpleadoSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UsuarioSerializer


class IngresoSalidaViewSet(viewsets.ModelViewSet):
    queryset = IngresoSalida.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = IngresoSalidaSerializer