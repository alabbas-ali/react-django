"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Static files
from . import settings
from django.conf.urls.static import static
# DRF Simple JWT library
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    
    # For REST login
    path('auth/', include('rest_framework.urls'), name='rest_login'),
    # For accessing Token to authenticate
    path('get-auth-token/', TokenObtainPairView.as_view(), name='get_auth_token'),
    path('refresh-auth-token/', TokenRefreshView.as_view(), name='refresh_auth_token'),
    path('verify-auth-token/', TokenVerifyView.as_view(), name='verify_auth_token'),
    
    # API for other apps
    path('webapi/accounts/', include('accounts.urls'), name='webapi_accounts'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
