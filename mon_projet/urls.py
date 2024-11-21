# mon_projet/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mon_portfolio.urls")),  # Inclut les URLs de `mon_application`
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
