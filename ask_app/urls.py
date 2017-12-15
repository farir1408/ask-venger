from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^question/(?P<question_id>[0-9]+)?/?$', views.question, name='question'),
    url(r'^ask/', views.ask, name='ask'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='signup'),
    url(r'^params/', views.params, name='params')
]
