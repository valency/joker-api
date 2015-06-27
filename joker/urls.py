from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/cust/get/$', views.get_cust_by_id),
    url(r'^api/cust/get_all/$', views.get_cust_all),
    url(r'^api/cust/add/$', views.add_cust),
    url(r'^api/cust/add_cust_from_csv/$', views.add_cust_from_csv),
    url(r'^api/cust/delete/$', views.remove_cust_by_id),
    url(r'^api/cust/delete_all/$', views.remove_cust_all),
    url(r'^api/cust/assign_pred/$', views.assign_pred),
    url(r'^api/cust/assign_pred_from_csv/$', views.assign_pred_from_csv),
    url(r'^api/cust/histogram/$', views.histogram),
    url(r'^api/cust/kmeans/$', views.kmeans),
    url(r'^api/cust/dist/$', views.cust_dist),
    url(r'^api/csv_to_json/$', views.csv_to_json)
]
