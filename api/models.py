from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Extensión del modelo de usuario con roles
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Usuario(AbstractUser):
    ROLES = [
        ('administrador', 'Administrador'),
        ('usuario', 'Usuario'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return self.username



class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre_categoria

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    stock_minimo = models.IntegerField(default=5)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    imagen = models.ImageField(null=True, blank=True, upload_to='images/')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_producto

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)  # 👈 ahora es opcional

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    TIPOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('qr', 'QR'),
        ('credito', 'Crédito')
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    fecha_compra = models.DateField()
    tipo_pago = models.CharField(max_length=20, choices=TIPOS_PAGO, default='efectivo')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra #{self.id} - {self.fecha_compra.strftime('%Y-%m-%d')}"

    @property
    def saldo_pendiente(self):
        total_pagado = sum(pago.monto_pagado for pago in self.pagos.all())
        return max(self.total - total_pagado, 0)

    @property
    def estado_pago(self):
        total_pagado = sum(pago.monto_pagado for pago in self.pagos.all())
        if total_pagado == 0:
            return "Pendiente"
        elif total_pagado < self.total:
            return "Parcial"
        else:
            return "Pagado"


class PagoCompra(models.Model):
    compra = models.ForeignKey("Compra", on_delete=models.CASCADE, related_name="pagos")
    fecha_pago = models.DateField(auto_now_add=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=[
        ('efectivo', 'Efectivo'),
        ('qr', 'QR'),
    ])

    def __str__(self):
        return f"Pago {self.monto_pagado} Bs - Compra #{self.compra.id}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto}"
    
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    ci_nit = models.CharField(max_length=50, blank=True, null=True)  # Cédula o NIT (obligatorio)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Venta(models.Model):
    TIPOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('qr', 'QR'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)  # Cliente opcional
    tipo_pago = models.CharField(max_length=20, choices=TIPOS_PAGO, default='efectivo')  # ✅ Nuevo campo

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.strftime('%Y-%m-%d')}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto}"



    #TABLA PARA VER LOS PRODUCTOS MAS VENDIDOS
class VentaProducto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
        
    #ESTA TABLA ES OPCIONAL
from django.utils.timezone import localtime
class HistorialStock(models.Model):
    TIPOS_MOVIMIENTO = [
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('ajuste', 'Ajuste'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre_producto} ({self.cantidad})"
    
    def __str__(self):
        fecha_local = localtime(self.fecha)
        return f"{fecha_local.strftime('%Y-%m-%d %H:%M:%S')} - {self.tipo_movimiento} - {self.producto.nombre_producto} ({self.cantidad})"