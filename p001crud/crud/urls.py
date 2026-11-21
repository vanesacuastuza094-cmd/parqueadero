
from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),

    path(
        "clientes/",
        views.lista_clientes,
        name="lista_clientes"
    ),

    path(
        "clientes/registrar/",
        views.registrar_cliente,
        name="registrar_cliente"
    ),

    path(
    "clientes/editar/<int:cliente_id>/",
    views.editar_cliente,
    name="editar_cliente"
),


    path(
        "vehiculos/",
        views.lista_vehiculos,
        name="lista_vehiculos"
    ),

    path(
        "vehiculos/registrar/",
        views.registrar_vehiculo,
        name="registrar_vehiculo"
    ),

    path(
        "vehiculos/editar/<int:vehiculo_id>/",
        views.editar_vehiculo,
        name="editar_vehiculo"
    ),


    path(
        "tarifas/",
        views.lista_tarifas,
        name="lista_tarifas"
    ),

    path(
        "tarifas/registrar/",
        views.registrar_tarifa,
        name="registrar_tarifa"
    ),

    path(
        "tarifas/editar/<int:tarifa_id>/",
        views.editar_tarifa,
        name="editar_tarifa"
    ),


    path(
        "ingresos/",
        views.lista_ingresos,
        name="lista_ingresos"
    ),

    path(
        "ingresos/registrar/",
        views.registrar_ingreso,
        name="registrar_ingreso"
    ),


    path(
        "salidas/",
        views.lista_salidas,
        name="lista_salidas"
    ),

    path(
        "salidas/registrar/<int:ingreso_id>/",
        views.registrar_salida,
        name="registrar_salida"
    ),

    path(
        "salidas/detalle/<int:ingreso_id>/",
        views.detalle_salida,
        name="detalle_salida"
    ),


    path(
        "empleados/",
        views.lista_empleados,
        name="lista_empleados"
    ),

    path(
        "empleados/registrar/",
        views.registrar_empleado,
        name="registrar_empleado"
    ),

    path(
        "empleados/editar/<int:empleado_id>/",
        views.editar_empleado,
        name="editar_empleado"
    ),

]
