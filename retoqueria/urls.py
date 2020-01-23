# -*- coding: utf-8 -*-


"""retoqueria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(r'^admin/auth/', include('sistema.urls')),
    url(r'^admin/sistema/', include('sistema.urls')),
    url(r'^admin/clientes/', include('clientes.urls')),
    url(r'^admin/funcionarios/', include('funcionarios.urls')),
    url(r'^admin/proveedores/', include('proveedores.urls')),
    url(r'^admin/materiales/', include('materiales.urls')),

    url(r'^admin/depositos/', include('depositos.urls')),
    url(r'^admin/servicios/', include('servicios.urls')),

    url(r'^admin/produccion/', include('produccion.urls')),

    url(r'^admin/ventas/', include('ventas.urls')),

    url(r'^admin/', include(admin.site.urls)), 
    url(r'^chaining/', include('smart_selects.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
