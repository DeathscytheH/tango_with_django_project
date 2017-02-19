# Como se dijo que la app manejaria las vistas, se creo este archivo. Aqui se
# manejaran los mapeos de las direcciones dentro de la app. Esto con el
# objetivo de que sea modular

from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^category/', views.show_category, name='category'),
]
