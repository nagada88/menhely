from django.urls import include, path, re_path

from . import views


urlpatterns = [
    re_path(r'^$', views.hirek, name='hirek'),
    re_path(r'bemutatkozas', views.bemutatkozas, name='bemutatkozas'),
    re_path(r'fogadjorokbe', views.fogadjorokbe, name='fogadjorokbe'),
    re_path(r'hirek', views.hirek, name='hirek'),
    re_path(r'allat', views.allat, name='allat'),
    re_path(r'hir', views.hir, name='hir'),
    re_path(r'help', views.help, name='help'),
    re_path(r'gyik', views.gyik, name='gyik')]