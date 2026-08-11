from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from farmer import views as farmer_views   # ✅ REQUIRED

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

    # HOME PAGE
    path('', farmer_views.index, name='index'),

    # FARMER APP URLS
    path('', include('farmer.urls')),

    # LOGOUT
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
