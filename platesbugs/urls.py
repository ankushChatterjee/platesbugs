
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from pbugs import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='index'),
    url(r'^login/*', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/*', views.signout, name='logout'),
    url(r'^home/', views.home, name='home'),
    url(r'^newuser/', views.newuser, name='newuser'),
    url(r'^validate-password/', views.validate_password, name='validate'),
    url(r'^add/', views.add, name='add'),
    url(r'^issue/(?P<pk>[0-9]+)/$', views.detail_issue, name='issue-detail'),
    url(r'^issue/edit/(?P<pk>[0-9]+)/$', views.edit_issue, name='issue-edit'),
    
]
