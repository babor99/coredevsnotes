from django.contrib import admin
from django.urls import path, include
import notes_app

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf.urls.static import static
from django.conf import settings

from notes_app.views import CustomTokenObtainView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('notes_app.urls')),
    path('api/get_token/', CustomTokenObtainView.as_view(), name='get_token'),
    # path('api/get_token/', TokenObtainPairView.as_view(), name='get_token'),
    # path('api/refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


