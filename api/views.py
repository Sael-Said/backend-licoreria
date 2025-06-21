from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import status

from .models import (
    Categoria, Producto, Proveedor, Compra, DetalleCompra,
    Cliente, Venta, DetalleVenta, VentaProducto, HistorialStock, PagoCompra
)
from .serializers import (
    UsuarioSerializer, CategoriaSerializer, ProductoSerializer, ProveedorSerializer,
    CompraSerializer, DetalleCompraSerializer, ClienteSerializer,
    VentaSerializer, DetalleVentaSerializer, VentaProductoSerializer, HistorialStockSerializer, PagoCompraSerializer
)

User = get_user_model()

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework.permissions import AllowAny

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]  # Hacer pública solo la lista
        return [permissions.IsAuthenticated()]  # Proteger crear, editar, eliminar

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = [permissions.IsAuthenticated]

class PagoCompraViewSet(viewsets.ModelViewSet):
    queryset = PagoCompra.objects.all()
    serializer_class = PagoCompraSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class DetalleCompraViewSet(viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [permissions.IsAuthenticated]

class VentaProductoViewSet(viewsets.ModelViewSet):
    queryset = VentaProducto.objects.all()
    serializer_class = VentaProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

class HistorialStockViewSet(viewsets.ModelViewSet):
    queryset = HistorialStock.objects.all()
    serializer_class = HistorialStockSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'error': 'El usuario está bloqueado'}, status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'rol': user.rol,
        })

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"success": "Logged out successfully."})
#esta es la vista para la pagina web para el catalogo de los productos.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Producto
from .serializers import ProductoCatalogoSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def catalogo_publico(request):
    productos = Producto.objects.filter(activo=True)
    serializer = ProductoCatalogoSerializer(productos, many=True)
    return Response(serializer.data)
