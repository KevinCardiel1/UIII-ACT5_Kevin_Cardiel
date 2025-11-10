# app_Disney/models.py

from django.db import models

# ======================
# MODELO PRODUCTO
# ======================
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    fecha_lanzamiento = models.DateField()
    en_promocion = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True) # Campo para imagen

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

# app_Disney/models.py

# ... (Modelo Producto y Pedido existentes)

# ======================
# MODELO CLIENTE
# ======================
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True) # Hice estos campos opcionales
    direccion = models.CharField(max_length=200, blank=True, null=True) # Hice estos campos opcionales
    fecha_registro = models.DateField(auto_now_add=True)
    puntos_disney = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ... (Modelos Producto y Cliente existentes)

# ======================
# MODELO PEDIDO
# ======================
class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='pedidos'
    )  # Relación 1-N (un cliente puede tener muchos pedidos)

    productos = models.ManyToManyField(
        Producto, related_name='pedidos'
    )  # Relación N-N (un pedido puede tener varios productos)

    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ], default='Pendiente') # Añadido un default para el estado
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Añadido un default
    metodo_pago = models.CharField(max_length=50, blank=True, null=True) # Hice opcional
    direccion_envio = models.CharField(max_length=200, blank=True, null=True) # Hice opcional

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre} ({self.estado})"