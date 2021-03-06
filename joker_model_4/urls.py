from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'customer', views.CustomerViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'get/$', views.get_cust_by_id),
    url(r'get_all/$', views.get_cust_all),
    url(r'add_cust_from_csv/$', views.add_cust_from_csv),
    url(r'delete_all/$', views.remove_cust_all),
    url(r'histogram/$', views.histogram),
    url(r'dist/$', views.cust_dist),
    url(r'rank/$', views.get_cust_rank),
    url(r'range/$', views.get_cust_field_range),
    url(r'unique/$', views.get_cust_field_unique),
    url(r'source/$', views.get_cust_sources)
]
