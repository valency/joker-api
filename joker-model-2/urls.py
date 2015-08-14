from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'customer', views.CustomerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^joker/model/2/get/$', views.get_cust_by_id),
    url(r'^joker/model/2/get_all/$', views.get_cust_all),
    url(r'^joker/model/2/add_cust_from_csv/$', views.add_cust_from_csv),
    url(r'^joker/model/2/delete_all/$', views.remove_cust_all),
    url(r'^joker/model/2/histogram/$', views.histogram),
    url(r'^joker/model/2/kmeans/$', views.kmeans),
    url(r'^joker/model/2/dist/$', views.cust_dist),
    url(r'^joker/model/2/rank/$', views.get_cust_rank),
    url(r'^joker/model/2/search/$', views.search_cust),
    url(r'^joker/model/2/range/$', views.get_cust_field_range),
    url(r'^joker/model/2/unique/$', views.get_cust_field_unique)
]
