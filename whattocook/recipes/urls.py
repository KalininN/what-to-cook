from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showrecipe/(?P<recipe_id>[0-9]+)/$', views.showrecipe, name='showrecipe'),
    url(r'^addrecipe/$', views.addrecipe, name='addrecipe'),
]
