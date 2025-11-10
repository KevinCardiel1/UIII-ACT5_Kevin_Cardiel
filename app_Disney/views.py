# app_Disney/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Cliente, Pedido # Importa el modelo Pedido
from datetime import date # Importa date para fecha_lanzamiento en Producto, etc.

def inicio_disneystore(request):
    return render(request, 'app_Disney/inicio.html')

def agregar_productos(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        categoria = request.POST['categoria']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        stock = request.POST['stock']
        # Usamos date.today() como valor por defecto si no se proporciona, o asumimos un campo de entrada de fecha
        fecha_lanzamiento = request.POST.get('fecha_lanzamiento', date.today())
        en_promocion = request.POST.get('en_promocion') == 'on' # Checkbox
        imagen = request.FILES.get('imagen') # Para manejar la carga de imágenes

        Producto.objects.create(
            nombre=nombre,
            categoria=categoria,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            fecha_lanzamiento=fecha_lanzamiento,
            en_promocion=en_promocion,
            imagen=imagen
        )
        return redirect('ver_productos')
    return render(request, 'app_Disney/productos/agregar_productos.html')

def ver_productos(request):
    productos = Producto.objects.all()
    return render(request, 'app_Disney/productos/ver_productos.html', {'productos': productos})

def actualizar_productos(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.categoria = request.POST['categoria']
        producto.descripcion = request.POST['descripcion']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.fecha_lanzamiento = request.POST.get('fecha_lanzamiento', producto.fecha_lanzamiento)
        producto.en_promocion = request.POST.get('en_promocion') == 'on'
        
        # Manejar la actualización de la imagen
        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']

        producto.save()
        return redirect('ver_productos')
    return render(request, 'app_Disney/productos/actualizar_productos.html', {'producto': producto})
   


# En Django, la función de actualización se suele usar para "mostrar el formulario de edición"
# y "procesar el envío del formulario". El nombre `realizar_actualizacion_productos`
# podría ser redundante si `actualizar_productos` ya maneja ambos.
# Por simplicidad, unificaremos en `actualizar_productos` el mostrar el formulario y procesar la actualización.
# Si prefieres una función separada para procesar, podríamos hacer esto:
# def realizar_actualizacion_productos(request, pk):
#     producto = get_object_or_404(Producto, pk=pk)
#     if request.method == 'POST':
#         # Lógica de actualización
#         producto.save()
#         return redirect('ver_productos')
#     return redirect('actualizar_productos', pk=pk) # Redirige de vuelta al formulario si no es POST válido o para mostrarlo

def borrar_productos(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST': # Confirmación de borrado
        producto.delete()
        return redirect('ver_productos')
    return render(request, 'app_Disney/productos/borrar_productos.html', {'producto': producto})

# ======================
# FUNCIONES PARA CLIENTES
# ======================

def agregar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        telefono = request.POST.get('telefono', '') # Usar .get para campos opcionales
        direccion = request.POST.get('direccion', '') # Usar .get para campos opcionales
        puntos_disney = request.POST.get('puntos_disney', 0) # Si no se envía, 0

        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            puntos_disney=puntos_disney
        )
        return redirect('ver_clientes')
    return render(request, 'app_Disney/clientes/agregar_clientes.html')


def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'app_Disney/clientes/ver_clientes.html', {'clientes': clientes})


def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.apellido = request.POST['apellido']
        cliente.correo = request.POST['correo']
        cliente.telefono = request.POST.get('telefono', '')
        cliente.direccion = request.POST.get('direccion', '')
        cliente.puntos_disney = request.POST.get('puntos_disney', cliente.puntos_disney)
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'app_Disney/clientes/actualizar_clientes.html', {'cliente': cliente})


def borrar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST': # Confirmación de borrado
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'app_Disney/clientes/borrar_clientes.html', {'cliente': cliente})

# ... (Funciones de Producto y Cliente existentes)

# ======================
# FUNCIONES PARA PEDIDOS
# ======================

def agregar_pedido(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        productos_seleccionados_ids = request.POST.getlist('productos') # getlist para múltiples selecciones
        estado = request.POST.get('estado', 'Pendiente')
        total_str = request.POST.get('total', '0.00')
        metodo_pago = request.POST.get('metodo_pago', '')
        direccion_envio = request.POST.get('direccion_envio', '')

        cliente = get_object_or_404(Cliente, pk=cliente_id)
        
        # Calcular el total si es necesario, o usar el enviado por el formulario
        total = float(total_str) # Convertir a float
        if not productos_seleccionados_ids and total == 0:
            # Si no hay productos y el total es 0, no creamos un pedido
            # O puedes decidir crear un pedido con 0 total y sin productos
            pass 
        else:
            # Crear el pedido
            pedido = Pedido.objects.create(
                cliente=cliente,
                estado=estado,
                total=total,
                metodo_pago=metodo_pago,
                direccion_envio=direccion_envio
            )
            # Añadir los productos (solo si hay)
            if productos_seleccionados_ids:
                productos_obj = Producto.objects.filter(id__in=productos_seleccionados_ids)
                pedido.productos.set(productos_obj) # Asigna los productos al pedido

        return redirect('ver_pedidos') # Redirige a la lista de pedidos
    
    return render(request, 'app_Disney/pedidos/agregar_pedido.html', {
        'clientes': clientes,
        'productos': productos,
        'estados': Pedido.estado.field.choices, # Para el combobox de estados
    })


def ver_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'app_Disney/pedidos/ver_pedidos.html', {'pedidos': pedidos})


def actualizar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        productos_seleccionados_ids = request.POST.getlist('productos')
        estado = request.POST.get('estado', 'Pendiente')
        total_str = request.POST.get('total', '0.00')
        metodo_pago = request.POST.get('metodo_pago', '')
        direccion_envio = request.POST.get('direccion_envio', '')

        pedido.cliente = get_object_or_404(Cliente, pk=cliente_id)
        pedido.estado = estado
        pedido.total = float(total_str)
        pedido.metodo_pago = metodo_pago
        pedido.direccion_envio = direccion_envio
        
        # Actualizar productos relacionados
        if productos_seleccionados_ids:
            productos_obj = Producto.objects.filter(id__in=productos_seleccionados_ids)
            pedido.productos.set(productos_obj)
        else:
            pedido.productos.clear() # Si no se selecciona ninguno, limpiar

        pedido.save()
        return redirect('ver_pedidos')
    
    return render(request, 'app_Disney/pedidos/actualizar_pedido.html', {
        'pedido': pedido,
        'clientes': clientes,
        'productos': productos,
        'estados': Pedido.estado.field.choices,
        'productos_en_pedido_ids': [p.id for p in pedido.productos.all()] # Para pre-seleccionar en el form
    })


def borrar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST': # Confirmación de borrado
        pedido.delete()
        return redirect('ver_pedidos')
    return render(request, 'app_Disney/pedidos/borrar_pedido.html', {'pedido': pedido})
