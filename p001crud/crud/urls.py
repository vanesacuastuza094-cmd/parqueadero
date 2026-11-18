
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
]
