from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'account', views.AccountViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'', include('rest_framework.urls', namespace='rest_framework')),
    url(r'sign-in/$', views.login),
    url(r'register/$', views.register),
    url(r'password/$', views.change_password),
    url(r'verify/$', views.verify)
]
