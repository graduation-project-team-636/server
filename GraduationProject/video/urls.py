from django.conf.urls import url
from video import views

urlpatterns = [
    url(r'^upload/', views.upload),
    url(r'^modify/', views.modify),
    url(r'^access?', views.access),
    url(r'^delete/', views.delete),
    url(r'^query/', views.query),
]
