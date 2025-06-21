from rest_framework import serializers
from .models import (
    Usuario, Categoria, Producto, Proveedor, Compra, DetalleCompra,
    Cliente, Venta, DetalleVenta, VentaProducto, HistorialStock, PagoCompra
)
from django.contrib.auth import get_user_model

User = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'rol', 'telefono', 'direccion', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)

        # 🔐 Si es administrador, dar permisos adicionales
        if user.rol == "administrador":
            user.is_staff = True
            user.is_superuser = True

        user.set_password(password)
        user.save()
        return user

# En serializers.py

class UsuarioSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False)
    categoria_nombre = serializers.CharField(source='categoria.nombre_categoria', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'
#serializer para catalogo

class ProductoCatalogoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre_categoria', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre_producto', 'descripcion', 'precio_venta', 'imagen', 'categoria_nombre']


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    saldo_pendiente = serializers.ReadOnlyField()
    estado_pago = serializers.ReadOnlyField()
    
    class Meta:
        model = Compra
        fields = '__all__'

class PagoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoCompra
        fields = '__all__'
        
class DetalleCompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre_producto', read_only=True)
    descripcion_producto = serializers.CharField(source="producto.descripcion", read_only=True)
    categoria_producto = serializers.CharField(source="producto.categoria.nombre_categoria", read_only=True)

    class Meta:
        model = DetalleCompra
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.SerializerMethodField()
    usuario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = [
            'id', 'usuario', 'cliente', 'fecha', 'total', 'tipo_pago',
            'cliente_nombre', 'usuario_nombre'
        ]

    def get_cliente_nombre(self, obj):
        return obj.cliente.nombre if obj.cliente else "Anónimo"

    def get_usuario_nombre(self, obj):
        return obj.usuario.username if obj.usuario else "Sin registrar"

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre_producto', read_only=True)
    descripcion_producto = serializers.CharField(source='producto.descripcion', read_only=True)
    categoria_producto = serializers.CharField(source='producto.categoria.nombre_categoria', read_only=True)

    class Meta:
        model = DetalleVenta
        fields = '__all__'

class VentaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaProducto
        fields = '__all__'

class HistorialStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialStock
        fields = '__all__'
