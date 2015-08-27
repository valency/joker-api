from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'customer', views.CustomerViewSet)
router.register(r'customer_set', views.CustomerSetViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'get/$', views.get_cust_by_id),
    url(r'get_all/$', views.get_cust_all),
    url(r'add_cust_from_csv/$', views.add_cust_from_csv),
    url(r'delete_all/$', views.remove_cust_all),
    url(r'histogram/$', views.histogram),
    url(r'kmeans/$', views.kmeans),
    url(r'dist/$', views.cust_dist),
    url(r'rank/$', views.get_cust_rank),
    url(r'range/$', views.get_cust_field_range),
    url(r'unique/$', views.get_cust_field_unique),
    url(r'source/$', views.get_cust_sources),
    url(r'set/create/$', views.create_set),
    url(r'set/search/$', views.get_set),
    url(r'set/retrieve_all_id/$', views.get_set_all)
]
