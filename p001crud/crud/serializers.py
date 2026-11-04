from rest_framework import serializers
from .models import TipoVehiculo,Tarifa,Vehiculo,Cliente,Empleado,Usuario,IngresoSalida

class TipoVehiculoSerializer(serializers.ModelSerializer):  
    class Meta:
        model = TipoVehiculo
        fields = '__all__'

        
class TarifaSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Tarifa
        fields = '__all__'


class VehiculoSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Vehiculo
        fields = '__all__'
        

class ClienteSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Cliente
        fields = '__all__'


class EmpleadoSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Empleado
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Usuario
        fields = '__all__'


class IngresoSalidaSerializer(serializers.ModelSerializer):  
    class Meta:
        model = IngresoSalida
        fields = '__all__'
