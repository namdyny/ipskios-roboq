"""mysite URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

import sys
# sys.path.append('.')
from app_home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_home.urls')),
    path('account/signin', auth_views.LoginView.as_view(template_name='app_account/signin.html', redirect_field_name='/', extra_context={'topnav_animate': 'svg-topnav-obj-account-rect'}), name='signin'),
    path('account/', include('app_account.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('roboq/', include('app_roboq.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

