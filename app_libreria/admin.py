from django.contrib import admin
from .models import Categoria, Libro, Proveedor, Inventario, CarritoItem, Pedido

# Registramos los modelos para que aparezcan en el panel de administrador
admin.site.register(Categoria)
admin.site.register(Libro)
admin.site.register(Proveedor)
admin.site.register(Inventario)
admin.site.register(CarritoItem)
admin.site.register(Pedido)