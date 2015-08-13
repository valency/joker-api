from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'account', views.AccountViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^joker-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^joker/auth/login/$', views.login),
    url(r'^joker/auth/register/$', views.register),
    url(r'^joker/auth/password/$', views.change_password)
]
