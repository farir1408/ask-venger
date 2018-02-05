import django.conf.urls
from . import views

urlpatterns = [
    django.conf.urls.url(r'^$', views.index, name='index'),
    django.conf.urls.url(r'^question/(?P<question_id>[0-9]+/?)', views.question, name='question'),
    django.conf.urls.url(r'^ask/?', views.ask, name='ask'),
    django.conf.urls.url(r'^login/?', views.login, name='login'),
    django.conf.urls.url(r'^register/?', views.register, name='signup'),
    django.conf.urls.url(r'^params/?', views.params, name='params'),
    django.conf.urls.url(r'^hot/?', views.hot, name="hot"),
    django.conf.urls.url(r'^logout/?', views.logout, name ='logout'),
]
