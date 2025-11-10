# app_Disney/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Rutas generales
    path('', views.inicio_disneystore, name='inicio_disneystore'),

    # Rutas para Productos
    path('productos/agregar/', views.agregar_productos, name='agregar_productos'),
    path('productos/', views.ver_productos, name='ver_productos'),
    path('productos/actualizar/<int:pk>/', views.actualizar_productos, name='actualizar_productos'),
    path('productos/borrar/<int:pk>/', views.borrar_productos, name='borrar_productos'),

    # Rutas para Clientes
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/actualizar/<int:pk>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/borrar/<int:pk>/', views.borrar_cliente, name='borrar_cliente'),

    # Rutas para Pedidos
    path('pedidos/agregar/', views.agregar_pedido, name='agregar_pedido'),
    path('pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('pedidos/actualizar/<int:pk>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('pedidos/borrar/<int:pk>/', views.borrar_pedido, name='borrar_pedido'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)