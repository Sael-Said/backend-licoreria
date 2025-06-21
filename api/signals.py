
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import DetalleCompra, DetalleVenta, Producto, Categoria, HistorialStock

# 1. Registro automático cuando se realiza una compra
@receiver(post_save, sender=DetalleCompra)
def registrar_historial_compra(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        producto.stock += instance.cantidad
        producto.save()

        HistorialStock.objects.create(
            producto=producto,
            tipo_movimiento='compra',
            cantidad=instance.cantidad,
            observaciones=f"Compra ID: {instance.compra.id}"
        )

# 2. Registro automático cuando se realiza una venta
@receiver(post_save, sender=DetalleVenta)
def registrar_historial_venta(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        producto.stock -= instance.cantidad
        producto.save()

        HistorialStock.objects.create(
            producto=producto,
            tipo_movimiento='venta',
            cantidad=-instance.cantidad,
            observaciones=f"Venta ID: {instance.venta.id}"
        )

# 3. Registro cuando el admin modifica el stock manualmente desde el panel
@receiver(pre_save, sender=Producto)
def registrar_ajuste_stock(sender, instance, **kwargs):
    try:
        original = Producto.objects.get(pk=instance.pk)
        diferencia = instance.stock - original.stock

        if diferencia != 0 and instance._state.adding is False:
            HistorialStock.objects.create(
                producto=instance,
                tipo_movimiento='ajuste',
                cantidad=diferencia,
                observaciones='Ajuste manual desde el panel de administración'
            )
    except Producto.DoesNotExist:
        pass  # Producto nuevo, no comparar

# 4. Registro cuando se elimina una categoría (y sus productos asociados)
@receiver(pre_delete, sender=Categoria)
def registrar_eliminacion_categoria(sender, instance, **kwargs):
    productos = Producto.objects.filter(categoria=instance)
    for producto in productos:
        HistorialStock.objects.create(
            producto=producto,
            tipo_movimiento='ajuste',
            cantidad=0,
            observaciones=f"Producto afectado por eliminación de categoría: {instance.nombre_categoria}"
        )
