from rest_framework import routers
from api.views import (
    ProductoViewSet, CategoriaViewSet, ProveedorViewSet, CompraViewSet, DetalleCompraViewSet, PagoCompraViewSet,
    ClienteViewSet, VentaViewSet, DetalleVentaViewSet, VentaProductoViewSet, HistorialStockViewSet,
    UsuarioViewSet, LoginView, LogoutView, catalogo_publico
)
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet)
router.register('categoria', CategoriaViewSet)
router.register('producto', ProductoViewSet)
router.register('proveedor', ProveedorViewSet)
router.register('compra', CompraViewSet)
router.register('pagocompra', PagoCompraViewSet)
router.register('detallecompra', DetalleCompraViewSet)
router.register('cliente', ClienteViewSet)
router.register('venta', VentaViewSet)
router.register('detalleventa', DetalleVentaViewSet)
router.register('ventaproducto', VentaProductoViewSet)  # Para productos más vendidos
router.register('historialstock', HistorialStockViewSet)  # Historial opcional

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('catalogo/', catalogo_publico, name='catalogo-publico'),
] + router.urls
