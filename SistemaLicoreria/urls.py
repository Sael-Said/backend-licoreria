from django.contrib import admin
from django.urls import path, include
# dos librerias  recien añadido para subir fotos 
from django.conf import settings
from django.conf.urls.static import static
from api.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-token-auth/', LoginView.as_view()),  # usa tu vista personalizada
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

