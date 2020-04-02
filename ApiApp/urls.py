"""ApiApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from account.api import (
    Users,
    Userr,
    # get_all_users,
    login
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login, name='login'),
    # url(r'api/users/$', Users.as_view(), name='users'),
    # url(r'^auth/', include('timed_auth_token.urls', namespace='auth')),
    # path('auth/', include(('timed_auth_token.urls', 'auth'))),
    path('api/users/', Users.as_view(), name='users'),
    path('api/user/', Userr.as_view(), name='user'),
    url(r'api/user/(?P<user_id>\d+)/$', Userr.as_view(), name='user'),
    

    # path('api/users/', get_all_users, name='users'),
]
