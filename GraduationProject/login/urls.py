from django.conf.urls import url
from login import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^user/profile/update', views.profile_update),
    url(r'^user/profile/', views.profile),
    url(r'^user/pwd_change', views.pwd_change),
    url(r'^user/avatar_change', views.avatar_change),
]
