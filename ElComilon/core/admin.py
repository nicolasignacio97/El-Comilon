from django.contrib import admin
from .models import Cargo, Cliente, DetallePedido, EmpresaConvenio,EstadoPedido, EstadoReclamo, Pedido, Platillo, Reclamo, Repartidor, Reporte, Representante, Restaurante, TipoCliente, TipoRestaurante, TipoServicio, TipoVehiculo, Trabajador, Vehiculo
# Register your models here.

admin.site.register(Cargo)
admin.site.register(Cliente)
admin.site.register(DetallePedido)
admin.site.register(EmpresaConvenio)
admin.site.register(EstadoPedido)
admin.site.register(EstadoReclamo)
admin.site.register(Pedido)
admin.site.register(Platillo)
admin.site.register(Reclamo)
admin.site.register(Repartidor)
admin.site.register(Reporte)
admin.site.register(Representante)
admin.site.register(Restaurante)
admin.site.register(TipoCliente)
admin.site.register(TipoRestaurante)
admin.site.register(TipoServicio)
admin.site.register(TipoVehiculo)
admin.site.register(Trabajador)
admin.site.register(Vehiculo)

