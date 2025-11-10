# app_Disney/admin.py

from django.contrib import admin
from .models import Producto, Cliente, Pedido # Importa Pedido

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'en_promocion', 'fecha_lanzamiento')
    list_filter = ('categoria', 'en_promocion', 'fecha_lanzamiento')
    search_fields = ('nombre', 'descripcion', 'categoria')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'correo', 'telefono', 'direccion', 'puntos_disney', 'fecha_registro')
    list_filter = ('fecha_registro', 'puntos_disney')
    search_fields = ('nombre', 'apellido', 'correo', 'telefono')
    ordering = ('apellido', 'nombre')

@admin.register(Pedido) # Registra el modelo Pedido
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'total', 'metodo_pago')
    list_filter = ('estado', 'fecha_pedido', 'metodo_pago')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'estado', 'id')
    raw_id_fields = ('cliente',) # Para mejorar la selección de cliente en el admin si hay muchos
    filter_horizontal = ('productos',) # Para un selector de ManyToMany más amigable en el admin