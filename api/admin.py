import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.contrib import admin
from django.db.models import Sum
from .models import Producto, VentaProducto, Categoria, Proveedor, Compra, DetalleCompra, Venta, DetalleVenta, Cliente, HistorialStock, PagoCompra

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio_venta', 'stock', 'cantidad_vendida')

    def cantidad_vendida(self, obj):
        resultado = VentaProducto.objects.filter(producto=obj).aggregate(total=Sum('cantidad'))
        return resultado['total'] or 0
    cantidad_vendida.short_description = 'Total Vendido'

    def productos_mas_vendidos(self, request):
        # Obtener los productos más vendidos
        productos = Producto.objects.all()
        ventas = [VentaProducto.objects.filter(producto=producto).aggregate(total=Sum('cantidad'))['total'] or 0 for producto in productos]
        nombres_productos = [producto.nombre_producto for producto in productos]

        # Crear gráfico
        fig, ax = plt.subplots()
        ax.barh(nombres_productos, ventas)
        ax.set_xlabel('Cantidad Vendida')
        ax.set_title('Productos Más Vendidos')

        # Generar la respuesta HTTP con la imagen del gráfico
        response = HttpResponse(content_type='image/png')
        fig.savefig(response, format="png")
        return response

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('productos-mas-vendidos/', self.admin_site.admin_view(self.productos_mas_vendidos), name='productos_mas_vendidos')
        ]
        return custom_urls + urls
#esto es para poder agregar administradores y usuarios desde el admin panel.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1

class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha_compra', 'tipo_pago', 'total', 'estado_pago', 'saldo_pendiente')
    inlines = [DetalleCompraInline]
    readonly_fields = ('estado_pago', 'saldo_pendiente')

class PagoCompraAdmin(admin.ModelAdmin):
    list_display = ('compra', 'fecha_pago', 'monto_pagado', 'metodo_pago')
    list_filter = ('metodo_pago', 'fecha_pago')
    search_fields = ('compra__id', 'compra__proveedor__nombre')
    ordering = ('-fecha_pago',)

admin.site.register(Compra, CompraAdmin)
admin.site.register(Usuario, UsuarioAdmin)

# Registrar en el admin
admin.site.register(Producto, ProductoAdmin)
admin.site.register(VentaProducto)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Venta)
admin.site.register(DetalleCompra)
admin.site.register(DetalleVenta)
admin.site.register(HistorialStock)
admin.site.register(Cliente)
admin.site.register(PagoCompra, PagoCompraAdmin)