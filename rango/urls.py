# Como se dijo que la app manejaria las vistas, se creo este archivo. Aqui se
# manejaran los mapeos de las direcciones dentro de la app. Esto con el
# objetivo de que sea modular
# Modificamos la url de categoria para pasar el parametro category_name_slug

from django.conf.urls import url
from rango import views

# Creamos un app_name para rango
app_name = 'rango'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
]
