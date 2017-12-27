from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.default, name='default'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^thanks$', views.thanks, name='thanks'),
]
