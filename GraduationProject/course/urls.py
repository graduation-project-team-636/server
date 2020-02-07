from django.conf.urls import url
from course import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^create/', views.create),
    url(r'^modify/', views.modify),
    url(r'^access?', views.access),
    url(r'^total_num/', views.total_num),
    url(r'^delete/', views.delete),
    url(r'^attend/', views.attend),
    url(r'^withdraw/', views.withdraw),
    url(r'^attended_by_users/', views.attended_by_users),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
