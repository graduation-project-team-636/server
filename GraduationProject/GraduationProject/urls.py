"""GraduationProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from login import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/index/', views.index),
    url(r'^api/login/', views.login),
    url(r'^api/register/', views.register),
    url(r'^api/logout/', views.logout),
    url(r'^api/user/profile/update', views.profile_update),
    url(r'^api/user/profile/', views.profile),
    url(r'^api/user/pwd_change', views.pwd_change),
    url(r'^api/user/avatar_change', views.avatar_change),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


