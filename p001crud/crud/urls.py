from rest_framework import routers
from .api import TipoVehiculoViewSet,TarifaViewSet,VehiculoViewSet,ClienteViewSet,EmpleadoViewSet,UsuarioViewSet,IngresoSalidaViewSet

router=  routers.DefaultRouter()

router.register('api/tipovehiculo', TipoVehiculoViewSet, 'TipoVehiculo')
urlpatterns = router.urls

router.register('api/tarifa', TarifaViewSet, 'Tarifa')
urlpatterns = router.urls

router.register('api/vehiculo', VehiculoViewSet, 'Vehiculo')
urlpatterns = router.urls

router.register('api/cliente', ClienteViewSet, 'Cliente')
urlpatterns = router.urls

router.register('api/empleado', EmpleadoViewSet, 'Empleado')
urlpatterns = router.urls

router.register('api/usuario', UsuarioViewSet, 'Usuario')
urlpatterns = router.urls

router.register('api/ingreso_salidaViewSet', IngresoSalidaViewSet, 'IngresoSalidaViewSet')
urlpatterns = router.urls